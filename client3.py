import socket 
import argparse
import time
import threading
def if_IP_is_Valid(IP):
    try:
        socket.inet_aton(IP)
        return True
    except socket.error:
        return False
def Starting_client(s_ip, s_port, time_duration, interval,format):
    try:
        start_time=time.time()
        client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((s_ip,s_port))
        sent_bytes=0
        while(time.time() -start_time)<time_duration:
            packet=bytearray(1024)
            sent_packet=client.send(packet)
            sent_bytes+=sent_packet
        Bits_Of_Data=sent_bytes*8
        bandwidath_bps=Bits_Of_Data/time_duration
        Bandwidth=bandwidath_bps/1000000
        print(f'Client-IP:Port         |      Session-Interval   |     Data-Transfered    |    Session-Bandwidth')
        print(f'{s_ip}:{s_port}        |       0.0 - {time_duration:.1f}          |     {changeIt(sent_bytes,format)}           |  {(Bandwidth):.2f} Mbps')   
    except ConnectionRefusedError:
        print("Check if server is running, Connection to server failed. Error 404.") 
def changeIt(sent_bytes,format):
    output=""
    if format == 'Bytes':
        sent_bytes = sent_bytes
        value_Unit = 'Bytes'
        output+=str(sent_bytes)+" "+value_Unit
    elif    format == 'GB':
        sent_bytes =sent_bytes / 1000000000
        value_Unit = 'GB'
        out=round(sent_bytes,2)
        output+=str(out)+value_Unit
    elif format == 'KB':
        sent_bytes = sent_bytes / 1024
        out=round(sent_bytes,2)
        value_Unit = 'KB'
        output+=str(out)+" "+value_Unit
    elif format == 'MB':
        sent_bytes =sent_bytes / 1000000
        value_Unit = 'MB'
        out=round(sent_bytes,2)
        output+=str(out)+value_Unit
   
    return output


