import sys

from view import print_accueil, print_add_player, print_find_player, print_modif_player, print_error_enter_int
from view import print_display_player_list, print_display_player_nb, print_modif_ok
from view import print_elements_tournament, print_elements_player, print_add_players_for_tournament
from view import print_save_players_for_tournament, print_add_newplayer_for_tournament
from view import print_list_player_find, print_player_find, print_error_id
from view import print_exicting_player, print_new_player_register, print_pass_validation
from view import print_add_genaral_remarks,print_add_timer_control
from view import print_add_players_for_tournament_new, print_classement
from view import print_modif_classement, print_menu_stat, print_classement_alphabet
from view import print_list_of_tournaments, print_menu_ajout_players_fot_tournament
from view import print_list_players_alphabet, print_add_player_impossible

from model import save_player, add_players, table_of_player, modification_of_player
from model import add_tournament, gathers_tournament_dictionary, save_tournament
from model import duplicate_search, Match, nunber_turn, save_resultat_tournament
from model import stat_classement, selection_tournament, start_tournament
from model import tournament_find, tournaments_recovery, control_already_selection

from settings import TURNS


def menu():
    ''' menu distribution function '''

    resultat = print_accueil()
    try:
        resultat = int(resultat)
    except:
        print_error_enter_int()
        menu()
    if resultat == 1: # adding player
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
    if resultat == 2: # player modification
        modif_menu()
    if resultat == 3: # creation of a tournament
        tour = 1
        elements = print_elements_tournament()
        tournament = add_tournament(elements)
        players = add_players_of_tournament(tournament)
        remarks = print_add_genaral_remarks()
        timer_control = print_add_timer_control()
        players_of_tournament = Match.match_generation(Match(), players)
        serialized_tournament = gathers_tournament_dictionary(
            tournament,
            players_of_tournament,
            remarks,
            timer_control
        )
        save_tournament(serialized_tournament)
        list_matchs = Match.generation_first_round(Match(), players_of_tournament, TURNS)
        list_match = Match.print_list_matchs(Match(), list_matchs)
        start_tournament()
        resultat_total = Match.play_first_turn(Match(), list_match)
        save_resultat_tournament(serialized_tournament, resultat_total)
        nunber_turn(TURNS, players_of_tournament, resultat_total, serialized_tournament, tour)
        save_resultat_tournament(serialized_tournament, resultat_total)
        menu()
    if resultat == 4: # to see all tournaments create and play tournaments not finalized
        try:
            reponse = tournament_find(TURNS)
            if reponse != "":
                retour = tournaments_recovery(reponse)
                players_of_tournament = retour[0]
                serialized_tournament = retour[1]
                turn = retour[2]
                if turn == 0:
                    tour = 0
                    list_matchs = Match.generation_first_round(Match(), players_of_tournament, TURNS)
                    list_match = Match.print_list_matchs(Match(), list_matchs)
                    start_tournament()
                    resultat_total = Match.play_first_turn(Match(), list_match)
                    save_resultat_tournament(serialized_tournament, resultat_total)
                    nunber_turn(TURNS, players_of_tournament, resultat_total, serialized_tournament, tour)
                    save_resultat_tournament(serialized_tournament, resultat_total)
                    menu()
                elif turn == 1:
                    tour = 1
                    resultat_total = serialized_tournament.get("resultat")
                    start_tournament()
                    nunber_turn(TURNS, players_of_tournament, resultat_total, serialized_tournament, tour)
                    save_resultat_tournament(serialized_tournament, resultat_total)
                    menu()
                else:
                    tour = turn
                    resultat_total = serialized_tournament.get("resultat")
                    turns = TURNS - turn + 1
                    start_tournament()
                    nunber_turn(turns, players_of_tournament, resultat_total, serialized_tournament, tour)
                    save_resultat_tournament(serialized_tournament, resultat_total)
                    menu()
            else:
                print("else")
                menu()
        except:
            menu()
    if resultat == 5: # see the ranking
        retour_list = stat_classement()
        player_tri_ranking = retour_list[0]
        print_classement(player_tri_ranking)
        menu()
    if resultat == 6: # allows the modification of rank points per players
        modif_classement()
        menu()
    if resultat == 7: # access to the report management menu
        retour_list = stat_classement()
        player_tri_ranking = retour_list[0]
        player_tri_alphabet = retour_list[1]
        tournoi = retour_list[2]
        print_classement(player_tri_ranking)
        choice = int(print_menu_stat())
        if choice == 1:
            print_classement(player_tri_ranking)
            print_pass_validation()
            menu()
        elif choice == 2:
            print_classement_alphabet(player_tri_alphabet)
            print_pass_validation()
            menu()
        elif choice == 3:
            tournament = selection_tournament()
            players = tournament.get("players")
            player_list =[]
            for v in players:
                for k, v in v.items():
                    player_list.append(v[0])
            tri_player_rank = sorted(player_list, key=lambda k: k["ranking"], reverse=True)
            print("\nclassement du tournoi :\n")
            p = 0
            for i in tri_player_rank:
                p += 1
                print("n°", p, i.get("pk"), "avec", i.get("ranking"), "point(s).")
            print_pass_validation()
            menu()
        elif choice == 4:
            tournament = selection_tournament()
            players = tournament.get("players")
            player_list = []
            for v in players:
                for k, v in v.items():
                    player_list.append(v[0])
            tri_player_alphabet = sorted(player_list, key=lambda k: k["pk"])
            print("\njoueur du tournoi :\n")
            for i in tri_player_alphabet:
                print(i.get("name"), i.get("first_name"), "avec", i.get("ranking"), "point(s).")
            print_pass_validation()
            menu()
        elif choice == 5:
            print_list_of_tournaments(tournoi)
            print_pass_validation()
            menu()
        elif choice == 6:
            tournament = selection_tournament()
            resultat = tournament.get("resultat")
            resultat = resultat[0]
            print("\nlistes des tours pour le tournoi ", tournament.get("pk"))
            print()
            t = 0
            for k in resultat:
                t += 1
                tour = "tour " + str(t)
                print(tour)
                list_tour = k.get(tour)
                for k, v in list_tour.items():
                    print("match : ", k)
                    print("         remporter par : ", v)
                print()
            print_pass_validation()
            menu()
        elif choice == 7:
            tournament = selection_tournament()
            resultat = tournament.get("resultat")
            resultat = resultat[0]
            print("\nlistes des matchs pour le tournoi", tournament.get("pk"))
            print()
            t = 0
            for k in resultat:
                t += 1
                tour = "tour " + str(t)
                list_tour = k.get(tour)
                m = 0
                for k, v in list_tour.items():
                    m += 1
                    print("match n°", m, ": ", k)
                    print("              remporter par : ", v)
            print_pass_validation()
            menu()
        elif choice == 8:
            print("\n" * 50)
            menu()
        else:
            print("ERREUR vous devez choisir un menu existant")
    if resultat == 8: # to exit the program
        sys.exit()
    else:
        print_error_enter_int()
        menu()


