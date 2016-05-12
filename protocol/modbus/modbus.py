#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

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

def modbus_scan(host):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    try:
        s.connect((host, 502))
    except socket.error, e:
        return "connect " + str(e)

    re_data = []
    for i in (0, 255):
        print i , ' ',
        if i > 15:
            id = hex(i)[2:]
        else:
            id = '0' + hex(i)[2:]
        buf = _0xtochar("00" + id + "00000005" + id + "2b0e0100")
        #print "00" + id + "00000005" + id + "2b0e0100 ",
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
    return {"host": host, "port": 502, "info": re_data}

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
    f1 = open("ip.txt", 'r')
    f2 = open("scan.txt", 'a')
    while True:
        host = f1.readline()
        print host,host[-1]
        if host[-1] == '\n':
            host = host[:-1]
        if host:
            data = modbus_scan(host)
            f2.write(str(data)+'\n')
        else:
            break
        print host, ' ', data
    f1.close()
    f2.close()

if __name__ == '__main__':
    main()