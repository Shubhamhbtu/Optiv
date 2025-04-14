import requests


def get_vt_report(ip, api_key):
    """
    Call VT API
    :param ip: IP to enrich
    :param api_key: VT APAI key
    :return: Response of VT analysis
    """
    try:
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        headers = {"x-apikey": api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        if response.ok:
            return parse_vt_response(response.json())
    except requests.HTTPError as herr:
        print(
            f"Error during VT api call. Status Code {response.status_code}. ERROR: {herr}"
        )


def parse_vt_response(data):
    """
    Parse VT data
    :param data: VT analysis data.
    :return: Object of VT analysis stat.
    """
    try:
        attributes = data.get("data", {}).get("attributes", {})
        analysis_summary = attributes.get("last_analysis_stats", {})
        return {
            "IP": data["data"]["id"],
            "Country": attributes.get("country", ""),
            "Malicious": analysis_summary.get("malicious", 0),
            "Suspicious": analysis_summary.get("suspicious", 0),
            "Undetected": analysis_summary.get("undetected", 0),
            "Harmless": analysis_summary.get("harmless"),
        }
    except Exception as err:
        print(f"Exception during parsing VT data. ERROR: {err}")
        return None