def modif_classement():
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
                        modif = print_modif_classement(player)
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
                    modif = print_modif_classement(player)
                    modification_of_player(modif)
                    print_modif_ok()
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
                        print("dict players", modif)
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
                    print("dict players", modif)
                    modification_of_player(modif)
                    print_modif_ok()
                    menu()


def add_players_of_tournament(tournament):
    """ function to add players to the tournament
    access to the database or register a new player """

    players = table_of_player()
    retour_list = stat_classement()
    player_tri_alphabet = retour_list[1]
    nombre_de_tours = tournament[0].get("nb_players")
    participants = []
    compteur = 0
    for i in range(int(nombre_de_tours)):
        compteur += 1
        choix = print_menu_ajout_players_fot_tournament()
        if choix == 1:
            no_selection = False
            while no_selection == False:
                print_list_players_alphabet(player_tri_alphabet)
                resultat = print_add_players_for_tournament()
                boucle = False
                while boucle == False:
                    for i in players:
                        if resultat == i.get("pk"):
                            no_selection = control_already_selection(participants, i)
                            if no_selection == True:
                                participants.append(i)
                                print_save_players_for_tournament(compteur, nombre_de_tours)
                                boucle = True
                                break
                            else:
                                print_add_players_for_tournament_new()
                                boucle = True
                                break
                    else:
                        print_error_id()
                        resultat = print_add_players_for_tournament()
                        boucle = False
        elif choix == 2:
            player = [print_elements_player()]
            add_player = add_players(player)
            player_valided = duplicate_search(add_player)
            seria = player_valided.get("valided")
            for s in seria:
                serialized_player = s
                if not serialized_player.get("pk") == None:
                    save_player([serialized_player])
                    print_new_player_register(serialized_player)
                    participants. append(serialized_player)
                    print_save_players_for_tournament(compteur, nombre_de_tours)
                    break
            ex = player_valided.get("no_valided")
            for i in ex:
                existing = i
                if not existing.get("pk") == None:
                    print_add_player_impossible(existing)
                    no_selection = control_already_selection(participants, i)
                    if no_selection == True:
                        participants.append(existing)
                        print_save_players_for_tournament(compteur, nombre_de_tours)
                        break
                    else:
                        print_add_players_for_tournament_new()
                        break
    return participants
