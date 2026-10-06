import os
import json
from dotenv import load_dotenv
import psycopg2
from countryinfo import CountryInfo

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


# connection = psycopg2.connect(
#     host=DB_HOST,
#     port=DB_PORT,
#     user=DB_USER,
#     password=DB_PASSWORD,
#     database=DB_NAME
# )

DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


connection = psycopg2.connect(DB_URL)

cursor = connection.cursor()

cursor.execute('''
--drop table if exists countries;
create table if not exists countries(
    id serial primary key,
    name varchar(50) unique,
    ISO json,
    capital varchar(60),
    area integer,
    population integer,
    languages text []
    
);
''')
connection.commit()

while True:
    country = input('country: ').lower()

    if country == 'stop':
        break

    data = CountryInfo(country).info()

    name = data.get('name')
    iso = data.get('ISO')
    capital = data.get('capital')
    area = data.get('area')
    population = data.get('population')
    languages = data.get('languages')

    cursor.execute('''
    insert into countries(name, ISO, capital, area, population, languages)
    values (%(name)s, %(iso)s, %(capital)s, %(area)s, %(population)s, %(languages)s) on conflict(name) do update set
                                                                ISO = %(iso)s,
                                                                capital = %(capital)s,
                                                                area = %(area)s,
                                                                population = %(population)s,
                                                                languages = %(languages)s;
    
    ''', {
        'name': name,
        'iso': json.dumps(iso),
        'capital': capital,
        'area': area,
        'population': population,
        'languages': languages
    })
    connection.commit()
    print(f'{country} saved')



connection.close()



