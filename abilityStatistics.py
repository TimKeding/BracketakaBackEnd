import csv

class AbilityStatistics:

    def __init__(self, pokedex, tournamentId):
        self.pokedex = pokedex
        self.tournamentId = tournamentId

    def getTotalAbilityUsage(self):
        cur = self.pokedex.conn.cursor()
        cur.execute(
            "SELECT ability, count(*) AS total, (count(*)/CAST((select count(*) from team) as float))*100 FROM tourney_pokemon "
            "WHERE tournament_id = ? "
            "GROUP BY ability ORDER BY total DESC", (self.tournamentId,))
        abilities = cur.fetchall()
        return list(abilities)

    def getAbilityUsagePerPokemon(self):
        cur = self.pokedex.conn.cursor()
        cur.execute(
            "SELECT tourney_pokemon.name, tourney_pokemon.ability, count(*) AS total, (count(*)/CAST(pokeTotal AS float))*100 FROM tourney_pokemon "
            "LEFT JOIN ( SELECT name, count(*) AS pokeTotal FROM tourney_pokemon "
            "WHERE tournament_id = ? "
            "GROUP BY name) AS totals ON tourney_pokemon.name = totals.name "
            "GROUP BY tourney_pokemon.name, tourney_pokemon.ability "
            "ORDER BY tourney_pokemon.name, total DESC", (self.tournamentId,))
        abilities = cur.fetchall()
        return abilities

    def getAbilityUsageForPokemon(self, pokedexId):
        return

    def exportAllStats(self):
        with open('./results/totalAbilityUsage.csv', mode='w', newline='') as abilityUsageFile:
            writer = csv.writer(abilityUsageFile, delimiter=',')
            writer.writerow(['Ability Usage Results', '(ability, instances, usage %)'])
            for item in self.getTotalAbilityUsage():
                writer.writerow(item)

        with open('./results/abilityUsagePerPokemon.csv', mode='w', newline='') as abilityUsagePerPokemonFile:
            writer = csv.writer(abilityUsagePerPokemonFile, delimiter=',')
            writer.writerow(['Ability Usage Per Pokemon Results', '(pokemon, ability, instances, usage %)'])
            for item in self.getAbilityUsagePerPokemon():
                writer.writerow(item)
        return

