import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders
from email.utils import parseaddr, formataddr

smtp_server = 'smtp.163.com'
from_addr = 'seankanthsu@163.com'
to_addr = 'seankanthsu@163.com'

def send_email(title, content, to_addr=to_addr, attach=None, passwd=None):
    msg = MIMEMultipart()
    msg['Subject'] = Header(title, charset='utf-8')
    msg['From'] = from_addr
    msg['To'] = ';'.join(to_addr) if isinstance(to_addr, (list, tuple)) else to_addr
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    if attach:
        for path in attach:
            if os.path.exists(path):
                print(path)
                filename = path.split('/')[-1] + '.txt'
                with open(path, 'rb') as f:
                    attachment = MIMEBase('text', 'txt', filename=filename)
                    attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                    attachment.set_payload(f.read())
                    encoders.encode_base64(attachment)
                    msg.attach(attachment)

    try:
        server = smtplib.SMTP(host=smtp_server, port=25, timeout=10)
        server.set_debuglevel(1)
        server.starttls()
        server.login(user=from_addr, password=passwd)
        server.sendmail(from_addr=from_addr, to_addrs=to_addr, msg=msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(str(e))
        return False

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store', default='Experiment', dest='title', help='title')
    parser.add_argument('-c', action='store', default='', dest='content', help='content')
    parser.add_argument('-a', action='append', default=[to_addr], dest='to_addrs', help='to_addrs')
    parser.add_argument('-f', action='append', default=[], dest='files', help='files')
    args = parser.parse_args()

    send_email(args.title, args.content, to_addr=args.to_addrs, attach=args.files, passwd='')