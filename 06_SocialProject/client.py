import cmd
import cowsay
import shlex
import sys
import socket
import time
import threading
import readline



class Client(cmd.Cmd):
    intro = "Welcome to the Cow chat!"
    prompt = "cowchat client$ "


    def __init__(self, socket):
        super(Client, self).__init__()
        self.socket = socket
        self.is_connected = True
        self.complete = None


    def request(self, query):
        self.socket.sendall(query.encode())


    def recieve(self):
        while self.is_connected:
            message = self.socket.recv(1024).decode().strip()
            if not self.is_connected:
                break
            if message.startswith("Message from user"):
                print(f"\n{message}\n{self.prompt}{readline.get_line_buffer()}", end="", flush=True)
            elif message.startswith("completelogin"):
                self.complete = message.split()[1:]
            elif message.startswith("completesay"):
                self.complete = message.split()[1:]
            else:
                print(f"\n{message}\n{self.prompt}", end="", flush=True)


    def do_who(self, args):
        self.request("who\n")


    def do_cows(self, args):
        self.request("cows\n")


    def do_login(self, args):
        self.request(f"login {args}\n")


    def do_say(self, args):
        self.request(f"say {args}\n")


    def do_yield(self, args):
        self.request(f"yield {args}\n")

    
    def do_quit(self, args):
        self.request("quit\n")
        self.socket.shutdown(socket.SHUT_RD)
        self.is_connected = False
        return 1


    def complete_login(self, text, line, begidx, endidx):
        self.request("completelogin\n")
        
        while self.complete is None:
            pass
        res = self.complete
        self.complete = None
        return self.complete


    def complete_say(self, text, line, begidx, endidx):
        self.request("completesay\n")

        while self.complete is None:
            pass
        res = self.complete
        self.complete = None
        return self.complete


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 1337
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        client = Client(s)
        handler = threading.Thread(target=client.recieve, args=())
        handler.start()
        client.cmdloop()
        handler.join()
