from ise_cli_handler import ise_cli_handler
import time

if __name__ == "__main__":
    print("[Info] Script init")
    ise_ssh_session = ise_cli_handler()

    while True:
        '''
        check and clear all existing sessions
        '''
        output = ise_ssh_session.remote_terminal.recv(65535)
        output_list = output.decode().split("\n")
        # print(output_list)
        if output_list[-1] == "ISE31-01/admin# ":
            # 如果不存在existing session
            print("[Info] no existing session")
            break
        else:
            # 如果存在existing session
            ise_ssh_session.clear_existing_session()
            # renew the connection
            ise_ssh_session = ise_cli_handler()
            print("[Warning] Destroy the existing session and create a new session")

    # "enter key" sleep for 2 sec
    ise_ssh_session.remote_terminal.send("\n".encode())
    ise_ssh_session.remote_terminal.send("\n".encode())
    ise_ssh_session.remote_terminal.send("\x03\n".encode())
    ise_ssh_session.remote_terminal.send("\n".encode())
    # ise_ssh_session.remote_terminal.send("exit\n".encode())
    time.sleep(2)

    # Apply the configuration
    output = ise_ssh_session.remote_terminal.recv(65535)
    output_list = output.decode().split("\n")
    # print(output_list)
    if "ISE31-01/admin#" in output_list[-1]:
        '''
        start to export the CA file if currently last line in ISE cli is "admin#"
        '''
        print("[Info] start to export the CA file")
        ise_ssh_session.remote_terminal.send("application configure ise\n".encode())
        ise_ssh_session.remote_terminal.send("7\n".encode())   # select the 7 to "export"
        time.sleep(5)
        # enter the repository
        ise_ssh_session.remote_terminal.send(f"{ise_ssh_session.target_repository}\n".encode())   # enter the ISE repository name
        time.sleep(5)
        # enter the CA file key
        ise_ssh_session.remote_terminal.send(f"{ise_ssh_session.ca_key}\n".encode())    # exported CA file key
        # print(ise_ssh_session.remote_terminal.recv(65535).decode().split("\n"))
        if "Enter encryption-key for export:" in ise_ssh_session.remote_terminal.recv(65535).decode().split("\n")[-2]:
            print("[Info] exporting start, estimation timing 100s")
            time.sleep(100)
            ca_export_result_output = ise_ssh_session.remote_terminal.recv(65535).decode().split("\n")
        else:
            print("[Warning] Export Fail, please check the status of ISE and 'ise_info.json' file")
            ise_ssh_session.remote_terminal.send("\x03\n".encode())
            ise_ssh_session.remote_terminal.send("\n".encode())
            ise_ssh_session.clear_existing_session()
            exit(0)

        # Export successfully judgement
        for line in ca_export_result_output:
            if "ISE CA keys export completed successfully" in line:
                print("[Info] Export Successfully!")
                ise_ssh_session.remote_terminal.send("0\n".encode())
                ise_ssh_session.remote_terminal.send("\n".encode())
                ise_ssh_session.remote_terminal.send("exit\n".encode())
                break
            elif ca_export_result_output.index(line) == len(ca_export_result_output) - 1:
                print("[Warning] Export Fail")
                ise_ssh_session.remote_terminal.send("0\n".encode())
                ise_ssh_session.remote_terminal.send("\n".encode())
                ise_ssh_session.remote_terminal.send("exit\n".encode())
                break
    else:
        print("[Warning] Session Status is abnormal, session is terminated")


    # destroy the session
    print(ise_ssh_session.remote_terminal.recv(65535).decode())
    ise_ssh_session.ssh_session.close()
