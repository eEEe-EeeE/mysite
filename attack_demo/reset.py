import mysql.connector
import os, json

DIR = os.path.dirname(__file__)

def reset_auto_increment(table_name):
    f = open(DIR + '\\connector_init.json', encoding='utf-8')
    args = json.loads(f.read())
    cnx = mysql.connector.connect(**args)
    cursor = cnx.cursor()

    print(f'reset {table_name} auto_increment=1.')
    description = f'alter table `{table_name}` auto_increment=1'
    cursor.execute(description)
    
    cursor.close()
    cnx.close()