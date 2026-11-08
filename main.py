
from decimal import Decimal, InvalidOperation

from currency_api import (
    ratebridge_fetch_pair_rate,
    ratebridge_list_currencies,
)
from db import open_ratebridge_store


def rb_app_capture_amount():
    while True:
        try:
            entered_amount = Decimal(
                input("\nEnter the amount to convert: ").strip()
            )

            if not entered_amount.is_finite() or entered_amount <= 0:
                print("Please enter a valid positive amount.")
                continue

            return entered_amount

        except InvalidOperation:
            print("Invalid input. Please enter a numeric amount.")


def rb_app_choose_currency(message, available_currencies):
    while True:
        selected_code = input(message).strip().upper()

        if selected_code not in available_currencies:
            print("Unsupported currency code. Please try again.")
            continue

        currency_name = available_currencies[selected_code]

        print(f"Selected currency: {currency_name} ({selected_code})")

        return selected_code


def rb_app_store_conversion(
    source_currency,
    destination_currency,
    original_amount,
    exchange_rate,
    final_amount,
):
    database_connection = open_ratebridge_store()

    if database_connection is None:
        print("Conversion completed, but the record could not be saved.")
        return

    database_cursor = None

    try:
        database_cursor = database_connection.cursor()

        insert_query = """
            INSERT INTO conversion_history
            (
                from_currency,
                to_currency,
                amount,
                exchange_rate,
                converted_amount
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        conversion_values = (
            source_currency,
            destination_currency,
            original_amount,
            exchange_rate,
            final_amount,
        )

        database_cursor.execute(insert_query, conversion_values)
        database_connection.commit()

        print("Conversion record saved successfully.")

    except Exception as database_error:
        database_connection.rollback()
        print("Database error while saving the record:", database_error)

    finally:
        if database_cursor is not None:
            database_cursor.close()

        database_connection.close()


def rb_app_process_conversion():
    print("\n" + "=" * 42)
    print("           RATEBRIDGE CONVERTER")
    print("=" * 42)

    currency_options = ratebridge_list_currencies()

    if currency_options is None:
        print("Unable to retrieve currency information.")
        print("Please check your internet connection.")
        return

    original_amount = rb_app_capture_amount()

    source_currency = rb_app_choose_currency(
        "Enter source currency code (e.g. INR): ",
        currency_options,
    )

    destination_currency = rb_app_choose_currency(
        "Enter target currency code (e.g. USD): ",
        currency_options,
    )

    exchange_rate, rate_date = ratebridge_fetch_pair_rate(
        source_currency,
        destination_currency,
    )

    if exchange_rate is None:
        print("Unable to complete the requested conversion.")
        return

    final_amount = (
        original_amount * Decimal(str(exchange_rate))
    ).quantize(Decimal("0.01"))

    print("\n" + "-" * 42)
    print("             CONVERSION RESULT")
    print("-" * 42)
    print(f"Original amount: {original_amount} {source_currency}")
    print(f"Converted value: {final_amount} {destination_currency}")
    print(
        f"Exchange rate:   1 {source_currency} = "
        f"{exchange_rate} {destination_currency}"
    )
    print(f"Reference date:  {rate_date}")
    print("-" * 42)

    rb_app_store_conversion(
        source_currency,
        destination_currency,
        original_amount,
        exchange_rate,
        final_amount,
    )


def rb_app_display_history():
    database_connection = open_ratebridge_store()

    if database_connection is None:
        print("Unable to access the conversion history.")
        return

    database_cursor = None

    try:
        database_cursor = database_connection.cursor()

        history_query = """
            SELECT
                id,
                from_currency,
                to_currency,
                amount,
                exchange_rate,
                converted_amount,
                converted_at
            FROM conversion_history
            ORDER BY converted_at DESC, id DESC
        """

        database_cursor.execute(history_query)
        saved_conversions = database_cursor.fetchall()

        print("\n" + "=" * 108)
        print("                  RATEBRIDGE CONVERSION HISTORY")
        print("=" * 108)

        if not saved_conversions:
            print("No conversion records found.")
            return

        print(
            f"{'ID':<5} {'FROM':<8} {'TO':<8} {'AMOUNT':<14} "
            f"{'RATE':<18} {'RESULT':<14} {'RECORDED AT':<22}"
        )

        print("-" * 108)

        for conversion in saved_conversions:
            print(
                f"{conversion[0]:<5} "
                f"{conversion[1]:<8} "
                f"{conversion[2]:<8} "
                f"{str(conversion[3]):<14} "
                f"{str(conversion[4]):<18} "
                f"{str(conversion[5]):<14} "
                f"{str(conversion[6]):<22}"
            )

        print("=" * 108)

    except Exception as history_error:
        print("Unable to retrieve conversion history:", history_error)

    finally:
        if database_cursor is not None:
            database_cursor.close()

        database_connection.close()


def rb_app_start_console():
    while True:
        print("\n" + "=" * 42)
        print("              RATEBRIDGE")
        print("=" * 42)
        print("1. Convert an amount")
        print("2. Review conversion records")
        print("3. Close application")

        menu_choice = input("\nChoose an option (1-3): ").strip()

        if menu_choice == "1":
            rb_app_process_conversion()

        elif menu_choice == "2":
            rb_app_display_history()

        elif menu_choice == "3":
            print("Thank you for using RateBridge. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    rb_app_start_console()
