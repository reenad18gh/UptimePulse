import sqlite3
from datetime import datetime, timezone

DB_NAME = "uptimepulse.db"


def get_conn():
    return sqlite3.connect(DB_NAME)


def get_recent_rows(limit=30):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT timestamp, status, reason
        FROM status_log
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_last_row():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT timestamp, status, reason
        FROM status_log
        ORDER BY id DESC
        LIMIT 1
    """)
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {"timestamp": row[0], "status": row[1], "reason": row[2]}


def get_last_closed_incident():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT start_ts, end_ts, duration_seconds
        FROM incidents
        WHERE end_ts IS NOT NULL
        ORDER BY id DESC
        LIMIT 1
    """)
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {"start_ts": row[0], "end_ts": row[1], "duration_seconds": row[2]}


def calc_uptime_percent(rows):
    if not rows:
        return 0.0
    up = sum(1 for _, s, _ in rows if s == "UP")
    return (up / len(rows)) * 100.0


def fmt_duration(seconds):
    if seconds is None:
        return "-"
    s = int(seconds)
    m = s // 60
    h = m // 60
    if h > 0:
        return f"{h}h {m%60}m"
    if m > 0:
        return f"{m}m"
    return f"{s}s"


def render_html(rows):
    now = datetime.now(timezone.utc).isoformat()

    last = get_last_row()
    last_inc = get_last_closed_incident()

    current_status = last["status"] if last else "UNKNOWN"
    current_reason = last["reason"] if last else ""
    last_checked = last["timestamp"] if last else "-"
    last_outage = fmt_duration(last_inc["duration_seconds"]) if last_inc else "-"

    uptime = calc_uptime_percent(list(reversed(rows)))
    status_class = "status-up" if current_status == "UP" else "status-down"

    table_rows = ""
    for ts, status, reason in rows:
        row_class = "status-up" if status == "UP" else "status-down"
        table_rows += (
            "<tr>"
            f"<td class='mono'>{ts}</td>"
            f"<td class='{row_class}'>{status}</td>"
            f"<td class='reason'>{reason}</td>"
            "</tr>"
        )

    return f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>UptimePulse Dashboard</title>
<style>
  :root {{
    --bg: #0b1220;
    --panel: #0f1a30;
    --panel2: #0b152a;
    --border: #1e2a44;
    --text: #e5e7eb;
    --muted: #9aa7bd;
    --brand: #38bdf8;
    --up: #22c55e;
    --down: #ef4444;
  }}

  body {{
    font-family: Arial, sans-serif;
    background: radial-gradient(1200px 700px at 20% 10%, #0f2a4a 0%, var(--bg) 55%);
    color: var(--text);
    margin: 0;
    padding: 28px;
  }}

  .wrap {{
    max-width: 1100px;
    margin: 0 auto;
  }}

  .header {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 18px;
  }}

  .title {{
    font-size: 28px;
    font-weight: 800;
    color: var(--brand);
    letter-spacing: 0.2px;
  }}

  .subtitle {{
    color: var(--muted);
    font-size: 13px;
  }}

  .card {{
    background: linear-gradient(180deg, var(--panel) 0%, var(--panel2) 100%);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);
    margin-bottom: 14px;
  }}

  .grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 14px;
  }}

  @media (max-width: 900px) {{
    .grid {{
      grid-template-columns: 1fr;
    }}
  }}

  .label {{
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 6px;
  }}

  .value {{
    font-size: 22px;
    font-weight: 800;
  }}

  .status-up {{
    color: var(--up);
    font-weight: 800;
  }}

  .status-down {{
    color: var(--down);
    font-weight: 800;
  }}

  .mono {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    font-size: 13px;
    color: #c7d2fe;
  }}

  .pill {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: rgba(255,255,255,0.03);
    font-weight: 800;
  }}

  .dot {{
    width: 10px;
    height: 10px;
    border-radius: 999px;
    background: var(--brand);
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
  }}

  th {{
    text-align: left;
    font-size: 12px;
    color: var(--muted);
    padding: 10px 8px;
    border-bottom: 1px solid var(--border);
  }}

  td {{
    padding: 10px 8px;
    border-bottom: 1px solid rgba(30,42,68,0.7);
    vertical-align: top;
    font-size: 14px;
  }}

  .reason {{
    color: #d1d5db;
  }}
</style>
</head>
<body>
  <div class="wrap">
    <div class="header">
      <div>
        <div class="title">UptimePulse</div>
        <div class="subtitle">Generated UTC {now}</div>
      </div>
      <div class="pill">
        <span class="dot"></span>
        <span>Live status</span>
      </div>
    </div>

    <div class="card">
      <div class="label">Current status</div>
      <div class="value">
        <span class="{status_class}">{current_status}</span>
      </div>
      <div class="subtitle">Last checked UTC {last_checked}</div>
      <div class="subtitle">Reason {current_reason}</div>
    </div>

    <div class="grid">
      <div class="card">
        <div class="label">Uptime last {len(rows)} samples</div>
        <div class="value">{uptime:.2f}%</div>
      </div>
      <div class="card">
        <div class="label">Last outage duration</div>
        <div class="value">{last_outage}</div>
      </div>
      <div class="card">
        <div class="label">Samples shown</div>
        <div class="value">{len(rows)}</div>
      </div>
    </div>

    <div class="card">
      <div class="label">Latest samples</div>
      <table>
        <thead>
          <tr>
            <th>Timestamp UTC</th>
            <th>Status</th>
            <th>Reason</th>
          </tr>
        </thead>
        <tbody>
          {table_rows}
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
"""


def write_dashboard():
    rows = get_recent_rows(30)
    html = render_html(rows)
    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    write_dashboard()
