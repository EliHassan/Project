import socket
import time
import argparse
import threadimport socket
import time
import argparse
import threading

DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 8088
DEFAULT_format = "MB"
CHUNK_SIZE = 1000

def valid_port(port):
    """
    Check if the port number is valid.
    """
    try:
        port = int(port)
        if not 1024 < port < 65536:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid port number: {port}")
    return port


def receive_data(conn, packet_size):
    received_bytes = 0
    start_time = time.time()
    while True:
        data = conn.recv(packet_size)
        if not data:
            break
        received_bytes += len(data)
    end_time = time.time()
    duration = end_time - start_time
    return received_bytes, duration


def handle_client(conn, addr, packet_size, args):
    print(f'A simpleperf client with {addr[0]}:{addr[1]} is connected with {args.bind}:{args.port}')
    received_bytes, duration = receive_data(conn, packet_size)

     # Calculate bandwidth and format output
    Total_transfer= received_bytes
    if args.format == 'Bytes':
        Total_transfer = received_bytes
        unit = 'Bytes'
    elif args.format == 'KB':
        Total_transfer = received_bytes / 1000
        unit = 'KB'
    elif args.format == 'MB':
       Total_transfer = received_bytes / 1000000
       unit = 'MB'
    else:
        Total_transfer = received_bytes / 1000000000
        unit = 'GB'
    
    data_bits = received_bytes * 8
    bandwidth_bps = data_bits / duration
    bandwidth_mbps = bandwidth_bps /1000000


    print(f'ID                   Interval      Receieved      Rate')
    print(f'{addr[0]}:{addr[1]}      0.0-{int(duration)}        {Total_transfer:.2f} {unit}           {bandwidth_mbps:.2f}Mbps ')

def main():

    parser = argparse.ArgumentParser("simpleperf server")
    parser.add_argument("-s", "--server", action="store_true", help="Enable server mode")
    parser.add_argument("-b", "--bind", default=DEFAULT_IP, help="IP address of server's interface (default: {})".format(DEFAULT_IP))
    parser.add_argument("-p", "--port", type=int, default=DEFAULT_PORT, help="Number on which the server should listen (default: {})".format(DEFAULT_PORT))
    parser.add_argument("-f", "--format",type=str , choices=["B", "KB", "MB","GB"], default="MB", help="Output data format (default: {})")
    args = parser.parse_args()

    if not args.server:
        print("Please you must run either in client or server mode  by using the -s flag or -c flag.")
        return

    packet_size = 1000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((args.bind, args.port))
    sock.listen()
    
    print(f'A simpleperf server is listening on port {args.port}')
    

    while True:
        conn, addr = sock.accept()
        threading.Thread(target=handle_client, args=(conn, addr, packet_size, args)).start(_)


if __name__ == '__main__':
    
    main()
ing

DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 8088
DEFAULT_format = "MB"
CHUNK_SIZE = 1000

def valid_port(port):
    """
    Check if the port number is valid.
    """
    try:
        port = int(port)
        if not 1024 < port < 65536:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid port number: {port}")
    return port


def receive_data(conn, packet_size):
    received_bytes = 0
    start_time = time.time()
    while True:
        data = conn.recv(packet_size)
        if not data:
            break
        received_bytes += len(data)
    end_time = time.time()
    duration = end_time - start_time
    return received_bytes, duration


def handle_client(conn, addr, packet_size, args):
    print(f'A simpleperf client with {addr[0]}:{addr[1]} is connected with {args.bind}:{args.port}')
    received_bytes, duration = receive_data(conn, packet_size)

     # Calculate bandwidth and format output
    Total_transfer= received_bytes
    if args.format == 'Bytes':
        Total_transfer = received_bytes
        unit = 'Bytes'
    elif args.format == 'KB':
        Total_transfer = received_bytes / 1000
        unit = 'KB'
    elif args.format == 'MB':
       Total_transfer = received_bytes / 1000000
       unit = 'MB'
    else:
        Total_transfer = received_bytes / 1000000000
        unit = 'GB'
    
    data_bits = received_bytes * 8
    bandwidth_bps = data_bits / duration
    bandwidth_mbps = bandwidth_bps /1000000


    print(f'ID                   Interval      Receieved      Rate')
    print(f'{addr[0]}:{addr[1]}      0.0-{int(duration)}        {Total_transfer:.2f} {unit}           {bandwidth_mbps:.2f}Mbps ')

def main():

    parser = argparse.ArgumentParser("simpleperf server")
    parser.add_argument("-s", "--server", action="store_true", help="Enable server mode")
    parser.add_argument("-b", "--bind", default=DEFAULT_IP, help="IP address of server's interface (default: {})".format(DEFAULT_IP))
    parser.add_argument("-p", "--port", type=int, default=DEFAULT_PORT, help="Number on which the server should listen (default: {})".format(DEFAULT_PORT))
    parser.add_argument("-f", "--format",type=str , choices=["B", "KB", "MB","GB"], default="MB", help="Output data format (default: {})")
    args = parser.parse_args()

    if not args.server:
        print("Please you must run either in client or server mode  by using the -s flag or -c flag.")
        return

    packet_size = 1000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((args.bind, args.port))
    sock.listen()
    
    print(f'A simpleperf server is listening on port {args.port}')
    

    while True:
        conn, addr = sock.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr, packet_size, args))
        t.start()


if __name__ == '__main__':
    
    main()
