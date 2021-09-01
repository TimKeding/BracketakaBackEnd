import sqlite3
from sqlite3 import Error
import requests
import json
import re

class Pokedex:

    def __init__(self):
        self.conn = None
        self.setupDatabase()

    def setupDatabase(self):
        self.createDBConnection()
        if self.conn is not None:
            self.createShowdownTables()
            self.createTournamentTables()
            self.populateDatabase()
        return

    def createShowdownTables(self):
        self.createPokemonSqlTable()
        self.createItemSqlTable()
        self.createAbilitySqlTable()
        self.createMoveSqlTable()
        self.createTypeChartSqlTable()
        return

    def createTournamentTables(self):
        self.createTourneyPokemonSqlTable()
        self.createTourneyMoveSqlTable()
        self.createTeamSqlTable()
        self.createTournamentSqlTable()
        return

    def createPokemonSqlTable(self):
        sqlCreatePokemonTable = """CREATE TABLE IF NOT EXISTS pokemon (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    pokedex_number integer NOT NULL,
                                    ref_name text NOT NULL,
                                    name text NOT NULL,
                                    type_1 text NOT NULL,
                                    type_2 text,
                                    height_m float,
                                    weight_kg float,
                                    ability_1 text NOT NULL,
                                    ability_2 text,
                                    ability_hidden text,
                                    hp integer NOT NULL,
                                    attack integer NOT NULL,
                                    defense integer NOT NULL,
                                    sp_attack integer NOT NULL,
                                    sp_defense integer NOT NULL,
                                    speed integer NOT NULL
                                );"""
        self.executeSQLCommand(sqlCreatePokemonTable)
        return

    def createItemSqlTable(self):
        sqlCreateItemTable = """CREATE TABLE IF NOT EXISTS item (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                sprite_number integer NOT NULL,
                                ref_name text NOT NULL,
                                name text NOT NULL
                            );"""
        self.executeSQLCommand(sqlCreateItemTable)
        return

    def createAbilitySqlTable(self):
        sqlCreateAbilityTable = """CREATE TABLE IF NOT EXISTS ability (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                ref_name text NOT NULL,
                                name text NOT NULL
                            );"""
        self.executeSQLCommand(sqlCreateAbilityTable)
        return

    def createMoveSqlTable(self):
        sqlCreateMoveTable = """CREATE TABLE IF NOT EXISTS move (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                ref_name text NOT NULL,
                                name text NOT NULL,
                                base_power integer NOT NULL,
                                accuracy integer,
                                category text NOT NULL,
                                type text NOT NULL
                            );"""
        self.executeSQLCommand(sqlCreateMoveTable)
        return

    def createTypeChartSqlTable(self):
        sqlCreateTypeChartTable = """CREATE TABLE IF NOT EXISTS type_chart (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                type text NOT NULL,
                                bug integer NOT NULL,
                                dark integer NOT NULL,
                                dragon integer NOT NULL,
                                electric integer NOT NULL,
                                fairy integer NOT NULL,
                                fighting integer NOT NULL,
                                fire integer NOT NULL,
                                flying integer NOT NULL,
                                ghost integer NOT NULL,
                                grass integer NOT NULL,
                                ground integer NOT NULL,
                                ice integer NOT NULL,
                                normal integer NOT NULL,
                                poison integer NOT NULL,
                                psychic integer NOT NULL,
                                rock integer NOT NULL,
                                steel integer NOT NULL,
                                water integer NOT NULL
                            );"""
        self.executeSQLCommand(sqlCreateTypeChartTable)
        return

    def createTourneyPokemonSqlTable(self):
        sqlCreatePokemonTable = """CREATE TABLE IF NOT EXISTS tourney_pokemon (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    pokemon_id integer NOT NULL,
                                    tournament_id NOT NULL,
                                    team_id integer NOT NULL,
                                    name text NOT NULL,
                                    level integer NOT NULL,
                                    type_1 text NOT NULL,
                                    type_2 text,
                                    ability text NOT NULL,
                                    item text,
                                    nature text NOT NULL,
                                    iv_hp integer NOT NULL,
                                    iv_atk integer NOT NULL,
                                    iv_def integer NOT NULL,
                                    iv_spa integer NOT NULL,
                                    iv_spd integer NOT NULL,
                                    iv_spe integer NOT NULL,
                                    ev_hp integer NOT NULL,
                                    ev_atk integer NOT NULL,
                                    ev_def integer NOT NULL,
                                    ev_spa integer NOT NULL,
                                    ev_spd integer NOT NULL,
                                    ev_spe integer NOT NULL,
                                    count integer,
                                    FOREIGN KEY (pokemon_id) REFERENCES pokedex (id),
                                    FOREIGN KEY (tournament_id) REFERENCES tournament(id),
                                    FOREIGN KEY (team_id) REFERENCES team (id)
                                );"""
        self.executeSQLCommand(sqlCreatePokemonTable)
        return

    def createTourneyMoveSqlTable(self):
        sqlCreateMoveTable = """CREATE TABLE IF NOT EXISTS tourney_move (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            move_id integer NOT NULL,
                                            tournament_id NOT NULL,
                                            pokemon_id integer NOT NULL,
                                            FOREIGN KEY (move_id) REFERENCES move (id),
                                            FOREIGN KEY (pokemon_id) REFERENCES tourney_pokemon (id),
                                            FOREIGN KEY (tournament_id) REFERENCES tournament(id)
                                        );"""
        self.executeSQLCommand(sqlCreateMoveTable)
        return

    def createTeamSqlTable(self):
        sqlCreateTeamTable = """CREATE TABLE IF NOT EXISTS team (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                tournament_id integer NOT NULL,
                                player_name text,
                                rank integer
                            );"""
        self.executeSQLCommand(sqlCreateTeamTable)
        return

    def createTournamentSqlTable(self):
        sqlCreateTournamentTable = """CREATE TABLE IF NOT EXISTS tournament (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        tournament_name text NOT NULL,
                                        series_rules text,
                                        start_date date,
                                        end_date date
                                    );"""
        self.executeSQLCommand(sqlCreateTournamentTable)

    def createDBConnection(self):
        dbFile = 'pokedexDatabase.db'
        self.conn = None
        try:
            self.conn = sqlite3.connect(dbFile)
        except Error as e:
            print(e)
        return

    def executeSQLCommand(self, sqlCommand, data_tuple=None):
        try:
            c = self.conn.cursor()
            if data_tuple is not None:
                c.execute(sqlCommand, data_tuple)
            else:
                c.execute(sqlCommand)
        except Error as e:
            print(e)
        return

    def finished(self):
        self.conn.close()
        return

    def populateDatabase(self):
        self.downloadDatabaseFiles()
        self.populatePokemon()
        self.populateItems()
        self.populateAbilities()
        self.populateMoves()
        self.populateTypeChart()

    def downloadDatabaseFiles(self):
        pokedexUrl = 'https://play.pokemonshowdown.com/data/pokedex.js'
        itemdexUrl = 'https://play.pokemonshowdown.com/data/items.js'
        movedexUrl = 'https://play.pokemonshowdown.com/data/moves.js'
        abilitydexUrl = 'https://play.pokemonshowdown.com/data/abilities.js'
        typeChartUrl = 'https://play.pokemonshowdown.com/data/typechart.js'

        pokedexRequest = requests.get(pokedexUrl)
        with open('./DatabaseJS/pokedex.js', 'wb') as outfile:
            outfile.write(pokedexRequest.content)
        itemRequest = requests.get(itemdexUrl)
        with open('./DatabaseJS/itemdex.js', 'wb') as outfile:
            outfile.write(itemRequest.content)
        moveRequest = requests.get(movedexUrl)
        with open('./DatabaseJS/movedex.js', 'wb') as outfile:
            outfile.write(moveRequest.content)
        abilityRequest = requests.get(abilitydexUrl)
        with open('./DatabaseJS/abilitydex.js', 'wb') as outfile:
            outfile.write(abilityRequest.content)
        typeChartRequest = requests.get(typeChartUrl)
        with open('./DatabaseJS/typeChart.js', 'wb') as outfile:
            outfile.write(typeChartRequest.content)

    def populatePokemon(self):
        sqlInsertPokemon = """INSERT INTO pokemon (pokedex_number, ref_name, name, type_1, type_2, height_m, weight_kg, ability_1, ability_2, 
                            ability_hidden, hp, attack, defense, sp_attack, sp_defense, speed) 
                            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""
        pokemonDict = self.parseJS("./DatabaseJS/pokedex.js")
        for pokemonName, pokemonValues in pokemonDict.items():
            num = pokemonValues['num']
            ref_name = pokemonName
            name = pokemonValues['name']
            type_1 = pokemonValues['types'][0]
            if len(pokemonValues['types']) == 2:
                type_2 = pokemonValues['types'][1]
            else:
                type_2 = None
            height_m = pokemonValues['heightm']
            weight_kg = pokemonValues['weightkg']
            ability_1 = pokemonValues['abilities']['0']
            if '1' in pokemonValues['abilities'].keys():
                ability_2 = pokemonValues['abilities']['1']
            else:
                ability_2 = None
            if 'H' in pokemonValues['abilities'].keys():
                ability_hidden = pokemonValues['abilities']['H']
            else:
                ability_hidden = None
            hp = pokemonValues['baseStats']['hp']
            attack = pokemonValues['baseStats']['atk']
            defense = pokemonValues['baseStats']['def']
            sp_attack = pokemonValues['baseStats']['spa']
            sp_defense = pokemonValues['baseStats']['spd']
            speed = pokemonValues['baseStats']['spe']
            data_tuple = (num, ref_name, name, type_1, type_2, height_m, weight_kg, ability_1, ability_2, ability_hidden, hp,
                          attack, defense, sp_attack, sp_defense, speed)
            self.executeSQLCommand(sqlInsertPokemon, data_tuple)
        return

    def populateItems(self):
        sqlInsertItem = """INSERT INTO item (sprite_number, ref_name, name) 
                                    VALUES(?,?, ?);"""
        itemDict = self.parseJS("./DatabaseJS/itemdex.js")
        for itemName, itemValues in itemDict.items():
            sprite_number = itemValues['spritenum']
            name = itemValues['name']
            data_tuple = (sprite_number, itemName, name)
            self.executeSQLCommand(sqlInsertItem, data_tuple)
        return

    def populateAbilities(self):
        sqlInsertAbility = """INSERT INTO ability (ref_name, name) 
                                    VALUES(?, ?);"""
        abilityDict = self.parseJS("./DatabaseJS/abilitydex.js")
        for abilityName, abilityValues in abilityDict.items():
            name = abilityValues['name']
            data_tuple = (abilityName, name)
            self.executeSQLCommand(sqlInsertAbility, data_tuple)
        return

    def populateMoves(self):
        sqlInsertMove = """INSERT INTO move (ref_name, name, base_power, accuracy, category, type) 
                                    VALUES(?,?,?,?,?, ?);"""
        moveDict = self.parseJS("./DatabaseJS/movedex.js")
        for moveName, moveValues in moveDict.items():
            name = moveValues['name']
            base_power = moveValues['basePower']
            if isinstance(moveValues['accuracy'], int):
                accuracy = moveValues['accuracy']
            else:
                accuracy = None
            category = moveValues['category']
            type = moveValues['type']
            data_tuple = (moveName, name, base_power, accuracy, category, type)
            self.executeSQLCommand(sqlInsertMove, data_tuple)
        return

    def populateTypeChart(self):
        sqlInsertType = """INSERT INTO type_chart (type, bug, dark, dragon, electric, fairy, fighting, fire, flying, ghost,
                            grass, ground, ice, normal, poison, psychic, rock, steel, water) 
                                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""
        typeChartDict = self.parseJS("./DatabaseJS/typeChart.js")
        for type, typeValues in typeChartDict.items():
            bug = typeValues['damageTaken']['Bug']
            dark = typeValues['damageTaken']['Dark']
            dragon = typeValues['damageTaken']['Dragon']
            electric = typeValues['damageTaken']['Electric']
            fairy = typeValues['damageTaken']['Fairy']
            fighting = typeValues['damageTaken']['Fighting']
            fire = typeValues['damageTaken']['Fire']
            flying = typeValues['damageTaken']['Flying']
            ghost = typeValues['damageTaken']['Ghost']
            grass = typeValues['damageTaken']['Grass']
            ground = typeValues['damageTaken']['Ground']
            ice = typeValues['damageTaken']['Ice']
            normal = typeValues['damageTaken']['Normal']
            poison = typeValues['damageTaken']['Poison']
            psychic = typeValues['damageTaken']['Psychic']
            rock = typeValues['damageTaken']['Rock']
            steel = typeValues['damageTaken']['Steel']
            water = typeValues['damageTaken']['Water']
            data_tuple = (type, bug, dark, dragon, electric, fairy, fighting, fire, flying, ghost, grass, ground, ice,
                          normal, poison, psychic, rock, steel, water)
            self.executeSQLCommand(sqlInsertType, data_tuple)

    def parseJS(self, fileName):
        with open(fileName, encoding='utf-8') as json_file:
            data = json_file.read()
            data = re.sub('(\w+):', r'"\1":', data)
            data = re.sub('""(\w+)":', r'"\1:', data)
            data = re.sub(' "(\w+)":', r' \1:', data)
            data = re.sub('-"(\w+)":', r'-\1:', data)
            obj = data[data.find('{'): data.rfind('}')+1]
            jsonDict = json.loads(obj)
        return jsonDict

    def insertTournament(self, tournamentData):
        sqlInsertTournament = """INSERT INTO tournament (tournament_name, series_rules, start_date, end_date) 
                                                    VALUES(?,?,?,?);"""
        self.executeSQLCommand(sqlInsertTournament, tournamentData)
        return

    def insertTeam(self, teamData):
        sqlInsertTeam = """INSERT INTO team (tournament_id, player_name, rank) 
                                                    VALUES(?,?,?);"""
        self.executeSQLCommand(sqlInsertTeam, teamData)
        return

    def insertTourneyPokemon(self, pokemonData):
        sqlInsertPokemon = """INSERT INTO tourney_pokemon (pokemon_id, tournament_id, team_id, name, level, type_1, type_2, ability,
                            item, nature, iv_hp, iv_atk, iv_def, iv_spa, iv_spd, iv_spe, ev_hp, ev_atk, ev_def, 
                            ev_spa, ev_spd, ev_spe) 
                                                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""
        self.executeSQLCommand(sqlInsertPokemon, pokemonData)
        return

    def insertTourneyMove(self, moveData):
        sqlInsertMove = """INSERT INTO tourney_move (move_id, tournament_id, pokemon_id) VALUES(?,?,?)"""
        self.executeSQLCommand(sqlInsertMove, moveData)
        return
