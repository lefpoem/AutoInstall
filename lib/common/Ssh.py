# import paramiko
# from lib.common.Logger import Logger
#
# # 定义连接SSH类
# class ClassCli:
#     def __init__(self, ip: str, username: str, passwd: str):
#         self.ip = ip
#         self.username = username
#         self.passwd = passwd
#         self.SSHConnect = self.__connect()
#         self.logger = Logger(self.__class__.__name__)
#
#     def __connect(self):
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动添加主机密钥
#         ssh.connect(self.ip, username=self.username, password=self.passwd)
#         return ssh
#
#     def exec_command(self, cmd: str):
#         stdin, stdout, stderr = self.SSHConnect.exec_command(cmd)
#         stdout_result = stdout.read().decode('utf-8', 'ignoring')
#         stderr_result = stderr.read().decode('utf-8', 'ignoring')
#         result = '{}\r\n{}'.format(cmd, stdout_result or stderr_result)
#         self.logger.info(result)
#         return '{}'.format(stdout_result or stderr_result)
#
#     def close(self):
#         self.SSHConnect.close()

import paramiko
from lib.common.Logger import Logger
import time
import re

class ClassCli:
    def __init__(self, ip: str, username: str, passwd: str):
        self.ip = ip
        self.username = username
        self.passwd = passwd
        self.SSHConnect = self.__connect()
        self.logger = Logger(self.__class__.__name__)
        self.shell = None

    def __connect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动添加主机密钥
        ssh.connect(self.ip, username=self.username, password=self.passwd)
        return ssh


    def open_shell(self):
        # 模拟交互式终端
        self.shell = self.SSHConnect.invoke_shell()
        time.sleep(1)  # 等待终端初始化完成

        # 读取并记录登录信息
        login_info = ""
        while self.shell.recv_ready():
            login_info += self.shell.recv(1024).decode('utf-8', 'ignore')
        self.logger.info("Login Information:\n" + login_info)

    def exec_command(self, cmd: str, waitstr: str = r'[#$]', timeout: int = 10):
        if not self.shell:
            self.open_shell()  # 如果shell未创建，则创建并记录登录信息

        # 发送命令
        self.shell.send(f"{cmd}\n")
        # 等待特定字符串出现
        start_time = time.time()
        output = ""
        while True:
            if self.shell.recv_ready():
                output += self.shell.recv(1024).decode('utf-8', 'ignore')
                if re.search(waitstr, output):
                    break
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Command execution timed out after {timeout} seconds")
            time.sleep(0.1)  # 稍作等待，避免CPU占用过高

        self.logger.info(output)
        return output

    def close(self):
        # 关闭SSH连接
        self.SSHConnect.close()
