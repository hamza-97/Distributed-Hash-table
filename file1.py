import socket
from thread import *
import threading
import sys
import pickle
import hashlib
import time
import os.path


IP_address = "127.0.0.1"
global port
max_nodes = 91
nodes = []
succ_list = []
class node:
	ID = None
	predecessor = None
	successor = None
	port = None
	key = None
	successor2 = None
	files = []
	ft = []

	def __init__(self, Port, ID):
		self.ID= ID
		self.port = Port
		self.successor= Port
		self.predecessor = Port
		node.successor2 = Port
		self.key = ID

def ft(node):

	while(1):
		myfinger = []
		time.sleep(10)
		myfinger.append(node.successor)
		# print "first entry ",node.successor
		mysucc = node.successor
		while (1):
			if (mysucc == node.port):
				break

			s = socket.socket()
			s.connect((IP_address,mysucc))
			s.send("Please succ")
			time.sleep(1)
			mysucc = int(s.recv(1024))
			# print "Hey bro my succ is ", mysucc
			if (mysucc == node.port):
				break
			myfinger.append(mysucc)

		num = 0
		num1 = 0
		for a in myfinger:
			# print a
			if num == 0 or num ==1 or num == 3 or num == 7:
				node.ft[num1] = a
				num1 +=1
			num +=1


def fail(node):
	while (1):
		time.sleep(10)
		try:

			msg = ""
			s = socket.socket()
			s.connect((IP_address,node.successor))
			s.send("Please succ")
			node.successor2 = int(s.recv(1024))
			for i in range(3):
				s.send("hello")
				time.sleep(0.5)
				msg = s.recv(1024)
				if msg == "ok":
					break

			if msg == "":
				node.successor = node.successor2
		except:
			abcdefghijkl = 0
			# print("wait")







def hasher(port):
	hashing = hashlib.sha1(str(port))
	hashing = int(hashing.hexdigest(), 16) % 91
	hashing = hashing % max_nodes
	return int(hashing)

def leaver(node):
	files = os.listdir(".")
	node.files.append(files)
	for fi in files:
		print "Giving away ", fi
		s = socket.socket()
		s.connect((IP_address,node.successor))
		s.send("Putting the file")
		time.sleep(0.5)
		s.send(fi)
		print "File name sent"
		check = s.recv(1024)
		print check
		if check == "Okay send":
			f = open(fi,'rb')
			reading = f.read(1024)
			while reading:
				s.send(reading)
				reading = f.read(1024)
			f.close()
			# s.send("File sent")
			s.close()
		if check == "I already have it":
			pass

	news = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	news.connect((IP_address,node.predecessor))
	news.send("1122")  #telling predecessor
	time.sleep(0.5)
	news.send(str(node.successor))
	news.close()
	thenews = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	thenews.connect((IP_address,node.successor))
	thenews.send("2211") #telling sucessor
	time.sleep(0.5)
	thenews.send(str(node.predecessor))
	
	
	thenews.close()

	sys.exit()

def clienthread(node,port,newsock):
	print "client"
	time.sleep(0.5)
	newsock.send(str(node.port))
	while(1):
		number = newsock.recv(1024)
		print "Here ", number
		if int(number) ==  1122:
			node.predecessor = int(client.recv(1024))
			print "Updated pred is ", node.predecessor
			break

		elif int(number) == 2211:
			node.successor = int(client.recv(1024))
			print "Updated suc is ", node.successor
			break

		if int(number) == 2:
			node.successor = port
			print "oOk"
			break

		elif int(number) == 11:
			node.successor = int(newsock.recv(1024))

			newsock = socket.socket()
			newsock.connect((IP_address,node.successor))
			newsock.send(str(int(number)))
			time.sleep(0.5)
			newsock.send(str(node.port))
			break


		elif int(number) == 12:
			node.successor = int(newsock.recv(1024))
			node.predecessor = port
			newsock = socket.socket()
			newsock.connect((IP_address,node.successor))
			newsock.send(str(int(number)))
			
			time.sleep(0.5)
			
			newsock.send(str(node.port))
			break

		elif int(number) == 13:
			node.successor = int(newsock.recv(1024))
			node.predecessor = port
			newsock = socket.socket()
			newsock.connect((IP_address,node.successor))
			newsock.send(str(int(number)))
			
			time.sleep(0.5)
			
			newsock.send(str(node.port))
			break

		elif int(number) == 999999:

			recv = int(newsock.recv(1024))
			print "again ",recv
			port = recv
			node.predecessor = int(recv)
			newsock = socket.socket()
			newsock.connect((IP_address,recv))
			newsock.send(str(node.port))





	print "node.predecessor is: ", node.predecessor
	print "node.successor is: ", node.successor	
	while (1):	
		print("1. Upload")
		print("2. Download")
		print("3. Predecessor")
		print("4. Successor")
		print("5. Join")
		print("6. Leave")
		print("7. Finger table")
		option = input("Select your option")
		
		if option == 6: #I think I should leave
			leaver(node)
			print("I am going far away")
			break
		if option == 2:
			# Time to get the file back
			file = raw_input("Which file do u want")
			already = os.path.isfile(str(file))
			if already:
				print("Bro you already have the file")
			else:
				getme(file,node)
		if option == 1:
			# We are putting the file on the DHT
			file = raw_input("What is the name of the file: ")
			already = os.path.isfile(str(file))
			if already== False:
				print("Bhai teray pass khud nahi hai")
			else:
				putfile(file,node)
		if option == 7:
			for i in range(4):
				if node.ft[i] != 0:
					print node.ft[i]

	print "node.predecessor is: ", node.predecessor
	print "node.successor is: ", node.successor	

	


