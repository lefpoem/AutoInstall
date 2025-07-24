# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from lib.common.Logger import Logger
from lib.common.Ssh import ClassCli

logger = Logger(__name__)

# Press te green button in the gutter to run the script.
if __name__ == '__main__':
    node = ClassCli("192.168.233.128", "root", "123456")
    node.exec_command("cd /var/lib/docker/containers && ls -lSh")
    container_id_set = node.exec_command("docker ps | tail -n 1 | awk '{print $1}'").splitlines()
    node.exec_command("ls /var/lib/docker/")
    node.close()

