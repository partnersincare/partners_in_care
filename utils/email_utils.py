import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from pathlib import Path
import json
import os


class EmailConfig:
    def __init__(self, config_filename=None, search_directory="utils"):
        if config_filename is None:
            config_filename = self._find_config_file(search_directory)
        self.config = self._load_config(config_filename)
        self.username = self.config["Alert_Email"]["username"]
        self.password = self.config["Alert_Email"]["password"]
        self.smtp_server = "smtp.hornellp.com"
        self.smtp_port = 587

    def _load_config(self, config_filename):
        """Load the config file."""
        with open(config_filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def _find_config_file(self, search_directory):
        """Search for the first JSON config file in the directory."""
        for root, _, files in os.walk(search_directory):
            for file in files:
                if file.endswith(".json"):
                    return os.path.join(root, file)
        raise FileNotFoundError(
            f"No JSON configuration file found in {search_directory}"
        )

    def get_receiver_emails(self, project_name):
        """Retrieve the correct email addresses for the data and project teams based on project name."""
        email_addresses = self.config["email_addresses"]
        return {
            "data_team": email_addresses.get(f"{project_name}_data_team"),
            "project_team": email_addresses.get(f"{project_name}_proj_team"),
        }


def create_email(subject, body, sender, receiver, priority="3", attachments=None):
    """Create an email with optional attachments."""
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = receiver
    message["X-Priority"] = priority

    # Email body
    html = f"""\
    <html>
      <body>
        <p>{body}</p>
      </body>
    </html>
    """
    message.attach(MIMEText(html, "html"))

    # Attach files if any
    if attachments:
        for path in attachments:
            attach_file_to_email(message, path)

    return message


def attach_file_to_email(message, file_path):
    """Attach a file to the email."""
    part = MIMEBase("application", "octet-stream")
    with open(file_path, "rb") as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition", f"attachment; filename={Path(file_path).name}"
    )
    message.attach(part)


def send_email(message, sender, receiver, config):
    """Send the email using the SMTP server."""
    with smtplib.SMTP(config.smtp_server, config.smtp_port) as server:
        server.starttls()
        server.login(config.username, config.password)
        server.sendmail(sender, receiver.split(","), message.as_string())


def send_task_alert(subject, body, project_name, config_filename=None):
    """Send a task alert to the teams specific to the project."""
    config = EmailConfig(config_filename=config_filename)  # Load configuration
    sender_email = "Joshua.allen@horne.com"

    # Get project-specific teams
    receivers = config.get_receiver_emails(project_name)

    if not receivers["data_team"] or not receivers["project_team"]:
        raise ValueError(
            f"Team emails for project '{project_name}' not found in config."
        )

    receiver_email = f"{receivers['data_team']},{receivers['project_team']}"

    email_message = create_email(subject, body, sender_email, receiver_email)
    send_email(email_message, sender_email, receiver_email, config)
