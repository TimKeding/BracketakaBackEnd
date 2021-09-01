import csv

class MoveStatistics:

    def __init__(self, pokedex, tournamentId):
        self.pokedex = pokedex
        self.tournamentId = tournamentId

    def getMoveUsage(self):
        cur = self.pokedex.conn.cursor()
        cur.execute("SELECT move.name, count(*) AS total, "
                    "(count(*)/CAST((SELECT count(*) FROM tourney_pokemon WHERE tournament_id = ?) AS float))*100 "
                    "FROM tourney_move JOIN move ON tourney_move.move_id = move.id "
                    "WHERE tournament_id = ? "
                    "GROUP BY move.name ORDER BY total DESC", (self.tournamentId, self.tournamentId))
        moves = cur.fetchall()
        return moves

    def getTypeUsage(self):
        cur = self.pokedex.conn.cursor()
        cur.execute("SELECT move.type, count(*) AS total, "
                    "(count(*)/CAST((SELECT count(*) FROM tourney_pokemon WHERE tournament_id = ?) AS float))*100 "
                    "FROM tourney_move JOIN move ON tourney_move.move_id = move.id "
                    "WHERE tournament_id = ? "
                    "GROUP BY move.type ORDER BY total DESC", (self.tournamentId, self.tournamentId))

        types = cur.fetchall()
        return types

    def getPhysicalUsage(self):
        cur = self.pokedex.conn.cursor()
        cur.execute("SELECT move.name, count(*) AS total, "
                    "(count(*)/CAST((SELECT count(*) FROM tourney_pokemon WHERE tournament_id = ?) AS float))*100 "
                    "FROM tourney_move JOIN move ON tourney_move.move_id = move.id "
                    "WHERE tournament_id = ? AND move.category = 'Physical' "
                    "GROUP BY move.name ORDER BY total DESC", (self.tournamentId, self.tournamentId))

        moves = cur.fetchall()
        return moves

    def getSpecialUsage(self):
        cur = self.pokedex.conn.cursor()
        cur.execute("SELECT move.name, count(*) AS total, "
                    "(count(*)/CAST((SELECT count(*) FROM tourney_pokemon WHERE tournament_id = ?) AS float))*100 "
                    "FROM tourney_move JOIN move ON tourney_move.move_id = move.id "
                    "WHERE tournament_id = ? AND move.category = 'Special' "
                    "GROUP BY move.name ORDER BY total DESC", (self.tournamentId, self.tournamentId))

        moves = cur.fetchall()
        return moves

    def getStatusUsage(self):
        cur = self.pokedex.conn.cursor()
        cur.execute("SELECT move.name, count(*) AS total, "
                    "(count(*)/CAST((SELECT count(*) FROM tourney_pokemon WHERE tournament_id = ?) AS float))*100 "
                    "FROM tourney_move JOIN move ON tourney_move.move_id = move.id "
                    "WHERE tournament_id = ? AND move.category = 'Status' "
                    "GROUP BY move.name ORDER BY total DESC", (self.tournamentId, self.tournamentId))

        moves = cur.fetchall()
        return moves

    def exportAllStats(self):
        self.exportMoveUsage()
        self.exportSpecialUsage()
        self.exportPhysicalUsage()
        self.exportStatusUsage()
        return

    def exportMoveUsage(self):
        with open('./results/totalMoveUsage.csv', mode='w', newline='') as moveUsageFile:
            writer = csv.writer(moveUsageFile, delimiter=',')
            writer.writerow(['Move type Usage Results', '(move type, instances, usage %)'])
            for item in self.getTypeUsage():
                writer.writerow(item)

            writer.writerow(['Move Usage Results', '(move, instances, usage %)'])
            for item in self.getMoveUsage():
                writer.writerow(item)
        return

    def exportSpecialUsage(self):
        with open('./results/specialMoveUsage.csv', mode='w', newline='') as specialMoveUsageFile:
            writer = csv.writer(specialMoveUsageFile, delimiter=',')
            writer.writerow(['Special Move Usage Results', '(move, instances, usage %)'])
            for item in self.getSpecialUsage():
                writer.writerow(item)
        return

    def exportPhysicalUsage(self):
        with open('./results/physicalMoveUsage.csv', mode='w', newline='') as physicalMoveUsageFile:
            writer = csv.writer(physicalMoveUsageFile, delimiter=',')
            writer.writerow(['Physical Move Usage Results', '(move, instances, usage %)'])
            for item in self.getPhysicalUsage():
                writer.writerow(item)
        return

    def exportStatusUsage(self):
        with open('./results/statusMoveUsage.csv', mode='w', newline='') as statusMoveUsageFile:
            writer = csv.writer(statusMoveUsageFile, delimiter=',')
            writer.writerow(['Status Move Usage Results', '(move, instances, usage %)'])
            for item in self.getStatusUsage():
                writer.writerow(item)
        return