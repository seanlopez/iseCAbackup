import paramiko
import time
import json

class ise_cli_handler(object):
    def __init__(self):
        configuration_file = open("ise_info.json", "r", encoding="utf-8")
        ise_info = json.loads(configuration_file.read())
        configuration_file.close()
        self.ise_ip = ise_info["host"]
        self.username = ise_info["username"]
        self.password = ise_info["password"]
        self.target_repository = ise_info["target_repository_name"]
        self.ca_key = ise_info["ca_key"]
        self.ssh_port = 22
        self.ssh_session = self.ssh_session_generator()
        '''
        invoke the terminal
        '''
        remote_terminal = self.ssh_session.invoke_shell()
        time.sleep(5)

        self.remote_terminal = remote_terminal

    def ssh_session_generator(self):
        '''
        create ssh session "client"
        :return: "client" object
        '''
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        client.connect(self.ise_ip, username=self.username, password=self.password, port=self.ssh_port)

        return client


    def clear_existing_session(self):
        '''
        delete existing session to avoid the maxium session issue
        :return:
        '''
        self.remote_terminal.send("1\n".encode())
        time.sleep(2)
        self.remote_terminal.send("1\n".encode())
        self.remote_terminal.send("\x03\n".encode())
        self.remote_terminal.send("\n".encode())
        self.remote_terminal.send("\n".encode())
        self.remote_terminal.send("exit\n".encode())
        time.sleep(5)
        output = self.remote_terminal.recv(65535)
        # print(output.decode())
        self.ssh_session.close()
