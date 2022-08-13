import pandas as pd
from socket import *

host = "192.168.107.249"
port = 8000
buf = 1024
addr = (host, port)
Buffer_size = 1023
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

df = pd.read_csv("database.csv")
while True:
    flag = 0
    user_ID, u_addr = UDPSock.recvfrom(Buffer_size)
    user_ID=user_ID.decode()
    for index, row in df.iterrows():
        if (row['ID'] == user_ID):
            print("User ID:", user_ID)
            print("Waiting for PIN")
            pinrequest = '1'
            flag=1
            UDPSock.sendto(pinrequest.encode(), u_addr)
            recvpin = UDPSock.recvfrom(Buffer_size)[0]
            recvpin=recvpin.decode()
            if (int(row["Pin"]) == int(recvpin)):
                print("Authentication Successful! ")
                option = '2'
                UDPSock.sendto(option.encode(), u_addr)
                t_amt = UDPSock.recvfrom(Buffer_size)[0]
                tamt = int(t_amt)
                if (tamt > int(row["Closing_Balance"])):
                    option = '4'
                    print("Insuficient funds")
                    UDPSock.sendto(option.encode(), u_addr)
                else:
                    cb=str(int(row["Closing_Balance"])- tamt)
                    df.loc[index,'Closing_Balance']=cb
                    df.to_csv("database.csv",index=False)
                    option = '5'
                    UDPSock.sendto(option.encode(), u_addr)
                    print("Successful Transaction!")
            else:
                print("Incorrect Pin")
                option = '3'
                UDPSock.sendto(option.encode(), u_addr)
    if(flag==0):
        print("User ID doesnt exist.")
        option='6'
        UDPSock.sendto(option.encode(), u_addr)
UDPSock.close()