def Client_Arguments_section(s_ip, s_port,time_duration,format,interval=None, num=None, parallel=None):
    try: 
        if interval:
            client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client.connect((s_ip,s_port))
            print("Sending Data in Intervals")
            print("==============================================================")
            print(f"|| imperf Client connected to Server at IP:{s_ip} : {s_port}  ||")
            print("==============================================================")     
            total_send=0
            start_time=time.time()
            last_print=start_time
            last_send=0
            current_time=time.time() 
            Up_Time=current_time-last_print              
            i=1
            print(f'Client/Process-ID         |      Session-Interval   |     Data-Transfered    |    Session-Bandwidth')
            while time.time()-start_time-1<=time_duration:
                packet=bytearray(1024)
                send_packet=client.send(packet)
                total_send+=send_packet
                current_time=time.time() 
                Up_Time=current_time-last_print        
                if current_time-last_print >=interval:
                    interval_send=total_send-last_send
                    print(f'{s_ip}:{s_port}            |            {i-1}- {i+interval-1}         |          {(interval_send,format)}      |     {(interval_send*8)/(Up_Time*1000000):.2f}Mbps')   
                    i+=interval
                    last_print=current_time
                    last_send=total_send
            Bits_Of_Data=total_send*8
            bandwidath_bps=Bits_Of_Data/time_duration
            Bandwidth=bandwidath_bps/1000000
            print("**************            |--------Statistics for current Sessions-----------|   **************")        
            print(f'{s_ip}:{s_port}            |         0.0 - {time_duration:.1f}       |          {changeIt(total_send,format)}      |     {(Bandwidth):.2f} Mbps')
        
        elif num:
            print("Sending {num},{Data_from_user} data to server")
            client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client.connect((s_ip,s_port))
            print("==============================================================") 
            print(f"Connected to Server @ {s_ip}: {s_port} Successfully")
            print("==============================================================") 
            Data_from_user=num.upper()
            Data_Size_Sent=int(Data_from_user[:-2])
            value_Unit=Data_from_user[-2:]   
            if Data_from_user[-2:] in ['KB','MB']:
                Data_Size_Sent=int(Data_from_user[:-2])
                value_Unit=Data_from_user[-2:]
                if value_Unit=='KB':
                    sent_bytes_expected_to_send = Data_Size_Sent*1024
                elif value_Unit=='MB':
                    sent_bytes_expected_to_send = Data_Size_Sent*1024*1024
            elif Data_from_user[-1:] =='B':
                Data_Size_Sent=int(Data_from_user[:-1])
                value_Unit='B'
                sent_bytes_expected_to_send=Data_Size_Sent
            else:
                raise ValueError("Please specify the data size you want to send")
            total_sendt=0
            start_time=time.time()
            while total_sendt<sent_bytes_expected_to_send:
                 packet=bytearray(1024)
                 sent_packet=client.send(packet)
                 total_sendt+=sent_packet
            end_time=time.time()
            duration=end_time-start_time
            Bits_Of_Data=total_sendt*8
            bandwidath_bps=Bits_Of_Data/duration
            Bandwidth=bandwidath_bps/1000000
            print(f'Client/Process-ID         |      Session-Interval   |     Data-Transfered    |    Session-Bandwidth')
            print(f'{s_ip}:{s_port}            |          0.0 - {duration:.1f}        |          {Data_Size_Sent}{value_Unit}      |     {Bandwidth:.2f} Mbps')
        elif parallel:
            threads = []
            for i in range(parallel):
                thread = threading.Thread(target=Starting_client, args=(s_ip, s_port, time_duration, interval,format))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()
        else:
            client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client.connect((s_ip,s_port))
            print("==============================================================") 
            print(f"Connection to server at {s_ip}: {s_port} Success")
            print("==============================================================") 
            start_time = time.time()
            sent_bytes=0          
            while(time.time() -start_time)<time_duration:
                packet=bytearray(1024)
                sent_packet=client.send(packet)
                sent_bytes+=sent_packet
            Bits_Of_Data=sent_bytes*8
            bandwidath_bps=Bits_Of_Data/Up_Time
            Bandwidth=bandwidath_bps/1000000
            print(f'Client/Process-ID         |      Session-Interval   |     Data-Transfered    |    Session-Bandwidth')
            print(f'{s_ip}:{s_port}            |          0.0 - {time_duration:.1f}        |          {changeIt(sent_bytes,format)}      |     {Bandwidth:.2f} Mbps')
    except ConnectionRefusedError:
        print("Error occured, Connection to server Failed!")  
def If_Limit_In_Range(value):
    Provided_Value = int(value)
    if Provided_Value < 1 or Provided_Value > 5:
        raise argparse.ArgumentTypeError(f"This {value} value is beyond the limit, please provide between 1-5")
    return Provided_Value

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simpleperf client mode')
    parser.add_argument('-c',   '--client',         action="store_true",                            help='Used to specify client mode')
    parser.add_argument('-I',   '--s_ip',           type=str,               default='127.0.0.1',    help='State IP of the Server to connect with')
    parser.add_argument('-p',   '--s_port',         type=int,               default=8088,           help='Mention the port to connect at')
    parser.add_argument('-t',   '--time_duration',  type=int,               default=5,              help='Duration of data sending')
    parser.add_argument("-f",   '--format',         type=str,               default="MB",           choices=[ 'GB','MB','Bytes','KB'],       help="This will help in displaying format of the data in statistics")
    parser.add_argument('-i',   '--interval',       type=int,                                       help='Interval for statistics Printing')
    parser.add_argument('-n',   '--num',            type=str,                                       help='Total number of bytes to send')
    parser.add_argument('-P',   '--parallel',       type=If_Limit_In_Range,                            help='Total No. of parallel connections')
    args = parser.parse_args()
    if not args.client:
            print('Error: you must run in server mode or client mode.')
            parser.print_usage()
            exit()
    Client_Arguments_section(args.s_ip, args.s_port, args.time_duration,args.format, args.interval, args.num, args.parallel )