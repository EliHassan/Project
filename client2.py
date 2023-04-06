import socket
import time
import argparse


def valid_port(port):
    """
    Check if the port number is valid.
    """
    try:
        port = int(port)
        if not 0 < port < 65536:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid port number: {port}")
    return port

parser = argparse.ArgumentParser(description='Simpleperf client mode')
parser.add_argument('-c','--client',         action="store_true",                    help='Simpleperf client mode')
parser.add_argument('-I','--server_ip',      type=str ,      default='127.0.0.1',    help='IP address of the simpleperf server')
parser.add_argument('-p','--server_port',    type=int,       default=8088,           help='Server port to connect to')
parser.add_argument('-t','--time',           type=int,       default=5,              help='Duration of data generation and sending')
parser.add_argument("-f", "--format",        type=str,       default="MB",           choices=['Bytes', 'KB', 'MB', 'GB'],       help="allow you to choose the format of the summary of the result")
parser.add_argument('-i','--interval',         type=int,        default=1,           help='Interval for statistics reporting')

args=parser.parse_args() 
''''
parser.add_argument('-n','num',         help='Total number of bytes to send')
parser.add_argument('-P','parallel',    type=int, help='Number of parallel connections')
'''
def main():
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((args.server_ip,args.server_port))
        print(f"Client connected to {args.server_ip}:{args.server_port}")
        start_time = time.time()
        global total_bytes 
        total_bytes=0

        while (time.time() - start_time) <args.time:
            data = bytearray(1000)
            sent_bytes = client.send(data)
            total_bytes += sent_bytes
        
        end_time=time.time()
        Duration=end_time-start_time
        bandwidth = total_bytes / Duration / 1000000 * 8

        if args.format == 'Bytes':
            total_bytes = total_bytes
            unit = 'Bytes'
        elif args.format == 'KB':
            total_bytes = total_bytes / 1000
            unit = 'KB'
        elif args.format == 'MB':
            total_bytes =total_bytes / 1000000
            unit = 'MB'
        else:  # args.format == 'GB'
            total_bytes =total_bytes / 1000000000
            unit = 'GB'
        print(f'ID               Interval        Transfer  Bandwidth')
        if(args.interval==1):
            print(f'{args.server_ip}:{args.server_port}   0.0 - {args.time:.1f}       {total_bytes:.2f}{unit} {bandwidth:.2f} Mbps')
        elif(args.interval!=1):
            for i in range(1,args.time,args.interval):
                print(f'{args.server_ip}:{args.server_port}   {float(i):.1f} - {(i+int(args.interval-1)):.1f}       {(total_bytes/i+1):.2f}{unit} {bandwidth:.2f} Mbps')
    except ConnectionRefusedError:
        print("Error: failed to connect to server")      
        
if __name__ == '__main__':
        if not args.client:
            print('Error: you must run in server mode or client mode.')
            parser.print_usage()
            exit()
        main()


     