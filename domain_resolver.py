import sqlite3
from sqlite3 import Error
import threading
import socket
import whois

def check_domain(domain):
    try:
        data = socket.gethostbyname(domain)
        return data
    except:
        return False

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_all_domains(conn):

    cur = conn.cursor()
    cur.execute("SELECT id, name FROM domain")

    rows = cur.fetchall()

    return rows

def update_chk(conn, ip):
    sql = ''' UPDATE domain
              SET chk = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, ip)
    conn.commit()

def main():
    database = r"/home/star/work/python/list.sqlite"

    # create a database connection
    conn = create_connection(database)
    with conn:
        rows = select_all_domains(conn)
        for row in rows:
            id = row[0]
            chk = check_domain(row[1])
            if chk:
                update_chk(conn, (chk, id))
                # print(row[1], ' ==> IP : ', chk) # Update for chk field as IP address
            else:
                domain = whois.query(row[1])
                if domain is None:
                    update_chk(conn, ('NA', id))
                    # print('NA')
                else:
                    update_chk(conn, (domain.registrar, id))
                    # print(domain.registrar)


if __name__ == '__main__':
    main()
