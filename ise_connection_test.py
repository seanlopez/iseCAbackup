import time
import paramiko


host = "10.124.158.173"
username = "admin"
password = "C!sc0123"

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
client.connect(host, username=username, password=password, port=22)

remote_conn = client.invoke_shell()
time.sleep(2)

remote_conn.send("\n".encode())
remote_conn.send("\n".encode())
time.sleep(2)

remote_conn.send("application configure ise\n".encode())
time.sleep(2)
remote_conn.send("0\n".encode())
remote_conn.send("\n".encode())
remote_conn.send("\n".encode())
remote_conn.send("\n".encode())
remote_conn.send("\n".encode())
remote_conn.send("exit\n".encode())
time.sleep(7)
output = remote_conn.recv(65535)
print(output.decode())


client.close()
