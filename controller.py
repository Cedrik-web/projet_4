from view import accueil, add_player, find_player, modif_player
from model import save_player, add_players, table_of_player, modification_of_player


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

def modif_menu():
    resultat = find_player()
    players = table_of_player()
    nb = len(resultat)
    nb_players = []
    if nb < 10:
        for player in players:
            for k, v in player.items():
                if v == resultat:
                    nb_players.append(player)
        for player in players:
            for k, v in player.items():
                if v == resultat:
                    if len(nb_players) == 1:
                        modif = modif_player(player)
                        modification_of_player(modif)
                        menu()
                    else:
                        print(player.get('name'), player.get('first_name'))
                        print('son ID est :', player.get('pk'), "\n")
        print("\n il y a ", len(nb_players), " resultat pour la recherche : ", resultat)
        print("veuillez utiliser ID du joueur")
        modif_menu()
    else:
        for player in players:
            for k, v in player.items():
                if v == resultat:
                    modif = modif_player(player)
                    modification_of_player(modif)
                    menu()




