from tournamentHandler import TournamentHandler
from tournamentStatistics import TournamentStatistics
from pokedex import Pokedex
import sys


def main():
    if len(sys.argv) == 2:
        tournamentFile = str(sys.argv[1])
    else:
        print("Error, file name not provided")
    pokedex = Pokedex()
    tournament = TournamentHandler(pokedex)
    tournament.insertTournament('./tournaments/' + tournamentFile)

    sqlGetLastTournamentId = """SELECT MAX(id) FROM tournament"""
    cur = pokedex.conn.cursor()
    cur.execute(sqlGetLastTournamentId)
    row = cur.fetchone()
    if row is not None:
        tournamentId = row[0]
    tournamentStatistics = TournamentStatistics(pokedex, tournamentId)
    tournamentStatistics.exportAllStats()
    pokedex.finished()


if __name__ == '__main__':
    main()
