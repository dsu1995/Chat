from socket import socket, gethostbyname, gethostname   
from threading import Thread       

class Chat:
	PORT = 12345

	def __init__(self, inport = PORT):
		self.insocket = socket()		
		self.source = None
		self.connection = None
		self.host = gethostbyname(gethostname())
		self.inport = inport
		self.insocket.bind((self.host, self.inport))
		self.insocket.listen(10)		
		Thread(target = self.listen, daemon = True).start()

		self.outsocket = None
		self.recipient = None		
		
	def listen(self):
		print("Listening on Server:", self.host, ", Port:", self.inport)
		while 1:
			self.connection, self.source = self.insocket.accept()
			print("Message from Server:", self.source[0], ", Port:", self.source[1])
			try:
				print(self.connection.recv(1024).decode())
			except Exception as e:
				print("Receive Failed:", e)
			self.connection.close()
	
	def reply(self, msg, outport = PORT):
		if self.source:
			self.send(msg, self.source[0], outport)
		else:
			print("No one to reply to")

	def send(self, msg, recipient = None, outport = PORT):
		if recipient:
			self.recipient = recipient
			
		self.outsocket = socket()
		try:
			self.outsocket.connect((self.recipient, outport))
			print("Connected to Server:", self.recipient, ", Port:", outport)
			self.outsocket.sendall(msg.encode())
			print("Message sent")
		except Exception as e:			
			print("Send Failed:", e)
		self.outsocket.close()	

	def __del__(self):
		print("Shutting down")
		if self.insocket:
			self.insocket.close()
		if self.outsocket:
			self.outsocket.close()     
		if self.connection:
			self.connection.close()
	    



