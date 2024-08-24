import curses
import socket
import threading

messages = []
def getMsg():
    while True:
        data = sock.recv(1024).decode("utf-8")
        if data:
            messages.append(data)

def sendMsg(msg):
    sock.sendall(msg.encode("utf-8"))


def chatInterface(stdscr):
    giris = False
    # Renkleri başlat
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

    # Pencere boyutlarını al
    height, width = stdscr.getmaxyx()

    # Chat mesajları için bir pencere oluştur
    chat_win = curses.newwin(height - 3, width, 0, 0)
    chat_win.box()

    # Giriş kısmı için bir pencere oluştur
    input_win = curses.newwin(3, width, height - 3, 0)
    input_win.box()

    # Mesajları tutacak bir liste
    current_message = ""

    # Giriş penceresi güncelleme işlemi
    def update_input_window():
        if giris == False:
            input_win.clear()
            input_win.box()
            input_win.addstr(1, 1, f"Kullanici Adi : {current_message}", curses.color_pair(1))
            input_win.refresh()

        else:

            input_win.clear()
            input_win.box()
            input_win.addstr(1, 1, f"Msg: {current_message}", curses.color_pair(1))
            input_win.refresh()

    # Chat penceresi güncelleme işlemi
    def update_chat_window():
        chat_win.clear()
        chat_win.box()
        for i, message in enumerate(messages[-(height - 5):]):
            chat_win.addstr(i + 1, 1, message, curses.color_pair(1))
        chat_win.refresh()

    stdscr.nodelay(True)

    while True:
        update_chat_window()
        update_input_window()

        try:
            key = stdscr.getch()
        except curses.error:
            key = -1

        if key == ord('q'):  # 'q' ya basınca çıkış yap
            break

        if key == curses.KEY_ENTER or key == 10:  # Enter tuşuna basılırsa
            if current_message.strip():
                if giris == False:
                    kullaniciAdi = current_message
                    sendMsg("#~grs" + kullaniciAdi)
                    messages.append("Giris Basarili! Kullanici Adiniz : " + kullaniciAdi)

                    giris = True

                else:
                    sendMsg(current_message)
            current_message = ""
        elif key != -1:

            if key == 127 or key == curses.KEY_BACKSPACE:
                current_message = current_message[:-1]
            elif 32 <= key <= 126:
                current_message += chr(key)

        curses.napms(50)

if __name__ == "__main__":
    messages.append("Hosgeldiniz! Lutfen Bir Kullanici Adi Girin.")
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(("192.168.112.191",1331))
    t1 = threading.Thread(target = curses.wrapper,args=(chatInterface,))
    t1.start()
    t2 = threading.Thread(target = getMsg)
    t2.start()
