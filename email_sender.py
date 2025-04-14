import smtplib
from email.message import EmailMessage
from email.utils import formataddr
import pandas as pd


def create_email_body(vt_data):
    """
    Create html table of VT data
    :param vt_data: list of VT analysis results
    :return: string: html data
    """
    try:
        df = pd.DataFrame(vt_data)
        return df.to_html(index=False)
    except Exception as err:
        print(f"Error while table creation. ERROR: {err}")


def send_email(sender_email, sender_password, receiver_email, excel_file, vt_data):
    """
    Send email to users
    :param sender_email: Sender email address
    :param sender_password:  Sender password
    :param receiver_email: Receiver email address
    :param excel_file: Excel file to attached
    :param vt_data: VirusTotal analysis results
    :return: None
    """
    try:
        msg = EmailMessage()
        msg["Subject"] = "VirusTotal IP address enrichment"
        msg["From"] = formataddr(("IP Enrichment", sender_email))
        msg["To"] = receiver_email

        html_body = create_email_body(vt_data)
        msg.set_content(
            "Your report is attached and summarized below.", subtype="plain"
        )
        msg.add_alternative(
            f"""
        <html>
            <body>
                <h2>VirusTotal Analysis Stats</h2>
                {html_body}
            </body>
        </html>
        """,
            subtype="html",
        )

        with open(excel_file, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=excel_file,
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
    except Exception as err:
        print(f"Error during Email sending. ERROR: {err}")
