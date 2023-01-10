from flask import Flask, request, render_template, jsonify
import socket
import json
import constantsAndKeys as ck

#https://www.w3schools.com/howto/howto_website_create_resume.asp

app = Flask(__name__, static_folder="static", static_url_path="")

host_ip, server_port = "0.0.0.0", 5000
internalServerIp, internalServerPort = "localhost", 9999

def sendPacket(content : dict) -> dict:

    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    toSend = json.dumps(content)

    try:
        # Establish connection to TCP server and exchange data
        tcp_client.connect((internalServerIp, internalServerPort))
        tcp_client.sendall(toSend.encode())

        # Read data from the TCP server and close the connection
        received = tcp_client.recv(5000).decode("utf-8")

    except:
        received = json.dumps({"responseCode" : 500})

    finally:
        tcp_client.close()

    processedText = received

    return json.loads(processedText)

@app.route("/resume")
def resume():

    #https://m-softtech.in/index.php/2022/03/03/how-to-create-a-resume-design-using-html-css/

    return render_template("resume.html")

@app.route("/mom")
def mom():
    return "Feel better"


@app.route("/test", methods = ["GET", "POST"])
def test():

    #a = sendPacket({"command" : "add", "args" : ["3", "2"]})

    if request.is_json:
        data = request.args.get("toAdd")

        a = sendPacket({"command" : "add", "args" : data.split()})

        #print(data, "printing")

        return jsonify(result = a["response"]['data'])

    return render_template("test.html")

#127.0.0.1
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/add", methods = ["GET", "POST"])
def showForm():

    if request.is_json:

        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        data = request.args.get("toAdd")

        toSend = {"command" : "add", "args" : data.split()}



        try:
            # Establish connection to TCP server and exchange data
            tcp_client.connect((host_ip, server_port))
            tcp_client.sendall(json.dumps(toSend).encode())

            # Read data from the TCP server and close the connection
            received = tcp_client.recv(1024)
        finally:
            tcp_client.close()

        processedText = received.decode("utf-8")

        print(processedText)
        

        return jsonify(result = 3)

    return render_template("myform.html")


@app.get("/run/1.18")
def showStatus():

    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Establish connection to TCP server and exchange data
        tcp_client.connect((internalServerIp, internalServerPort))
        tcp_client.sendall(("check " + "1.18").encode())

        # Read data from the TCP server and close the connection
        received = tcp_client.recv(1024)
    finally:
        tcp_client.close()

    processedText = received.decode("utf-8")

    return processedText

tmp = 0
@app.route("/1.18", methods = ["GET", "POST"])
def showLogs():

    #ADD notification for server running

    global tmp
    
    if request.is_json:

        tmp += 1

        toSend = {
            "command" : "logs",
            "args" : "None"
        }

        response = sendPacket(toSend)

        response = response["response"]["data"].splitlines()

        toSend = {"command" : "status",
                  "args" : ["1.18"]}

        status = sendPacket(toSend)

        status = status["response"]["data"]

        return jsonify(count = tmp, logs = response, status = status)

    return render_template("1.18.html")

@app.route("/logs", methods = ['GET', "POST"])
def showLog():

    global tmp

    if request.is_json:

        tmp += 1

        toSend = {
            "command" : "logs",
            "args" : "None"
        }

        response = sendPacket(toSend)

        print(response)

        return jsonify(count = tmp, logs = "AAAAA", op = "true")
    
    return render_template("myform.html")

"""

#for repeated calls

setInterval(ajaxCall, 1000)

function ajaxCall() {
    $(document).ready(function(){
            $.ajax({
                url : "/1.18",
                type : "get",
                contentType : "application/json",
                data : {
                    button_text : $(this).text()
                },
                
                success : function(response){
                    $("button").text(response.seconds)
                }
            })
        })
}

-----------------------------------

function ajaxCall() {
    $(document).ready(function(){
        $("button").click(function(){
            $.ajax({
                url : "/1.18",
                type : "get",
                contentType : "application/json",
                data : {
                    button_text : $(this).text()
                },
                
                success : function(response){
                    $("button").text(response.seconds)
                }
            })
        })
    })
}

calls on click

"""



if __name__ == "__main__":
    app.run(host=host_ip, port = server_port)