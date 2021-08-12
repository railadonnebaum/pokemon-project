from connection.config import connection
import requests
from setup.insert_info import insert_pokemon, insert_type, insert_pokemon_type
from connection.config import pokemon_API_url


def find_by_type(type):
    try:
        with connection.cursor() as cursor:
            query = 'SELECT name FROM pokemon JOIN pokemon_type JOIN types' \
                    '    ON pokemon.id=pokemon_type.pokemon and pokemon_type.type=types.id' \
                    '        WHERE types.type =%s'
            cursor.execute(query, type)
            result = cursor.fetchall()
            for i in range(len(result)):
                result[i] = result[i]['name']
            return result
    except Exception:
        pass


def get_trainers_by_pokemon(pokemon):
    try:
        with connection.cursor() as cursor:
            query = "SELECT owner FROM ownedBy " \
                    "JOIN pokemon ON pokemon.id = ownedBy.pokemon " \
                    "WHERE pokemon.name = %s"
            cursor.execute(query, pokemon)
            result = cursor.fetchall()
            for i in range(len(result)):
                result[i] = result[i]['owner']
            return result
    except Exception:
        print("DB Error")


def get_pokemon_by_owner(trainer):
    try:
        with connection.cursor() as cursor:
            query = 'SELECT  pokemon.name' \
                    '    FROM pokemon WHERE (%s IN (' \
                    '         SELECT owner FROM ownedBy ' \
                    '                WHERE ownedBy.pokemon=pokemon.id))'
            cursor.execute(query, (trainer))
            result = cursor.fetchall()
            for i in range(len(result)):
                result[i] = result[i]['name']
            return result
    except Exception:
        print("DB Error")


def add_pokemon(id, name, height, weight, types):
    res1 = insert_pokemon(id, name, height, weight)
    res2 = True
    if res1:
        for type in types:
            res2 = insert_pokemon_type(id, type)
    if res1 and res2:
        return True
    else:
        return False


def delete_pokemon(id):
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM pokemon WHERE pokemon.id = %s;"
            cursor.execute(query, id)
            connection.commit()
            return True
    except Exception:
        print("DB Error")
        return False


def delete_pokemon_of_trainer(trainer_name):
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM ownedBy WHERE owner = %s;"
            cursor.execute(query, trainer_name)
            connection.commit()
            return True
    except Exception:
        print("DB Error")
        return False


def update_pokemon_type(name):
    try:
        pokemon_url = f'{pokemon_API_url}' + name + '/'
        pokemon = requests.get(url=pokemon_url, verify=True)
        if pokemon.status_code == 404:
            return 404
        pokemon = pokemon.json()
        pokemon_id = pokemon["id"]
        for element in pokemon["types"]:
            pokemon_type = element["type"]["name"]
            insert_type(pokemon_type)
            insert_pokemon_type(pokemon_id, pokemon_type)
        return 200
    except:
        return 500


def pokemon_evolve(pokemon_name, trainer_name):
    try:
        pokemon_url = f'{pokemon_API_url}' + pokemon_name + '/'
        pokemon = requests.get(url=pokemon_url, verify=True)
        if pokemon.status_code == 404:
            return ("not found", 404)
        pokemon = pokemon.json()
        old_id = pokemon['id']
        url = pokemon['species']['url']
        pokemon = requests.get(url=url, verify=True)
        if pokemon.status_code == 404:
            return ("not found", 404)
        pokemon = pokemon.json()
        url = pokemon['evolution_chain']['url']
        pokemon = requests.get(url=url, verify=True)
        if pokemon.status_code == 404:
            return ("not found", 404)
        pokemon = pokemon.json()
        chain = pokemon['chain']
        while (chain['species']['name'] != pokemon_name):
            chain = chain['evolves_to']
        if (chain['evolves_to'] == []):
            return ("can't evolve", 500)
        name = chain['evolves_to'][0]['species']['name']
        pokemon_url = f'{pokemon_API_url}' + name + '/'
        pokemon = requests.get(url=pokemon_url, verify=True)
        if pokemon.status_code == 404:
            return ("not found", 404)
        pokemon = pokemon.json()
        insert_pokemon_evolve(name, pokemon)
        return update_evolve_pokemon(old_id, pokemon, trainer_name)
    except:
        return ("pokemon evolve failed", 500)


def update_evolve_pokemon(old_id, pokemon, trainer_name):
    with connection.cursor() as cursor:
        query = "SELECT TRUE FROM ownedBy where owner= %s and pokemon= %s;"
        cursor.execute(query, (trainer_name, old_id))
        result = cursor.fetchall()
        if result == ():
            return ("trainer does not have this pokemon", 500)
        query = "UPDATE ownedBy SET pokemon = %s WHERE owner= %s and pokemon= %s;"
        cursor.execute(query, (pokemon['id'], trainer_name, old_id))
        connection.commit()
        return ("pokemon evolve successfully", 200)


def insert_pokemon_evolve(name, pokemon):
    with connection.cursor() as cursor:
        query = "SELECT TRUE FROM pokemon where pokemon.id = %s"
        cursor.execute(query, pokemon['id'])
        result = cursor.fetchall()
        if result == ():
            add_pokemon(pokemon['id'], name, pokemon['height'], pokemon['weight'], [])
            update_pokemon_type(name)
