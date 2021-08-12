import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="password",
    db="sql_pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

server_port = 3000
pokemon_API_url = "https://pokeapi.co/api/v2/pokemon/"
project_url = "http://127.0.0.1:3000/pokemon/"
