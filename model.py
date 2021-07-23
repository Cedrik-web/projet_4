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
    ''' naming of parameters and serialization of players '''

    serialized_player = []
    for i in players:
        print(i)
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


def gathers_tournament_dictionary(tournoi, players):
    for i in tournoi:
        tournament = i
    list_players = []
    nb = []
    for p in players:
        nb.append(p)
        player = {len(nb): p}
        list_players.append(player)
    tournament["players"] = list(list_players)
    return tournament


def add_tournament(tour):
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
        "nb_players": tournament.nb_players,
    }
    serialized_tournament.append(serialized)
    return serialized_tournament


#
class Match:
    def __init__(self):
        pass

