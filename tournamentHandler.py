import requests
from bs4 import BeautifulSoup
import csv
import datetime
import re

class TournamentHandler:

    def __init__(self, pokedex):
        self.pokedex = pokedex

    def insertTournament(self, tournamentFile):
        sqlGetLastTournamentId = """SELECT MAX(id) FROM tournament"""
        with open(tournamentFile) as tournament:
            tournamentInfo = csv.reader(tournament, delimiter=',')
            tournamentDetails = next(tournamentInfo)
            tournamentName = tournamentDetails[0]
            tournamentRules = tournamentDetails[1]
            tournamentStart = tournamentDetails[2]
            tournamentStartDate = datetime.datetime.strptime(tournamentStart, '%Y-%m-%d')
            tournamentEnd = tournamentDetails[3]
            tournamentEndDate = datetime.datetime.strptime(tournamentEnd, '%Y-%m-%d')
            tournamentData = (tournamentName, tournamentRules, tournamentStartDate, tournamentEndDate)
            self.pokedex.insertTournament(tournamentData)

            cur = self.pokedex.conn.cursor()
            cur.execute(sqlGetLastTournamentId)
            row = cur.fetchone()
            if row != None:
                tournamentId = row[0]

            for team in tournamentInfo:
                self.insertTeam(team, tournamentId)
        return

    def insertTeam(self, team, tournamentId):
        sqlGetLastTeamId = """SELECT MAX(id) FROM team"""
        teamFile = team[0]
        ranking = 0
        if len(team) > 2:
            ranking = team[2]

        self.pokedex.insertTeam((tournamentId, team[1], ranking))

        cur = self.pokedex.conn.cursor()
        cur.execute(sqlGetLastTeamId)
        row = cur.fetchone()
        if row != None:
            teamId = row[0]

        teamTable = self.parseTeam(teamFile)
        self.insertPokemons(teamTable, teamId, tournamentId)
        return

    def parseTeam(self, teamFile):
        request = requests.get(teamFile).text
        soup = BeautifulSoup(request, 'html.parser')
        teamTable = soup.find_all(text=True)
        parsedTeamTable = []

        for row in teamTable:
            splitData = re.split('\n- |@ |\n| \(', row)
            for pos, i in enumerate(splitData):
                i = str.strip(i)
                i = i.replace('Gmax', '')
                i = re.sub('[\W_]+', '', i).lower()
                if i == 'asone':
                    horse = splitData[pos+1]
                    horse = str.strip(horse)
                    horse = re.sub('[\W_]+', '', horse).lower()
                    i += horse
                    splitData[pos+1] = ''
                if i != '' and len(i) > 1:
                    parsedTeamTable.append(i)

        return parsedTeamTable[2:-5]

    def insertPokemons(self, teamTable, teamId, tournamentId):
        for i in range(len(teamTable)):
            pokemon = teamTable[i].lower()
            pokemon = ''.join(e for e in pokemon if e.isalnum())
            cur = self.pokedex.conn.cursor()
            cur.execute("SELECT id, type_1, type_2 FROM pokemon WHERE ref_name like '{}'".format(pokemon))
            row = cur.fetchone()
            if row != None:
                self.insertPokemon(teamTable[i:], row, teamId, tournamentId)
        return

    def insertPokemon(self, strippedTeamTable, pokemonDetails, teamId, tournamentId):
        sqlGetLastPokemonId = """SELECT MAX(id) FROM pokemon"""
        pokedexId = pokemonDetails[0]
        type1 = pokemonDetails[1]
        type2 = pokemonDetails[2]
        pokemonName = strippedTeamTable[0]
        item = None
        ability = None
        level = 50
        nature = "Serious"
        ivs = {'hp':31,'atk':31,'def':31,'spa':31,'spd':31,'spe':31}
        evs = {'hp':0,'atk':0,'def':0,'spa':0,'spd':0,'spe':0}

        cur = self.pokedex.conn.cursor()
        position = 1
        while(strippedTeamTable[position] != 'ability' and strippedTeamTable[position] != 'level'):
            cur.execute("SELECT name FROM item WHERE ref_name like '{}'".format(strippedTeamTable[position]))
            row = cur.fetchone()
            if row != None:
                item = row[0]
            position += 1

        if position < len(strippedTeamTable) and strippedTeamTable[position] == "level":
            level = strippedTeamTable[position+1]
            position += 2
        if strippedTeamTable[position] == "ability":
            position += 1

        cur.execute("SELECT name from ability where ref_name like '{}'".format(strippedTeamTable[position]))
        row = cur.fetchone()
        if row != None:
            ability = row[0]
            position += 1

        if position < len(strippedTeamTable) and strippedTeamTable[position] == "level":
            level = strippedTeamTable[position+1]
            position += 2
        if position < len(strippedTeamTable) and strippedTeamTable[position] == "shiny":
            position += 2
        if position < len(strippedTeamTable) and strippedTeamTable[position] == "evs":
            position += 1
            for i in range(6):
                if position >= len(strippedTeamTable):
                    break
                evStats = re.split('(\d+)', strippedTeamTable[position])
                if len(evStats) == 1 or \
                        evStats[2] not in ivs.keys():
                    break
                evValue = evStats[1]
                evType = evStats[2]
                evs[evType] = int(evValue)
                position += 1
        if position < len(strippedTeamTable) and strippedTeamTable[position][-6:] == "nature":
            nature = strippedTeamTable[position][:-6]
            position += 1
        if position < len(strippedTeamTable) and strippedTeamTable[position] == "ivs":
            position += 1
            for i in range(6):
                if position >= len(strippedTeamTable):
                    break
                ivStats = re.split('(\d+)', strippedTeamTable[position])
                if len(ivStats) == 1 or \
                        ivStats[2] not in ivs.keys():
                    break
                ivValue = ivStats[1]
                ivType = ivStats[2]
                ivs[ivType] = int(ivValue)
                position += 1
        pokemonData = (pokedexId, tournamentId, teamId, pokemonName, level, type1, type2, ability, item, nature,
                       ivs['hp'], ivs['atk'], ivs['def'], ivs['spa'], ivs['spd'], ivs['spe'],
                       evs['hp'], evs['atk'], evs['def'], evs['spa'], evs['spd'], evs['spe'])
        self.pokedex.insertTourneyPokemon(pokemonData)
        cur.execute(sqlGetLastPokemonId)
        row = cur.fetchone()
        pokemonId = None
        if row != None:
            pokemonId = row[0]
        if position < len(strippedTeamTable):
            done = False
            while not done and position < len(strippedTeamTable):
                cur.execute("SELECT id FROM move WHERE ref_name like '{}'".format(strippedTeamTable[position]))
                row = cur.fetchone()
                if row != None:
                    moveId = row[0]
                    moveData = (moveId, tournamentId, pokemonId)
                    self.pokedex.insertTourneyMove(moveData)
                    position += 1
                else:
                    done = True

        return
