import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()


class NotificationManager:

    def __init__(self):
        self.my_email = os.getenv('EMAIL_ACCOUNT')
        self.pw = os.getenv('EMAIL_PW')
        self.receiver = "anhnguyen.workmail@gmail.com"

    def send_email(self, content):

        msg = MIMEMultipart()
        msg['From'] = self.my_email
        msg['To'] = self.receiver

        msg['Subject'] = "Alert low price ticket"
        body = content
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # Send the email
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()  # Secure the connection
                connection.login(self.my_email, self.pw)
                connection.send_message(msg)
                print('Email sent successfully!')
        except Exception as e:
            print(f'Error: {e}')