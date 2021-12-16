"""
Send email every N seconds.
"""

import time
import smtplib
import argparse
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage


def parse_user_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--every_n_seconds",
        type=int,
        default=3600,
        help="send email every n seconds"
    )
    parser.add_argument(
        "--sender",
        type=str,
        help="email of sender"
    )
    parser.add_argument(
        "--sender_password",
        type=str,
        help="sender email password"
    )
    parser.add_argument(
        "--receiver",
        type=str,
        help="email of receiver"
    )
    parser.add_argument(
        "--image_path",
        type=str,
        default=None,
        help="path to image to attach",
        required=False,
    )
    parser.add_argument(
        "--email_server",
        type=str,
        default="smtp.gmail.com",
        help="path to email server",
        required=False,
    )
    parser.add_argument(
        "--email_port",
        type=int,
        default=465,
        help="path to email port",
        required=False
    )

    return parser.parse_args()


def send_email(
    sender,
    receiver,
    sender_password,
    image_path,
    email_server,
    email_port
    ):

    # Create the root message
    msg_root = MIMEMultipart("related")
    msg_root["Subject"] = "Capture from Video Feed"
    msg_root["From"] = sender
    msg_root["To"] = receiver

    # Set alternative configuration
    msg_alt = MIMEMultipart("alternative")
    msg_root.attach(msg_alt)

    # Define email format
    msg_text = MIMEText('<br><img src="cid:image1"><br>', "html")
    msg_alt.attach(msg_text)

    # Check if an image was provided
    if image_path is not None:

        # Read image
        img = open(image_path, "rb")
        msg_img = MIMEImage(img.read())
        img.close()

        # Define the image's ID as referenced above
        msg_img.add_header("Content-ID", "<image1>")
        msg_root.attach(msg_img)

    # Send email
    server_ssl = smtplib.SMTP_SSL(email_server, email_port)
    server_ssl.login(sender, sender_password)
    server_ssl.sendmail(sender, receiver, msg_root.as_string())
    server_ssl.close()

    # Notify
    print("Sent email.")


if __name__ == "__main__":

    # Parse user arguments
    args = parse_user_arguments()

    # Keep sending emails
    while True:

        # Send
        send_email(
            sender=args.sender,
            receiver=args.receiver,
            sender_password=args.sender_password,
            image_path=args.image_path,
            email_server=args.email_server,
            email_port=args.email_port,
        )

        # Pause
        time.sleep(args.every_n_seconds)
