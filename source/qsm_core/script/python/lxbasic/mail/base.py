# coding:utf-8
from __future__ import print_function

import os

import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

from email.mime.base import MIMEBase

from email import encoders

from ..wrap import *


class MySmtp:
    SERVER = "smtp.qq.com"
    PORT = 465
    # todo: save in local configure
    SENDER_EMAIL = "cb.dong@foxmail.com"
    SENDER_PASSWORD = "yqlpstrjwirxbgda"


class MyMail(object):

    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self._smtp_server = smtp_server
        self._smtp_port = smtp_port
        self._sender_email = sender_email
        self._sender_password = sender_password

    def send(self, receiver_email, subject, body, files):
        sender_email = self._sender_email
        sender_password = self._sender_password
        smtp_server = self._smtp_server
        smtp_port = self._smtp_port

        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # 邮件正文
        msg.attach(MIMEText(body, 'plain'))

        # 添加多个附件
        for i_file_path in files:
            try:
                with open(i_file_path, "rb") as attachment:
                    i_file_name = os.path.basename(i_file_path)
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment; filename="%s"' % i_file_name)
                    msg.attach(part)
            except Exception as e:
                print("无法添加附件 %s: %s" % (i_file_path, str(e)))

        # 发送邮件
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        try:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("邮件发送成功")
        except Exception as e:
            print("邮件发送失败:", str(e))
        finally:
            server.quit()

    @classmethod
    def test(cls):
        cls(
            smtp_server=MySmtp.SERVER,
            smtp_port=MySmtp.PORT,
            sender_email=MySmtp.SENDER_EMAIL,
            sender_password=MySmtp.SENDER_PASSWORD,
        ).send(
            receiver_email="bao.d.c@foxmail.com",
            subject='python mail send test',
            body="This is a test email with multiple attachments sent from Python.",
            files=['E:/myworkspace/mail-send/2025-0210/dokuwiki-0/dokuwiki.7z.001']
        )

    @classmethod
    def send_files_to_xj(cls, directory_path):
        import os

        directory_path = ensure_string()

        file_names = os.listdir(directory_path)

        name = os.path.basename(directory_path)

        for i_file_name in file_names:
            i_file_path = u'{}/{}'.format(directory_path, i_file_name)
            i_subject = u'{}/{}'.format(name, i_file_name)
            i_body = i_file_path
            cls(
                smtp_server=MySmtp.SERVER,
                smtp_port=MySmtp.PORT,
                sender_email=MySmtp.SENDER_EMAIL,
                sender_password=MySmtp.SENDER_PASSWORD,
            ).send(
                receiver_email='dong.changbao@qinsmoon.cn',
                subject=i_subject,
                body=i_body,
                files=[i_file_path]
            )
