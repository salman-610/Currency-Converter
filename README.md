RateBridge — Currency Converter

Project Introduction

RateBridge is a Python-based currency conversion application that allows users to convert monetary amounts between supported currencies. It retrieves reference exchange rates from an external API, calculates converted values, and stores completed transactions in a MySQL database for future reference.

This project demonstrates practical implementation of API integration, input validation, numerical calculations, database connectivity, and error handling through a command-line application.

Key Capabilities

- Currency Lookup: Retrieves supported currency codes and their corresponding names.
- Amount Validation: Accepts positive numeric amounts and handles invalid input.
- Exchange-Rate Retrieval: Fetches reference exchange rates for the selected currency pair.
- Conversion Calculation: Calculates the converted amount using the retrieved rate and rounds the result to two decimal places.
- Persistent Storage: Saves completed conversion details in a MySQL database.
- History Review: Displays previously saved transactions, with the latest records shown first.
- Error Handling: Handles API communication issues and database-related errors.

Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and calculations |
| Frankfurter API | Reference exchange-rate data |
| MySQL | Conversion history storage |
| MySQL Workbench | Database administration |
| Requests | HTTP communication with the API |
| MySQL Connector/Python | Database connectivity |

Project Files

- 'main.py' — Controls the application menu, user input, conversion process, and history display.
- 'currency_api.py' — Retrieves currency information and exchange rates from the API.
- 'db.py' — Handles the connection between the application and MySQL.
- 'database.sql' — Creates the database and conversion history table.
- 'requirements.txt' — Lists the external Python packages required by the project.
- '.gitignore' — Excludes local and unnecessary files from version control.

Prerequisites

- Python 3
- MySQL Server
- Internet connection
- MySQL Workbench (recommended for database management)

Installation and Setup

1. Prepare the Python Environment

Create a Python virtual environment, activate it, and install the dependencies listed in 'requirements.txt'.

2. Configure the Database

Open 'database.sql' in MySQL Workbench and execute the script. It creates the 'currency_converter' database and the 'conversion_history' table.

The table contains the following fields:

- 'id' — Unique record identifier.
- 'from_currency' — Source currency code.
- 'to_currency' — Target currency code.
- 'amount' — Original amount entered by the user.
- 'exchange_rate' — Reference rate used for the conversion.
- 'converted_amount' — Calculated converted amount.
- 'converted_at' — Timestamp indicating when the record was created.

3. Configure Database Credentials

Set the 'MYSQL_PASSWORD' environment variable to the password of the local MySQL account configured in 'db.py'.

The application reads the password from the environment rather than storing credentials directly in the source code. Do not publish database passwords or other sensitive information to the repository.

4. Start the Application

After installing the dependencies and configuring the database connection, run 'main.py' using the configured Python environment.

Using the Application

RateBridge provides three menu options:

1. Convert an Amount — Converts an entered amount between two supported currencies.
2. Review Conversion Records — Displays previously saved conversion transactions from MySQL.
3. Close Application — Exits the program.

To perform a conversion, enter a positive amount, select the source and target currency codes, and review the calculated result along with the exchange-rate reference date.

When the database connection is available, the completed conversion is saved automatically for future review.

Exchange-Rate Information

RateBridge uses the [Frankfurter API](https://api.frankfurter.dev/v2) to retrieve reference exchange rates. The API does not require an API key.

The displayed rates are reference values and may differ from the rates offered by banks, payment providers, or currency-exchange services. The application also displays the rate reference date to indicate the date associated with the retrieved data.

Possible Improvements

- Introduce a graphical user interface.
- Add search and filtering options for conversion history.
- Support exporting conversion records to CSV.
- Include charts for analysing conversion activity.
- Implement automated tests for input validation and conversion calculations.

Author

Salman A