
from player.model import table_of_player, modification_of_player, activate
from player.view import print_find_player, print_display_player_list, \
    print_display_player_nb
from tournament.model import table_of_tournament
from view import print_list_tournament, print_choice_tournament, \
    print_find_tournament, print_tournament_finished,  \
    print_tournament_not_start, print_tournament_start,\
    print_input_selection_tournament, \
    print_space, print_modif_classement, print_modif_ok, print_error_id


def selection_tournament():
    ''' allows to select a tournament in the dictionary '''

    tournaments = table_of_tournament()
    liste_tournoi = []
    for i in tournaments:
        print_list_tournament(i)
        liste_tournoi.append(i.get("pk"))
    choix = print_choice_tournament()
    while choix not in liste_tournoi:
        print_error_id()
        choix = print_choice_tournament()
    else:
        for i in tournaments:
            if i.get("pk") == choix:
                tournament = i
                return tournament


def tournament_find(TURNS):
    ''' alows you to search among the tournaments which have ended
        which are in progress and those which have not started '''

    tournaments = table_of_tournament()
    match = []
    tour = []
    end = []
    no_start = []
    start = []
    print_find_tournament()
    for i in tournaments:
        tour.append(i.get("resultat"))
        if tour == [[]]:
            match.append(i.get("pk"))
            no_start.append(i)
            tour.clear()
        else:
            for t in tour:
                nb_turns = (len(t))
                if nb_turns == TURNS:
                    end.append(i)
                    tour.clear()
                else:
                    match.append(i.get("pk"))
                    start.append(i)
                    tour.clear()
    for i in end:
        print_tournament_finished(i)
    print_space()
    for i in no_start:
        print_tournament_not_start(i)
    for i in start:
        print_tournament_start(i)
    print_space()
    reponse = print_input_selection_tournament()
    return reponse


def tournaments_recovery(answer):
    ''' manage the resumption of tournament and what turn it was '''

    tournaments = table_of_tournament()
    players = []
    tournament = []
    turn = 0
    serialized_tournament = []
    for i in tournaments:
        if i.get("pk") == answer:
            serialized_tournament.append(i)
            players_brut = i.get("players")
            tournament.append(i.get("resultat"))
            for p in players_brut:
                for k, v in p.items():
                    players.append(v)
    if tournament == [[]]:
        return players, serialized_tournament[0], turn
    else:
        for r in tournament:
            nb = len(r)
            if nb == 1:
                turn = 1
            elif nb == 2:
                turn = 2
            elif nb == 3:
                turn = 3
        return players, serialized_tournament[0], turn


def modif_classement():
    ''' allows you to search for the player to modify by name
        which returns a list of all the players with this name
        or by ID to directly select the player to modify '''

    players = table_of_player()
    activate(players)  # manage autocomplementation
    resultat = print_find_player()
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
                    else:
                        print_display_player_list(player)
        print_display_player_nb(len(nb_players), resultat)
    else:
        for player in players:
            for k, v in player.items():
                if v == resultat:
                    modif = print_modif_classement(player)
                    modification_of_player(modif)
                    print_modif_ok()
