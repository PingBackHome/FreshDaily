from flask import Flask, render_template
import requests
from datetime import datetime
import threading
import time

app = Flask(__name__)

def refresh_tickets(api_key):
    while True:
        # Voer de logica uit om tickets te vernieuwen

        domain = 'it2grow'

        url = f"https://{domain}.freshdesk.com/api/v2/tickets"
        headers = {
            "Content-Type": "application/json"
        }

        params = {
            "order_by": "created_at",
            "order_type": "desc",
            "per_page": 5
        }

        response = requests.get(url, auth=(api_key, 'X'), headers=headers, params=params)

        if response.status_code == 200:
            tickets = response.json()
            filtered_tickets = []

            for ticket in tickets:
                # Controleer of het ticket gesloten is
                if ticket['status'] != 5:  # 5 betekent gesloten
                    to_emails = ticket['to_emails']
                    if to_emails:
                        first_cc_email = to_emails[0]
                    else:
                        first_cc_email = "N/A"
                    subject = ticket['subject']
                    status = ticket['status']
                    created_at = ticket['created_at']
                    ticket_id = ticket['id']
                    responder_id = ticket['responder_id']
                    priority = ticket['priority']

                    # Get agent details
                    agent_url = f"https://{domain}.freshdesk.com/api/v2/agents/{responder_id}"
                    agent_response = requests.get(agent_url, auth=(api_key, 'X'), headers=headers)

                    if agent_response.status_code == 200:
                        agent = agent_response.json()
                        agent_name = agent['contact']['name']
                    else:
                        agent_name = "Unknown"

                    created_at_datetime = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                    created_at_formatted = created_at_datetime.strftime("%H:%M:%S %d-%m-%y")

                    # Vertaal de prioriteit naar tekstwaarde
                    priority_text = translate_priority(priority)

                    ticket['cc_email'] = first_cc_email
                    ticket['created_at_formatted'] = created_at_formatted
                    ticket['agent_name'] = agent_name
                    ticket['priority_text'] = priority_text

                    filtered_tickets.append(ticket)

            # Stel de vernieuwde ticketgegevens in als een globale variabele
            app.tickets = filtered_tickets

            # Berekent het totale aantal tickets
            total_tickets = len(filtered_tickets)
            
            # Berekent de agent met de meeste tickets
            agents = {}
            for ticket in filtered_tickets:
                agent_name = ticket['agent_name']
                if agent_name in agents:
                    agents[agent_name] += 1
                else:
                    agents[agent_name] = 1

            agent_with_most_tickets = max(agents, key=agents.get)

            # Beschikbare agents
            available_agents = list(agents.keys())

            # Stel de extra gegevens in als globale variabelen
            app.total_tickets = total_tickets
            app.agent_with_most_tickets = agent_with_most_tickets
            app.available_agents = available_agents
        else:
            error_message = f"Error retrieving tickets: {response.status_code}"
            if 'errors' in response.json():
                errors = response.json()['errors']
                error_details = "\n".join([f"- {error}" for error in errors])
                error_message += f"\nError details:\n{error_details}"
            print(error_message)

        # Wacht 10 seconden voordat opnieuw te starten
        time.sleep(10)

def translate_priority(priority):
    if priority == 1:
        return 'Low'
    elif priority == 2:
        return 'Medium'
    elif priority == 3:
        return 'High'
    elif priority == 4:
        return 'Urgent'
    else:
        return 'Unknown'

@app.route('/')
def index():
    return render_template('dashboard.html', tickets=app.tickets, total_tickets=app.total_tickets, 
                           agent_with_most_tickets=app.agent_with_most_tickets, 
                           available_agents=app.available_agents)

if __name__ == '__main__':
    # Vraag de gebruiker om de API-sleutel
    api_key = input("Voer de API-sleutel in: ")
    
    # Start een aparte thread voor het vernieuwen van de tickets
    refresh_thread = threading.Thread(target=refresh_tickets, args=(api_key,))
    refresh_thread.daemon = True
    refresh_thread.start()

    # Start de Flask-applicatie
    app.run()
