from config import *
from abuseipdb import fetch_abuse_ips, save_to_excel
from vt_enrichment import get_vt_report
from database import save_to_mongodb
from email_sender import send_email


def main():
    """
    Main function
    """
    abuse_data = fetch_abuse_ips(ABUSEIPDB_API_KEY)
    excel_file = save_to_excel(abuse_data)
    vt_results = []
    for entry in abuse_data:
        ip = entry["ipAddress"]
        vt_report = get_vt_report(ip, VT_API_KEY)
        if vt_report:
            vt_results.append(vt_report)

    save_to_mongodb(vt_results, MONGO_URI)
    send_email(EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER, excel_file, vt_results)


if __name__ == "__main__":
    main()
