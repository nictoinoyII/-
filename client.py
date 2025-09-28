import socket
import threading

HOST = "localhost"
PORT = 23456


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"{message}")
        except:
            break


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print("Введите сообщения для отправки. Для выхода введите 'exit'.\nP.S. это бета версия!")
    while True:
        threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
        msg = input("")
        if msg.lower() == 'exit':
            break
        sock.sendall(msg.encode('utf-8'))

    sock.close()


if __name__ == "__main__":
    main()