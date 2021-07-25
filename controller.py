from view import print_accueil, print_add_player, print_find_player, print_modif_player, print_error_enter_int
from view import print_display_player_list, print_display_player_nb, print_modif_ok
from view import print_elements_tournament, print_elements_player, print_add_players_for_tournament
from view import print_save_players_for_tournament, print_add_newplayer_for_tournament
from view import print_list_player_find, print_player_find, print_error_id
from view import print_exicting_player, print_new_player_register
from view import print_add_genaral_remarks,print_add_timer_control

from model import save_player, add_players, table_of_player, modification_of_player
from model import add_tournament, gathers_tournament_dictionary, save_tournament
from model import duplicate_search

def menu():
    ''' menu distribution function '''

    resultat = print_accueil()
    try:
        resultat = int(resultat)
    except:
        print_error_enter_int()
        menu()
    if resultat == 1:
        player = print_add_player()
        add_player = add_players(player)
        resultat = duplicate_search(add_player)
        serialized_player = resultat.get("valided")
        existing = resultat.get("no_valided")
        if not serialized_player == []:
            save_player(serialized_player)
            print_new_player_register(serialized_player)
        if not existing == []:
            print_exicting_player(existing)
        menu()
    if resultat == 2:
        modif_menu()
    if resultat == 3:
        elements = print_elements_tournament()
        tournament = add_tournament(elements)
        players = add_players_of_tournament(tournament)
        remarks = print_add_genaral_remarks()
        timer_control = print_add_timer_control()
        serialized_tournament = gathers_tournament_dictionary(
            tournament,
            players,
            remarks,
            timer_control
        )
        save_tournament(serialized_tournament) 
    if resultat == 4:
        pass
    if resultat == 5:
        pass
    if resultat == 6:
        pass
    if resultat == 7:
        pass
    else:
        print_error_enter_int()
        menu()

def modif_menu():
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
                        menu()
                    else:
                        print_display_player_list(player)
        print_display_player_nb(len(nb_players), resultat)
        modif_menu()
    else:
        for player in players:
            for k, v in player.items():
                if v == resultat:
                    modif = print_modif_player(player)
                    modification_of_player(modif)
                    print_modif_ok()
                    menu()

def add_players_of_tournament(tournament):
    """ function to add players to the tournament
    access to the database or register a new player """

    for i in tournament:
        tournoi = i
    participants = []
    table_players = table_of_player()
    nb_str = tournoi.get("nb_players")
    nb_int = int(nb_str)
    for i in range(nb_int):
        player = []
        resultat = print_add_players_for_tournament()
        for i in table_players:
            if resultat == i.get("pk"):
                player.append(i)
                break
            elif resultat == i.get("name"):
                player.append(i)
        if len(player) == 1:
            participants.append(player)
            print_save_players_for_tournament()
        else:
            print_player_find(player)
            participant = []
            for i in player:
                print_list_player_find(i, resultat)
                participant.append(i)
            resultat = print_add_newplayer_for_tournament()
            if len(resultat) > 10:
                for i in participant:
                    if resultat == i.get("pk"):
                        participants.append(i)
                        break
                else:
                    print_error_id()
                    resultat = input()
                print_save_players_for_tournament()
            else:
                elements = []
                element = print_elements_player()
                elements.append(element)
                add_player = add_players(elements)
                resultat = duplicate_search(add_player)
                serialized_player = resultat.get("valided")
                existing = resultat.get("no_valided")
                if not serialized_player == []:
                    save_player(serialized_player)
                    print_new_player_register(serialized_player)
                if not existing == []:
                    print_exicting_player(existing)
                participants.append(serialized_player)
                print_save_players_for_tournament() 
    return participants



