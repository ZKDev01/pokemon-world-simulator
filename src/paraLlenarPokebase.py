import sqlite3
import requests
import random
import json

from utils import *
from Pokemon import *


conn = sqlite3.connect('pokedex.db')
cursor = conn.cursor()

#cursor.execute(f'DROP TABLE Effects')

#cursor.execute('''CREATE TABLE IF NOT EXISTS Effects (
#                    id INTEGER PRIMARY KEY AUTOINCREMENT,
#                    effect TEXT NOT NULL
#               )''')

#conn.commit()

cursor.execute('SELECT effect FROM Moves')
effects_at_db = cursor.fetchall()

effects = []

for effect_db in effects_at_db:
    effect_ = effect_db[0]
    if effect_ not in effects:
        effects.append(effect_)
        cursor.execute('''INSERT INTO Effects(effect) VALUES(?)''', (effect_,))

conn.commit()

def get_pokemon_data(pokemon_id):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
cursor.execute(f'SELECT * FROM Pokemons WHERE id = {25}')
pok = cursor.fetchall()[0]

cursor.execute(f'SELECT type_id FROM Pokemon_Types WHERE pokemon_id = {25}')
types_id = cursor.fetchall()

pok_types = []
for i in range(len(types_id)):
    cursor.execute(f'SELECT name FROM Types WHERE id = {types_id[i][0]}')
    type = cursor.fetchall()[0][0]
    pok_types.append(type)

id,name,height,weight,base_experience,growth_rate, generation, hp, attack, defense, specialAttack,specialDefense,speed,lvl = pok[0],pok[1],pok[2],pok[3],pok[4],pok[5],pok[6],pok[7],pok[8],pok[9],pok[10],pok[11],pok[12],random.randint(1,30)

pokemon = Pokemon(id, name, pok_types, height, weight, base_experience, growth_rate, generation, hp, attack, defense,
                  specialAttack, specialDefense, speed, lvl)



