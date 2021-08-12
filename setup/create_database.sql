USE sql_pokemon;

CREATE TABLE pokemon (
    id int PRIMARY KEY,
    name VARCHAR(20),
    height float,
    weight float
);

CREATE TABLE types(
    id int AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(20) UNIQUE
);

CREATE TABLE pokemon_type(
    pokemon int,
    type int,
    FOREIGN KEY (pokemon) REFERENCES pokemon(id)
    ON DELETE CASCADE,
    FOREIGN KEY (type) REFERENCES types(id)
    ON DELETE CASCADE,
    CONSTRAINT pokemon_type PRIMARY KEY (pokemon, type)
);

CREATE TABLE owner (
    name VARCHAR(20) PRIMARY KEY,
    town VARCHAR(20)
);

CREATE TABLE ownedBy (
    pokemon int,
    owner VARCHAR(20),
    FOREIGN KEY (owner) REFERENCES owner(name),
    FOREIGN KEY (pokemon) REFERENCES pokemon(id),
    CONSTRAINT ownedBy PRIMARY KEY (owner,pokemon)
);


