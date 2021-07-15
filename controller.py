from view import accueil
from model import add_player


def menu():
    resultat = int(accueil())
    if resultat == 1:
        add_player()
    if resultat == 2:
        Player()
    if resultat == 3:
        Tournament()
    if resultat == 4:
        Player()
    if resultat == 5:
        Player()
    if resultat == 6:
        Match()
    else:
        print("erreur , vous devez choisir un menu existant .")
        menu()