from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
import smtplib


class email(object):
    def __init__(self):
        self.__sender = 'banxiaoer_admin@163.com'
        self.__pw = 'KMWRPPFYOLUAVRTA'
        self.__smtp_server = self._init_smtp_server('smtp.163.com', self.__sender, self.__pw)

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def _init_smtp_server(self, smtp_server, user, password):
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.login(user, password)
        return server

    def quit_server(self):
        self.__smtp_server.quit()

    def send_mail(self, subject, context):
        receivers = ['banxiaoer_admin@163.com']
        msg = MIMEText(context, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8').encode()
        try:
            self.__smtp_server.sendmail(self.__sender, receivers, msg.as_string())
            print("已发送邮件")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")


    def send_zip_file(self, receivers, zip_file):
        # receiver = ['285843349@qq.com', '1298649162@qq.com']
        emails_list = [re['email'] for re in receivers]
        to_users = [self._format_addr('{name} <{email}>'.format(**re)) for re in receivers]
        msg = MIMEMultipart()
        msg['From'] = self._format_addr('班小二 <%s>' % self.__sender)
        msg['To'] = ','.join(to_users)
        msg['Subject'] = Header('来自本周导出任务', 'utf-8').encode()
        msg.attach(MIMEText('本周导出数据，请查收', 'plain', 'utf-8'))
        with open(zip_file, 'rb') as f:
            mime = MIMEBase('application', 'zip')
            mime.add_header('Content-Disposition', 'attachment', filename=zip_file)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)
        try:
            self.__smtp_server.sendmail(self.__sender, emails_list, msg.as_string())
            print("已发送邮件")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")
