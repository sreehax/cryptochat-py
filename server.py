import socketserver, threading
from socket import AF_INET6
dictionary = {}
fail = b"fuck off\n"
class CryptoChatHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global dictionary
        data = self.request[0]
        socket = self.request[1];
        if(data.startswith(b"addme")):
            if (self.client_address[0], self.client_address[1]) in dictionary:
                socket.sendto(b"already exists\n", self.client_address);
            else:
                original = self.client_address
                socket.sendto(b"Username: ", self.client_address);
                while True:
                    username = socket.recvfrom(32);
                    if(username[1] == original):
                        break
                    else:
                        socket.sendto(fail, username[1])
                username = username[0]
                if(username[-1] == 10):
                    username = username[:-1]
                values = list(dictionary.values())
                if(username in values):
                    socket.sendto(b"username exists\n", self.client_address);
                else:
                    dictionary[(self.client_address[0], self.client_address[1])] = username
        elif(data.startswith(b"kickme")):
            try:
                del dictionary[(self.client_address[0], self.client_address[1])]
                socket.sendto(b"success\n", self.client_address);
            except KeyError:
                socket.sendto(b"nonexistent\n", self.client_address);
        elif(data.startswith(b"ls")):
            for key in dictionary:
                s = str(key[0]) + "," + str(key[1])+":"
                s = s.encode()
                s = s + dictionary[key] + b"\n"
                socket.sendto(s, self.client_address);
        elif(data.startswith(b"req")):
            original = self.client_address
            socket.sendto(b"Username: ", self.client_address);
            while True:
                username = socket.recvfrom(32);
                if(username[1] == original):
                    break
                else:
                    socket.sendto(fail, username[1])
            username = username[0]
            if(username[-1] == 10):
                username = username[:-1]
            addr = False
            keys = list(dictionary.keys())
            values = list(dictionary.values())
            i = 0;
            v = -86;
            while i < len(values):
                if values[i] == username:
                    v = i
                    break
                i = i + 1
            if(v != -86 and keys[v] == (self.client_address[0], self.client_address[1])):
                socket.sendto(b"That is you\n", self.client_address);
            elif(v != -86):
                addr = keys[v]
                a = addr[0]+","+str(addr[1])+"\n"
                a = a.encode()
                msg = b"request-from " + addr[0].encode() + b"," + str(addr[1]).encode() + b"\n"
                socket.sendto(msg, (addr[0], addr[1]))
                socket.sendto(a, self.client_address)
            else:
                socket.sendto(b"Not Found\n", self.client_address)

        else:
            socket.sendto(fail, self.client_address);
class CryptoChatServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    address_family = AF_INET6
    daemon_threads = True
    allow_reuse_address = True
if __name__ == "__main__":
    HOST, PORT = "::", 6666
    server = CryptoChatServer((HOST, PORT), CryptoChatHandler);
    server.serve_forever();
