import json
from connection.config import connection


def insert_info():
    with open('pokemon_data.json', 'r') as pokemon_data:
        data = json.load(pokemon_data)
        for elem in data:
            insert_pokemon(elem['id'], elem['name'], elem['height'], elem['weight'])
            for owner in elem['ownedBy']:
                insert_owner(owner['name'], owner['town'])
                insert_ownedBy(elem['id'], owner['name'])


def insert_pokemon(id, name, height, weight):
    try:
        with connection.cursor() as cursor:
            query = "insert into pokemon values (%s, %s, %s, %s)"
            cursor.execute(query, (id, name, height, weight))
            connection.commit()
            return True
    except:

        return False


def insert_owner(name, town):
    try:
        with connection.cursor() as cursor:
            query = "insert into owner values (%s, %s)"
            cursor.execute(query, (name, town))
            connection.commit()
            return True
    except:
        return False


def insert_ownedBy(pokemon, owner):
    try:
        with connection.cursor() as cursor:
            query = "insert into ownedby values (%s, %s)"
            cursor.execute(query, (pokemon, owner))
            connection.commit()
            return True
    except:
        return False


def insert_type(type):
    try:
        with connection.cursor() as cursor:
            query = "insert into types values (%s,%s)"
            cursor.execute(query, (None, type))
            connection.commit()
            return True
    except:
        return False


def insert_pokemon_type(pokemon, type):
    type = get_type_id(type)
    try:
        with connection.cursor() as cursor:
            query = "insert into pokemon_type values (%s, %s)"
            cursor.execute(query, (pokemon, type))
            connection.commit()
            return True
    except:
        return False


def get_type_id(type):
    try:
        with connection.cursor() as cursor:
            query = "SELECT id from types WHERE type = %s;"
            cursor.execute(query, (type))
            result = cursor.fetchall()
            return result[0]['id']
    except Exception:
        pass
# insert_info()