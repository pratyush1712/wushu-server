import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class WushuEmail:
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    CHUNK_SIZE = 100

    def __init__(self, gmail_username, gmail_password, email_subject="", email_body=""):
        """
        Initialize the WushuEmail instance.
        """
        self.gmail_username = gmail_username
        self.gmail_password = gmail_password
        self.email_message = self.create_email_msg(email_subject, email_body)

    def create_email_msg(self, subject, body):
        """
        Create a MIMEMultipart email message.
        """
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.gmail_username
        body_content = MIMEText(body, "html")
        msg.attach(body_content)
        return msg

    def attach_images(self, images_paths):
        """
        Attach images to the email.
        """
        for path, cid in images_paths.items():
            with open(path, "rb") as f:
                img = MIMEImage(f.read())
                img.add_header("Content-ID", f"<{cid}>")
                self.email_message.attach(img)

    def send_email(self, receivers):
        """
        Send the email to a list of receivers. Handles batch sending.
        """
        num_receivers = len(receivers)
        for i in range(0, num_receivers, self.CHUNK_SIZE):
            to = receivers[i : i + self.CHUNK_SIZE]
            smtp_server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
            with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as smtp_server:
                smtp_server.starttls()
                smtp_server.login(self.gmail_username, self.gmail_password)
                smtp_server.sendmail(
                    self.gmail_username, to, self.email_message.as_string()
                )


if __name__ == "__main__":
    email_subject = "Your Subject Here"
    email_body = "Your Email Body Here"
    wushu_email = WushuEmail(
        os.environ.get("GMAIL_USER"),
        os.environ.get("GMAIL_PASSWORD"),
        email_subject,
        email_body,
    )

    # Images to be attached (paths and corresponding Content-ID)
    image_paths = {
        "./images/facebook.png": "facebook",
        "./images/instagram.png": "instagram",
        # ... add other images here ...
    }
    wushu_email.attach_images(image_paths)

    # Recipients list
    recipients = ["ps2245@cornell.edu"]
    wushu_email.send_email(recipients)
