import readline
import sys
from datetime import datetime

from tinydb import TinyDB
from tinydb.table import Document

from settings import PLAYERS_OF_TOURNAMENT


# player model creation
class Player:

    def __init__(self, name, first_name, birth_date, sex=None, ranking=0):
        self.pk = name + "_" + first_name + "_" + birth_date[-4:]
        self.name = name
        self.first_name = first_name
        self.birth_date = birth_date
        self.sex = sex
        self.ranking = ranking


def add_players(players):
    ''' named parameters and serialization of players items '''

    serialized_player = []
    for i in players:
        new_player = i
        player = Player(
            name=new_player.get("name"),
            first_name=new_player.get("first_name"),
            birth_date=new_player.get("birth_date"),
            sex=new_player.get("sex"),
            ranking=new_player.get("ranking"),
        )
        serialized = {
            "pk": player.pk,
            "name": player.name,
            "first_name": player.first_name,
            "birth_date": player.birth_date,
            "sex": player.sex,
            "ranking": player.ranking,
        }
        serialized_player.append(serialized)
    return serialized_player


def save_player(serialized_player):
    ''' save players in the players table and save in the db.json file '''

    db = TinyDB("db.json")
    players_table = db.table("players")
    players_table.insert_multiple(serialized_player)


def save_tournament(serialized_tournament):
    ''' save tournament in the tournament table and save in the db.json file '''

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


def table_of_player():
    ''' allows you to retrieve the players table from the db.json file '''

    db = TinyDB("db.json")
    players_table = db.table("players").all()
    return players_table


def table_of_tournament():
    ''' allows you to retrieve the tournament table from the db.json file '''

    db = TinyDB("db.json")
    tournament_table = db.table("tournament").all()
    return tournament_table


def modification_of_player(modif):
    ''' allows you to save changes to a player on db.json file '''

    players = table_of_player()
    db = TinyDB("db.json").table("players")
    for player in players:
        if player.get("pk") == modif.get("pk"):
            player_doc_id = player.doc_id
            db.upsert(Document(modif, doc_id=player_doc_id))


def clean_input(data):
    ''' general function to protect the program from
        incorrect user input '''

    tiny = data.lower()
    text = tiny.replace(" ", "-")
    char = "!#$%&*()"
    for i in char:
        text = text.replace(i, "")
    accent = "éèêë"
    for a in accent:
        text = text.replace(a, "e")
    accent_a = text.replace("à", "a")
    accent_u = accent_a.replace("ù", "u")
    new_data = accent_u
    return new_data


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


