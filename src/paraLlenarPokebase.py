import sqlite3
import requests
import random
import json

from utils import *


conn = sqlite3.connect('pokedex.db')
cursor = conn.cursor()

def get_pokemon_data(pokemon_id):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
cursor.execute(f'SELECT * FROM Pokemons WHERE id = {25}')
pok = cursor.fetchall()[0]

id,name,height,weight,base_experience,growth_rate, generation, hp, attack, defense, specialAttack,specialDefense,speed,lvl = pok[0],pok[1],pok[2],pok[3],pok[4],pok[5],pok[6],pok[7],pok[8],pok[9],pok[10],pok[11],pok[12],random.randint(0,30)

pokemon = Pokemon(id, name, height, weight, base_experience, growth_rate, generation, hp, attack, defense,
                  specialAttack, specialDefense, speed, lvl)



