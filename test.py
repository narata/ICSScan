import sys
import socket
import struct
import MySQLdb
from sql_db.connect import *
"""
con = connect_db()
print con
cur = con.cursor()
print cur.execute('select * from PortScans')
cur.execute("insert into PortScans () values('11111','fdsafdas','fdsafdsa')")
con.commit()
"""
IP = "1.1.1.1"
int_ip = socket.ntohl(struct.unpack('I', socket.inet_aton(str(IP)))[0])
print int_ip
new_ip = socket.inet_ntoa(struct.pack('I', socket.htonl(int_ip)))
print new_ip
for i in range(0,8):
    print i
