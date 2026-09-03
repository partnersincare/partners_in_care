"""
Email Utility Module for SMTP-Based Emailing

This module provides the `DsEmail` class, a streamlined utility for sending emails
using SMTP. It supports optional attachments, HTML formatting, CC/BCC recipients, 
and customizable retry behavior. The class retrieves SMTP configuration settings 
from a specified JSON configuration file.

Typical Usage Example:
    email_client = DsEmail(search_directory='/path/to/config', logger=my_logger)
    email_client.send_email(
        subject="Test Email",
        body="This is a test email.",
        sender="sender@example.com",
        receiver="receiver@example.com",
        attachments=["/path/to/attachment.txt"]
    )

Note:
    - Ensure SMTP credentials and server information are correctly configured 
      in the JSON file located in the provided directory.
    - Recommended to pass in a logger object for tracking email send status.

Classes:
    DsEmail - A utility for configuring and sending emails via SMTP.

Raises:
    NoInternalLogging - A warning if a logger is not provided, which is optional
                        but recommended for tracking internal email processes.
"""

import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from pathlib import Path
from typing import List, Optional
import time
import os
from ..config_tools import ConfigTools


class DsEmail:
    """
    A utility class for sending formatted emails with optional attachments using SMTP.

    This class retrieves SMTP and authentication settings from a configuration file
    and provides a streamlined method for sending emails, including support for
    HTML formatting and attachments.
    """

    def __init__(self, search_directory: str = None) -> None:
        """
        Initializes the DsEmail class with SMTP configuration settings.

        Args:
            search_directory (str, optional): The directory path to locate the JSON configuration file. Defaults to cwd if not specified
        """

        if search_directory is None:
            search_directory = str(os.getcwd())
        self.config = ConfigTools(search_directory=search_directory)
        self.username = self.config.get_config_value("Alert_Email", "username")
        self.password = self.config.get_config_value("Alert_Email", "password")
        self.smtp_server = self.config.get_config_value("Alert_Email", "smtp_server")
        self.smtp_port = self.config.get_config_value("Alert_Email", "smtp_port")
        self.default_sender = self.config.get_config_value(
            "Alert_Email", "default_sender"
        )

    def send_email(
        self,
        subject: str,
        body: str,
        sender: str,
        receiver: str,
        priority: str = "3",
        attachments: Optional[List[str]] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        retries: int = 3,
        delay: int = 5,
    ) -> None:
        """
        Creates, formats, and sends an email with optional attachments, CC, and BCC support.

        Args:
            subject (str): The subject of the email.
            body (str): The body content of the email.
            sender (str): The sender's email address.
            receiver (str): The receiver's email address (comma-separated for multiple recipients).
            priority (str, optional): The priority of the email ("1" for high, "3" for normal, "5" for low).
            attachments (Optional[List[str]], optional): A list of file paths to attach to the email.
            cc (Optional[str], optional): Comma-separated list of CC recipients.
            bcc (Optional[str], optional): Comma-separated list of BCC recipients.
            retries (int, optional): Number of retry attempts in case of failure.
            delay (int, optional): Delay in seconds between retries.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        message = self.__create_message__(
            subject, body, sender, receiver, priority, cc, attachments
        )

        for attempt in range(retries):
            try:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.username, self.password)
                    server.sendmail(
                        sender,
                        [email.strip() for email in receiver.split(",")]
                        + [email.strip() for email in (cc or "").split(",") if email]
                        + [email.strip() for email in (bcc or "").split(",") if email],
                        message.as_string(),
                    )
                return True
            except smtplib.SMTPException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(delay)
        print("All attempts to send email failed.")
        return False

    def __attach_file_to_email__(self, message: MIMEMultipart, file_path: str) -> None:
        """
        Attaches a file to an email message.

        Args:
            message (MIMEMultipart): The email message to which the file will be attached.
            file_path (str): The file path of the attachment.

        Raises:
            FileNotFoundError: If the attachment file is not found.
        """
        try:
            part = MIMEBase("application", "octet-stream")
            with open(file_path, "rb") as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition", f"attachment; filename={Path(file_path).name}"
            )
            message.attach(part)
        except FileNotFoundError:

            print(f"Attachment file not found: {file_path}")
            raise
        except (PermissionError, OSError) as e:
            print(f"Error reading attachment file {file_path}: {e}")
            raise

    def __create_message__(
        self,
        subject: str,
        body: str,
        sender: str,
        receiver: str,
        priority: str = "3",
        cc: Optional[str] = None,
        attachments: Optional[List[str]] = None,
    ) -> MIMEMultipart:
        """
        Creates and formats an email message with optional CC, BCC, and attachments.

        Args:
            subject (str): The subject of the email.
            body (str): The body content of the email.
            sender (str): The sender's email address.
            receiver (str): The primary recipient's email address (comma-separated for multiple recipients).
            priority (str, optional): The priority of the email ("1" for high, "3" for normal, "5" for low).
            cc (Optional[str], optional): Comma-separated list of CC recipients.
            bcc (Optional[str], optional): Comma-separated list of BCC recipients.
            attachments (Optional[List[str]], optional): A list of file paths to attach to the email.

        Returns:
            MIMEMultipart: The constructed email message ready to be sent.
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = receiver
        message["X-Priority"] = priority

        # Email body
        html_body = f"<html><body><p>{body}</p></body></html>"
        message.attach(MIMEText(html_body, "html"))

        # Handle CC and BCC
        if cc:
            message["Cc"] = cc

        # Attach files if any
        if attachments:
            for file_path in attachments:
                self.__attach_file_to_email__(message, file_path)

        return message

    def send_task_alert_email(self, subject, body, project_name):
        """
        Sends a task alert email message to teh data and project team.

        Args:
            subject (str): The subject of the email.
            body (str): The body content of the email.
            project_name (str): The name of the project, used to grab the data and project team emails.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """

        try:
            data_team = self.config.get_config_value(
                "email_addresses", f"{project_name}_data_team"
            )
        except KeyError as e:
            raise ValueError(
                f"Data Team emails for project '{project_name}' not found in config."
            ) from e
        try:
            project_team = self.config.get_config_value(
                "email_addresses", f"{project_name}_project_team"
            )

        except KeyError:
            project_team = None
        if not project_team:
            receiver_email = data_team
        else:
            receiver_email = f"{data_team},{project_team}"

        result = self.send_email(
            subject=subject,
            body=body,
            sender=self.default_sender,
            receiver=receiver_email,
        )
        return result
