import logging
from Tool.Config.configTool import ConfigTool


class LogTool(object):
    '''
      logging.basicConfig()�����п�ͨ���������������loggingģ��Ĭ����Ϊ�����ò�����
      filename����ָ�����ļ�������FiledHandler����߻���彲��handler�ĸ����������־�ᱻ�洢��ָ�����ļ��С�
      filemode���ļ��򿪷�ʽ����ָ����filenameʱʹ�����������Ĭ��ֵΪ��a������ָ��Ϊ��w����
      format��ָ��handlerʹ�õ���־��ʾ��ʽ��
      datefmt��ָ������ʱ���ʽ��
      level������rootlogger����߻ὲ�����������־����
      stream����ָ����stream����StreamHandler������ָ�������sys.stderr,sys.stdout�����ļ���Ĭ��Ϊsys.stderr����ͬʱ�г���filename��stream������������stream�����ᱻ���ԡ�

      format�����п����õ��ĸ�ʽ������
       %(name)s Logger������
       %(levelno)s ������ʽ����־����
       %(levelname)s �ı���ʽ����־����
       %(pathname)s ������־���������ģ�������·����������û��
       %(filename)s ������־���������ģ����ļ���
       %(module)s ������־���������ģ����
       %(funcName)s ������־��������ĺ�����
       %(lineno)d ������־���������������ڵĴ�����
       %(created)f ��ǰʱ�䣬��UNIX��׼�ı�ʾʱ��ĸ� ������ʾ
       %(relativeCreated)d �����־��Ϣʱ�ģ���Logger������ ���ĺ�����
       %(asctime)s �ַ�����ʽ�ĵ�ǰʱ�䡣Ĭ�ϸ�ʽ�� ��2003-07-08 16:49:45,896�������ź�����Ǻ���
       %(thread)d �߳�ID������û��
       %(threadName)s �߳���������û��
       %(process)d ����ID������û��
       %(message)s�û��������Ϣ
    '''
    file_path = ConfigTool.get('Log', 'Path')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=file_path,
                        filemode='w')

    def debug(self, message):
        logging.debug(message)

    def info(self, message):
        logging.info(message)

    def warning(self, message):
        logging.warning(message)

    def error(self, message):
        logging.error(message)

    def critical(self, message):
        logging.critical(message)






