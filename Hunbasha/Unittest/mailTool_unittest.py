# <html><h1>ÄãºÃ</h1></html>

# encoding=utf-8

from Tool.Email.emailTool import MailTool
import unittest


class MailTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sendtext(self):
        text = 'I love python'
        subject = 'Test'
        MailTool.send_text_mail(text, subject)


if __name__ == '__main__':
    unittest.main()
