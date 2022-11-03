import os
import smtplib

import dotenv
class Notificator():
    def __init__(self) -> None:
        self.s = smtplib.SMTP_SSL('smtp.mail.ru',465)
        dotenv.load_dotenv()
        self.email = os.getenv('cve_mail')
        self.password = os.getenv('cve_mail_password')
        self.s.login(f"{self.email}", f"{self.password}")

    def notificator(self,subject,text,where_to_mail):
        msg = 'Subject: {}\n\n{}'.format(subject,text)
        self.s.sendmail(f"{self.email}", where_to_mail, msg)
