import socket

# konfiguracja serwera
HOST = '127.0.0.1'
PORT = 5005

# slownik z klientami
clients = {}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Serwer UDP uruchomiony na {HOST}:{PORT}")

try:
    while True:
        # odbieranie danych z sieci
        data, client_address = server_socket.recvfrom(1024)
        
        # rozlaczanie
        if not data:
            if client_address in clients:
                nickname = clients[client_address]
                del clients[client_address]
                print(f"[-] Użytkownik {nickname} ({client_address}) rozłączył się.")
            continue
            
        message_type = data[0:1]
        payload = data[1:]
        
        # rejestracja uzytkownika
        if message_type == b"\x00":
            nickname = payload.decode('utf-8', errors='ignore').strip()
            clients[client_address] = nickname
            print(f"[+] Zarejestrowano użytkownika: {nickname} z adresu {client_address}")
            
        # przesylanie wiadomosci
        elif message_type == b"\x01":
            if client_address not in clients:
                print(f"[!] Ignorowanie wiadomości od nieznanego adresu: {client_address}")
                continue
                
            sender_nickname = clients[client_address]
            message_text = payload.decode('utf-8', errors='ignore')
            
            # formatowanie wiadomosci
            broadcast_message = f"{sender_nickname}: {message_text}".encode('utf-8')
            
            print(f"[Wiadomość] {sender_nickname}: {message_text}")
            
            # rozsylanie do innych klientow
            for target_address in clients:
                if target_address != client_address:
                    server_socket.sendto(broadcast_message, target_address)

except KeyboardInterrupt:
    print("\nZamykanie serwera.")
finally:
    server_socket.close()