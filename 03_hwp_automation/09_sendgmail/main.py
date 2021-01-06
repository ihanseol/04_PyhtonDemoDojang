import os
import smtplib
from ntpath import basename

from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

from config import GMAIL


def send_gmail():
    msg = MIMEMultipart()

    try:
        for file in filenames:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(file, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % basename(file))
            msg.attach(part)
    except Exception as e:
        print(e)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(my_id, my_app_pass)
    msg.attach(MIMEText(content))
    msg['Subject'] = subject


    s.sendmail(my_id, send_to, msg.as_string())
    s.quit()

def set_config():
    my_id = GMAIL['id']
    my_app_pass = GMAIL['app_pass']
    send_to = ['whackur@gmail.com', 'test@gmail.com']
    subject = 'Hello! This is subject'
    content = 'This is content'

    attach_path = os.path.dirname(os.path.realpath(__file__)) + '/attachments/'
    filenames = [os.path.join(attach_path, f) for f in os.listdir(attach_path)]
    
    print(my_id, send_to, subject, content, attach_path, filenames)
    return (my_id, my_app_pass, send_to, subject, content, attach_path, filenames)

if __name__ == "__main__":
    (my_id, my_app_pass, send_to, subject, content, attach_path, filenames) = set_config()
    send_gmail()