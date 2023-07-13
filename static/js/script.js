document.addEventListener('DOMContentLoaded', function() {
    // Functie om de huidige tijd weer te geven
    function displayCurrentTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('nl-NL');
        const clockElement = document.getElementById('clock');
        clockElement.textContent = timeString;
    }

    // Functie om de tabel met tickets te vernieuwen
    function refreshTicketsTable() {
        const ticketsTable = document.getElementById('tickets-table');

        fetch('/tickets')
            .then(response => response.json())
            .then(tickets => {
                let html = '';
                tickets.forEach(ticket => {
                    html += `
                        <tr>
                            <td>${ticket.ticket_id}</td>
                            <td>${ticket.subject}</td>
                            <td>${ticket.status}</td>
                            <td>${ticket.priority}</td>
                            <td>${ticket.agent}</td>
                            <td>${ticket.created_at}</td>
                        </tr>
                    `;
                });
                ticketsTable.innerHTML = html;
            })
            .catch(error => {
                console.error('Fout bij het vernieuwen van de tickets:', error);
            });
    }

    // Vernieuw de tijd elke seconde
    setInterval(displayCurrentTime, 1000);

    // Vernieuw de tabel elke 15 seconden
    setInterval(refreshTicketsTable, 15000);

    // Toon de huidige tijd en vernieuw de tabel bij het laden van de pagina
    displayCurrentTime();
    refreshTicketsTable();
});
