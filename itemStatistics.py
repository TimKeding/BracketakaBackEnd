import csv

class ItemStatistics:

    def __init__(self, pokedex, tournamentId):
        self.pokedex = pokedex
        self.tournamentId = tournamentId

    def getTotalItemUsage(self):
        cur = self.pokedex.conn.cursor()
        cur.execute(
            "SELECT item, count(*) AS total, (count(*)/CAST((select count(*) from team) as float))*100 FROM tourney_pokemon "
            "WHERE tournament_id = ? "
            "GROUP BY item ORDER BY total DESC", (self.tournamentId,))
        items = cur.fetchall()
        return list(items)

    def getItemUsagePerPokemon(self):
        cur = self.pokedex.conn.cursor()
        cur.execute(
            "SELECT tourney_pokemon.name, tourney_pokemon.item, count(*) AS total, (count(*)/CAST(pokeTotal AS float))*100 FROM tourney_pokemon "
            "LEFT JOIN ( SELECT name, count(*) AS pokeTotal FROM tourney_pokemon "
            "WHERE tournament_id = ? "
            "GROUP BY name) AS totals ON tourney_pokemon.name = totals.name "
            "GROUP BY tourney_pokemon.name, tourney_pokemon.item "
            "ORDER BY tourney_pokemon.name, total DESC", (self.tournamentId,))
        items = cur.fetchall()
        return items

    def getAllItems(self):
        cur = self.pokedex.conn.cursor()
        cur.execute(
            "SELECT * FROM item")
        items = cur.fetchall()
        return items

    def getItemUsageForPokemon(self, pokedexId):
        return

    def exportAllStats(self):
        with open('./results/totalItemUsage.csv', mode='w', newline='') as itemUsageFile:
            writer = csv.writer(itemUsageFile, delimiter=',')
            writer.writerow(['Item Usage Results', '(item, instances, usage %)'])
            for item in self.getTotalItemUsage():
                writer.writerow(item)

        with open('./results/itemUsagePerPokemon.csv', mode='w', newline='') as itemUsagePerPokemonFile:
            writer = csv.writer(itemUsagePerPokemonFile, delimiter=',')
            writer.writerow(['Item Usage Per Pokemon Results', '(pokemon, item, instances, usage %)'])
            for item in self.getItemUsagePerPokemon():
                writer.writerow(item)
        return

    def exportAllItems(self):
        with open('./results/allItems.csv', mode='w', newline='') as itemFile:
            writer = csv.writer(itemFile, delimiter=',')
            for item in self.getAllItems():
                writer.writerow(item)
        return
