
from model import tournament_find, tournaments_recovery
from player.model import add_players_of_tournament
from settings import TURNS
from tournament.model import Match, start_tournament,\
    save_resultat_tournament,\
    nunber_turn, add_tournament, \
    gathers_tournament_dictionary, save_tournament
from tournament.view import print_elements_tournament,\
    print_add_genaral_remarks,\
    print_add_timer_control, print_error


def play_tournament(tour):
    ''' management menu for create a tournament and saving it '''

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
    list_matchs = Match.generation_first_round(
        Match(), players_of_tournament, TURNS)
    list_match = Match.print_list_matchs(Match(), list_matchs)
    start_tournament()
    resultat_total = Match.play_first_turn(Match(), list_match)
    save_resultat_tournament(serialized_tournament, resultat_total)
    nunber_turn(
        TURNS,
        players_of_tournament,
        resultat_total, serialized_tournament, tour)
    save_resultat_tournament(serialized_tournament, resultat_total)


def menu_tournament():
    ''' menu to retrieve the ID of the tournament register to start
        or finish '''

    reponse = tournament_find(TURNS)
    if reponse != "":
        retour = tournaments_recovery(reponse)
        players_of_tournament = retour[0]
        serialized_tournament = retour[1]
        turn = retour[2]
        if turn == 0:  # turn hos for value an integer which corresponds to the
            tour = 0   # number of round already made
            list_matchs = Match.generation_first_round(
                Match(), players_of_tournament, TURNS)
            list_match = Match.print_list_matchs(Match(), list_matchs)
            start_tournament()
            resultat_total = Match.play_first_turn(Match(), list_match)
            save_resultat_tournament(serialized_tournament, resultat_total)
            nunber_turn(TURNS,
                        players_of_tournament,
                        resultat_total, serialized_tournament, tour)
            save_resultat_tournament(serialized_tournament, resultat_total)
        elif turn == 1:
            tour = 1
            resultat_total = serialized_tournament.get("resultat")
            start_tournament()
            nunber_turn(TURNS,
                        players_of_tournament,
                        resultat_total, serialized_tournament, tour)
            save_resultat_tournament(serialized_tournament, resultat_total)
        else:
            tour = turn
            resultat_total = serialized_tournament.get("resultat")
            turns = TURNS - turn + 1
            start_tournament()
            nunber_turn(turns,
                        players_of_tournament,
                        resultat_total, serialized_tournament, tour)
            save_resultat_tournament(serialized_tournament, resultat_total)
    else:
        print_error()
