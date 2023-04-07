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
# Create an argument parser object

parser = argparse.ArgumentParser(description='Simpleperf client mode')


# Add arguments to the parser
parser.add_argument('-c',                    action="store_true",                    help='Simpleperf client mode')
parser.add_argument('-I',                    type=str ,      default='127.0.0.1',    help='IP address of the simpleperf server')
parser.add_argument('-p',                    type=int,       default=8088,           help='Server port to connect to')
parser.add_argument('-t',                    type=int,       default=5,              help='Duration of data generation and sending')
parser.add_argument("-f",                    type=str,       default="MB",           choices=['Bytes', 'KB', 'MB', 'GB'],       help="allow you to choose the f of the summary of the result")
parser.add_argument("-n",                    type=int,       default=10,             help="number of packets to send")
parser.add_argument("-i",                    type=float,     default=1.0,            help="time i between packets in seconds")
parser.add_argument("-P",                    type=int,       default=1,              help="number of parallel connections")

# Parse the arguments from the command line
args = parser.parse_args()

# Use the arguments in your program
num = args.n
i = args.i
parallel = args.P

def main():
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((args.I,args.p))
        print(f"Client connected to {args.I}:{args.p}")
        start_time = time.time()
        global total_bytes 
        total_bytes=0

        while (time.time() - start_time) <args.t:
            data = bytearray(1000)
            sent_bytes = client.send(data)
            total_bytes += sent_bytes
        
        end_time=time.time()
        Duration=end_time-start_time
        bandwidth = total_bytes / Duration / 1000000 * 8

        if args.f == 'Bytes':
            total_bytes = total_bytes
            unit = 'Bytes'
        elif args.f == 'KB':
            total_bytes = total_bytes / 1000
            unit = 'KB'import socket
import time
import argparse
import multiprocessing


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
# Create an argument parser object

parser = argparse.ArgumentParser(description='Simpleperf client mode')


# Add arguments to the parser
parser.add_argument('-c',                    action="store_true",                    help='Simpleperf client mode')
parser.add_argument('-I',                    type=str ,      default='127.0.0.1',    help='IP address of the simpleperf server')
parser.add_argument('-p',                    type=int,       default=8088,           help='Server port to connect to')
parser.add_argument('-t',                    type=int,       default=5,              help='Duration of data generation and sending')
parser.add_argument("-f",                    type=str,       default="MB",           choices=['Bytes', 'KB', 'MB', 'GB'],       help="allow you to choose the f of the summary of the result")
parser.add_argument("-n",                    type=int,       default=10,             help="number of packets to send")
parser.add_argument("-i",                    type=float,     default=1.0,            help="time i between packets in seconds")
parser.add_argument("-P",                    type=int,       default=1,              help="number of parallel connections")

# Parse the arguments from the command line
args = parser.parse_args()

# Use the arguments in your program
num = args.n
i = args.i
parallel = args.P

def main(number):
    
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((args.I,args.p))
        print(f"Client connected to {args.I}:{args.p}")
        start_time = time.time()
        global total_bytes 
        total_bytes=0

        while (time.time() - start_time) <args.t:
            data = bytearray(1000)
            sent_bytes = client.send(data)
            total_bytes += sent_bytes
        
        end_time=time.time()
        Duration=end_time-start_time
        bandwidth = total_bytes / Duration / 1000000 * 8

        if args.f == 'Bytes':
            total_bytes = total_bytes
            unit = 'Bytes'
        elif args.f == 'KB':
            total_bytes = total_bytes / 1000
            unit = 'KB'
        elif args.f == 'MB':
            total_bytes =total_bytes / 1000000
            unit = 'MB'
        else:  # args.f == 'GB'
            total_bytes =total_bytes / 1000000000
            unit = 'GB'
        print(f'ID               Interval        Transfer  Bandwidth')
        if(args.i==1):
            print(f'{args.I}:{args.p}   0.0 - {args.t:.1f}       {total_bytes:.2f}{unit} {bandwidth:.2f} Mbps')
        elif(args.i!=1):
            for i in range(1,args.t,args.i):
                print(f'{args.I}:{args.p}   {float(i):.1f} - {(i+int(args.i-1)):.1f}       {(total_bytes/i+1):.2f}{unit} {bandwidth:.2f} Mbps')
    except ConnectionRefusedError:
        print("Error: failed to connect to server")      
        
if __name__ == '__main__':
  if not args.c:
    print('Error: you must run in server mode or c mode.')
    parser.print_usage()
    exit()
  pool = multiprocessing.Pool (args.P)
  pool.map (main, range (args.P))

     
        elif args.f == 'MB':
            total_bytes =total_bytes / 1000000
            unit = 'MB'
        else:  # args.f == 'GB'
            total_bytes =total_bytes / 1000000000
            unit = 'GB'
        print(f'ID               Interval        Transfer  Bandwidth')
        if(args.i==1):
            print(f'{args.I}:{args.p}   0.0 - {args.t:.1f}       {total_bytes:.2f}{unit} {bandwidth:.2f} Mbps')
        elif(args.i!=1):
            for i in range(1,args.t,args.i):
                print(f'{args.I}:{args.p}   {float(i):.1f} - {(i+int(args.i-1)):.1f}       {(total_bytes/i+1):.2f}{unit} {bandwidth:.2f} Mbps')
    except ConnectionRefusedError:
        print("Error: failed to connect to server")      
        
if __name__ == '__main__':
        if not args.c:
            print('Error: you must run in server mode or c mode.')
            parser.print_usage()
            exit()
        main()


     
