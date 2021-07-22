from view import accueil, add_player, find_player, modif_player, error_enter_int
from view import display_player_list, display_player_nb, modif_ok
from view import elements_tournament
from model import save_player, add_players, table_of_player, modification_of_player


def menu():
    ''' menu distribution function '''

    resultat = accueil()
    try:
        resultat = int(resultat)
    except:
        error_enter_int()
        menu()
    if resultat == 1:
        player = add_player()
        serialized = add_players(player)
        save_player(serialized)
        menu()
    if resultat == 2:
        modif_menu()
    if resultat == 3:
        elements_tournament()
    if resultat == 4:
        pass
    if resultat == 5:
        pass
    if resultat == 6:
        pass
    if resultat == 7:
        pass
    else:
        error_enter_int()
        menu()

def modif_menu():
    ''' allows you to search for the player to modify by name
        which returns a list of all the players with this name
        or by ID to directly select the player to modify '''

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
                        modif_ok()
                        menu()
                    else:
                        display_player_list(player)
        display_player_nb(len(nb_players), resultat)
        modif_menu()
    else:
        for player in players:
            for k, v in player.items():
                if v == resultat:
                    modif = modif_player(player)
                    modification_of_player(modif)
                    modif_ok()
                    menu()




