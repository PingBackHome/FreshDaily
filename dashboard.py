from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def dashboard():
    conn = sqlite3.connect('/home/dev/projects/frshdash/db/freshdaily.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, subject, status, priority, agent, created_at FROM tickets ORDER BY created_at DESC LIMIT 10")
    tickets = cursor.fetchall()
    
    cursor.execute("SELECT agent, COUNT(*) FROM tickets GROUP BY agent")
    agent_summary = dict(cursor.fetchall())
    
    formatted_tickets = []
    for ticket in tickets:
        ticket_id, subject, status, priority, agent, created_at = ticket
        created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
        formatted_created_at = created_at.strftime("%H:%M:%S %d-%m-%Y")
        formatted_tickets.append((ticket_id, subject, status, priority, agent, formatted_created_at))
    
    return render_template('dashboard.html', tickets=formatted_tickets, agent_summary=agent_summary)

@app.route('/tickets')
def get_tickets():
    conn = sqlite3.connect('/home/dev/projects/frshdash/db/freshdaily.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, subject, status, priority, agent, created_at FROM tickets ORDER BY created_at DESC LIMIT 10")
    tickets = cursor.fetchall()

    formatted_tickets = []
    for ticket in tickets:
        ticket_id, subject, status, priority, agent, created_at = ticket
        created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
        formatted_created_at = created_at.strftime("%H:%M:%S %d-%m-%Y")
        formatted_tickets.append({
            'ticket_id': ticket_id,
            'subject': subject,
            'status': status,
            'priority': priority,
            'agent': agent,
            'created_at': formatted_created_at
        })

    return jsonify(formatted_tickets)

if __name__ == '__main__':
    app.run()
