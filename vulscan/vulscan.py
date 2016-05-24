#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re

sys.path.append("/Applications/XAMPP/xamppfiles/htdocs/ICSScan")
from sql_db.connect import connect_db

os.chdir(sys.path[0])

con = connect_db()
cur = con.cursor()

def vulscan():

    parameter = sys.argv[1]
    mode = sys.argv[2]
    choose_site = sys.argv[3]
    choose_poc = sys.argv[4]
    threads = sys.argv[5]
    timeout = sys.argv[6]
    if choose_site == 'file':
        if os.path.isfile(parameter):
            if choose_poc == 'file':
                command = "python Pocsuite/pocsuite.py -r Pocsuite/pocsuite/plugins/ -f " + parameter + " " + mode + " --report report.html --threads " + threads + " --timeout " + timeout
                os.popen(command)
                return 0

            else:
                if os.path.isfile("Pocsuite/pocsuite/plugins/"+choose_poc):
                    command = "python Pocsuite/pocsuite.py -r Pocsuite/pocsuite/plugins/" + choose_poc + " -f " + parameter + " " + mode + " --report report.html --threads " + threads + " --timeout " + timeout
                    os.popen(command)
                    return 0
                else:
                    return 1
        else:
            return 3
    else:
        fp = open('site','w')
        if ',' in parameter:
            host_list = parameter.split(',')
            for host in host_list:
                fp.write(host + '\n')
        else:
            host_list = parameter
            fp.write(host_list)
        fp.close()
        if choose_poc == 'file':
            command = "python Pocsuite/pocsuite.py -r Pocsuite/pocsuite/plugins/ -f site " + mode + " --report report.html --threads " + threads+ " --timeout " + timeout
            os.popen(command)
            return 0
        else:
            if os.path.isfile("Pocsuite/pocsuite/plugins/" + choose_poc):
                command = "python Pocsuite/pocsuite.py -r Pocsuite/pocsuite/plugins/" + choose_poc + " -f site " + mode + " --report report.html --threads " + threads+ " --timeout " + timeout
                os.popen(command)
                return 0
            else:
                return 1

def sql_in():

    fp = open("report.html",'r')
    if fp:
        buf = fp.read()
        result = re.findall(r"<td>(.+?)</td>", buf)
        for i in range(0, len(result), 6):
            sql = result[i:i + 6]
            cur.execute('insert into Scan (Url, poc_name, poc_id, component, version, status) values(%s, %s, %s, %s, %s, %s)', (sql[0], sql[1], sql[2], sql[3], sql[4], sql[5]))
            con.commit()
        #数据插入成功
        fp.close()
        return 0
    else:
        #无数据/插入数据库失败
        fp.close()
        return 2


def main():
    vul = vulscan()
    if vul == 0:
        return sql_in()
    else:
        return vul

if __name__ == '__main__':
    print main()