import os
import sys

sys.path.append("/Applications/XAMPP/xamppfiles/htdocs/ICSScan")
from sql_db.connect import connect_db

con = connect_db()
cur = con.cursor()

def main():
    name = ''
    author = ''
    desc = ''
    source_code = ''
    dir = os.listdir("../plugins")
    for file in dir:
        file = "../plugins/" + file
        #print file
        if os.path.isfile(file):
            fp = open(file,'r')
            while(True):
                code = fp.readline()
                if code:
                    code = code.strip('\n').split('=')
                    #print code
                    if code[0].strip(' \n\t') == 'name':
                        name = code[1].strip("' ")
                    elif code[0].strip(' \t\n') == 'author':
                        author = code[1].strip("' []")
                    elif code[0].strip(' \t\n') == 'desc':
                        desc = code[1].strip("' ")
                        while(True):
                            buf = fp.readline()
                            if buf.strip('\n\t ') == "'''":
                                break
                            else:
                                desc = desc + buf.strip(' ')
                else:
                    break
            fp.seek(0, 0)
            source_code = fp.read()
            if (cur.execute('select * from Plugin where Name = %s', [name]) != 0):
                cur.execute('update Plugin set Author = %s, Description = %s, Code = %s where Name = %s', [author, desc, source_code, name])
            else:
                cur.execute('insert into Plugin (Name, Author, Description, Code) values(%s, %s, %s, %s)', [name, author, desc, source_code])
            con.commit()
            #print author,desc,name
    return 1

if __name__ == '__main__':
    print main()