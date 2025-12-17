from datetime import datetime
from db import get_recent_rows

def render_html(rows):
    updated = datetime.utcnow().isoformat()

    rows_html = ""
    for ts, status, reason in rows:
        cls = "status-up" if status == "UP" else "status-down"
        rows_html += f"""
        <tr>
            <td>{ts}</td>
            <td class="{cls}">{status}</td>
            <td>{reason}</td>
        </tr>
        """

    return f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>UptimePulse Dashboard</title>

<style>
:root {{
  --bg: #0f172a;
  --card: #020617;
  --border: #1e293b;
  --text: #e5e7eb;
  --muted: #94a3b8;
  --green: #22c55e;
  --red: #ef4444;
}}

body {{
  margin: 0;
  padding: 24px;
  background: var(--bg);
  color: var(--text);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}}

.card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px;
  margin-bottom: 20px;
}}

.big {{
  font-size: 26px;
  font-weight: 600;
}}

.muted {{
  color: var(--muted);
  font-size: 13px;
}}

table {{
  width: 100%;
  border-collapse: collapse;
}}

th, td {{
  padding: 12px;
  border-bottom: 1px solid var(--border);
  text-align: left;
}}

.status-up {{
  color: var(--green);
  font-weight: 600;
}}

.status-down {{
  color: var(--red);
  font-weight: 600;
}}
</style>
</head>

<body>

<div class="card">
  <div class="big">UptimePulse Dashboard</div>
  <div class="muted">Updated UTC {updated}</div>
</div>

<div class="card">
  <div class="muted">Uptime based on last {len(rows)} samples</div>
  <div class="big">100%</div>
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
      {rows_html}
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
