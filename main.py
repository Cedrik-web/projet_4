from model import Player


def new_player():
    print("entrer le nom ")
    Player.name = input()
    print("entrer le prénom")
    Player.first_name = input()
    print("entrer la date d'anniversaire")
    Player.birth_date = input()
    print("entrer le sex")
    Player.sex = input()
    print("entrer les points")
    Player.ranking = input()


new_player()


player = Player()

serialized_player = {
    'Roux' : player.name,
    '26/05/1978' : player.birth_date,
    'Jean' : player.first_name,
    'Homme' : player.sex,
    '230' : player.ranking,
}

