import sys

from model import modif_classement, selection_tournament
from player.controller import menu_add_player, menu_modif_player
from player.model import stat_classement
from tournament.controller import play_tournament, menu_tournament
from view import print_accueil, print_menu_stat, print_pass_validation, \
    print_classement_alphabet, print_space, print_choice_input_menu, \
    print_classement_of_tournament, print_list_tournaments, \
    print_tournament_time, print_tournament_resultat, \
    print_list_match_by_tournament,  print_list_resultat_match, \
    print_tri_player_of_tournament_rank, print_menu_existing, \
    print_tri_player_of_tournament_alphabet, print_classement, \
    print_list_of_tournaments, print_resultat_match, \
    print_error_enter_int, print_classement_player_of_tournament


def menu():
    ''' menu distribution function '''

    resultat = print_accueil()
    try:
        resultat = print_choice_input_menu(resultat)
    except ValueError:
        print_error_enter_int()
        menu()
    if resultat == 1:  # adding player
        menu_add_player()
        menu()
    if resultat == 2:  # player modification
        menu_modif_player()
        menu()
    if resultat == 3:  # creation of a tournament
        tour = 1
        play_tournament(tour)
        menu()
    if resultat == 4:  # to see all tournaments
        try:           # create and play tournaments not finalized
            menu_tournament()
            menu()
        except ValueError:
            menu()
    if resultat == 5:  # see the ranking
        retour_list = stat_classement()
        player_tri_ranking = retour_list[0]
        print_classement(player_tri_ranking)
        menu()
    if resultat == 6:  # allows the modification of rank points per players
        modif_classement()
        menu()
    if resultat == 7:  # access to the report management menu
        menu_rapports()
        menu()
    if resultat == 8:  # to exit the program
        sys.exit()
    else:
        print_error_enter_int()
        menu()


def menu_rapports():
    ''' application report management menu '''

    retour_list = stat_classement()
    player_tri_ranking = retour_list[0]
    player_tri_alphabet = retour_list[1]
    tournoi = retour_list[2]
    print_classement(player_tri_ranking)
    choice = int(print_menu_stat())
    if choice == 1:  # tri players by ranking
        print_classement(player_tri_ranking)
        print_pass_validation()
        menu()
    elif choice == 2:  # tri players by aphabetical order
        print_classement_alphabet(player_tri_alphabet)
        print_pass_validation()
        menu()
    elif choice == 3:  # player list of a tournament by ranking
        tournament = selection_tournament()
        players = tournament.get("players")
        player_list = []
        for i in players:
            for k, v in i.items():
                player_list.append(v)
        tri_player_rank = sorted(player_list, key=lambda k: k["ranking"],
                                 reverse=True)
        print_classement_of_tournament()
        p = 0
        for i in tri_player_rank:
            p += 1
            print_tri_player_of_tournament_rank(i, p)
        print_pass_validation()
    elif choice == 4:  # player list of a tournament by alphabetical order
        tournament = selection_tournament()
        players = tournament.get("players")
        player_list = []
        for i in players:
            for k, v in i.items():
                player_list.append(v)
        tri_player_alphabet = sorted(player_list, key=lambda k: k["pk"])
        print_classement_player_of_tournament()
        for i in tri_player_alphabet:
            print_tri_player_of_tournament_alphabet(i)
        print_pass_validation()
    elif choice == 5:  # tournament list
        print_list_of_tournaments(tournoi)
        print_pass_validation()
    elif choice == 6:  # all the round of a tournament
        tournament = selection_tournament()
        resultat = tournament.get("resultat")
        print_list_tournaments(tournament)
        t = 0
        for round in resultat:
            t += 1
            print_tournament_time(t)
            for k, v in round.items():
                list_tour = v
                match = []
                resultat = []
                for k, v in list_tour.items():
                    match.append(k)
                    resultat.append(v)
                print_tournament_resultat(resultat)
            print_space()
        print_pass_validation()
    elif choice == 7:  # all the matches of a tournaments
        tournament = selection_tournament()
        resultat = tournament.get("resultat")
        print_list_match_by_tournament(tournament)
        t = 0
        for round in resultat:
            t += 1
            print_resultat_match(t)
            for k, v in round.items():
                list_tour = v
                match = []
                resultat = []
                for k, v in list_tour.items():
                    match.append(k)
                    resultat.append(v)
                del match[0]
                del match[-1]
                del resultat[0]
                del resultat[-1]
                for i, j in zip(match, resultat):
                    print_list_resultat_match(i, j)
            print_space()
        print_pass_validation()
    elif choice == 8:  # for exit
        print_space() * 50
    else:
        print_menu_existing()




