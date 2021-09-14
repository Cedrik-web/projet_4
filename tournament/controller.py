from datetime import datetime

from model import MyCompleter
from player.model import Player, MethodePlayer
from settings import TURNS, PLAYERS_OF_TOURNAMENT
from tournament.model import Match, Tournament, PlayTournament
from tournament.view import ViewTournament, ViewMenuTournament, ViewMatch, ViewShare


#  the tournament menu class manages the creation or search of an existing tournament to the management
#  of rounds and matches then saving.
class MenuTournament:

    def menu_tournament(self):
        """menu to retrieve the ID of the tournament register to start
            or finish """

        tournaments = Tournament().table_of_tournament()
        viewmenutournament = ViewMenuTournament()
        reponse = MethodeTournament().tournament_find(TURNS, tournaments)  # return ID input
        players_of_tournament = []
        if reponse != "":
            playtournament = PlayTournament()
            tournament = playtournament.tournaments_recovery(reponse, tournaments)
            #   returns the selected tournament
            turn = playtournament.tournaments_recovery2(tournament)
            #   return to which turn was the tournament
            for i in tournament:
                list_players = i.get("players")
                for p in list_players:
                    players_of_tournament.append(p)
                    #   returns a dictionary list of participating players
            serialized_tournament = tournament[0]
            #   transform the list into a dictionary by removing them []
            if turn is None:
                tour = 1
                viewmenutournament.print_starting_round(tour)
                #   ask if we want to start the round
                self.menu_manage_first_round(players_of_tournament, serialized_tournament)
            elif turn == 0:  # turn has for value an integer which corresponds to the state of the tournament saved
                tour = 1
                viewmenutournament.print_starting_round(tour)
                #   ask if we want to start the round
                self.menu_manage_first_round(players_of_tournament, serialized_tournament)
            elif turn == 1:
                tour = 1
                tours = tour + 1
                viewmenutournament.print_starting_round(tours)
                playtournament.menu_manage_other_round(serialized_tournament, players_of_tournament, tour)
            else:
                tour = turn
                tours = tour + 1
                viewmenutournament.print_starting_round(tours)
                playtournament.menu_manage_other_round(serialized_tournament, players_of_tournament, tour)
        else:
            ViewShare().print_error()

    def play_tournament(self, tour):
        # management menu for create a tournament and saving it

        methodetournament = MethodeTournament()
        viewtournament = ViewTournament()
        tournament = Tournament()
        player = Player.table_of_player()
        list_tournament = tournament.table_of_tournament()
        elements = methodetournament.element_of_tournament(player)
        serialized_tournament = tournament.add_tournament(elements)
        players = serialized_tournament.get("players")
        players_of_tournament = Match().match_generation(players)
        reponse = PlayTournament.control_already_selection(list_tournament, serialized_tournament)
        if not reponse:
            viewtournament.print_tournament_existing()
            from controller import MainMenu
            MainMenu().menu()
        MenuTournament().menu_manage_save_tournament(serialized_tournament, players_of_tournament, tour)

    def menu_manage_first_round(self, players_of_tournament, serialized_tournament):
        # manage the first round

        match = Match()
        tournament = Tournament()
        tour = 1
        playtournament = PlayTournament()
        list_matchs = match.generation_first_round(players_of_tournament)
        #   returns the list of matches of the first round
        list_match = MethodeMatch().display_list_matchs(list_matchs, tour)
        #   displays the list of matches in console
        MethodeTournament().start_tournament()
        #   requests the start of the lap as well as the start of the stopwatch
        resultat_total = MethodeMatch().play_turn(list_match, resultat_total={}, tour=1)
        #   play the round, and return a list of the results of that round add to the tournament result
        tournament.save_resultat_tournament(serialized_tournament, resultat_total)
        #   save tournament progress
        playtournament.nunber_turn(TURNS, players_of_tournament, resultat_total, serialized_tournament, tour=1)
        tournament.save_resultat_tournament(serialized_tournament, resultat_total)
        #   save tournament progress

    def menu_manage_save_tournament(self, serialized_tournament, players_of_tournament, tour):
        """manage the save elements of tournament"""

        match = Match()
        tournament = Tournament()
        resultat_total = {}
        methodematch = MethodeMatch()
        playtournament = PlayTournament()
        tournament.save_tournament(serialized_tournament)
        list_matchs = match.generation_first_round(players_of_tournament)
        list_match = methodematch.display_list_matchs(list_matchs, tour)
        MethodeTournament().start_tournament()
        resultat_total = methodematch.play_turn(list_match, resultat_total, tour)
        tournament.save_resultat_tournament(serialized_tournament, resultat_total)
        playtournament.nunber_turn(TURNS, players_of_tournament, resultat_total, serialized_tournament, tour)
        tournament.save_resultat_tournament(serialized_tournament, resultat_total)


