from chalice import Chalice
import psycopg2
import os
from datetime import datetime
import json
import requests
import socket
import re


app = Chalice(app_name='create-db-user')
app.debug = True

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = 'host'
DB_PORT = 5432


def create_user(user_name, passwd):
    try:
        sql = f"CREATE USER {user_name} WITH PASSWORD '{passwd}';"
        app.log.debug(sql)
        con = psycopg2.connect(database='postgres', user=DB_USER, password=DB_PASSWORD,
                               host=socket.gethostbyname(DB_HOST), port=DB_PORT)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()
    except psycopg2.DatabaseError as err:
        con.close()
        app.log.debug(f"Failed to create user, error {err}")


def execute_query(sql, host, database='postgres'):
    try:
        con = psycopg2.connect(
            database=database,
            user=DB_USER,
            password=DB_PASSWORD,
            host=host,
            port=5432)
        cur = con.cursor()
        cur.execute(sql)

        con.commit()
        cur.close()
        con.close()
    except psycopg2.DatabaseError as err:
        print("Error {}".format(err))



@app.on_sqs_message(queue='create-db-account', batch_size=1)
def handle_sqs_message(event):
    for record in event:
        """ Body: user:tenant:password """
        app.log.debug(f"Received message with contents: {record.body}")
        user, tenant, passwd = [re.sub('"', '', x) for x in record.body.split(':')]

        create_user(user, passwd)

