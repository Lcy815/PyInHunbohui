# coding=utf-8
import smtplib
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Tool.Config.configTool import ConfigTool
from Tool.Log.logTool import LogTool


'''
   一些常用邮箱发件服务器及端口号
   邮箱   发件服务器    非SSL协议端口    SSL协议端口
   163   smtp.163.com      25             465/587
   qq    smtp.qq.com       25             465/587

   发送邮件的几个错误：
   1.550错误（smtplib.SMTPAuthenticationError: (550, b'User has no permission')）
     535错误（smtplib.SMTPAuthenticationError: (535, b'Error: authentication failed')）
     邮箱一般是不开启客户端授权的，所以登录是拒绝的，需要去邮箱开启，然后会发送短信
     获取授权码作为客户端登录的密码（login方法中的密码）
   2.503错误（503 ‘Error: A secure connection is requiered(such as ssl)’之类）
     例如我们使用QQ邮箱是需要SSL登录的，所以需要smtplib.SMTP()改成smtplib.SMTP_SSL()

   @from_addr  发送邮件的地址
   @to_addr    接收邮件的地址（可以是列表）
   @mail_host  邮箱的SMTP服务器地址
   @mail_port  邮件服务器端口号
   @mail_pass  邮箱开启smtp 需要的授权码
'''


def str_to_list(destination):
    '''
       将配置文件中的收件方转为列表
    :param destination: 收信方str
    :return:  收信人列表
    '''
    return destination.split(',')

# 邮件信息配置读取
section = 'Email'
from_addr = ConfigTool.get(section, 'From_mail')
to_addr = str_to_list(ConfigTool.get(section, 'To_mail'))
mail_host = ConfigTool.get(section, 'Host')
mail_port = int(ConfigTool.get(section, 'Port'))
mail_pass = ConfigTool.get(section, 'Pass')

print(from_addr, to_addr, mail_host, mail_port, mail_pass)


def str_to_list(destination):
    '''
       将配置文件中的收件方转为列表
    :param destination: 收信方str
    :return:  收信人列表
    '''
    return destination.split(',')


class MailTool(object):

    @classmethod
    def send_text_mail(cls, text, subject):
        '''
           发送文本信息邮件
        :param text:    文本信息
        :param subject: 邮件主题
        :return:        null
        '''
        try:
            '''
               MIMETest(content, type, 编码)  创建邮件信息主体
               msg['Subject']                 邮件主题
               msg['From']                    邮件发送方
               msg['To']                      收件方
            '''
            msg = MIMEText(text, 'plain', 'utf-8')
            msg['From'] = from_addr
            msg['To'] = ','.join(to_addr)
            msg['Subject'] = subject

            LogTool.info('Start to connection mail server ， 收信人:{to_mail}'.format(to_mail=to_addr))

            server = smtplib.SMTP_SSL(mail_host, mail_port)
            server.login(from_addr, mail_pass)
            server.sendmail(from_addr, to_addr, msg.as_string())
        except Exception as e:
            LogTool.error('Faild send Email , error message is {err}'.format(err=e))
        else:
            LogTool.info('Success send Email')
            server.quit()

    @classmethod
    def send_html_mail(cls, html, subject):
        '''
           发送html格式的邮件
        :param html:     html文本
        :param subject:  邮件主题
        :return:        null
        '''
        try:
            msg = MIMEText(html, 'html', 'utf-8')
            msg['Subject'] = subject

            LogTool.info('Start to connection mail server ， 收信人:{to_mail}'.format(to_mail=to_addr))

            smtp = smtplib.SMTP_SSL(mail_host, mail_port)
            smtp.login(from_addr, mail_pass)
            smtp.sendmail(from_addr, to_addr, msg.as_string())
        except Exception as e:
            LogTool.error('Faild send Email , error message is {err}'.format(err=e))
        else:
            LogTool.info('Success send Email')
            smtp.quit()

    @classmethod
    def send_attachment_mail(cls, text, subject, path):
        '''
           发送文本和附件的邮件
        :param text:     正文文本
        :param subject:  邮件主题
        :param path:     附件路径
        :return:         null
        '''
        try:
            # 创建邮件对象  MIMEMultipart  指定类型为 alternative可以支持同时发送html和plain，但是
            # 不会都显示，html优先显示
            msg = MIMEMultipart('alternative')
            msg['From'] = from_addr
            msg['To'] = to_addr
            msg['Subject'] = subject

            # 邮件的正文还是MIMEText
            part1 = MIMEText(text, 'plain', 'utf-8')

            # 添加附件
            att1 = MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
            att1['Content-Type'] = 'application/octet-stream'
            att1['Content-Disposition'] = 'attachment;filename="6.jpg"'
            att1['Content-ID'] = '<0>'

            msg.attach(att1)
            msg.attach(part1)

            LogTool.info('Start to connection mail server ， 收信人:{to_mail}'.format(to_mail=to_addr))

            smtp = smtplib.SMTP_SSL(mail_host, mail_port)
            smtp.login(from_addr, mail_pass)
            smtp.sendmail(from_addr, to_addr, msg
                          .as_string())
        except Exception as e:
            LogTool.error('Faild send Email , error message is {err}'.format(err=e))
        else:
            LogTool.info('Success send Email')
            smtp.quit()

'''
Message
+- MIMEBase
   +- MIMEMultipart
   +- MIMENonMultipart
      +- MIMEMessage
      +- MIMEText
      +- MIMEImage

'''
