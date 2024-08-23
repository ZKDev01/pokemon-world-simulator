import sqlite3
import requests
import random
from utils import *

def get_pokemon_data(pokemon_id):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
first_pokemon = get_pokemon_data(60)
specie_url = first_pokemon['species']['url']
specie = requests.get(specie_url)
if specie.status_code == 200:
    specie = specie.json()
else:
    pass

id = first_pokemon['id']
name = first_pokemon['name']
base_experience = first_pokemon['base_experience']
height = first_pokemon['height']
weight = first_pokemon['weight']
abilities = first_pokemon['abilities']
forms = first_pokemon['forms']
held_items = first_pokemon['held_items']
location_areas = first_pokemon['location_area_encounters']
moves = first_pokemon['moves']
past_types = first_pokemon['past_types']
species = first_pokemon['species']
stats = first_pokemon['stats']
types = first_pokemon['types']
lvl = 1

pokemon = Pokemon()

print(first_pokemon)

conn = sqlite3.connect('pokemon.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS pokemons(
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        
    )''')