def putfile(file,node):
	print "we are about to insert file ", file
	file_hash = hashlib.sha1(file)
	file_hash = int(file_hash.hexdigest(), 16) % 43 + 2000
	print "file hash is " ,file_hash
	if file_hash == node.ID:
		return
	succ = node.successor
	me = node.port
	while (1):
		print "Hey"
		if file_hash > me and file_hash <= succ:
			print "case 1"
			s = socket.socket()
			s.connect((IP_address,succ))
			s.send("Putting the file")
			time.sleep(0.5)
			s.send(file)
			check = s.recv(1024)
			print check
			if check == "Okay send":
				f = open(file,'rb')
				reading = f.read(1024)
				while reading:
					s.send(reading)
					reading = f.read(1024)
				f.close()
				s.send("File sent")
				s.close()
				break
		elif file_hash < me and file_hash < succ and succ < me:
			s = socket.socket()
			s.connect((IP_address,succ))
			s.send("Putting the file")
			time.sleep(0.5)
			s.send(file)
			check = s.recv(1024)
			print check
			if check == "Okay send":
				f = open(file,'rb')
				reading = f.read(1024)
				while reading:
					s.send(reading)
					reading = f.read(1024)
				f.close()
				s.send("File sent")
				s.close()
				break

		elif file_hash > me and succ < me:
			s = socket.socket()
			s.connect((IP_address,succ))
			s.send("Putting the file")
			time.sleep(0.5)
			s.send(file)
			check = s.recv(1024)
			print check
			if check == "Okay send":
				f = open(file,'rb')
				reading = f.read(1024)
				while reading:
					s.send(reading)
					reading = f.read(1024)
				f.close()
				s.send("File sent")
				s.close()
				break


		else:
			print "best"
			s = socket.socket()
			s.connect((IP_address,succ))
			s.send("Please succ")
			time.sleep(0.5)
			recv = int(s.recv(1024))
			me = succ
			succ = recv
			if succ == node.port:
				break
			# newsock = socket.socket()
			# newsock.connect((IP_address,recv))
			# node = node(IP_address,recv)
			# newsock.send(str(node.port))


		# elif file_hash > node.ID and file_hash <= hasher(node.predecessor):


		# else:



	


def getme(file,node):
	print "Getting file ", file
	file_hash = hashlib.sha1(file)
	file_hash = int(file_hash.hexdigest(), 16) % 43 + 2000
	# file_hash = file_hash & max_nodes
	print "file hash is " ,file_hash
	succ = node.successor
	me = node.port
	if file_hash == node.port:
		print "File not found"
		return
	while (1):
		if file_hash > me and file_hash <= succ:
			# file has to be with the successor
			s = socket.socket()
			s.connect((IP_address,succ))
			s.send("Please send file")
			time.sleep(0.5)
			s.send(file)
			check = s.recv(1024)
			if check == "Yeah bro have it":
				f = open(file,'wb')
				reading = s.recv(1024)
				while (reading):
					f.write(reading)
					reading = s.recv(1024)
				print "received"
				f.close()
				print "file received"
				print "now to send the successor"
				news1 = socket.socket()
				news1.connect((IP_address,node.successor))
				print "now connected to server"
				news1.send("Putting the file")
				time.sleep(0.5)
				news1.send(file)
				time.sleep(0.1)
				check = news1.recv(1024)
				print check
				if check == "Okay send":
					f = open(file,'rb')
					reading = f.read(1024)
					while reading:
						news1.send(reading)
						reading = f.read(1024)
					f.close()
					news1.send("File sent")
					news1.close()



				return
			else:
				print "File not found"
				return
		elif file_hash < me and file_hash < succ and succ < me:
			s = socket.socket()
			s.connect((IP_address,succ))
			s.send("Please send file")
			time.sleep(0.5)
			s.send(file)
			check = s.recv(1024)
			if check == "Yeah bro have it":
				f = open(file,'wb')
				reading = s.recv(1024)
				while (reading):
					f.write(reading)
					reading = s.recv(1024)
				print "received"
				f.close()
				print "file received"
				return
			else:
				print "File not found"
				return

		elif file_hash > me and succ < me:
			s = socket.socket()
			s.connect((IP_address,succ))
			s.send("Please send file")
			time.sleep(0.5)
			s.send(file)
			check = s.recv(1024)
			if check == "Yeah bro have it":
				f = open(file,'wb')
				reading = s.recv(1024)
				while (reading):
					f.write(reading)
					reading = s.recv(1024)
				print "received"
				f.close()
				print "file received"
				return
			else:
				print "File not found"
				return
		else:
				print "best"
				s = socket.socket()
				s.connect((IP_address,succ))
				s.send("Please succ")
				time.sleep(0.5)
				recv = int(s.recv(1024))
				me = succ
				succ = recv
				if me == node.port:
					print "File not found"
					break









