import socket
import threading

HOST = '0.0.0.0'
PORT = 23456

clients = []

def handle_client(client_socket, addr):
    print(f"Подключение от {addr}")
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"{addr} говорит: {message}")
            clientm = f"{addr} говорит: {message}"
            # Рассылаем сообщение всем клиентам, кроме отправителя
            broadcast(clientm, client_socket)
    except ConnectionResetError:
        print(f"Соединение с {addr} потеряно")
    finally:
        clients.remove(client_socket)
        client_socket.close()
        print(f"Отключено {addr}")

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message.encode('utf-8'))
            except:
                pass

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()



    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        client_sock, addr = server_socket.accept()
        clients.append(client_sock)
        threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True).start()

if __name__ == "__main__":
    main()