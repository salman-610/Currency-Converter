
from decimal import Decimal, InvalidOperation

from currency_api import get_exchange_rate, get_supported_currencies
from db import connect_database


def get_amount():
    while True:
        try:
            amount = Decimal(input("\nEnter amount to convert: ").strip())

            if not amount.is_finite() or amount <= 0:
                print("Please enter a positive, valid amount.")
                continue

            return amount

        except InvalidOperation:
            print("Invalid amount. Please enter a number.")


def get_currency(prompt, supported_currencies):
    while True:
        currency = input(prompt).strip().upper()

        if currency not in supported_currencies:
            print("Unsupported currency code. Please try again.")
            continue

        print(f"Selected: {supported_currencies[currency]} ({currency})")
        return currency


def save_conversion(from_currency, to_currency, amount, exchange_rate, converted_amount):
    connection = connect_database()

    if connection is None:
        print("Conversion completed, but history could not be saved.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO conversion_history
            (from_currency, to_currency, amount, exchange_rate, converted_amount)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            from_currency,
            to_currency,
            amount,
            exchange_rate,
            converted_amount
        )

        cursor.execute(query, values)
        connection.commit()
        print("Conversion saved to MySQL successfully!")

    except Exception as error:
        connection.rollback()
        print("Could not save conversion history:", error)

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def convert_currency():
    print("\n" + "=" * 40)
    print("       CURRENCY CONVERTER")
    print("=" * 40)

    supported_currencies = get_supported_currencies()

    if supported_currencies is None:
        print("Unable to retrieve currencies. Check your internet connection.")
        return

    amount = get_amount()
    from_currency = get_currency("Convert from (e.g. USD): ", supported_currencies)
    to_currency = get_currency("Convert to (e.g. INR): ", supported_currencies)

    exchange_rate, rate_date = get_exchange_rate(
        from_currency,
        to_currency
    )

    if exchange_rate is None:
        print("Conversion failed. Please try again later.")
        return

    converted_amount = (
        amount * Decimal(str(exchange_rate))
    ).quantize(Decimal("0.01"))

    print("\n" + "-" * 40)
    print("CONVERSION RESULT")
    print("-" * 40)
    print(f"From:           {amount} {from_currency}")
    print(f"To:             {converted_amount} {to_currency}")
    print(
        f"Exchange rate:  1 {from_currency} = "
        f"{exchange_rate} {to_currency}"
    )
    print(f"Rate date:      {rate_date}")
    print("-" * 40)

    save_conversion(
        from_currency,
        to_currency,
        amount,
        exchange_rate,
        converted_amount
    )


def view_conversion_history():
    connection = connect_database()

    if connection is None:
        print("Unable to connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, from_currency, to_currency, amount,
                   exchange_rate, converted_amount, converted_at
            FROM conversion_history
            ORDER BY converted_at DESC, id DESC
        """)

        records = cursor.fetchall()

        print("\n" + "=" * 100)
        print("                    CONVERSION HISTORY")
        print("=" * 100)

        if not records:
            print("No conversion history found.")
            return

        print(
            f"{'ID':<5} {'FROM':<8} {'TO':<8} {'AMOUNT':<14} "
            f"{'RATE':<18} {'CONVERTED':<14} {'DATE':<20}"
        )
        print("-" * 100)

        for record in records:
            print(
                f"{record[0]:<5} {record[1]:<8} {record[2]:<8} "
                f"{str(record[3]):<14} {str(record[4]):<18} "
                f"{str(record[5]):<14} {str(record[6]):<20}"
            )

        print("=" * 100)

    except Exception as error:
        print("Unable to retrieve conversion history:", error)

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def main():
    while True:
        print("\n" + "=" * 40)
        print("       CURRENCY CONVERTER MENU")
        print("=" * 40)
        print("1. Convert Currency")
        print("2. View Conversion History")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            convert_currency()
        elif choice == "2":
            view_conversion_history()
        elif choice == "3":
            print("Thank you for using Currency Converter!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


main()
