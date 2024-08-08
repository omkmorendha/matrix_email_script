import os
import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def load_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()

def send_email(subject, content, to_email, template):
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = int(os.environ.get("SMTP_PORT"))
    smtp_login = os.environ.get("SMTP_LOGIN")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    smtp_email = os.environ.get("FROM_EMAIL")

    msg = MIMEMultipart()

    from_name = os.environ.get("FROM_NAME")
    msg["From"] = f"{from_name} <{smtp_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject

    html_message = template.replace("$subject", subject).replace("$content", content)
    msg.attach(MIMEText(html_message, "html"))


    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.login(smtp_login, smtp_password)
            server.sendmail(smtp_login, to_email, msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")


def send_emails_from_csv(csv_file_path, template_path):
    template = load_template(template_path)
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            subject = row["Subject"]
            email_content = row["Email Content"]
            to_email = row["Email"]
            send_email(subject, email_content, to_email, template)


if __name__ == "__main__":
    csv_file_path = "./data.csv"
    template_path = "./email_template.html"
    send_emails_from_csv(csv_file_path, template_path)