# Node wo hai jiss ka saath connect howa hai
def serverthread(client,info,node):
	print "Server"
	receiver = client.recv(1024)
	print ("incoming " + str(receiver) + "also " + str(node.port))
	if receiver == "Please succ":
		print "ok"
		client.send(str(node.successor))
	elif receiver == "Please send file":
		filename = client.recv(1024)
		already = os.path.isfile(str(filename))
		if already == True:
			client.send("Yeah bro have it")
			f = open(filename,'rb')
			reading = f.read(1024)
			while reading:
				client.send(reading)
				reading = f.read(1024)
			f.close()
			client.send("File sent")
			client.close()
		else:
			client.send("not found")



	elif receiver == "Putting the file":
		filename = client.recv(1024)
		already = os.path.isfile(str(filename))
		if already == True:
			client.send("I already have it") 
			return
		else:
			client.send("Okay send")
			f = open(filename,'wb')
			reading = client.recv(1024)
			while (reading):
				f.write(reading)
				reading = client.recv(1024)
			print "received"
			f.close()
			print "file received"
			return



	elif int(receiver) ==  1122:
		node.successor = int(client.recv(1024))
		print ("Updated pred server is ", node.successor)
	elif int(receiver) == 2211:
		node.predecessor = int(client.recv(1024))
		print ("Updated succ server is ", node.predecessor)

	elif int(receiver) == 11:
		node.predecessor = int(client.recv(1024))
	elif int(receiver) == 12:
		node.predecessor = int(client.recv(1024))
	elif int(receiver) == 13:
		node.predecessor = int(client.recv(1024))

	else:
		newport = int (receiver)
		
		print newport
		if node.predecessor == node.successor and node.port == node.predecessor and node.port == node.successor:
			print("There are only 2 nodes for now")
			node.predecessor = newport
			node.successor = newport
			client.send("2")

		else:
			# case 1 node is in between
			if node.port < newport and node.successor > newport: 
					# if node.predecessor >= newport:
					print("case 1") #11
					succ = node.successor
					node.successor = newport
					client.send("11")
					time.sleep(0.5)
					client.send(str(succ))

					
			# case 2 node is end
			elif node.successor < node.port and node.port<newport:
					# if node.predecessor <= newport:
					succ = node.successor
					node.successor = newport
					print "case 2"
					client.send("12")
					time.sleep(0.5)
					# send predecssor
					client.send(str(succ))
			elif node.port > newport and newport < node.successor and node.successor < node.port:
					pred = node.predecessor
					node.predecessor = newport
					print "case 3"
					client.send("12")
					time.sleep(0.5)
					# send predecssor
					client.send(str(pred))
			# case 3 node is start
			# elif node.port > newport:
			# 	succ = node.successor
			# 	node.successor = newport
			# 	print "case 4"
			# 	client.send("13")
			# 	time.sleep(0.5)
			# 	client.send(str(succ))
			# 	node.successor = int(client.recv(1024))
			else:
				client.send("999999")
				time.sleep(0.5)
				client.send(str(node.successor))
	print "node.predecessor is: ", node.predecessor
	print "node.successor is: ", node.successor

					



def main():
	global port
	global IP_address
	The_port = int(sys.argv[1])
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((IP_address,The_port))
	s.listen(5)
	hashed = hasher(The_port)
	# hashed = hashed.hexdigest()
	# ID = int(hashed)
	ID = hashed

	print "The id is " ,ID
	newnode = node(The_port,ID)
	start_new_thread(fail,(newnode,))
	for i in range(4):
		newnode.ft.append(0)

	start_new_thread(ft,(newnode,))
	files = os.listdir(".")
	# newnode.files.append(files)
	print files

	asking = raw_input("Are you a new node?")
	if asking == 'yes':
		counter = 0
		print "New node is now " ,newnode.port
		news = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print "About to connect"
		news.connect((IP_address,newnode.port))
		print("Yeah connected")
		print "predecessor is ", newnode.predecessor
		print "successor is ", newnode.successor
		print("Connected to itself")
		counter = counter + 1
		start_new_thread(clienthread,(newnode,newnode.port,news))
		while True:
			client,info = s.accept()
			if counter ==1:
				print "Lets now wait for another node"
				counter = counter + 1
			else:
				print("connected to ", info)

			start_new_thread(serverthread,(client,info,newnode))
	else:
		known_port = raw_input("What is the port?")
		known_port = int(known_port)
		newnode.predecessor = known_port
		news = socket.socket()
		news.connect((IP_address,known_port))
		print "You are now connected to ", known_port

		start_new_thread(clienthread,(newnode,known_port,news))
		while True:
			client,info = s.accept()
			print ("connected to ", info)
			start_new_thread(serverthread,(client,info,newnode))





if __name__ == '__main__':
	main()