# set method used by the tournament class
class MethodeTournament:

    def add_players_of_tournament(self, players):
        """ function to add players to the tournament
        access to the database or register a new player """

        viewtournament = ViewTournament()
        retour_list = MethodePlayer().stat_classement()
        player_tri_alphabet = retour_list[1]
        nombre_de_tours = PLAYERS_OF_TOURNAMENT
        participants = []
        save_player = []
        compteur = 0
        for i in range(int(nombre_de_tours)):  # add all tournament players
            compteur += 1
            boucle = False
            while not boucle:
                choix = self.ask_which_player_of_tournament()
                if choix == 1:  # display player list by alphabetical order
                    try:
                        if len(player_tri_alphabet) != 0:
                            viewtournament.print_list_players_alphabet(player_tri_alphabet)
                            boucle = self.control_add_the_existing_player(participants, players, compteur)
                    except ValueError:
                        viewtournament.print_not_list_player_existing()
                        self.create_and_add_new_player_of_tournament(participants, save_player, compteur)
                        boucle = True
                elif choix == 2:  # create a new player and add player them to the tournament
                    self.create_and_add_new_player_of_tournament(participants, save_player, compteur)
                    boucle = True
        return participants, save_player

    def add_timer_control(self):
        # control display and good feedback from the input

        resultat = ViewTournament().print_add_timer_control()
        timer_control = []
        if int(resultat) == 1:
            timer_control.append("bullet")
        elif int(resultat) == 2:
            timer_control.append("blitz")
        elif int(resultat) == 3:
            timer_control.append("coup rapide")
        else:
            ViewTournament().print_error_enter_selection()
            self.add_timer_control()
        return timer_control

    def element_of_tournament(self, player):
        # control display and good feedback from the input

        viewtournament = ViewTournament()
        retour = viewtournament.print_elements_tournament()
        viewtournament.print_date_of_tournament()
        date = self.element_date_controller()
        # add players of tournament
        player_recovery = self.add_players_of_tournament(player)
        players = player_recovery[0]  # list player of tournament
        save_player = player_recovery[1]  # player create for save
        Player.save_player(save_player)
        remarks = viewtournament.print_add_genaral_remarks()
        timer_control = self.add_timer_control()
        elements = {
            "name": retour[0],
            "location": retour[1],
            "date": date,
            "players": players,
            "remarks": remarks,
            "timer_control": timer_control,
        }
        return elements

    def element_date_controller(self):
        ''' control the input console for the birth date of the player '''

        methodecontrol = MethodeControl()
        day = methodecontrol.control_enter_by_while("jour", 31)
        month = methodecontrol.control_enter_by_while("mois", 12)
        year = methodecontrol.control_enter_by_while("année", 1000)
        day_str = str(day)
        month_str = str(month)
        if len(month_str) == 1:
            str_month = "0" + month_str
        else:
            str_month = str(month)
        if len(day_str) == 1:
            str_day = "0" + day_str
        else:
            str_day = str(day)
        birth_date = str_day + "/" + str_month + "/" + str(year)
        return birth_date

    def ask_which_player_of_tournament(self):
        # control display and good feedback from the input

        ViewTournament().print_menu_ajout_players_for_tournament()
        choice = MethodeControl().control_enter_by_while(2, 102)
        return choice

    def control_add_the_existing_player(self, participants, players, compteur):
        # check if the entry corresponds to an existing player

        MyCompleter.activate(players)
        viewtournament = ViewTournament()
        resultat = viewtournament.print_add_players_for_tournament()
        for i in players:  # control if the player is not already recording
            if resultat == i.get("pk"):
                playtournament = PlayTournament()
                no_selection = playtournament.control_already_selection(participants, i)
                if no_selection:  # instantiate the player to the tournament
                    player = playtournament.add_players_tournament(i)
                    participants.append(player)
                    viewtournament.print_save_players_for_tournament(compteur, PLAYERS_OF_TOURNAMENT)
                    return True
                elif no_selection is None:  # instantiate the player to the tournament
                    player = playtournament.add_players_tournament(i)
                    participants.append(player)
                    viewtournament.print_save_players_for_tournament(compteur, PLAYERS_OF_TOURNAMENT)
                    return True
                else:
                    viewtournament.print_add_players_for_tournament_inpossible()
                    viewtournament.print_continue()
                    return False
        else:
            viewtournament.print_error_id_tournament()
            return False

    def create_and_add_new_player_of_tournament(self, participants, save_player, compteur):
        # to create and add a new player in the tournament

        viewtournament = ViewTournament()
        new_player = self.elements_player()
        add_player = Player(**new_player).add_players(new_player)
        player_valided = PlayTournament().duplicate_search_player(add_player)
        seria = player_valided.get("valided")
        for s in seria:  # check if the player already exists
            serialized_player = s
            if not serialized_player.get("pk") is None:
                save_player.append(serialized_player)
                from player.view import ViewPlayer
                ViewPlayer().print_new_player_register()
                participants.append(serialized_player)
                viewtournament.print_save_players_for_tournament(compteur, PLAYERS_OF_TOURNAMENT)
                break
        ex = player_valided.get("no_valided")
        for i in ex:
            existing = i
            if not existing.get("pk") is None:
                viewtournament.print_add_player_impossible(existing)
                no_selection = PlayTournament().control_already_selection(participants, i)
                if no_selection:
                    participants.append(existing)
                    viewtournament.print_save_players_for_tournament(compteur, PLAYERS_OF_TOURNAMENT)
                    break
                else:
                    viewtournament.print_add_players_for_tournament_inpossible()
                    viewtournament.print_continue()
                    break

    def control_sex_player(self):
        # control display and good feedback from the input

        viewtournament = ViewTournament()
        while True:
            try:
                sex = int(viewtournament.print_sex_control())
                if sex == 1:
                    sex = "homme"
                    return str(sex)
                elif sex == 2:
                    sex = "femme"
                    return str(sex)
                else:
                    viewtournament.print_error_number_sex()
                    del sex
                    self.control_sex_player()
            except ValueError:
                viewtournament.print_error_number_sex()

    def control_ranking_player(self):
        # returns a list to view

        viewtournament = ViewTournament()
        viewtournament.print_ranking_player()
        ranking = 0
        while ranking != int:
            try:
                nb = viewtournament.print_ranking_player_input()
                ranking += nb
                break
            except ValueError:
                viewtournament.print_ranking_player_error_enter()
        viewtournament.print_ranking_player_view(ranking)
        return ranking

    def elements_player(self):
        # control display and good feedback from the input

        viewtournament = ViewTournament()
        elements = []
        retour = viewtournament.print_first_elements_player()
        elements.append(retour[0])
        elements.append(retour[1])
        elements.append(self.element_date_controller())
        elements.append(self.control_sex_player())
        viewtournament.print_first_recap_elements_player(elements)
        elements.append(self.control_ranking_player())
        element = {
            "name": elements[0],
            "first_name": elements[1],
            "birth_date": elements[2],
            "sex": elements[3],
            "ranking": elements[4],
        }
        return element

    def start_tournament(self):
        # control the start of tournaments

        reponse = ViewTournament().print_start_tournament()
        if reponse == "non":
            from controller import MainMenu
            MainMenu().menu()
        else:
            pass

    def tournament_find(self, TURNS, tournaments):
        """alows you to search among the tournaments which have ended
            which are in progress and those which have not started"""

        viewtournament = ViewTournament()
        match = []
        tour = []
        end = []
        no_start = []
        start = []
        viewtournament.print_find_tournament()
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
            viewtournament.print_tournament_finished(i)
        viewtournament.print_space()
        for i in no_start:
            viewtournament.print_tournament_not_start(i)
        for i in start:
            viewtournament.print_tournament_start(i)
        viewtournament.print_space()
        reponse = viewtournament.print_input_selection_tournament()
        return reponse


