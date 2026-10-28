
import requests


API_BASE_URL = "https://api.frankfurter.dev/v2"


def get_supported_currencies():
    url = f"{API_BASE_URL}/currencies"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        return {
            item["iso_code"]: item["name"]
            for item in data
            if "iso_code" in item and "name" in item
        }

    except (
        requests.exceptions.RequestException,
        ValueError,
        KeyError,
        TypeError
    ) as error:
        print("Unable to retrieve supported currencies:", error)
        return None


def get_exchange_rate(from_currency, to_currency):
    from_currency = from_currency.strip().upper()
    to_currency = to_currency.strip().upper()

    if from_currency == to_currency:
        return 1.0, "Same currency"

    url = f"{API_BASE_URL}/rate/{from_currency}/{to_currency}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        exchange_rate = float(data["rate"])
        rate_date = data.get("date", "Unknown")

        return exchange_rate, rate_date

    except requests.exceptions.RequestException as error:
        print("Unable to retrieve exchange rates:", error)

    except (ValueError, KeyError, TypeError):
        print("Invalid response received from the currency API.")

    return None, None
