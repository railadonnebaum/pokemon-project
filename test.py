import json
import requests
from connection.config import pokemon_API_url
from connection.config import project_url
from setup.insert_info import insert_type
from connection.config import connection


# before every time you run the test you must run the sql file (Drop+create for each table),
# and then run insert_info() in insert_info file.

# test1
def test_get_pokemons_by_type():
    insert_type('normal')
    try:
        with connection.cursor() as cursor:
            query1 = "SELECT  id  FROM  types WHERE type='normal';"
            cursor.execute(query1)
            result = cursor.fetchall()
        with connection.cursor() as cursor:
            query1 = "insert into pokemon_type values (133,%s);"
            cursor.execute(query1, result[0]['id'])
            connection.commit()
    except:
        pass
    url = f'{project_url}get-pokemon-by-type/normal'
    pokemon = requests.get(url=url, verify=False)
    pokemon = pokemon.json()
    assert 'eevee' in pokemon, "test failed"
    url = f'{project_url}update-pokemon-type/normal'
    requests.put(url=url)
    try:
        with connection.cursor() as cursor:
            query = "SELECT COUNT(*) from types WHERE type = 'normal';"
            cursor.execute(query)
            result = cursor.fetchall()
            assert result == 1, "test failed"
    except Exception:
        return False




# test2
def test_add_pokemon():
    pokemon_url = f'{pokemon_API_url}yanma/'
    pokemon = requests.get(url=pokemon_url, verify=True)
    pokemon = pokemon.json()
    data = json.dumps({
        "id": pokemon['id'],
        "name": "yanma",
        "height": pokemon['height'],
        "weight": pokemon['weight'],
        "types": []
    })
    url = f'{project_url}add-pokemon'
    headers = {
        'Content-Type': 'application/json'
    }
    requests.request("POST", url, headers=headers, data=data, verify=True)
    url = f'{project_url}update-pokemon-type/yanma'
    requests.put(url=url)
    url = f'{project_url}get-pokemon-by-type/bug'
    pokemon = requests.get(url=url)
    pokemon = pokemon.json()
    assert 'yanma' in pokemon, "test failed"
    url = f'{project_url}get-pokemon-by-type/flying'
    pokemon = requests.get(url=url)
    pokemon = pokemon.json()
    assert 'yanma' in pokemon, "test failed"





# test3
def test_update_pokemon_types():
    url = f'{project_url}update-pokemon-type/venusaur'
    requests.put(url=url)
    url = f'{project_url}get-pokemon-by-type/poison'
    pokemon = requests.get(url=url)
    pokemon = pokemon.json()
    assert 'venusaur' in pokemon, "test failed"
    url = f'{project_url}get-pokemon-by-type/grass'
    pokemon = requests.get(url=url)
    pokemon = pokemon.json()
    assert 'venusaur' in pokemon, "test failed"


# test4
def test_get_pokemons_by_owner():
    client_url = f'{project_url}get-pokemon-by-trainer/Drasna'
    res = requests.get(url=client_url)
    assert (res.json() == ["wartortle", "caterpie", "beedrill", "arbok", "clefairy", "wigglytuff", "persian",
                           "growlithe", "machamp", "golem", "dodrio", "hypno", "cubone", "eevee", "kabutops"])


# test5
def test_get_owners_of_a_pokemon():
    client_url = f'{project_url}get-trainers-by-pokemon/charmander'
    res = requests.get(url=client_url)
    assert (res.json() == ["Giovanni", "Jasmine", "Whitney"])


def test_evolve():
    url = f'{project_url}pokemon-evolve'
    data = json.dumps({
        "pokemon": "pinsir",
        "trainer": "Whitney"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    res = requests.request("PUT", url, headers=headers, data=data, verify=True)
    assert (res.json() == "can't evolve")

    url = f'{project_url}pokemon-evolve'
    data = json.dumps({
        "pokemon": "spearow",
        "trainer": "Archie"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    res = requests.request("PUT", url, headers=headers, data=data, verify=True)
    assert (res.json() == "trainer does not have this pokemon")

    url = f'{project_url}pokemon-evolve'
    data = json.dumps({
        "pokemon": "oddish",
        "trainer": "Whitney"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    res = requests.request("PUT", url, headers=headers, data=data, verify=True)
    assert (res.json() == "pokemon evolve successfully")
    url = f'{project_url}pokemon-evolve'
    data = json.dumps({
        "pokemon": "oddish",
        "trainer": "Whitney"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    res = requests.request("PUT", url, headers=headers, data=data, verify=True)
    assert (res.json() == "trainer does not have this pokemon")

    client_url = f'{project_url}get-pokemon-by-trainer/Whitney'
    res = requests.get(url=client_url)
    assert 'gloom' in res.json(), 'test failed'
