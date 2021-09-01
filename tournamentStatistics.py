from moveStatistics import MoveStatistics
from itemStatistics import ItemStatistics
from abilityStatistics import AbilityStatistics
import csv

class TournamentStatistics:

    def __init__(self, pokedex, tournamentId):
        self.pokedex = pokedex
        self.tournamentId = tournamentId
        self.moveStatistics = MoveStatistics(pokedex, tournamentId)
        self.itemStatistics = ItemStatistics(pokedex, tournamentId)
        self.abilityStatistics = AbilityStatistics(pokedex, tournamentId)

    def getPokemonUsage(self):
        cur = self.pokedex.conn.cursor()
        cur.execute("SELECT name, count(*) AS total, "
                    "(count(*)/CAST((select count(*) from team) as float))*100 AS prob FROM tourney_pokemon "
                    "WHERE tournament_id = ?"
                    "GROUP BY name ORDER BY total DESC", (self.tournamentId,))
        pokemon = cur.fetchall()
        return pokemon

    def getTeammateUsage(self):
        cur = self.pokedex.conn.cursor()
        cur.execute(
            "SELECT tourney_pokemon.name, pokemon2.name, count(*) AS total, "
            "(count(*)/CAST((select count(*) from team) as float))*100 FROM tourney_pokemon "
            "JOIN tourney_pokemon AS pokemon2 ON tourney_pokemon.team_id = pokemon2.team_id and tourney_pokemon.name != pokemon2.name "
            "WHERE tourney_pokemon.tournament_id = ? "
            "GROUP BY tourney_pokemon.name, pokemon2.name ORDER BY total DESC", (self.tournamentId,))
        teammates = cur.fetchall()
        teammatesDict = {}
        for group in teammates:
            key = frozenset(group[:-2])
            teammatesDict[key] = group[-2:]
        teammateResults = []
        for key, value in teammatesDict.items():
            teammateResults.append(list(key) + list(value))
        return teammateResults

    def get3CoreUsage(self):
        cur = self.pokedex.conn.cursor()
        cur.execute(
            "SELECT poke1, poke2, poke3, total, percent FROM "
            "(SELECT pokemon1.name as poke1, pokemon2.name as poke2, pokemon3.name as poke3, count(*) AS total, "
            "(count(*)/CAST((select count(*) from team) as float))*100 as percent FROM tourney_pokemon AS pokemon1 "
            "JOIN tourney_pokemon AS pokemon2 ON pokemon1.team_id = pokemon2.team_id and "
            "pokemon1.name != pokemon2.name "
            "JOIN tourney_pokemon AS pokemon3 ON pokemon1.team_id = pokemon3.team_id and "
            "pokemon1.name != pokemon3.name and pokemon2.name != pokemon3.name "
            "WHERE pokemon1.tournament_id = ? "
            "GROUP BY pokemon1.name, pokemon2.name, pokemon3.name) "
            "WHERE total > 1 "
            "ORDER BY total DESC", (self.tournamentId,))
        teammates = cur.fetchall()
        teammatesDict = {}
        for group in teammates:
            key = frozenset(group[:-2])
            teammatesDict[key] = group[-2:]
        teammateResults = []
        for key, value in teammatesDict.items():
            teammateResults.append(list(key) + list(value))
        return teammateResults

    def get4CoreUsage(self):
        cur = self.pokedex.conn.cursor()
        cur.execute(
            "SELECT poke1, poke2, poke3, poke4, total, percent FROM "
            "(SELECT pokemon1.name as poke1, pokemon2.name as poke2, pokemon3.name as poke3, pokemon4.name as poke4, "
            "count(*) AS total, (count(*)/CAST((select count(*) from team) as float))*100 as percent "
            "FROM tourney_pokemon AS pokemon1 "
            "JOIN tourney_pokemon AS pokemon2 ON pokemon1.team_id = pokemon2.team_id and "
            "pokemon1.name != pokemon2.name "
            "JOIN tourney_pokemon AS pokemon3 ON pokemon1.team_id = pokemon3.team_id and "
            "pokemon1.name != pokemon3.name and pokemon2.name != pokemon3.name "
            "JOIN tourney_pokemon AS pokemon4 ON pokemon1.team_id = pokemon4.team_id and "
            "pokemon1.name != pokemon4.name and pokemon2.name != pokemon4.name and pokemon3.name != pokemon4.name "
            "WHERE pokemon1.tournament_id = ? "
            "GROUP BY pokemon1.name, pokemon2.name, pokemon3.name, pokemon4.name) "
            "WHERE total > 1 ORDER BY total DESC", (self.tournamentId,))
        teammates = cur.fetchall()
        teammatesDict = {}
        for group in teammates:
            key = frozenset(group[:-2])
            teammatesDict[key] = group[-2:]
        teammateResults = []
        for key, value in teammatesDict.items():
            teammateResults.append(list(key) + list(value))
        return teammateResults

    def get5CoreUsage(self):
        cur = self.pokedex.conn.cursor()
        cur.execute(
            "SELECT poke1, poke2, poke3, poke4, poke5, total, percent FROM "
            "(SELECT pokemon1.name as poke1, pokemon2.name as poke2, pokemon3.name as poke3, pokemon4.name as poke4, "
            "pokemon5.name as poke5, count(*) AS total, (count(*)/CAST((select count(*) from team) as float))*100 as percent "
            "FROM tourney_pokemon AS pokemon1 "
            "JOIN tourney_pokemon AS pokemon2 ON pokemon1.team_id = pokemon2.team_id and "
            "pokemon1.name != pokemon2.name "
            "JOIN tourney_pokemon AS pokemon3 ON pokemon1.team_id = pokemon3.team_id and "
            "pokemon1.name != pokemon3.name and pokemon2.name != pokemon3.name "
            "JOIN tourney_pokemon AS pokemon4 ON pokemon1.team_id = pokemon4.team_id and "
            "pokemon1.name != pokemon4.name and pokemon2.name != pokemon4.name and pokemon3.name != pokemon4.name "
            "JOIN tourney_pokemon AS pokemon5 ON pokemon1.team_id = pokemon5.team_id and "
            "pokemon1.name != pokemon5.name and pokemon2.name != pokemon5.name and pokemon3.name != pokemon5.name "
            "and pokemon4.name != pokemon5.name "
            "WHERE pokemon1.tournament_id = ? "
            "GROUP BY pokemon1.name, pokemon2.name, pokemon3.name, pokemon4.name, pokemon5.name) "
            "WHERE total > 1 ORDER BY total DESC", (self.tournamentId,))
        teammates = cur.fetchall()
        teammatesDict = {}
        for group in teammates:
            key = frozenset(group[:-2])
            teammatesDict[key] = group[-2:]
        teammateResults = []
        for key, value in teammatesDict.items():
            teammateResults.append(list(key) + list(value))
        return teammateResults

    def get6CoreUsage(self):
        cur = self.pokedex.conn.cursor()
        cur.execute(
            "SELECT poke1, poke2, poke3, poke4, poke5, poke6, total, percent FROM "
            "(SELECT pokemon1.name as poke1, pokemon2.name as poke2, pokemon3.name as poke3, pokemon4.name as poke4, "
            "pokemon5.name as poke5, pokemon6.name as poke6, count(*) AS total, (count(*)/CAST((select count(*) from team) as float))*100 as percent "
            "FROM tourney_pokemon AS pokemon1 "
            "JOIN tourney_pokemon AS pokemon2 ON pokemon1.team_id = pokemon2.team_id and "
            "pokemon1.name != pokemon2.name "
            "JOIN tourney_pokemon AS pokemon3 ON pokemon1.team_id = pokemon3.team_id and "
            "pokemon1.name != pokemon3.name and pokemon2.name != pokemon3.name "
            "JOIN tourney_pokemon AS pokemon4 ON pokemon1.team_id = pokemon4.team_id and "
            "pokemon1.name != pokemon4.name and pokemon2.name != pokemon4.name and pokemon3.name != pokemon4.name "
            "JOIN tourney_pokemon AS pokemon5 ON pokemon1.team_id = pokemon5.team_id and "
            "pokemon1.name != pokemon5.name and pokemon2.name != pokemon5.name and pokemon3.name != pokemon5.name "
            "and pokemon4.name != pokemon5.name "
            "JOIN tourney_pokemon AS pokemon6 ON pokemon1.team_id = pokemon6.team_id and "
            "pokemon1.name != pokemon6.name and pokemon2.name != pokemon6.name and pokemon3.name != pokemon6.name "
            "and pokemon4.name != pokemon6.name and pokemon5.name != pokemon6.name "
            "WHERE pokemon1.tournament_id = ? "
            "GROUP BY pokemon1.name, pokemon2.name, pokemon3.name, pokemon4.name, pokemon5.name, pokemon6.name) "
            "WHERE total > 1 ORDER BY total DESC", (self.tournamentId,))
        teammates = cur.fetchall()
        teammatesDict = {}
        for group in teammates:
            key = frozenset(group[:-2])
            teammatesDict[key] = group[-2:]
        teammateResults = []
        for key, value in teammatesDict.items():
            teammateResults.append(list(key) + list(value))
        return teammateResults

    def getTeammateProbability(self):
        # Probability of B given A = p(A&B)/p(A)
        cur = self.pokedex.conn.cursor()
        cur.execute("SELECT teammates.pokemon_a, teammates.pokemon_b, teammates.total AS total, (teammates.prob_together/single.prob)*100 AS prob FROM "
                    "(SELECT name, (count(*)/CAST((select count(*) from team) as float))*100 AS prob FROM tourney_pokemon "
                    "WHERE tourney_pokemon.tournament_id = ? "
                    "GROUP BY name) AS single JOIN "
                    "(SELECT pokemon1.name AS pokemon_a, pokemon2.name AS pokemon_b, count(*) AS total, "
                    "(count(*)/CAST((select count(*) from team) AS float))*100 AS prob_together FROM tourney_pokemon AS pokemon1 "
                    "JOIN tourney_pokemon AS pokemon2 ON pokemon1.team_id = pokemon2.team_id and pokemon1.name != pokemon2.name "
                    "WHERE pokemon1.tournament_id = ? "
                    "GROUP BY pokemon1.name, pokemon2.name) as teammates ON single.name = teammates.pokemon_a "
                    "ORDER BY total DESC, prob DESC", (self.tournamentId, self.tournamentId))

        teammateProb = cur.fetchall()
        return teammateProb

    def getTeammateProbabilityAlt(self):
        # Probability of B given A = p(A&B)/p(A)
        pokemonUsage = self.getPokemonUsage()
        teammateUsage = self.getTeammateUsage()
        teammateProbability = {}

        for pokemon in pokemonUsage:
            pokemonName = pokemon[0]
            pokemonProb = pokemon[2]
            for teammates in teammateUsage:
                teamCount = teammates[2]
                teamProb = teammates[3]
                if teammates[0] == pokemonName:
                    teammateProbability[(pokemonName, teammates[1])] = [teamCount, teamProb/pokemonProb]
                if teammates[1] == pokemonName:
                    teammateProbability[(pokemonName, teammates[0])] = [teamCount, teamProb/pokemonProb]
        probResults = list(map(list, teammateProbability.items()))
        probResults.sort(key=lambda x: (x[1][0], x[1][1]), reverse=True)
        return probResults

    def getTypeUsage(self):
        cur = self.pokedex.conn.cursor()
        cur.execute("SELECT type, count(*) AS total FROM "
                    "(SELECT type_1 AS type FROM tourney_pokemon WHERE type IS NOT NULL AND tournament_id = ?"
                    "UNION ALL "
                    "SELECT type_2 AS type FROM tourney_pokemon WHERE type IS NOT NULL AND tournament_id = ?) "
                    "GROUP BY type ORDER by total DESC", (self.tournamentId, self.tournamentId))

        typeUsage = cur.fetchall()
        return typeUsage

    def getTotalPlayers(self):
        cur = self.pokedex.conn.cursor()
        cur.execute("SELECT count(*) FROM team WHERE tournament_id LIKE ?", (self.tournamentId,))
        totalPlayers = cur.fetchone()[0]
        return totalPlayers

    def getTotalPokemon(self):
        cur = self.pokedex.conn.cursor()
        cur.execute(
            "SELECT count(*) AS total FROM tourney_pokemon "
            "WHERE tournament_id = ?", (self.tournamentId,))
        totalPokemon = cur.fetchone()[0]
        return totalPokemon

    def getTotalUniquePokemon(self):
        cur = self.pokedex.conn.cursor()
        cur.execute(
            "SELECT count(DISTINCT name) FROM tourney_pokemon "
            "WHERE tournament_id = ?", (self.tournamentId,))
        totalUniquePokemon = cur.fetchone()[0]
        return totalUniquePokemon

    def getSingleInstancePokemon(self):
        cur = self.pokedex.conn.cursor()
        cur.execute(
            "SELECT name FROM (SELECT name, count(*) AS total FROM tourney_pokemon "
            "WHERE tournament_id = ? "
            "GROUP BY name) WHERE total = 1", (self.tournamentId,))
        singlePokemon = cur.fetchall()
        return singlePokemon

    def exportAllStats(self):
        self.exportGeneralPokemonStats()
        self.exportPokemonUsageStats()
        self.itemStatistics.exportAllStats()
        self.abilityStatistics.exportAllStats()
        self.moveStatistics.exportAllStats()
        return

    def exportGeneralPokemonStats(self):
        with open('./results/generalPokemonStats.csv', mode='w', newline='') as generalPokemonStatsFile:
            writer = csv.writer(generalPokemonStatsFile, delimiter=',')
            writer.writerow(['Total Players', self.getTotalPlayers()])
            writer.writerow(['Total Pokemon', self.getTotalPokemon()])
            writer.writerow(['Total Unique Pokemon', self.getTotalUniquePokemon()])
            writer.writerow(['Pokemon Type Usage'])
            self.getTypeUsage()
            for type in self.getTypeUsage():
                writer.writerow(type)
            writer.writerow(['Pokemon only appearing once'])
            for pokemon in self.getSingleInstancePokemon():
                writer.writerow(pokemon)
        return

    def exportPokemonUsageStats(self):
        self.exportSinglePokemonUsage()
        self.exportTeammateUsage()
        self.exportTeammateProbability()
        return

    def exportSinglePokemonUsage(self):
        with open('./results/singlePokemonUsage.csv', mode='w', newline='') as singlePokemonUsageFile:
            writer = csv.writer(singlePokemonUsageFile, delimiter=',')
            writer.writerow(['Pokemon Usage Results', '(pokemon, instances, usage %)'])
            for pokemon in self.getPokemonUsage():
                writer.writerow(pokemon)
        return

    def exportTeammateUsage(self):
        with open('./results/teammateUsage.csv', mode='w', newline='') as teammateUsageFile:
            writer = csv.writer(teammateUsageFile, delimiter=',')
            writer.writerow(['Teammate Usage Results', '(pokemon, instances, usage %)'])
            writer.writerow(['6 Core Results'])
            for teammates in self.get6CoreUsage():
                writer.writerow(teammates)
            writer.writerow(['5 Core Results'])
            for teammates in self.get5CoreUsage():
                writer.writerow(teammates)
            writer.writerow(['4 Core Results'])
            for teammates in self.get4CoreUsage():
                writer.writerow(teammates)
            writer.writerow(['3 Core Results'])
            for teammates in self.get3CoreUsage():
                writer.writerow(teammates)
            writer.writerow(['2 Core Results'])
            for teammates in self.getTeammateUsage():
                writer.writerow(teammates)
        return

    def exportTeammateProbability(self):
        with open('./results/teammateProbability.csv', mode='w', newline='') as teammateProbabilityFile:
            writer = csv.writer(teammateProbabilityFile, delimiter=',')
            writer.writerow(['Pokemon Probability Results',
                             '(pokemon 1, pokemon 2, % chance that pokemon 1 will have pokemon 2 as a partner)'])
            for pokemon in self.getTeammateProbability():
                writer.writerow(pokemon)
        return