import os
import smtplib
import imghdr
from email.message import EmailMessage

password = os.getenv("GMAIL_PASSWORD")
sender = os.getenv("SENDER")
receiver = os.getenv("RECEIVER")


def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "Intruder Pic"
    email_message.set_content("There's an intruder!")

    with open(image_path, "rb") as file:
        content = file.read()

    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password)
    gmail.sendmail(sender, receiver, email_message.as_string())
    gmail.quit()


# Testing method by itself
if __name__ == "__main__":
    send_email(image_path="images/test.png")
