Currency Converter

Overview

A Python-based currency converter that retrieves exchange rates through an API, performs currency calculations, and stores conversion records in a MySQL database.

Features

- Convert between supported currencies.
- Retrieve exchange rates from the Frankfurter API.
- Validate currency codes and numeric amounts.
- Display conversion results and the reference rate date.
- Save conversion details in MySQL.
- View previous conversions through the application menu.
- Handle API and database connection errors.

Technologies

- Python
- Frankfurter Exchange Rate API
- MySQL
- MySQL Workbench
- Requests
- MySQL Connector/Python

Project Structure

```text
currency_converter_project/
├── main.py
├── currency_api.py
├── db.py
├── requirements.txt
├── README.md
└── .gitignore
```

Requirements

- Python 3
- MySQL Server
- Internet connection

Install the dependencies listed in `requirements.txt` and configure the MySQL database before running the application.

Database Configuration

Create a database named `currency_converter` and a table named `conversion_history` with columns for the source currency, target currency, original amount, exchange rate, converted amount, and conversion timestamp.

Configure the MySQL connection to use the `MYSQL_PASSWORD` environment variable. Never store database credentials in the source code or publish them to GitHub.

Usage

Start the application using your Python environment. Choose an option from the menu to convert currencies, view conversion history, or exit.

API Information

This project uses the [Frankfurter API](https://api.frankfurter.dev/v2) to retrieve reference exchange rates. No API key is required. Rates may not represent real-time trading or transaction prices.

Future Enhancements

- Graphical user interface
- Search and filter conversion history
- Export history to CSV
- Conversion history visualizations

Author

Salman A
