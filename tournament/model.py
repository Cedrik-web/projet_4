
from datetime import datetime
import sys

from tinydb import TinyDB
from tinydb.table import Document

from settings import PLAYERS_OF_TOURNAMENT
from tournament.view import print_start_tournament, \
    print_start_chrono, print_menu_match_tournament, \
    print_player_winner, print_player_pat, print_error, \
    print_ending_first_round, print_ending_chrono, \
    print_ending_other_round, print_view_match_possition, print_view_match


def save_tournament(serialized_tournament):
    ''' save tournament in the tournament table
        and save in the db.json file '''

    db = TinyDB("db.json")
    tournament_table = db.table("tournament")
    tournament_table.insert(serialized_tournament)


def save_resultat_tournament(serialized_resultat, tournament):
    ''' saves the modification of a tournament, etc result ... '''

    tournaments = table_of_tournament()
    db = TinyDB("db.json").table("tournament")
    serialized_resultat.update({"resultat": tournament})
    for t in tournaments:
        if t.get("pk") == serialized_resultat.get("pk"):
            tournoi_doc_id = t.doc_id
            db.upsert(Document(serialized_resultat, doc_id=tournoi_doc_id))


def table_of_tournament():
    ''' allows you to retrieve the tournament table from the db.json file '''

    db = TinyDB("db.json")
    tournament_table = db.table("tournament").all()
    return tournament_table


#  creation of the tournament class and manage tournaments
class Tournament:

    def __init__(self, name, location, date):
        self.pk = name + "_" + location + "_" + date[-4:]
        self.name = name
        self.location = location
        self.date = date
        self.turns = PLAYERS_OF_TOURNAMENT / 2
        self.nb_players = PLAYERS_OF_TOURNAMENT
        self.resultat = []


def gathers_tournament_dictionary(tournoi, players, remarks, timer_control):
    ''' add players to tournament elements '''

    for i in tournoi:
        tournament = i
    list_players = []
    nb = []
    for p in players:
        nb.append(p)
        player = {len(nb): p}
        list_players.append(player)
    tournament["players"] = list(list_players)
    tournament["remarks"] = list(remarks)
    tournament["timer_control"] = list(timer_control)
    return tournament


def add_tournament(tour):
    ''' named parameter and serialization of tournament items '''

    serialized_tournament = []
    tournament = Tournament(
        name=tour.get("name"),
        location=tour.get("location"),
        date=tour.get("date"),
    )
    serialized = {
        "pk": tournament.pk,
        "name": tournament.name,
        "location": tournament.location,
        "date": tournament.date,
        "turns": tournament.turns,
        "nb_players": tournament.nb_players,
        "resultat": tournament.resultat,
    }
    serialized_tournament.append(serialized)
    return serialized_tournament


def start_tournament():
    ''' control the start of tournaments '''

    reponse = print_start_tournament()
    if reponse == "non":
        sys.exit()
    else:
        pass


def control_already_selection(list_participant, player):
    ''' checks if the player is in the list and answers true or false '''

    for i in list_participant:
        if player.get("pk") == i.get("pk"):
            valided = False
            return valided
    else:
        valided = True
        return valided


