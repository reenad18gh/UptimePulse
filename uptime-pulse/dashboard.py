import sqlite3
from datetime import datetime, timezone

DB_NAME = "uptimepulse.db"


def get_recent_rows(limit=30):
    conn = sqlite3.connect(DB_NAME)
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


def calc_uptime_percent(rows):
    if not rows:
        return 0.0

    up = sum(1 for _, status, _ in rows if status == "UP")
    return (up / len(rows)) * 100.0


def render_html(rows):
    rows_for_stats = list(reversed(rows))
    uptime = calc_uptime_percent(rows_for_stats)

    table_rows = ""
    for ts, status, reason in rows:
        status_class = "status-up" if status == "UP" else "status-down"
        table_rows += (
            "<tr>"
            f"<td>{ts}</td>"
            f"<td class='{status_class}'>{status}</td>"
            f"<td>{reason}</td>"
            "</tr>"
        )

    now = datetime.now(timezone.utc).isoformat()

    return f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>UptimePulse Dashboard</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #f5f7fa;
  margin: 24px;
}}
.card {{
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}}
.big {{
  font-size: 24px;
  font-weight: bold;
}}
.muted {{
  color: #666;
  font-size: 13px;
}}
.status-up {{
  color: #0a8a3a;
  font-weight: bold;
}}
.status-down {{
  color: #c62828;
  font-weight: bold;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  margin-top: 12px;
}}
th {{
  background: #f0f2f5;
  text-align: left;
  padding: 10px;
  font-size: 13px;
}}
td {{
  border-bottom: 1px solid #eee;
  padding: 10px;
  font-size: 14px;
}}
</style>
</head>
<body>

<div class="card">
  <div class="big">UptimePulse Dashboard</div>
  <div class="muted">Updated UTC {now}</div>
</div>

<div class="card">
  <div class="muted">Uptime based on last {len(rows_for_stats)} samples</div>
  <div class="big">{uptime:.2f}%</div>
</div>

<div class="card">
  <div class="big">Latest samples</div>
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
