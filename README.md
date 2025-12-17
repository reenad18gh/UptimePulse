UptimePulse

A lightweight uptime monitoring system built with Python.
It continuously checks service availability, stores results, and publishes a live status dashboard using GitHub Pages.

Live Dashboard
https://reenad18gh.github.io/UptimePulse/

What this project does

You monitor critical endpoints.
You detect downtime.
You store incidents.
You publish uptime metrics in a public dashboard.

No frameworks.
No magic.
Just clean backend logic.

Features

HTTP and TCP uptime monitoring

Configurable check intervals and timeouts

SQLite-based incident storage

Static HTML dashboard generation

GitHub Pages deployment

Ready for Telegram alerts

Environment-based configuration

Architecture Overview
+-------------------+
|   monitor.py      |
|-------------------|
| - HTTP/TCP checks |
| - Status detection|
| - Change tracking |
+---------+---------+
          |
          v
+-------------------+
|      db.py        |
|-------------------|
| - SQLite storage  |
| - Incidents log   |
| - Uptime samples  |
+---------+---------+
          |
          v
+-------------------+
|   dashboard.py    |
|-------------------|
| - Read DB data    |
| - Render HTML     |
| - Generate report |
+---------+---------+
          |
          v
+-----------------------+
|   dashboard.html      |
|-----------------------|
| - Static dashboard    |
| - Uptime metrics      |
| - Latest incidents   |
+-----------------------+
          |
          v
+-----------------------+
|   GitHub Pages        |
|-----------------------|
| Public status page    |
+-----------------------+


This is a real monitoring pipeline.
Not a demo script.

Project Structure
uptime-pulse/
├── monitor.py        # Core monitoring loop
├── db.py             # SQLite access layer
├── dashboard.py      # HTML dashboard generator
├── dashboard.html    # Generated output
├── config.py         # Environment configuration
├── notifier.py       # Alert integrations
├── requirements.txt
├── .env.example
└── uptimepulse.db

How it works

monitor.py checks configured targets

Status changes are detected

Results are saved into SQLite

dashboard.py generates HTML

GitHub Pages publishes the dashboard

No backend server required.

Configuration

All settings are environment-driven.

CHECK_INTERVAL_SECONDS=30
REQUEST_TIMEOUT_SECONDS=3

HTTP_TARGETS=https://example.com
TCP_TARGETS=8.8.8.8:53

ENABLE_TELEGRAM=false
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

Run locally
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python monitor.py


Generate dashboard manually:

python dashboard.py

Why this project matters

This project demonstrates:

Backend monitoring logic

Stateful data handling

Automation and reporting

Production-style structure

GitHub Pages deployment

This is not CRUD.
This is systems thinking.

Future improvements

Uptime charts (24h / 7d)

Multi-service dashboards

Alert cooldown logic

Docker support

Web-based configuration

Author

Built by Rinad Alghamdi
Focused on backend systems and infrastructure tooling
