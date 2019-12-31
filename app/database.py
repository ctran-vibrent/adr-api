import mysql.connector as mysql
from sshtunnel import SSHTunnelForwarder

import os
tunnel_host = os.environ['TUNNEL_HOST']
tunnel_port = int(os.environ['TUNNEL_PORT'])
tunnel_user = os.environ['TUNNEL_USER']
tunnel_pass = os.environ['TUNNEL_PASS']
#
db = os.environ['DATABASE']
db_user = os.environ['USER']
db_password = os.environ['PASSWORD']
db_host = os.environ['HOST']
db_port = int(os.environ['PORT'])

def tunnel_connect(command):
    def connect_tunnel(*args, **kwargs):
        server = SSHTunnelForwarder(
            (tunnel_host, tunnel_port),
            ssh_username=tunnel_user,
            ssh_password=tunnel_pass,
            remote_bind_address=(db_host, db_port)
        )
        server.start()
        kwargs['bind_port'] = server.local_bind_port
        x = command(*args, **kwargs)
        server.stop()
        return x
    return connect_tunnel

@tunnel_connect
def mySQL_connect(*args, **kwargs):
    cnx = mysql.connect(
        user=db_user,
        password=db_password,
        host='127.0.0.1', port=kwargs['bind_port'],
        database='adr')
    query = args[0]
    cur = cnx.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return rows
