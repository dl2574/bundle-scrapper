import smtplib
from environs import Env

from email.message import EmailMessage

class Mailer():
    def __init__(self):
        self.env = Env()
        self.mail_list = []
        self.sender_account = []
        self.sender_password = []
        
        self.env.read_env()
    
    def send_new_bundle_email(self, bundles):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.sender_account, self.sender_password)
        
        email_to = ", ".join(self.mail_list)
        message = self.create_new_bundle_message(bundles)
        
        server.sendmail(self.sender_account, email_to, message)
        server.quit()
        
    def create_new_bundle_message(self, bundles):
        pass