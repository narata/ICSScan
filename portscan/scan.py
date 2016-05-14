"""

"""
import socket
import struct
from port import *
from threading import *
import sys
sys.path.append("..")
from sql_db.connect import connect_db

con = connect_db()
cur = con.cursor()

def TCP_Scan(host, port, timeout, scan_result):
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host,port))
        sock.close()
        if result == 0:
            scan_result.append(port)
        else:
            return False
    except:
        return False

def scan(host, timeout, choose):
    scan_result = []
    if choose == "common":
        port_list = common_port_list
        threads = 1000
    else:
        port_list = ics_port_list
        threads = 12
    for port in port_list:
        while(True):
            if activeCount() <= threads:
                Thread(target=TCP_Scan, args=(host, port, timeout, scan_result)).start()
                break
            else:
                continue
    while(True):
        if activeCount() < 2:
            return scan_result

def portscan(host, timeout, choose):
    result = scan(host, timeout, choose)
    port_serv = {}
    if (result != []):
        for port in result:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknow service"
            port_serv[port] = service_list[port] if port in ics_port_list else service
    # print port_serv

    if (cur.execute('select * from PortScans where host = %s', [host]) != 0):
        if (choose == "common"):
            cur.execute('update PortScans set common_port = "%s" where host = %s', [port_serv, host])
        else:
            cur.execute('update PortScans set ics_port = "%s" where host = %s', [port_serv, host])
    else:
        if (choose == "common"):
            cur.execute('insert into PortScans (host,common_port) values(%s,"%s")', (host, port_serv))
        else:
            cur.execute('insert into PortScans (host,ics_port) values(%s,"%s")', (host, port_serv))
    con.commit()
    return 1

def main():
    timeout = int(sys.argv[3])
    choose = sys.argv[4]
    threads = int(sys.argv[2])
    if ',' in sys.argv[1]:
        host_list = sys.argv[1].split(',')
        for host in host_list:
            if portscan(host, timeout, choose) != 1:
                return 0

    elif '-' in sys.argv[1]:
        host_list = sys.argv[1].split('-')
        start_ip = socket.ntohl(struct.unpack('I', socket.inet_aton(str(host_list[0])))[0])
        end_ip = socket.ntohl(struct.unpack('I', socket.inet_aton(str(host_list[1])))[0])
        for host in range(start_ip, end_ip+1):
            host = socket.inet_ntoa(struct.pack('I', socket.htonl(host)))
            if portscan(host, timeout, choose) != 1:
                return 0
    else:
        if portscan(sys.argv[1], timeout, choose) != 1:
            return 0
    return 1

if __name__ == '__main__':
    """
    host = "109.3.164.230"
    threads = 10
    timeout = 5
    choose = "ics"
    print scan(host,threads,timeout,choose)
    """
    print main()
