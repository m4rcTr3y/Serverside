#:last modified 28/02/2019
#Author:marktrevis
#date:27/02/2019
#email:marktrevis61@gmail.com
#facebook:markenzie trevis

#Server_side :onnet text message  encrypted chat program

from socket import *
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from time import sleep

class serv:
  def __init__(self) :
     
     
     self.Authent = []
     self.client = []
     self.client1 = []
     self.server = []
     self.buff = 800
     
  
  def Authentication(self):
    Authent_provided = self.server[0]
    pauth = str(Authent_provided).encode() 
    salt = b'salt_' 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
   )
    key = base64.urlsafe_b64encode(kdf.derive(pauth))
    
    self.Authent.append(key.decode())
    
      
  def client_run(self):
   sck = socket(AF_INET,SOCK_STREAM)
   inp = input("Enter user id:")
   self.client1.append(inp)
   sleep(5)
   print("client connection started to server\n")
   ip = input("enter IP address:")
   port = input("enter port number:")
   sck.connect((ip,int(port) ))
   num = self.client1[0]
   sck.send(num.encode())
   print("Authenticating....  to ",ip)
   sleep(1)
   s =  sck.recv(self.buff)
   self.Authent.append(s.decode())
   print("received authentication code from",ip,"\n ")
   sleep(2)
   print("starting Authentication....... \n")
   sleep(3)
   print("Authenticated, connection successful...")
   sleep(2)
   print("waiting for message")
   while True:
    recvm = sck.recv(self.buff)
    k = Fernet(self.Authent[0])
    feedback = k.decrypt(recvm)
    print('recieved:',feedback.decode())
    inpi = input("Enter message:")
    text = inpi.encode()
    enc = k.encrypt(text)
    sck.send(enc)
    print("message sent")
    

  def server_run(self):
   inp = input("Enter Encrypt:")
   self.server.append(inp)
   sleep(3)
   print("starting server.........")
   sck = socket(AF_INET,SOCK_STREAM)
   sck.bind(("",1025))
   sck.listen(5)
   c,a = sck.accept()
   nu = c.recv(self.buff).decode()
   self.client.append(nu)
   print("recieved client authentication")
   sleep(3)
   
   print("checking client {} connected...".format(a[0]))
   k = self.server[0]   
   self.Authentication()
   c.send(self.Authent[0].encode())
   print("Authenticated to {}".format(a[0]),'name:',self.client[0])
   while True:
    inh = input("Enter message:")
    text = inh.encode()
    k = Fernet(self.Authent[0])
    enc = k.encrypt(text)
    c.send(enc)
    print("message sent")
    recvm = c.recv(self.buff)
    fdbck = k.decrypt(recvm)
    print('recieved:',fdbck.decode())
     
  def enc_run(self):
   inp = input("Enter 1-server /2-client::")
   if inp == '1':
    sleep(1)
    print("Running as server..\n")
    sleep(2)
    self.server_run()
   elif inp =='2':
    print("Started as client\n")
    sleep(2)
    self.client_run()
   else:
    print("time out.... wrong input")
    import sys
    sys.exit()
     
if __name__=="__main__":
  serv().enc_run()
     
