import serial
ser = serial.Serial("COM4")
ser.baudrate = 9600

from socket import *
host = "192.168.254.249"
port = 8000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
Buffer_size = 1023

while True:
    user_ID = []
    for i in range(8):
        user_ID.append(ser.read().decode('ascii'))
    uid=''.join([str(ele) for ele in user_ID])
    print("Welcome: Connecting to server...")
    UDPSock.sendto(uid.encode(), addr)
    option= int(UDPSock.recvfrom(Buffer_size)[0])
    if(option==6):
        print("User Doesn't Exist")
    else:
        pin=input("Enter your PIN: ")
        UDPSock.sendto(pin.encode(), addr)
        option = int(UDPSock.recvfrom(Buffer_size)[0])
        if(option==3):
            print("Authentication Failed")
        else:
            amt=input("Authentication Successful \nEnter Transaction Amount: " )
            UDPSock.sendto(amt.encode(), addr)
            option = int(UDPSock.recvfrom(Buffer_size)[0])
            if(option==4):
                print("Transaction Failed")
            else:
                print("Successful Transaction")

UDPSock.close()


