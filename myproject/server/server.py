import threading
import re
import requests
import logging
import socket
import json
import signal
from collections import defaultdict

B_SERVER_ADDRESS = '127.0.0.1'
B_SERVER_PORT = 8002

logging.basicConfig(filename='Matched_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

patterns = []

django_server_url = 'http://127.0.0.1:8000'

def load_patterns():
    global patterns
    with open('rules.py', 'r', encoding='utf-8') as file:
        for line in file:
            pattern = line.strip()
            if pattern:  # 빈 라인 무시
                patterns.append(re.compile(pattern))
    
    if not patterns:
        print("No patterns loaded from rules.py.")
    else:
        print(f"Loaded {len(patterns)} patterns from rules.py.")

def handle_client(client_socket, client_address):
    try:
        request = client_socket.recv(4096)
        if not request:
            raise ValueError("Empty request received")

        data = json.loads(request.decode())
        if 'packet_data' not in data:
            raise ValueError("Invalid packets data format")

        matched_packets, unmatched_packets = process_packets([data])

        if matched_packets:
            print(matched_packets)
            send_to_django(matched_packets, '/api/matched_packets')
        if unmatched_packets:
            send_to_django(unmatched_packets, '/api/unmatched_packets')

        client_socket.send("Data processed and sent to Django server.".encode())
        
    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()

#패킷 문자열검사부분
def process_packets(packets):
    matched_packets = []
    unmatched_packets = []

    if not patterns:
        print("No patterns available for matching.")
        return matched_packets, unmatched_packets

    for packet in packets:
        if not isinstance(packet, dict) or 'packet_data' not in packet:
            print("Invalid packet format:", packet)
            continue

        matched = False
        matched_pattern = None 
        
        for pattern in patterns:
            if pattern.search(packet['packet_data']):
                matched = True
                matched_pattern = pattern.pattern
                break
        
        if matched:
            matched_packets.append(packet)
            logging.info(f"Matched packet data: {packet['packet_data']}")
            logging.info(f"Matched with pattern: {matched_pattern}")
            send_notification_to_django("Suspicious packet detected", '/api/notify')
        else:
            unmatched_packets.append(packet)

    return matched_packets, unmatched_packets

def send_notification_to_django(message, endpoint):
    try:
        response = requests.post(f'{django_server_url}{endpoint}', json={'message': message})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send notification to Django server: {e}")

def send_to_django(packets, endpoint):
    try:
        response = requests.post(f'{django_server_url}{endpoint}', json={'packets': packets})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send packets to Django server: {e}")

def protocol_count(protocol):
    try:
        response = requests.post(f'{django_server_url}/packet', json={'protocol': protocol})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to increment protocol count: {e}")
        
def start_server():
    load_patterns()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((B_SERVER_ADDRESS, B_SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on {B_SERVER_ADDRESS}:{B_SERVER_PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()

def sigint_handler(signal, frame):
    print("Received SIGINT, shutting down server...")
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    start_server()