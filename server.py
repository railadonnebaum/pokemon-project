from flask import Response, request, Flask

from controller import get_pokemon_by_trainer_controller, get_pokemon_by_type_controller, \
    update_pokemon_type_controller, add_pokemone_controller, delete_pokemon_controller, \
    pokemon_evolve_controller, get_trainers_by_pokemon_controller, delete_pokemon_by_trainer_controller

import json
from connection.config import server_port

server = Flask(__name__)

'''
returns all the pokemons with the specific type
:param name of type
:return all the pokemon with the specific type
'''


@server.route('/pokemon/get-pokemon-by-type/<type>', methods=['GET'])
def get_pokemon_by_type(type):
    res = Response(json.dumps(get_pokemon_by_type_controller(type)), status=200)
    print(res)
    return res


'''
update the types of a specific pokemon
:param name of pokemon
:return a relevant message
'''


@server.route('/pokemon/update-pokemon-type/<name>', methods=['PUT'])
def update_pokemon_type(name):
    res = update_pokemon_type_controller(name)
    if res == 200:
        return Response(json.dumps("updated successfully"), status=200)
    if res == 404:
        return Response(json.dumps("name not found"), status=404)
    return Response(json.dumps("updated failed"), status=500)


'''
:param name of trainer
:return all the pokemons of a specific trainer
'''


@server.route('/pokemon/get-pokemon-by-trainer/<trainer>', methods=['GET'])
def get_pokemon_by_trainer(trainer):
    return Response(json.dumps(get_pokemon_by_trainer_controller(trainer)))


'''
adds a pokemon with the given values
:body - {id:.. , name:.., height:.., weight:.., types:...}
:return a relevant message
'''


@server.route('/pokemon/add-pokemon', methods=['POST'])
def add_pokemon():
    pokemon = request.get_json()
    res = add_pokemone_controller(pokemon['id'], pokemon['name'], pokemon['height'], pokemon['weight'],
                                  pokemon['types'])
    if res:
        return Response(json.dumps("added successfully"), status=201)
    return Response(json.dumps("added failed"), status=500)


'''
deletes a specific pokemon
:pokemon id
:return a relevant message
'''


@server.route('/pokemon/delete-pokemon/<id>', methods=['DELETE'])
def delete_pokemon(id):
    res = delete_pokemon_controller(id)
    if res:
        return Response(json.dumps("delete successfully"), status=200)
    return Response(json.dumps("delete failed"), status=500)


'''
deletes all the pokemons of a given trainer
:param name of trainer
:return a relevant message
'''


@server.route('/pokemon/delete-pokemon-by-trainer/<trainer_name>', methods=['DELETE'])
def delete_pokemon_by_trainer(trainer_name):
    res = delete_pokemon_by_trainer_controller(trainer_name)
    if res:
        return Response(json.dumps("delete successfully"), status=200)
    return Response(json.dumps("delete failed"), status=500)


'''
:param name of pokemon
:return all the trainer of the specific pokemon
'''


@server.route('/pokemon/get-trainers-by-pokemon/<name>', methods=['GET'])
def get_trainers_by_pokemon(name):
    res = get_trainers_by_pokemon_controller(name)
    return Response(json.dumps(res))


'''
evolves a specific pokemon
:body: {pokemon: pokemon_name , trainer: trainer_name}
:return a relevant message
'''


@server.route('/pokemon/pokemon-evolve', methods=['PUT'])
def pokemon_evolve():
    data = request.get_json()
    res = pokemon_evolve_controller(data['pokemon'], data['trainer'])
    return Response(json.dumps(res[0]), status=res[1])


if __name__ == '__main__':
    server.run(port=server_port)
