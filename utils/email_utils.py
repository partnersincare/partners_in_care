from email.utils import formatdate
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
from pathlib import Path
import json

config_file_path = (
    "utils\\config_partners_in_care.json"  # located in the same directory as this file
)
with open(config_file_path, "r") as file:
    config_object = json.load(file)

partners_in_care_data_team = config_object["email_addresses"][
    "partners_in_care_data_team"
]


def send_email(subject, body, sender, receiver, attachments=None, priority="3"):
    # Read the config file for AL ERAP.

    username = config_object["Alert_Email"]["username"]
    password = config_object["Alert_Email"]["password"]

    sender_email = sender

    receiver_email = receiver

    # receiver_email = "aashish.adhikari@hornellp.com"
    # heather.heath@hornellp.com, hilaire.hopper@hornellp.com"

    # Generate email.
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    message["X-Priority"] = priority

    # write HTML part
    html = """\
    <html>
      <body>

        <p>{body}</p>


      </body>
    </html>
    """.format(
        body=body
    )

    # convert HTML part to MIMEText objects and add it to the MIMEMultipart message
    body = MIMEText(html, "html")
    message.attach(body)
    if attachments is not None:
        for path in attachments:
            part = MIMEBase("application", "octet-stream")
            with open(path, "rb") as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition", "attachment; filename={}".format(Path(path).name)
            )
            message.attach(part)

    # send email
    server = smtplib.SMTP("smtp.hornellp.com", 80)
    server.connect("smtp.hornellp.com", 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(sender_email, receiver_email.split(","), message.as_string())
    server.quit()


def send_task_alert(subject, body):
    sender_email = "Joshua.allen@horne.com"
    receiver_email = partners_in_care_data_team
    send_email(subject, body, sender_email, receiver_email)
