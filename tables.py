import psycopg2
from psycopg2 import OperationalError

from config import localhost, user, password, db_name

# def create_connection(localhost, user, password, db_name):
# connection = None
#    try:
#        connection = psycopg2.connect(
#        localhost=localhost,
#        user=user,
#        password=password,
#        db_name=db_name,
#        )
#    print("[INFO] Connection to PostgreSQL has success")
#    except OperationalError as e:
#    print(f"The error '{e}' occured")
#    return connection


connection = psycopg2.connect("host='localhost' user='user' password='password' dbname='db_name'")

connection.autocommit = True


def create_table_vk_candidates():
    with connection.cursor() as cursor:
        cursor.excute(
            """CREATE TABLE IF NOT EXISTS vk_candidates (
            id serial,
            vk_id varchar(50) NOT NULL PRIMARY key);"""
        )
    print('The table vk_candidates successfully created')

def insert_vk_candidates(first_name, last_name, vk_id, vk_link):
    with connection.cursor() as cursor:
        cursor.excute(
            f"""INSRERT INTO vk_candidates (vk_id)
            VALUES ('{vk_id}');"""
        )

def create_table_seen():
    with connection.cursor() as cursor:
        cursor.excute(
            """CREATE TABLE IF NOT EXISTS vk_candidates (
            id serial,
            vk_id varchar(50) NOT null PRIMARY key);"""
        )
    print ('The table seen successfully created')

def insert_seen(vk_id, offset):
    with connection.cursor() as cursor:
        cursor.excute(
            f"""INSRERT INTO seen (vk_id)
            VALUES ('{vk_id}')
            OFFSET '{offset}';"""
        )

def select(offset):
    with connection.cursor() as cursor:
        cursor.excute(
            f"""SELECT vc.vk_id, s.vk_id
            FROM vk_candidates AS vc
            RIGHR JOIN seen AS s
            ON vc.vk_id = s.vk_id
            WHERE s.vk_id IS NULL
            OFFSET '{offset}';"""
        )
    return cursor.fetchone()

def create_db():
    create_table_vk_candidates()
    create_table_seen()
