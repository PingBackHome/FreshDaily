# FreshDaily Dashboard for Freshdesk

The FreshDaily Dashboard is a web application developed to display ticket information and provide a summary of agents with the most tickets. It offers an overview of the 10 latest tickets, including details such as ticket ID, subject, status, priority, assigned agent, and creation date.

## Features

- Display of the 10 latest tickets with essential information.
- Summary of agents with the most tickets.
- Dynamic refreshing of table content and summary without page reloading.

## Technologies

This project utilizes the following technologies:

- **Python**: The programming language for the backend logic and querying data from the SQLite database.
- **Flask**: A Python web framework for developing the web application and delivering dynamic HTML templates.
- **SQLite**: A relational database engine for storing and managing ticket data.
- **HTML**: The markup language for structuring the web pages and displaying data.
- **CSS**: The styling language for enhancing the appearance and layout of the web pages.
- **JavaScript**: The programming language for adding interactive features and refreshing table content without page reloading.

## Installation

To run the FreshDaily Dashboard application locally, follow these steps:

1. Clone the repository to your local environment.
2. Ensure that Python 3 is installed on your system.
3. Install the required Python packages using `pip install -r requirements.txt`.
4. Start `db_worker.py` from /scripts/db_scripts
5. Verify the database configuration and adjust the paths if necessary in `dashboard.py`.
6. Run the application using the command `python dashboard.py`.
7. Open a web browser and navigate to `http://localhost:5000` to view the FreshDaily Dashboard.

## Contributing

Contributions to the FreshDaily Dashboard are welcome! If you find an issue or want to propose an improvement, please create an issue in the GitHub project. If you want to contribute code, you can submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code according to the terms of the license.
