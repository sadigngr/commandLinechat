from socket import * 
import threading
import time

sock = socket(AF_INET,SOCK_STREAM)
sock.bind(("192.168.112.191",1331))
sock.listen(10)
print("Dinleniyor!")
conList = []
def Server(con,addr):
    kullaniciAdi = ""
    print(addr,"Katildi!")
    while True:
        data = con.recv(2048).decode("utf-8")
        if data:
            if "#~grs" in data:
                kullaniciAdi = data[5:]
                sendMsg(kullaniciAdi + " Sunucuya Katildi!")
            else:
                print(data)
                sendMsg(kullaniciAdi+" : "+data)

def sendMsg(msg):
    for i in conList:
        i.sendall(msg.encode("utf-8"))


while True:

    con,addr = sock.accept()
    conList.append(con)
    t = threading.Thread(target = Server, args = (con,addr, ))
    t.start()

    print("Dinleniyor!")
    



