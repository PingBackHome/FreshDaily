import sqlite3
import requests
import time
from datetime import date
import signal
import sys

# Vraag domein en API-sleutel aan de gebruiker
freshdesk_domain = input("Voer het Freshdesk-domein in: ")
api_key = input("Voer de Freshdesk API-sleutel in: ")

# Verbinding maken met de database
conn = sqlite3.connect('/home/dev/projects/frshdash/db/freshdaily.db')
cursor = conn.cursor()

def clear_database():
    # Leeg de tickets tabel in de database
    cursor.execute("DELETE FROM tickets")
    conn.commit()

def signal_handler(sig, frame):
    # Handel het SIGINT-signaal af (bijvoorbeeld bij Ctrl+C)
    clear_database()
    sys.exit(0)

# Registreer de signal handler voor SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Oneindige lus voor doorlopend controleren en bijwerken
while True:
    try:
        # Datum van vandaag
        today = date.today().isoformat()

        # API-verzoek om tickets op te halen
        url = f"https://{freshdesk_domain}.freshdesk.com/api/v2/tickets?updated_since={today}"
        headers = {
            "Content-Type": "application/json",
        }
        auth = (api_key, "X")
        response = requests.get(url, headers=headers, auth=auth)

        # Controleren of het API-verzoek succesvol was
        if response.status_code == 200:
            # JSON-gegevens van de API-respons ophalen
            tickets = response.json()

            added_count = 0
            removed_count = 0

            # Tickets in de database plaatsen of verwijderen
            for ticket in tickets:
                if ticket['status'] in [4, 5]:
                    # Verwijder het ticket uit de database als het resolved of closed is
                    cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket['id'],))
                    removed_count += 1
                elif ticket['status'] == 2:
                    # Controleren of het ticket al in de database bestaat
                    cursor.execute("SELECT id FROM tickets WHERE id = ?", (ticket['id'],))
                    existing_ticket = cursor.fetchone()

                    if existing_ticket:
                        # Update het ticket als het al in de database bestaat
                        cursor.execute('''
                            UPDATE tickets SET
                            subject = ?,
                            created_at = ?,
                            status = ?,
                            responder_id = ?,
                            priority = ?
                            WHERE id = ?
                        ''', (
                            ticket['subject'],
                            ticket['created_at'],
                            ticket['status'],
                            ticket['responder_id'],
                            ticket['priority'],
                            ticket['id']
                        ))
                    else:
                        # Voeg het ticket toe aan de database als het nieuw is
                        cursor.execute('''
                            INSERT INTO tickets (id, subject, created_at, status, responder_id, priority)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (
                            ticket['id'],
                            ticket['subject'],
                            ticket['created_at'],
                            ticket['status'],
                            ticket['responder_id'],
                            ticket['priority']
                        ))
                        added_count += 1

                    # Get agent details
                    agent_url = f"https://{freshdesk_domain}.freshdesk.com/api/v2/agents/{ticket['responder_id']}"
                    agent_response = requests.get(agent_url, auth=(api_key, 'X'), headers=headers)

                    if agent_response.status_code == 200:
                        agent = agent_response.json()
                        agent_name = agent['contact']['name']
                    else:
                        agent_name = "Unknown"

                    # Voeg de agentnaam toe aan de database entry
                    cursor.execute('''
                        UPDATE tickets SET
                        agent = ?
                        WHERE id = ?
                    ''', (
                        agent_name,
                        ticket['id']
                    ))

            # Bevestig de wijzigingen in de database
            conn.commit()

            # Uitvoer van log
            print(f"{added_count} items toegevoegd, {removed_count} items verwijderd.")

        else:
            print("Fout bij het ophalen van tickets van de Freshdesk API.")

        # Wacht 1 minuut voordat de volgende iteratie begint
        time.sleep(15)

    except Exception as e:
        print("Er is een fout opgetreden:", str(e))
        clear_database()
        sys.exit(1)

# Sluit de databaseverbinding
conn.close()
