
from decimal import Decimal, InvalidOperation

from currency_api import (
    ratebridge_fetch_pair_rate,
    ratebridge_list_currencies,
)
from db import open_ratebridge_store


def ratebridge_read_amount():
    while True:
        try:
            amount = Decimal(input("\nAmount to convert: ").strip())

            if not amount.is_finite() or amount <= 0:
                print("Enter a positive, finite amount.")
                continue

            return amount

        except InvalidOperation:
            print("Invalid amount. Enter a numeric value.")


def ratebridge_select_currency(prompt, currency_catalog):
    while True:
        currency_code = input(prompt).strip().upper()

        if currency_code not in currency_catalog:
            print("Currency code not found. Please try again.")
            continue

        print(
            f"Currency selected: {currency_catalog[currency_code]} "
            f"({currency_code})"
        )
        return currency_code


def ratebridge_record_conversion(
    source_code,
    target_code,
    source_amount,
    rate_value,
    target_amount,
):
    connection = open_ratebridge_store()

    if connection is None:
        print("Result calculated, but the history could not be saved.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        statement = """
            INSERT INTO conversion_history
            (from_currency, to_currency, amount, exchange_rate, converted_amount)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            statement,
            (
                source_code,
                target_code,
                source_amount,
                rate_value,
                target_amount,
            ),
        )

        connection.commit()
        print("Conversion record saved.")

    except Exception as error:
        connection.rollback()
        print("Unable to save the conversion record:", error)

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def ratebridge_convert():
    print("\n" + "=" * 42)
    print("           RATEBRIDGE CONVERTER")
    print("=" * 42)

    currency_catalog = ratebridge_list_currencies()

    if currency_catalog is None:
        print("Currency information is unavailable. Check your connection.")
        return

    source_amount = ratebridge_read_amount()

    source_code = ratebridge_select_currency(
        "Source currency code (e.g. INR): ",
        currency_catalog,
    )

    target_code = ratebridge_select_currency(
        "Target currency code (e.g. SGD): ",
        currency_catalog,
    )

    rate_value, reference_date = ratebridge_fetch_pair_rate(
        source_code,
        target_code,
    )

    if rate_value is None:
        print("The conversion could not be completed.")
        return

    target_amount = (
        source_amount * Decimal(str(rate_value))
    ).quantize(Decimal("0.01"))

    print("\n" + "-" * 42)
    print("             CONVERSION RESULT")
    print("-" * 42)
    print(f"Original amount: {source_amount} {source_code}")
    print(f"Converted value: {target_amount} {target_code}")
    print(f"Rate:            1 {source_code} = {rate_value} {target_code}")
    print(f"Rate reference:  {reference_date}")
    print("-" * 42)

    ratebridge_record_conversion(
        source_code,
        target_code,
        source_amount,
        rate_value,
        target_amount,
    )


def ratebridge_show_history():
    connection = open_ratebridge_store()

    if connection is None:
        print("Cannot access conversion history.")
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

        history_rows = cursor.fetchall()

        print("\n" + "=" * 108)
        print("                    RATEBRIDGE CONVERSION RECORDS")
        print("=" * 108)

        if not history_rows:
            print("No saved conversions are available.")
            return

        print(
            f"{'ID':<5} {'FROM':<8} {'TO':<8} {'AMOUNT':<14} "
            f"{'RATE':<18} {'RESULT':<14} {'RECORDED AT':<22}"
        )
        print("-" * 108)

        for row in history_rows:
            print(
                f"{row[0]:<5} {row[1]:<8} {row[2]:<8} "
                f"{str(row[3]):<14} {str(row[4]):<18} "
                f"{str(row[5]):<14} {str(row[6]):<22}"
            )

        print("=" * 108)

    except Exception as error:
        print("Unable to load saved conversions:", error)

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def ratebridge_launch():
    while True:
        print("\n" + "=" * 42)
        print("              RATEBRIDGE")
        print("=" * 42)
        print("1. Convert an amount")
        print("2. Review conversion records")
        print("3. Close application")

        selection = input("\nChoose an option (1-3): ").strip()

        if selection == "1":
            ratebridge_convert()
        elif selection == "2":
            ratebridge_show_history()
        elif selection == "3":
            print("RateBridge session ended.")
            break
        else:
            print("Invalid selection. Choose 1, 2, or 3.")


ratebridge_launch()
