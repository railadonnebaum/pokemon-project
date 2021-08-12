from service import find_by_type, get_pokemon_by_owner, add_pokemon, delete_pokemon, \
    update_pokemon_type, pokemon_evolve, get_trainers_by_pokemon, delete_pokemon_of_trainer


def get_pokemon_by_type_controller(pokemon_type):
    return find_by_type(pokemon_type)


def pokemon_evolve_controller(pokemon, trainer):
    return pokemon_evolve(pokemon, trainer)


def update_pokemon_type_controller(name):
    return update_pokemon_type(name)


def get_pokemon_by_trainer_controller(trainer):
    return get_pokemon_by_owner(trainer)


def add_pokemone_controller(id, name, height, weight, types):
    return add_pokemon(id, name, height, weight, types)


def delete_pokemon_controller(id):
    return delete_pokemon(id)


def delete_pokemon_by_trainer_controller(trainer_name):
    return delete_pokemon_of_trainer(trainer_name)


def get_trainers_by_pokemon_controller(pokemon):
    return get_trainers_by_pokemon(pokemon)