def duplicate_search(player):
    '''check ij the ID is not already referenced in the database '''

    players = table_of_player()
    nb_players = []
    valided = []
    no_valided = []
    dict = {"valided": valided,
            "no_valided": no_valided,
            }
    if len(player) > 1:
        for p in player:
            for k, v in p.items():
                if k == "pk":
                    nb_players.append(v)
            nb_str = len(nb_players)
            nb_int = nb_str
            if nb_int == 1:
                for i in players:
                    if p.get("pk") == i.get("pk"):
                        no_valided.append(p)
                        break
                else:
                    valided.append(p)
            else:
                for i in players:
                    if p.get("pk") == i.get("pk"):
                        no_valided.append(p)
                        break
                else:
                    valided.append(p)
    else:
        try:
            for p in player:
                for i in players:
                    if p.get("pk") == i.get("pk"):
                        no_valided.append(p)
                        break
                else:
                    valided.append(p)
        except:
            for i in players:
                for j in player:
                    if j == i.get("pk"):
                        no_valided.append(j)
                        break
            else:
                valided.append(j)
    return dict


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

        tri = sorted(player_of_tournament, key=lambda k: k["ranking"], reverse=True)
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
            print("\nmatch n°", m, ":")
            for i in list:
                print(i.get("pk"))
        return list_match

    def play_first_turn(self, list_match):
        ''' play the first round of the tournament '''

        resultat_total = []
        resultat_tour1 = {}
        date_start = datetime.now()
        date = str(date_start)
        resultat_tour1.update({"debut round": date})
        print("\ndate et heure du début de round:", date)
        for i in list_match:
            joueur1 = i[0]
            joueur2 = i[1]
            match = joueur1.get("pk") + " / " + joueur2.get("pk")
            print("\n resultat pour le match :", match, "\n")
            print(" - tape 1 si", joueur1.get('pk'), "a gagner.")
            print(" - tape 2 si", joueur2.get('pk'), "a gagner.")
            print(" - si pat tapez 3")
            resultat = int(input("                                    : "))
            joueur1["meet"] = [joueur2.get("pk")]
            joueur2["meet"] = [joueur1.get("pk")]
            if resultat == 1:
                print("                                                         ", joueur1.get('pk'), " GAGNE !!\n")
                joueur1["point_tournament"] = self.winner
                joueur1["match_win"] += 1
                joueur2["point_tournamant"] = self.loser
                joueur2["match_lose"] += 1
                winner = joueur1.get("pk")
                resultat_tour1.update({match: winner})
            elif resultat == 2:
                print("                         ", joueur2, " GAGNE !!\n")
                joueur1["point_tournament"] = self.loser
                joueur1["match_lose"] += 1
                joueur2["point_tournament"] = self.winner
                joueur2["match_win"] += 1
                winner = joueur2.get("pk")
                resultat_tour1.update({match: winner})
            elif resultat == 3:
                print("                                     match nul \n")
                joueur1["point_tournament"] = self.draw
                joueur1["match_pat"] += 1
                joueur2["point_tournament"] = self.draw
                joueur2["match_pat"] += 1
                winner = "pat match nul"
                resultat_tour1.update({match: winner})
            else:
                print("ERREUR")
        print("---------------------------round : 1 terminé----------------------------\n")
        date_end = datetime.now()
        date = str(date_end)
        resultat_tour1.update({"fin round": date})
        print("date et heure de fin de round", date)
        resultat_total.append({"round 1": resultat_tour1})
        return resultat_total

    def generation_next_round(self, player_of_tournament):
        ''' generates match pairs from the 2nd round '''

        list_player = []
        list_match = []
        tri_rank = sorted(player_of_tournament, key=lambda k: k["ranking"], reverse=True)
        tri_tour = sorted(tri_rank, key=lambda k: k["point_tournament"], reverse=True)
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
            answers = Match.find_player_already_play(self, joueur1, joueur2, tri_tour, position2, list_player)
            player = answers[0]
            if player != joueur2:
                new_match = joueur1, player
                list_match.append(new_match)
            else:
                new_match = joueur1, joueur2
                list_match.append(new_match)
        return player_of_tournament, list_match

    def find_player_already_play(self, joueur1, joueur2, tri_tour, position, list_player):
        ''' check if the player has already been selected '''

        list_player.append(joueur1.get("pk"))
        t = -1
        new_joueur = joueur2
        while new_joueur.get("pk") in joueur1.get("meet"):
            try:
                position += 2
                new_joueur = tri_tour[position]
            except:
                t += 2
                new_joueur = tri_tour[t]
            while new_joueur.get("pk") in list_player:
                try:
                    position += 2
                    new_joueur = tri_tour[position]
                except:
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
        resultat_tour.update({"début round": date})
        print("\ndate et heure de debut de round:", date)
        for i in list_match:
            joueur1 = i[0]
            joueur2 = i[1]
            match = joueur1.get("pk") + " / " + joueur2.get("pk")
            print("\n resultat pour le match :", match, "\n")
            print(" - tape 1 si", joueur1.get('pk'), " a gagner.")
            print(" - tape 2 si", joueur2.get('pk'), " a gagner.")
            print(" - si pat tapez 3")
            resultat = int(input("                               : "))
            joueur1["meet"] += [joueur2.get("pk")]
            joueur2["meet"] += [joueur1.get("pk")]
            if resultat == 1:
                print("                                                         ", joueur1.get('pk'), " GAGNE !!\n")
                joueur1["point_tournament"] = joueur1.get("point_tournament") + self.winner
                joueur1["match_win"] += 1
                joueur2["point_tournament"] = joueur2.get("point_tournament") + self.loser
                joueur2["match_lose"] += 1
                winner = joueur1.get("pk")
                resultat_tour.update({match: winner})
            elif resultat == 2:
                print("                         ", joueur2, " GAGNE !!\n")
                joueur1["point_tournament"] = joueur1.get("point_tournament") + self.loser
                joueur1["match_lose"] += 1
                joueur2["point_tournament"] = joueur2.get("point_tournament") + self.winner
                joueur2["match_win"] += 1
                winner = joueur2.get("pk")
                resultat_tour.update({match: winner})
            elif resultat == 3:
                print("                                     match nul \n")
                joueur1["point_tournament"] = joueur1.get("point_tournament") + self.draw
                joueur1["match_pat"] += 1
                joueur2["point_tournament"] = joueur2.get("point_tournament") + self.draw
                joueur2["match_pat"] += 1
                winner = "pat match nul"
                resultat_tour.update({match: winner})
            else:
                print("ERREUR")
        print("---------------------------round : " + str(tour) + " terminé----------------------------\n")
        date_end = datetime.now()
        date = str(date_end)
        resultat_tour.update({"fin round": date})
        print(" date et heure de fin de round :", date)
        resultat_total.append({"round " + str(tour): resultat_tour})
        return resultat_total


