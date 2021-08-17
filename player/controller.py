
from player.model import add_players, duplicate_search, save_player, \
    table_of_player, modification_of_player
from player.view import print_add_player, print_find_player, \
    print_modif_player, print_display_player_list, \
    print_display_player_nb, print_new_player_register
from view import print_exicting_player, print_modif_ok


def menu_add_player():
    ''' management menu addition players '''

    player = print_add_player()
    add_player = add_players(player)
    resultat = duplicate_search(add_player)
    serialized_player = resultat.get("valided")
    existing = resultat.get("no_valided")
    if not serialized_player == []:
        save_player(serialized_player)
        print_new_player_register()
    if not existing == []:
        print_exicting_player(existing)


def menu_modif_player():
    ''' allows you to search for the player to modify by name
        which returns a list of all the players with this name
        or by ID to directly select the player to modify '''

    resultat = print_find_player()
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
                        modif = print_modif_player(player)
                        modification_of_player(modif)
                        print_modif_ok()
                    else:
                        print_display_player_list(player)
        print_display_player_nb(len(nb_players), resultat)
        menu_modif_player()
    else:
        for player in players:
            for k, v in player.items():
                if v == resultat:
                    modif = print_modif_player(player)
                    modification_of_player(modif)
                    print_modif_ok()
