import psycopg2
from psycopg2 import OperationalError

from config import localhost, user, password, db_name


connection = psycopg2.connect(
    "host='" + localhost + "' user='" + user + "' password='" + password + "' dbname='" + db_name + "'")

connection.autocommit = True

def create_table_seen():
    cur = connection.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS seen (
            id serial,
            vk_id varchar(50)  NOT null,
            seen_vk_id varchar(50) NOT null);"""
                )
    print('The table seen successfully created')


def insert_seen(vk_id, vk_seen_id):
    cur = connection.cursor()
    cur.execute(f"""INSERT INTO seen (vk_id, seen_vk_id)
            VALUES ('{vk_id}', '{vk_seen_id}');"""
                )


def check_if_seen(vk_id, vk_candidate):
    cur = connection.cursor()
    cur.execute(
        f"""SELECT seen_vk_id
            FROM seen WHERE vk_id = '{vk_id}' AND seen_vk_id = '{vk_candidate}'"""
    )
    return cur.fetchone()

def create_db():
    create_table_seen()
