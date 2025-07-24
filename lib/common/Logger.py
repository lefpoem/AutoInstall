import logging


class Logger:
    def __init__(self, __name__):
        # 获取日志记录器
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        # 获取控制台处理器
        self.handler = logging.StreamHandler()
        self.handler.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            '[%(levelname)s]:%(asctime)s - %(filename)s:%(lineno)s: %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        pass

    def info(self, str):
        return self.logger.info(str)

    def error(self, str):
        return self.logger.error(str)

    def debug(self, str):
        return self.logger.debug(str)
