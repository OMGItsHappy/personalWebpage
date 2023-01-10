import socketserver
import os
import subprocess
import json
import socket

def add(a : int, b : int):
    return a+b


"""

responseCode : xxx,

response :{

}


{
    command : "",
    args : []
}
"""

def handleRequest(payload):
    payload = json.loads(payload)
    if payload["command"] == "logs":
        return returnLogs()

    if payload["command"] == "add":

        payload = {"responseCode" : 200,
            "response" : {
                "data" : add(int(payload["args"][0]), int(payload["args"][1]))
            }
        }
    


    if payload["command"] == "status":
        toCheck = payload['args'][0]

        a = subprocess.check_output("screen -ls".split()).decode("utf-8")

        if toCheck in a:
            payload = {"responseCode" : 200,
                        "response" : {
                            "data" : "Server " + toCheck + " Is Online"
                        }}
    
        else:
            payload = {"responseCode" : 500,
                "response" : {
                    "data" : "Server " + toCheck + " Is Offline"
                }
            }

        return payload



def returnLogs():
    try:

        f = open("/home/server/1.18/logs/latest.log", "r") 

        payload = f.read()

        payload = {"responseCode" : 200,
            "response" : {
                "data" : payload
            }
        }

        f.close()
    
    except:

        payload = {"responseCode" : 500,
                    "response" : {
                        "error" : "file could not be read",
                        "data" : ""
                    }
        }    

    if len(payload["response"]["data"]) > 2000:
        payload["response"]["data"] = payload["response"]["data"][-2000:]
    

    return payload

class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    The TCP Server class for demonstration.

    Note: We need to implement the Handle method to exchange data
    with TCP client.

    """

    def handle(self):
        # self.request - TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        self.data = self.data.decode("utf-8")

        payload = handleRequest(self.data)

        #payload = {"responseCode" : 200}

        self.request.sendall(json.dumps(payload).encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    subprocess.Popen("kill $(lsof -t -i:9999)".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    p = subprocess.Popen(["python3", "webserver.py"])

    # Init the TCP server object, bind it to the localhost on 9999 port
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer, bind_and_activate=False)

    tcp_server.allow_reuse_address = True
    tcp_server.server_bind()
    tcp_server.server_activate()

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.

    try:
        tcp_server.serve_forever()
    except KeyboardInterrupt:

        subprocess.Popen("kill $(lsof -t -i:9999)".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tcp_server.server_close()

        print("Bye, killed web server")

        p.kill()

        print('killed webserver too')