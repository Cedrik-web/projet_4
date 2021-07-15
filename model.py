from tinydb import TinyDB


#
class Player:
    def __init__(self , name, first_name, birth_date, sex, ranking=0):
        self.name = name
        self.first_name = first_name
        self.birth_date = birth_date
        self.sex = sex
        self.ranking = ranking


def new_player():
    print("entrer le nom du joueur")
    name = input()
    print("entrer le prénom du joueur")
    first_name = input()
    print("entrer la date de naissance du joueur comme ceci ../../....")
    birth_date = input()
    print("entrer le sex du joueur")
    sex = input()
    print("entrer les points du joueur")
    ranking = input()
    player = Player(name=name, first_name=first_name, birth_date=birth_date, sex=sex, ranking=ranking)
    serialized_player = {
        "name" : player.name,
        "first_name" : player.first_name,
        "birth_date" : player.birth_date,
        "sex" : player.sex,
        "ranking" : player.ranking,
        }
    return serialized_player

def add_player():
    serialized_player = []
    serialized_player.append(new_player())
    print("voulez vous rajouter un autre joueur ?")
    reponse = input()
    while reponse == "oui":
        serialized_player.append(new_player())
        print("voulez vous rajouter un autre joueur ?")
        reponse = input()

    db = TinyDB("db.json")
    players_table = db.table("players")
    players_table.insert_multiple(serialized_player)


#
class Tournament:
    def __init__(self):
        pass


#
class Match:
    def __init__(self):
        pass