# set method used by the match class
class MethodeMatch:

    def display_list_matchs(self, list_match, tour):
        # show match list request

        viewmatch = ViewMatch()
        viewmatch.print_view_round()
        m = 0
        for list in list_match:
            m += 1
            viewmatch.print_view_match_possition(m)
            for i in list:
                viewmatch.print_view_match(i)
        return list_match

    def play_turn(self, list_match, resultat_total, tour):
        # play round of the tournament

        viewmatch = ViewMatch()
        matchs = Match()
        resultat_tour = {}
        date_start = datetime.now()
        date = str(date_start)
        resultat_tour.update({"debut round": date})
        #   put in the dictionary the date and time of departure of the tour
        viewmatch.print_start_chrono(tour, date)
        for i in list_match:
            joueur1 = i[0]
            joueur2 = i[1]
            match = joueur1.get("pk") + " / " + joueur2.get("pk")
            resultat = MethodeControl().control_choice_resultat_match(match, joueur1, joueur2)
            #   control the manager input of an int between 1 and 3
            #   add to the player dictionary in the key meet his opponent
            if resultat == 1:  # for player1 win
                viewmatch.print_player_winner(joueur1)
                resultat_tour = matchs.distribution_of_points_and_resultat(joueur1, joueur2, match, resultat_tour)
                #   retrieves the result and distributes the points according to the results of the turn
            elif resultat == 2:  # for player 2 win
                viewmatch.print_player_winner(joueur2)
                resultat_tour = matchs.distribution_of_points_and_resultat(joueur2, joueur1, match, resultat_tour)
                #   retrieves the result and distributes the points according to the results of the turn
            elif resultat == 3:  # for pat
                viewmatch.print_player_pat()
                resultat_tour = matchs.distribution_of_points_and_resultat_pat(joueur1, joueur2, match, resultat_tour)
                #   retrieves the result and distributes the points according to the results of the turn
        viewmatch.print_ending_round(tour)
        date_end = datetime.now()
        date = str(date_end)
        resultat_tour.update({"fin round": date})
        #   records in the result dictionary the date and time of the tournament
        resultat_total.update({"round " + str(tour): resultat_tour})
        #   update of the tournament result dictionary with the result of the round
        viewmatch.print_ending_chrono(tour, date)
        return resultat_total


