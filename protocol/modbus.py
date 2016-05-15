#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import struct
from threading import *
import sys
sys.path.append("..")
from sql_db.connect import connect_db

con = connect_db()
cur = con.cursor()

_errors = {
        0:      'No reply',
        # Modbus errors
        1:      'ILLEGAL FUNCTION',
        2:      'ILLEGAL DATA ADDRESS',
        3:      'ILLEGAL DATA VALUE',
        4:      'SLAVE DEVICE FAILURE',
        5:      'ACKNOWLEDGE',
        6:      'SLAVE DEVICE BUSY',
        8:      'MEMORY PARITY ERROR',
        0x0A:   'GATEWAY PATH UNAVAILABLE',
        0x0B:   'GATEWAY TARGET DEVICE FAILED TO RESPOND'
    }

#十六进制字符串转化为普通字符串
def _0xtochar(_0x):
    charlen = len(_0x)
    rechar = ''
    if charlen % 2 != 0:
        print "input error!"
    else:
        for i in range(0, charlen/2):
            rechar = rechar + chr(int(_0x[i*2]+_0x[i*2+1], 16))
        return rechar

def modbus_scan(host, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, 502))
    except socket.error, e:
        return "connect " + str(e)

    re_data = []
    for i in (0, 255):
        if i > 15:
            id = hex(i)[2:]
        else:
            id = '0' + hex(i)[2:]
        buf = _0xtochar("00" + id + "00000005" + id + "2b0e0100")
        try:
            s.sendall(buf)
        except socket.error, e:
            return "sendsll " + str(e)
        try:
            data = s.recv(1024)
        except socket.error,e:
            return "recv " + str(e)
        if data:
            re_data.append(print_recv(data))
            if re_data[0] == "Not modbus":
                break
    s.close()
    result =  re_data[0][1]
    if (cur.execute('select * from ICSfind where ip = %s', [host]) != 0):
        cur.execute('update ICSfind set protocol = "Modbus" , info = %s where ip = %s', [result, host])
    else:
        cur.execute('insert into ICSfind (ip, protocol, info) values(%s, %s, %s)', [host, 'Modbus', result])
    con.commit()
    return 1

def print_recv(data):
    total_len = len(data)
    """
    for i in range(0,total_len):
        print hex(ord(data[i])),
    print
    """
    data_len = ord(data[4])*256 + ord(data[5])
    if ord(data[2])*256 + ord(data[3]) != 0:
        return "Not modbus"
    else:
        if data_len == total_len - 6:
            if data[7] == chr(0x2b):
                next_id = ord(data[12])
                data_num = ord(data[13])
                num = 15
                return_data = ''
                for j in range(0,data_num):
                    data1_len = ord(data[num])
                    num += 1
                    for i in range(num,num+data1_len):
                        return_data += data[i]
                    return_data += ' '
                    num = num + data1_len + 1
                return (ord(data[6]), "Device: " + return_data)
            else:
                if data[7] == chr(0xab):
                    return (ord(data[6]), "Device info error: " + _errors[ord(data[8])] if _errors.has_key(ord(data[8])) else "unknow error")
                else:
                    return (ord(data[6]), "Device info error: unknow error")
        else:
            return (ord(data[6]), "Device info error: unknow error")

def main():
    threads = int(sys.argv[2])
    timeout = int(sys.argv[3])

    if ',' in sys.argv[1]:
        host_list = sys.argv[1].split(',')
        for host in host_list:
            while(True):
                if activeCount() <= threads:
                    Thread(target=modbus_scan, args=(host, timeout)).start()
                    break
                else:
                    continue

    elif '-' in sys.argv[1]:
        host_list = sys.argv[1].split('-')
        start_ip = socket.ntohl(struct.unpack('I', socket.inet_aton(str(host_list[0])))[0])
        end_ip = socket.ntohl(struct.unpack('I', socket.inet_aton(str(host_list[1])))[0])
        for host in range(start_ip, end_ip + 1):
            host = socket.inet_ntoa(struct.pack('I', socket.htonl(host)))
            while (True):
                if activeCount() <= threads:
                    Thread(target=modbus_scan, args=(host, timeout)).start()
                    break
                else:
                    continue
    else:
        host = sys.argv[1]
        modbus_scan(host, timeout)
    while(True):
        if activeCount() < 2:
            return 1

if __name__ == '__main__':
    print main()