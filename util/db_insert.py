import os
import psycopg2
import sqlite3
import ast
import traceback
from util.config import secrets

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# conn = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
conn = psycopg2.connect(
    host="localhost",
    dbname=secrets['NAME'],
    user=secrets['USER'],
    password=secrets['PASSWORD']
)
# conn = psycopg2.connect(
#     dbname=secrets['NAME'],
#     user=secrets['USER'],
#     password=secrets['PASSWORD'],
#     host='<aws rdb endpoint>',
#     port='5432'
# )

try:
    cursor = conn.cursor()
    # with open(os.path.join(BASE_DIR, '/Users/asoa/Documents/PycharmProjects/sisterlocks/scraper/sisterlocks/sisterlocks/spiders/CONSULTANTS.txt')) as f:
    # with open(os.path.join(BASE_DIR, '/Users/asoa/Documents/PycharmProjects/sisterlocks/scraper/sisterlocks/sisterlocks/spiders/TRAINEES.txt')) as f:
    with open(os.path.join(BASE_DIR, '/Users/asoa/Documents/PycharmProjects/sisterlocks/scraper/sisterlocks/sisterlocks/spiders/APPROVED_TRAINEES.txt')) as f:
        for line in f.readlines():
            try:
            ## postgres
                d = ast.literal_eval(line.strip())
                # consultant insert
                # cursor.execute(f'''
                #    INSERT INTO public.consultants_consultant(name, state, city, description, phone, email, r_certified, ambassador, distributor, trainee, trichology, zipcode, approved, web_site, likes)
                #    VALUES ('{d['name']}','{d['state']}','{d['city']}','','{d['phone']}','{d['email']}','{d['r_certified']}','{d['ambassador']}','{0}','{0}','{0}','NA','{d['approved']}','{d['website']}', '{d['likes']}');
                # ''')
                # trainee insert
                cursor.execute(f'''
                    INSERT INTO public.consultants_consultant(name, state, city, description, phone, email, r_certified, ambassador, distributor, trainee, trichology, zipcode, approved, web_site, likes)
                    VALUES ('{d['name']}','{d['state']}','{d['city']}','','{d['phone']}','{d['email']}','{d['r_certified']}','{d['ambassador']}','{0}','{1}','{0}','NA','{d['approved']}','{d['website']}','{d['likes']}');
                ''')
            except Exception as e:
                print(e)

            ## sqlite
            # d = ast.literal_eval(line.strip())
            # use for consultants
            # cursor.execute(''' INSERT INTO consultants_consultant VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (None, d['name'],d['state'],d['city'],'',d['email'],0,0,0,0,0,'NA',d['approved'],'NA', 'NA'))


            # use for trainee
            # cursor.execute(''' INSERT INTO consultants_consultant VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (None, d['name'],d['state'],d['city'],'',d['email'],0,0,0,0,0,'NA',d['approved'],'NA',d['phone']))


except Exception as e:
    print(e)

try:
    conn.commit()
    print('wrote to db')
except Exception as e:
    print(e)






