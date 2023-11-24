import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import logging
import re
import traceback

class Email_managment:

    @staticmethod
    def send_email(server, port, username, password, sender, recipient, subject, body, attachment=None):
        if Email_managment.validateEmail(recipient):
            try:
                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = recipient
                msg['Subject'] = subject
            
                msg.attach(MIMEText(body, 'html'))
            
                if attachment:
                    with open(attachment, 'rb') as f:
                        part = MIMEApplication(f.read(), Name=attachment)
                        part['Content-Disposition'] = 'attachment; filename="%s"' % attachment
                        msg.attach(part)
        
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(server, port, context=context) as smtp:
                    smtp.login(username, password)
                    smtp.sendmail(sender, recipient, msg.as_string())
                    smtp.quit()
                    logging.info("e-mail sending successed:" + sender + " -> " + recipient)
                    return True
            except Exception as e:
                logging.error("e-mail sending failed:" + str(e), exc_info=True)
                print("\n邮件发送失败：" + str(e))
                traceback.print_exc()
                return False
        else:
            logging.info("邮箱地址格式错误!")
    

    def validateEmail(email):
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            #print(f'邮箱地址验证成功——>{email}')
            return True
        else:
            print(f'邮箱地址格式验证失败——>{email}')
            return False



#测试用代码        
# 设置SMTP服务器信息
server = ""
port = 465
username = ""
password = ""          
recipient = ''
subject = 'test' 
body = '<html>this is a test email</html> ' 
email_managment = Email_managment()

result = email_managment.send_email(server, port, username,  password, username, recipient, subject, body, attachment=None)
print(result)
if result:
    print('发送成功')
else:
    print('发送失败')

