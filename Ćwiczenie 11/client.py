import socket
import sys
import select

# konfiguracja polaczenia
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5005
server_address = (SERVER_HOST, SERVER_PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setblocking(False)

# podanie nickname'u
nickname = input("Podaj swój nickname: ")

# wysylanie pakietu powitalnego ze znakiem \0
welcome_packet = b"\x00" + nickname.encode('utf-8')
client_socket.sendto(welcome_packet, server_address)
print("Połączono z serwerem. Napisz coś i naciśnij Enter. Wpisz 'exit' aby wyjść.\n")

try:
    while True:
        read_sockets, _, _ = select.select([0, client_socket], [], [])
        
        for notified_socket in read_sockets:
            # jesli dane od serwera
            if notified_socket == client_socket:
                data, _ = client_socket.recvfrom(1024)
                print(data.decode('utf-8'))
                
            # cos z klawiatury
            elif notified_socket == 0:
                line = sys.stdin.readline().strip()
                
                if line.lower() == 'exit':
                    # pusty diagram do rozlaczania
                    client_socket.sendto(b"", server_address)
                    raise KeyboardInterrupt
                
                if line:
                    message_packet = b"\x01" + line.encode('utf-8')
                    client_socket.sendto(message_packet, server_address)

except KeyboardInterrupt:
    print("\nRozłączanie i zamykanie klienta.")
finally:
    client_socket.close()