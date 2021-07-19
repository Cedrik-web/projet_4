from tinydb import TinyDB


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
    players_table.truncate()
    players_table.insert_multiple(serialized_player)


def modification_of_player(resultat):
    db = TinyDB("db.json")
    players_table = db.table('players').all()
    print(players_table)

#
class Tournament:
    def __init__(self):
        pass


#
class Match:
    def __init__(self):
        pass

