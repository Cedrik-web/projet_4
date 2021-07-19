from view import accueil, add_player, modif_player
from model import save_player, add_players, modification_of_player


def menu():
    resultat = int(accueil())
    if resultat == 1:
        player = add_player()
        serialized = add_players(player)
        save_player(serialized)
    if resultat == 2:
        modif_menu()
    if resultat == 3:
        pass
    if resultat == 4:
        pass
    if resultat == 5:
        pass
    if resultat == 6:
        pass
    else:
        print("erreur , vous devez choisir un menu existant .")
        pass

def modif_menu():
    resultat = modif_player()
    print(resultat)
    modification_of_player(resultat)