# Create class Match who initiates the characteristics to ask for the match
class Match:

    def __init__(self):
        self.nb_players = 2
        self.winner = 1.0
        self.loser = 0.0
        self.draw = 0.5
        self.point = self.winner + self.loser + self.draw

    def match_generation(self, players):
        ''' add players to the match and serialized them
            return the list of players '''

        player_of_tournament = []
        tour = 0
        for i in players:
            tour += 1
            player = i
            point_tournament = 0
            match_win = 0
            match_lose = 0
            match_pat = 0
            serialized_players = {
                "pk": player.get("pk"),
                "ranking": player.get("ranking"),
                "point_tournament": point_tournament,
                "meet": [],
                "match_win": match_win,
                "match_lose": match_lose,
                "match_pat": match_pat,
            }
            player_of_tournament.append(serialized_players)
        return player_of_tournament

    def generation_first_round(self, player_of_tournament, turns):
        ''' generate the first matches then award points and update status
            match by players '''

        tri = sorted(player_of_tournament, key=lambda k: k["ranking"],
                     reverse=True)
        nb_player = int(len(tri) / 2)
        list_player_a = tri[:nb_player]
        list_player_b = tri[nb_player:]
        list_match = []
        position = -1
        for i in range(turns):
            position += 1
            p1 = list_player_a[position]
            p2 = list_player_b[position]
            match = [p1, p2]
            list_match.append(match)
        return list_match

    def print_list_matchs(self, list_match):
        ''' show match list request '''

        m = 0
        for list in list_match:
            m += 1
            print_view_match_possition(m)
            for i in list:
                print_view_match(i)
        return list_match

    def play_first_turn(self, list_match):
        ''' play the first round of the tournament '''

        resultat_total = []
        resultat_tour1 = {}
        date_start = datetime.now()
        date = str(date_start)
        resultat_tour1.update({"debut round": date})
        print_start_chrono(date)
        for i in list_match:
            joueur1 = i[0]
            joueur2 = i[1]
            match = joueur1.get("pk") + " / " + joueur2.get("pk")
            resultat = print_menu_match_tournament(match, joueur1, joueur2)
            joueur1["meet"] = [joueur2.get("pk")]
            joueur2["meet"] = [joueur1.get("pk")]
            if resultat == 1:
                print_player_winner(joueur1)
                joueur1["point_tournament"] = self.winner
                joueur1["match_win"] += 1
                joueur2["point_tournamant"] = self.loser
                joueur2["match_lose"] += 1
                winner = joueur1.get("pk")
                resultat_tour1.update({match: winner})
            elif resultat == 2:
                print_player_winner(joueur2)
                joueur1["point_tournament"] = self.loser
                joueur1["match_lose"] += 1
                joueur2["point_tournament"] = self.winner
                joueur2["match_win"] += 1
                winner = joueur2.get("pk")
                resultat_tour1.update({match: winner})
            elif resultat == 3:
                print_player_pat()
                joueur1["point_tournament"] = self.draw
                joueur1["match_pat"] += 1
                joueur2["point_tournament"] = self.draw
                joueur2["match_pat"] += 1
                winner = "pat match nul"
                resultat_tour1.update({match: winner})
            else:
                print_error()
        print_ending_first_round()
        date_end = datetime.now()
        date = str(date_end)
        resultat_tour1.update({"fin round": date})
        print_ending_chrono(date)
        resultat_total.append({"round 1": resultat_tour1})
        return resultat_total

    def generation_next_round(self, player_of_tournament):
        ''' generates match pairs from the 2nd round '''

        list_player = []
        list_match = []
        tri_rank = sorted(player_of_tournament, key=lambda k: k["ranking"],
                          reverse=True)
        tri_tour = sorted(tri_rank, key=lambda k: k["point_tournament"],
                          reverse=True)
        position1 = -2
        position2 = -1
        t = 0
        for i in range(4):
            ''' genere les matchs '''
            t += 1
            position1 += 2
            position2 += 2
            joueur1 = tri_tour[position1]
            joueur2 = tri_tour[position2]
            answers = Match.find_player_already_play(self,
                                                     joueur1,
                                                     joueur2,
                                                     tri_tour,
                                                     position2,
                                                     list_player)
            player = answers[0]
            if player != joueur2:
                new_match = joueur1, player
                list_match.append(new_match)
            else:
                new_match = joueur1, joueur2
                list_match.append(new_match)
        return player_of_tournament, list_match

    def find_player_already_play(self, joueur1,
                                 joueur2,
                                 tri_tour, position, list_player):
        ''' check if the player has already been selected '''

        list_player.append(joueur1.get("pk"))
        t = -1
        new_joueur = joueur2
        while new_joueur.get("pk") in joueur1.get("meet"):
            try:
                position += 2
                new_joueur = tri_tour[position]
            except IndexError:
                t += 2
                new_joueur = tri_tour[t]
            while new_joueur.get("pk") in list_player:
                try:
                    position += 2
                    new_joueur = tri_tour[position]
                except IndexError:
                    t += 2
                    new_joueur = tri_tour[t]
        new_player = new_joueur
        list_player.append(new_player.get("pk"))
        return new_player, list_player

    def gestion_match(self, list_match, resultat_total, tour):
        ''' play rounds matches from the 2nd round '''

        resultat_tour = {}
        resultat_total = resultat_total
        date_start = datetime.now()
        date = str(date_start)
        resultat_tour.update({"debut round": date})
        print_start_chrono(date)
        for i in list_match:
            joueur1 = i[0]
            joueur2 = i[1]
            match = joueur1.get("pk") + " / " + joueur2.get("pk")
            resultat = print_menu_match_tournament(match, joueur1, joueur2)
            joueur1["meet"] += [joueur2.get("pk")]
            joueur2["meet"] += [joueur1.get("pk")]
            if resultat == 1:
                print_player_winner(joueur1)
                joueur1["point_tournament"] = joueur1.get(
                    "point_tournament") + self.winner
                joueur1["match_win"] += 1
                joueur2["point_tournament"] = joueur2.get(
                    "point_tournament") + self.loser
                joueur2["match_lose"] += 1
                winner = joueur1.get("pk")
                resultat_tour.update({match: winner})
            elif resultat == 2:
                print_player_winner(joueur2)
                joueur1["point_tournament"] = joueur1.get(
                    "point_tournament") + self.loser
                joueur1["match_lose"] += 1
                joueur2["point_tournament"] = joueur2.get(
                    "point_tournament") + self.winner
                joueur2["match_win"] += 1
                winner = joueur2.get("pk")
                resultat_tour.update({match: winner})
            elif resultat == 3:
                print_player_pat()
                joueur1["point_tournament"] = joueur1.get(
                    "point_tournament") + self.draw
                joueur1["match_pat"] += 1
                joueur2["point_tournament"] = joueur2.get(
                    "point_tournament") + self.draw
                joueur2["match_pat"] += 1
                winner = "pat match nul"
                resultat_tour.update({match: winner})
            else:
                print_error()
        print_ending_other_round(tour)
        date_end = datetime.now()
        date = str(date_end)
        resultat_tour.update({"fin round": date})
        print_ending_chrono(date)
        resultat_total.append({"round " + str(tour): resultat_tour})
        return resultat_total


def nunber_turn(turns, players_of_tournament,
                resultat_total, serialized_tournament, tour):
    ''' function that controls the course of laps from the 2nd ( by a loop) '''

    turn = turns - 1
    tour = tour
    for i in range(turn):
        tour += 1
        retour2 = Match.generation_next_round(Match(), players_of_tournament)
        list_matchs = retour2[1]
        list_match = Match.print_list_matchs(Match(), list_matchs)
        start_tournament()
        resultat_tournament = Match.gestion_match(Match(),
                                                  list_match,
                                                  resultat_total, tour)
        save_resultat_tournament(serialized_tournament, resultat_tournament)
    return resultat_tournament