class MethodeControl:

    def control_choice_resultat_match(self, match, joueur1, joueur2):
        # control that return on the match result is indeed an int between 1 and 3

        while True:
            try:
                while True:
                    answer = ViewMatch().print_menu_match_tournament(match, joueur1, joueur2)
                    if 0 < answer < 4:
                        return answer
                    else:
                        ViewTournament().print_error_enter_selection()
            except ValueError:
                ViewTournament().print_control_wrong_enter()

    def control_enter_by_while(self, data, data2):
        # check that the entry is indeed one of the expected

        viewtournament = ViewTournament()
        if 0 < data2 < 100:
            while True:
                try:
                    while True:
                        answer = viewtournament.print_control_input(data)
                        if 0 < answer <= data2:
                            return answer
                        else:
                            viewtournament.print_control_wrong_number(data2)
                except ValueError:
                    viewtournament.print_control_wrong_enter()
        elif 101 < data2 < 103:
            while True:
                try:
                    while True:
                        answer = viewtournament.print_control_input_none_view()
                        if 0 < answer <= data2:
                            return answer
                        else:
                            viewtournament.print_control_wrong_number(data)
                except ValueError:
                    viewtournament.print_control_wrong_enter()
        elif data2 > 105:
            while True:
                try:
                    while True:
                        answer = viewtournament.print_control_input(data)
                        if 1930 < answer < 2150:
                            return answer
                        else:
                            viewtournament.print_error_enter_years()
                except ValueError:
                    viewtournament.print_control_wrong_enter()

    def unexpected_error(self):
        """catch an exception and throw it back to view"""

        ViewMatch().print_error_exception()
