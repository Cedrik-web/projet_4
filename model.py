from tinydb import TinyDB, Query
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
    serialized_player = []
    for i in players:
        print(i)
        new_player = i
        player = Player(
            name=new_player.get('name'),
            first_name=new_player.get('first_name'),
            birth_date=new_player.get('birth_date'),
            sex=new_player.get('sex'),
            ranking=new_player.get('ranking'),
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
    db = TinyDB("db.json")
    players_table = db.table("players")
    players_table.insert_multiple(serialized_player)


def table_of_player():
    db = TinyDB("db.json")
    players_table = db.table('players').all()
    return players_table

def modification_of_player(modif):
    players = table_of_player()
    db = TinyDB("db.json").table('players')
    for player in players:
        if player.get('pk') == modif.get('pk'):
            player_doc_id = player.doc_id
            db.upsert(Document(modif, doc_id=player_doc_id))
            print("modification effectué")

def clean_input(data):
    tiny = data.lower()
    without_space = tiny.replace(' ', '-')
    char = "!#$%&*()"
    for i in char:
        without_space = without_space.replace(i, '')
    accent = "éèêë"
    for a in accent:
        without_space = without_space.replace(a, "e")
    accent_a = without_space.replace("à", "a")
    accent_u = accent_a.replace("ù", "u")
    new_data = accent_u
    return new_data



    #
class Tournament:
    def __init__(self):
        pass


#
class Match:
    def __init__(self):
        pass

