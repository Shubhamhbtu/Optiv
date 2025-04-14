import requests
import pandas as pd


def fetch_abuse_ips(api_key, confidence=97, limit=5):
    """
    Call AbuseIPDb api.
    :param api_key: API key of AbuseIPDb
    :param confidence: Confidence score to filter IP address
    :param limit: Number of IPs to be fetch
    :return: Response of AbuseIPDb
    """
    try:
        url = "https://api.abuseipdb.com/api/v2/blacklist"
        headers = {"Key": api_key, "Accept": "application/json"}
        params = {"confidenceMinimum": confidence, "limit": limit}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()["data"]
    except requests.HTTPError as herr:
        print(
            f"Error during AbuseIPDB API call. Status Code: {response.status_code}, Error: {herr}"
        )
        return None


def save_to_excel(data, filename="abuse_ips.xlsx"):
    """
    Saving result to excel file
    :param data: Data to save.
    :param filename: Filename
    :return: Filename
    """
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        return filename
    except Exception as err:
        print(f"Error saving to Excel: {err}")
        return None
