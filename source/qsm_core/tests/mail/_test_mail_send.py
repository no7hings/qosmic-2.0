# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# 邮箱账号和授权码
sender_email = "cb.dong@foxmail.com"
sender_password = "yqlpstrjwirxbgda"  # QQ邮箱的授权码
receiver_email = "bao.d.c@foxmail.com"
smtp_server = "smtp.qq.com"
smtp_port = 465  # QQ SMTP端口

# 创建邮件对象
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "Test Email with Attachment"

# 邮件正文
body = "This is a test email with attachment sent from Python."
msg.attach(MIMEText(body, 'plain'))

# 添加附件
filename = "E:/myworkspace/mail-send/2025-0210/dokuwiki.7z.001"  # 这里替换为你要发送的文件名
attachment = open(filename, "rb")  # 打开附件文件

part = MIMEBase('application', 'octet-stream')
part.set_payload(attachment.read())
encoders.encode_base64(part)  # 编码附件内容
part.add_header('Content-Disposition', 'attachment; filename="%s"' % filename)
msg.attach(part)

# 发送邮件
try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # 使用SSL连接
    server.login(sender_email, sender_password)  # 登录QQ邮箱
    server.sendmail(sender_email, receiver_email, msg.as_string())  # 发送邮件
    print("邮件发送成功")
except Exception as e:
    print("邮件发送失败:", e)
finally:
    server.quit()  # 退出SMTP服务
