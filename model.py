from collections import OrderedDict

from tinydb import TinyDB
from tinydb.table import Document


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
    db = TinyDB("db.json")
    tournament_table = db.table("tournament")
    tournament_table.insert(serialized_tournament)

def table_of_player():
    ''' allows you to retrieve the players table from the db.json file '''

    db = TinyDB("db.json")
    players_table = db.table("players").all()
    return players_table

def table_of_tournament():
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
        self.name = name
        self.location = location
        self.date = date
        self.turns = 4
        self.nb_players = 2


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
        "name": tournament.name,
        "location": tournament.location,
        "date": tournament.date,
        "turns": tournament.turns,
        "nb_players": tournament.nb_players
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
                    valided.append(i)
            else:
                for i in players:
                    for j in player:
                        if j == i.get("pk"):
                            no_valided.append(j)
                            break
                else:
                    valided.append(j)
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


#
class Match:
    def __init__(self):
        self.nb_players = 2
        self.winner = 1.0
        self.loser = 0.0
        self.draw = 0.5
        self.point = self.winner + self.loser + self.draw

    def match_generation(self, players, turns):
        nb_players = len(players)
        nb_match = int(nb_players / 2)
        player_of_tournament = []
        tour = 0
        for i in players:
            tour += 1
            i = i[0]
            point_tournament = 0
            match_win = 0
            match_lose = 0
            match_pat = 0
            pk = (i.get("name") + "_" + i.get("first_name"))
            serialized_players = {
                "pk": pk,
                "ranking": i.get("ranking"),
                "point_tournament": point_tournament,
                "match_win": match_win,
                "match_lose": match_lose,
                "match_pat": match_pat,
            }
            player_of_tournament.append(serialized_players)
        tri = sorted(player_of_tournament, key=lambda k: k["ranking"], reverse=True)
        list_match = []
        position1 = -1
        position2 = 2
        for i in range(nb_match):
            position1 += 1
            position2 += 1
            p1 = tri[position1]
            p2 = tri[position2]
            match = [p1 , p2]
            list_match.append(match)
        resultat_total = []
        resultat_tour1 = {}
        for i in list_match:
            joueur1 = i[0]
            joueur2 = i[1]
            match = joueur1.get("pk") + " / " + joueur2.get("pk")
            print("\n resultat pour le match :", match, "\n")
            print(" - tape 1 si", joueur1.get('pk'), "a gagner.")
            print(" - tape 2 si", joueur2.get('pk'), "a gagner.")
            print(" - si pat tapez 3")
            resultat = int(input("                                    : "))
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
        print("---------------------------tour : 1 terminé----------------------------\n")
        resultat_total.append({"tour 1": resultat_tour1})
        t = 1
        for i in range(turns - 1):
            t += 1
            get_tour = "tour " + str(t - 1)
            print(get_tour)
            tri_rank = sorted(player_of_tournament, key=lambda k: k["ranking"], reverse=True)
            tri_tour = sorted(tri_rank, key=lambda k: k["point_tournament"], reverse=True)
            resultat_tour = {}
            list_match2 = []
            position1 = -2
            position2 = -1
            out_list = resultat_total[0]
            control_name = out_list.get(get_tour)
            for k, v in control_name.items():
                print(k)
            for i in range(nb_match):
                position1 += 2
                position2 += 2
                joueur1 = tri_tour[position1]
                joueur2 = tri_tour[position2]
                control = joueur1.get("pk") + " / " + joueur2.get("pk")
                control2 = joueur2.get("pk") + " / " + joueur1.get("pk")
                tp = 1
                while k == control or control2:
                    tp += 1
                    print("match " + k + " et deja jouer")
                    other_player = tri_tour[tp]
                    print(other_player)
                    k = joueur1.get("pk") + " / " + other_player.get("pk")
                    print(k)
                else:
                    new_match = [joueur1, joueur2]
                    list_match2.append(new_match)
            for i in list_match2:
                joueur1 = i[0]
                joueur2 = i[1]
                match = joueur1.get("pk") + " / " + joueur2.get("pk")
                print("\n resultat pour le match :", match, "\n")
                print(" - tape 1 si", joueur1.get('pk'), " a gagner.")
                print(" - tape 2 si", joueur2.get('pk'), " a gagner.")
                print(" - si pat tapez 3")
                resultat = int(input("                               : "))
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
            print("---------------------------tour : " + str(t) + " terminé----------------------------\n")
            resultat_total.append({"tour " + str(t): resultat_tour})

players = [[{
    "name": "rougier",
    "first_name": "cedrik",
    "birth_date": "26/05/1978",
    "sex": "homme",
    "ranking": 523.0,
    }],
    [{
    "name": "dour",
    "first_name": "sabrina",
    "birth_date": "22/04/1994",
    "sex": "femme",
    "ranking": 253.0,
    }],
    [{
    "name": "lantiat",
    "first_name": "sebastien",
    "birth_date": "16/06/1986",
    "sex": "homme",
    "ranking": 25.0,
    }],
    [{
    "name": "rainbault",
    "first_name": "lilou",
    "birth_date": "10/07/2002",
    "sex": "femme",
    "ranking": 702.0,
    }],
    [{
    "name": "rougier",
    "first_name": "franck",
    "birth_date": "26/05/1978",
    "sex": "homme",
    "ranking": 53.0,
    }],
    [{
    "name": "dour",
    "first_name": "emmy",
    "birth_date": "22/04/1994",
    "sex": "femme",
    "ranking": 142.0,
    }],
    [{
    "name": "lantiat",
    "first_name": "steve",
    "birth_date": "16/06/1986",
    "sex": "homme",
    "ranking": 251.0,
    }],
    [{
    "name": "rainbault",
    "first_name": "stephanie",
    "birth_date": "10/07/2002",
    "sex": "femme",
    "ranking": 72.5,
    }]]
match = Match()
match.match_generation(players, 4)