import sqlite3

def show_tickets():
    # Verbinding maken met de database
    conn = sqlite3.connect('/home/dev/projects/frshdash/db/freshdaily.db')
    cursor = conn.cursor()

    # Query om alle tickets op te halen en op volgorde van nieuw naar oud te sorteren
    cursor.execute("SELECT * FROM tickets ORDER BY created_at DESC")
    tickets = cursor.fetchall()

    # Uitvoer van de tickets
    for ticket in tickets:
        print("Ticket ID:", ticket[0])
        print("Onderwerp:", ticket[1])
        print("Aangemaakt op:", ticket[2])
        print("Status:", ticket[3])
        print("Responder ID:", ticket[4])
        print("Prioriteit:", ticket[5])
        print("Agent", ticket[6])
        print("------------------------")

    # Sluit de databaseverbinding
    conn.close()

# Commando om tickets te controleren
def check_tickets_command():
    print("Tickets in de database:")
    show_tickets()

# Test het commando door het aan te roepen
check_tickets_command()
