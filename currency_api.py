
import requests


RATEBRIDGE_API_ROOT = "https://api.frankfurter.dev/v2"


def ratebridge_list_currencies():
    endpoint = f"{RATEBRIDGE_API_ROOT}/currencies"

    try:
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()

        currency_items = response.json()

        return {
            item["iso_code"]: item["name"]
            for item in currency_items
            if "iso_code" in item and "name" in item
        }

    except (
        requests.exceptions.RequestException,
        ValueError,
        KeyError,
        TypeError,
    ) as error:
        print("Could not retrieve the currency list:", error)
        return None


def ratebridge_fetch_pair_rate(source_code, target_code):
    source_code = source_code.strip().upper()
    target_code = target_code.strip().upper()

    if source_code == target_code:
        return 1.0, "Same currency"

    endpoint = (
        f"{RATEBRIDGE_API_ROOT}/rate/"
        f"{source_code}/{target_code}"
    )

    try:
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()

        rate_details = response.json()

        rate_value = float(rate_details["rate"])
        reference_date = rate_details.get("date", "Unknown")

        return rate_value, reference_date

    except requests.exceptions.RequestException as error:
        print("Could not retrieve the exchange rate:", error)

    except (ValueError, KeyError, TypeError):
        print("The API returned an unexpected exchange-rate response.")

    return None, None
