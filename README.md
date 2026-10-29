RateBridge — Currency Converter

Project Introduction

RateBridge is a Python application for converting monetary amounts between supported currencies. It retrieves exchange-rate information from an external API, calculates converted values, and stores completed conversions in a MySQL database for later review.

The project demonstrates API communication, input validation, numerical calculations, database operations, and error handling in a command-line application.

Key Capabilities

- Currency lookup: Retrieves supported currency codes and their names from the API.
- Amount validation: Accepts positive numeric amounts and rejects invalid entries.
- Exchange-rate retrieval: Requests the reference rate for the selected currency pair.
- Conversion calculation: Multiplies the entered amount by the retrieved rate and rounds the result to two decimal places.
- Persistent records: Saves conversion details in MySQL.
- History review: Displays previously recorded conversions, with the newest records shown first.
- Error handling: Reports problems with API requests and database operations.

Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and calculations |
| Frankfurter API | Currency reference-rate data |
| MySQL | Conversion record storage |
| MySQL Workbench | Database administration |
| Requests | HTTP communication with the API |
| MySQL Connector/Python | Database connectivity |

Source Files

- 'main.py' — manages the application menu, user input, conversion calculations, and history display.
- 'currency_api.py' — retrieves currency information and exchange rates.
- 'db.py' — establishes the MySQL connection.
- 'requirements.txt' — lists the required Python packages.
- '.gitignore' — excludes local and unnecessary files from version control.

Prerequisites

- Python 3
- MySQL Server
- An internet connection
- MySQL Workbench, recommended for database setup

Installation

Create a Python virtual environment, activate it, and install the packages listed in 'requirements.txt'.

Configure MySQL with a database named 'currency_converter' and a table named 'conversion_history' containing the following fields:

- 'id' — unique record identifier
- 'from_currency' — source currency code
- 'to_currency' — target currency code
- 'amount' — original amount
- 'exchange_rate' — rate used for the conversion
- 'converted_amount' — calculated result
- 'converted_at' — record creation timestamp

Set the 'MYSQL_PASSWORD' environment variable to the password for the local MySQL account used by the application. Keep credentials outside the source code and never publish them to the repository.

Install the project dependencies from 'requirements.txt', then start the application by running 'main.py' in your configured Python environment.

Using the Application

The application menu offers three options:

1. Convert an amount between two supported currencies.
2. Review conversion records saved in MySQL.
3. Close the application.

Enter a positive amount, choose the source and target currency codes, and review the calculated result and rate reference date. A successful conversion is saved to the database when the connection is available.

Exchange-Rate Information

RateBridge uses the [Frankfurter API](https://api.frankfurter.dev/v2) to retrieve reference exchange rates. The API does not require an API key.

Reference rates may not match the prices offered by banks, payment providers, or currency-exchange services. The returned rate date is displayed to help users understand which reference data was used.

Possible Improvements

- Add a graphical interface.
- Search conversion records by currency or date.
- Export saved records to CSV.
- Add charts for historical conversion activity.
- Add automated tests for input validation and conversion calculations.

Author

Salman A