def start_tournament():
    ''' control the start of tournaments '''

    print("\n")
    print("Pour commencer le round et activé le chrono,")
    reponse = input("appuyer sur ENTRER                            ou non pour sortir: ")
    if reponse == "non":
        sys.exit()
    else:
        pass


def nunber_turn(turns, players_of_tournament, resultat_total, serialized_tournament, tour):
    ''' function that controls the course of laps from the 2nd ( by a loop) '''

    turn = turns - 1
    tour = tour
    for i in range(turn):
        tour += 1
        retour2 = Match.generation_next_round(Match(), players_of_tournament)
        list_matchs = retour2[1]
        list_match = Match.print_list_matchs(Match(), list_matchs)
        start_tournament()
        resultat_tournament = Match.gestion_match(Match(), list_match, resultat_total, tour)
        save_resultat_tournament(serialized_tournament, resultat_tournament)
    return resultat_tournament


# class that supports text autocomplementation
class MyCompleter(object):  # Custom completer

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options
                                if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]
        # return match indexed by state
        try:
            return self.matches[state]
        except IndexError:
            return None


def activate():
    ''' manage autocomplementation '''

    players = table_of_player()
    text = []
    for i in players:
        text.append(i.get("pk"))
    completer = MyCompleter(text)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')


def stat_classement():
    ''' returns a classification by rank or alphabetical '''

    players = table_of_player()
    tournaments = table_of_tournament()
    tri_rank = sorted(players, key=lambda k: k["ranking"], reverse=True)
    tri_alphabet = sorted(players, key=lambda k: k["pk"])
    player_tri_ranking = []
    player_tri_alphabet = []
    for i in tri_rank:
        player_tri_ranking.append(i)
    for j in tri_alphabet:
        player_tri_alphabet.append(j)
    return player_tri_ranking, player_tri_alphabet, tournaments


def selection_tournament():
    ''' allows to select a tournament in the dictionary '''

    tournaments = table_of_tournament()
    liste_tournoi = []
    for i in tournaments:
        print("ID du tournoi :", i.get("pk"))
        liste_tournoi.append(i.get("pk"))
    print("\nchoisis ton tournoi par l'ID")
    choix = input()
    while not choix in liste_tournoi:
        print("ERREUR vous avez mal saisie l'ID, reconnencer")
        choix = input()
    else:
        for i in tournaments:
            if i.get("pk") == choix:
                tournament = i
                return tournament


def tournament_find(TURNS):
    ''' alows you to search among the tournaments which have ended
        which are in progress and those which have not started '''

    tournaments = table_of_tournament()
    match = []
    tour = []
    end = []
    no_start = []
    start = []
    print("\nrecherche des tournois créer et non finaliser.\n")
    for i in tournaments:
        tour.append(i.get("resultat"))
        if tour == [[]]:
            match.append(i.get("pk"))
            no_start.append(i)
            tour.clear()
        else:
            for t in tour:
                nb_turns = (len(t))
                if nb_turns == TURNS:
                    end.append(i)
                    tour.clear()
                else:
                    match.append(i.get("pk"))
                    start.append(i)
                    tour.clear()
    for i in end:
        print("tournoi fini :", "le", i.get("name"), "de", i.get("location"), "du", i.get("date"))
    print()
    for i in no_start:
        print("tournoi non commencer voici leurs ID :", i.get("pk"))
        print(" - ", i.get("pk"))
    for i in start:
        print("tournoi non finaliser voici leurs ID :")
        print(" - ", i.get("pk"))
    print()
    reponse = input("entre l'ID ou appuie entrer pour sortir de la selection: ")
    return reponse


def tournaments_recovery(answer):
    ''' mamage the resumption of tournament and what turn it was '''

    tournaments = table_of_tournament()
    players = []
    tournament = []
    turn = 0
    for i in tournaments:
        if i.get("pk") == answer:
            serialized_tournament = i
            players_brut = i.get("players")
            tournament.append(i.get("resultat"))
            for p in players_brut:
                for k, v in p.items():
                    players.append(v)
    if tournament == [[]]:
        return players, serialized_tournament, turn
    else:
        for r in tournament:
            nb = len(r)
            if nb == 1:
                turn = 1
            elif nb == 2:
                turn = 2
            elif nb == 3:
                turn = 3
    return players, serialized_tournament, turn


def control_already_selection(list_participant, player):
    ''' checks if the player is in the list and answers true or false '''

    for i in list_participant:
        if player.get("pk") == i.get("pk"):
            valided = False
            return valided
    else:
        valided =True
        return valided

