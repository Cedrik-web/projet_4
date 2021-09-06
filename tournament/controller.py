
from datetime import datetime

from model import MyCompleter
from player.model import Player, MethodePlayer
from settings import TURNS, PLAYERS_OF_TOURNAMENT
from tournament.model import Match, Tournament, PlayTournament
from tournament.view import ViewTournament, ViewMenuTournament, ViewMatch, ViewShare


#  the tournament menu class manages the creation or search of an existing tournament to the management
#  of rounds and matches then saving.
class MenuTournament:

    def menu_manage_first_round(self, players_of_tournament, serialized_tournament):
        '''manage the first round'''

        list_matchs = Match.generation_first_round(Match(), players_of_tournament)
        list_match = MethodeMatch.display_list_matchs(MethodeMatch(), list_matchs)
        MethodeTournament.start_tournament(MethodeTournament)
        resultat_total = MethodeMatch.play_first_turn(MethodeMatch(), list_match)
        Tournament.save_resultat_tournament(Tournament, serialized_tournament, resultat_total)
        PlayTournament.nunber_turn(PlayTournament, TURNS, players_of_tournament, resultat_total,
                                   serialized_tournament, tour=1)
        Tournament.save_resultat_tournament(Tournament, serialized_tournament, resultat_total)

    def menu_manage_save_tournament(self, serialized_tournament, players_of_tournament, tour):
        '''manage the save elements of tournament'''

        Tournament.save_tournament(Tournament, serialized_tournament)
        list_matchs = Match.generation_first_round(Match(), players_of_tournament)
        list_match = MethodeMatch.display_list_matchs(MethodeMatch(), list_matchs)
        MethodeTournament.start_tournament(MethodeTournament)
        resultat_total = MethodeMatch.play_first_turn(MethodeMatch(), list_match)
        Tournament.save_resultat_tournament(Tournament, serialized_tournament, resultat_total)
        PlayTournament.nunber_turn(PlayTournament, TURNS, players_of_tournament, resultat_total,
                                   serialized_tournament, tour)
        Tournament.save_resultat_tournament(Tournament, serialized_tournament, resultat_total)

    def menu_tournament(self):
        ''' menu to retrieve the ID of the tournament register to start
            or finish '''

        tournaments = Tournament.table_of_tournament(Tournament)
        reponse = MethodeTournament.tournament_find(MethodeTournament, TURNS, tournaments)  # return ID input
        if reponse != "":
            retour = PlayTournament.tournaments_recovery(PlayTournament, reponse, tournaments)
            players_of_tournament = retour[0]
            serialized_tournament = retour[1]
            turn = retour[2]
            if turn == 0:  # turn has for value an integer which corresponds to the
                tour = 0
                ViewMenuTournament.print_starting_round(ViewMenuTournament, tour)
                self.menu_manage_first_round(self, players_of_tournament, serialized_tournament)
            elif turn == 1:
                tour = 1
                ViewMenuTournament.print_starting_round(ViewMenuTournament, tour)
                PlayTournament.menu_manage_other_round(PlayTournament, serialized_tournament,
                                                       players_of_tournament, tour)
            else:
                tour = turn
                ViewMenuTournament.print_starting_round(ViewMenuTournament, tour)
                PlayTournament.menu_manage_other_round(PlayTournament, serialized_tournament,
                                                       players_of_tournament, tour)
        else:
            ViewShare.print_error(ViewShare)


# set method used by the tournament class
class MethodeTournament:

    def play_tournament(self, tour):
        ''' management menu for create a tournament and saving it '''

        player = Player.table_of_player(Player)
        elements = self.element_of_tournament(self)
        tournament = Tournament.add_tournament(Tournament, elements)
        retour = self.add_players_of_tournament(self, player)
        players = retour[0]
        save_player = retour[1]
        Player.save_player(Player, save_player)
        remarks = ViewTournament.print_add_genaral_remarks(ViewTournament)
        timer_control = self.add_timer_control(self)
        players_of_tournament = Match.match_generation(Match, players)
        serialized_tournament = PlayTournament.gathers_tournament_dictionary(
            PlayTournament, tournament, players_of_tournament, remarks, timer_control)
        list_tournament = Tournament.table_of_tournament(Tournament)
        reponse = PlayTournament.control_already_selection(PlayTournament, list_tournament, serialized_tournament)
        if not reponse:
            ViewTournament.print_tournament_existing(ViewTournament)
            from controller import MainMenu
            MainMenu.menu(MainMenu)
        MenuTournament.menu_manage_save_tournament(MenuTournament, serialized_tournament, players_of_tournament, tour)

    def add_players_of_tournament(self, players):
        """ function to add players to the tournament
        access to the database or register a new player """

        retour_list = MethodePlayer.stat_classement(MethodePlayer)
        player_tri_alphabet = retour_list[1]
        nombre_de_tours = PLAYERS_OF_TOURNAMENT
        participants = []
        save_player = []
        compteur = 0
        for i in range(int(nombre_de_tours)):  # add all tournament players
            compteur += 1
            boucle = False
            while not boucle:
                choix = self.ask_which_player_of_tournament(self)
                if choix == 1:  # display player list by alphabetical order
                    try:
                        if len(player_tri_alphabet) != 0:
                            ViewTournament.print_list_players_alphabet(ViewTournament, player_tri_alphabet)
                            boucle = self.control_add_the_existing_player(self, participants, players, compteur)
                    except ValueError:
                        ViewTournament.print_not_list_player_existing(ViewTournament)
                        self.create_and_add_new_player_of_tournament(self, participants, save_player, compteur)
                        boucle = True
                elif choix == 2:  # create a new player and add player them to the tournament
                    self.create_and_add_new_player_of_tournament(self, participants, save_player, compteur)
                    boucle = True
        return participants, save_player

    def add_timer_control(self):
        # control display and good feedback from the input

        resultat = ViewTournament.print_add_timer_control(ViewTournament)
        timer_control = []
        if int(resultat) == 1:
            timer_control.append("bullet")
        elif int(resultat) == 2:
            timer_control.append("blitz")
        elif int(resultat) == 3:
            timer_control.append("coup rapide")
        else:
            ViewTournament.print_error_enter_selection(ViewTournament)
            self.print_add_timer_control(self)
        return timer_control

    def element_of_tournament(self):
        # control display and good feedback from the input

        retour = ViewTournament.print_elements_tournament(ViewTournament)
        ViewTournament.print_date_of_tournament(ViewTournament)
        date = self.print_date_controller(self)
        elements = {
            "name": retour[0],
            "location": retour[1],
            "date": date,
            }
        return elements

    def print_date_controller(self):
        ''' control the input console for the birth date of the player '''

        day = MethodeControl.control_enter_by_while(MethodeControl, "jour", 31)
        month = MethodeControl.control_enter_by_while(MethodeControl, "mois", 12)
        year = MethodeControl.control_enter_by_while(MethodeControl, "année", 1000)
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

        ViewTournament.print_menu_ajout_players_for_tournament(ViewTournament)
        choice = MethodeControl.control_enter_by_while(MethodeControl, 2, 102)
        return choice

    def control_add_the_existing_player(self, participants, players, compteur):
        '''check if the entry corresponds to an existing player'''

        MyCompleter.activate(MyCompleter, players)
        resultat = ViewTournament.print_add_players_for_tournament(ViewTournament)
        for i in players:  # control if the player is not already recording
            if resultat == i.get("pk"):
                no_selection = PlayTournament.control_already_selection(PlayTournament, participants, i)
                if no_selection:  # instantiate the player to the tournament
                    player = PlayTournament.add_players_tournament(PlayTournament, **i)
                    participants.append(player)
                    ViewTournament.print_save_players_for_tournament(ViewTournament, compteur, PLAYERS_OF_TOURNAMENT)
                    return True
                elif no_selection is None:  # instantiate the player to the tournament
                    player = PlayTournament.add_players_tournament(PlayTournament, **i)
                    participants.append(player)
                    ViewTournament.print_save_players_for_tournament(ViewTournament, compteur, PLAYERS_OF_TOURNAMENT)
                    return True
                else:
                    ViewTournament.print_add_players_for_tournament_inpossible(ViewTournament)
                    ViewTournament.print_continue(ViewTournament)
                    return False
        else:
            ViewTournament.print_error_id_tournament(ViewTournament)
            return False

    def create_and_add_new_player_of_tournament(self, participants, save_player, compteur):
        '''to create and add a new player in the tournament'''

        new_player = self.elements_player(self)
        add_player = Player.add_players(Player, new_player)
        player_valided = PlayTournament.duplicate_search_player(PlayTournament, add_player)
        seria = player_valided.get("valided")
        for s in seria:  # check if the player already exists
            serialized_player = s
            if not serialized_player.get("pk") is None:
                save_player.append(serialized_player)
                from player.view import ViewPlayer
                ViewPlayer.print_new_player_register(ViewPlayer)
                participants.append(serialized_player)
                ViewTournament.print_save_players_for_tournament(ViewTournament, compteur, PLAYERS_OF_TOURNAMENT)
                break
        ex = player_valided.get("no_valided")
        for i in ex:
            existing = i
            if not existing.get("pk") is None:
                ViewTournament.print_add_player_impossible(ViewTournament, existing)
                no_selection = PlayTournament.control_already_selection(PlayTournament, participants, i)
                if no_selection:
                    participants.append(existing)
                    ViewTournament.print_save_players_for_tournament(ViewTournament, compteur, PLAYERS_OF_TOURNAMENT)
                    break
                else:
                    ViewTournament.print_add_players_for_tournament_inpossible(ViewTournament)
                    ViewTournament.print_continue(ViewTournament)
                    break

    def control_sex_player(self):
        # control display and good feedback from the input

        sex = ViewTournament.print_sex_control(ViewTournament)
        if sex == "1":
            sex = "homme"
            return sex
        elif sex == "2":
            sex = "femme"
            return sex
        else:
            ViewTournament.print_error_number_sex(ViewTournament)
            del sex
            self.control_sex_player(self)

    def control_ranking_player(self):
        # returns a list to view

        ViewTournament.print_ranking_player(ViewTournament)
        ranking = 0
        while ranking != int:
            try:
                nb = ViewTournament.print_ranking_player_input(ViewTournament)
                ranking += nb
                break
            except ValueError:
                ViewTournament.print_ranking_player_error_enter(ViewTournament)
        ViewTournament.print_ranking_player_view(ViewTournament, ranking)
        return ranking

    def elements_player(self):
        # control display and good feedback from the input

        elements = []
        retour = ViewTournament.print_first_elements_player(ViewTournament)
        elements.append(retour[0])
        elements.append(retour[1])
        elements.append(self.print_date_controller(self))
        elements.append(self.control_sex_player(self))
        ViewTournament.print_first_recap_elements_player(ViewTournament, elements)
        elements.append(self.control_ranking_player(self))
        element = {
            "name": elements[0],
            "first_name": elements[1],
            "birth_date": elements[2],
            "sex": elements[3],
            "ranking": elements[4],
        }
        return element

    def start_tournament(self):
        ''' control the start of tournaments '''

        reponse = ViewTournament.print_start_tournament(ViewTournament)
        if reponse == "non":
            from controller import MainMenu
            MainMenu.menu(MainMenu)
        else:
            pass

    def tournament_find(self, TURNS, tournaments):
        ''' alows you to search among the tournaments which have ended
            which are in progress and those which have not started '''

        match = []
        tour = []
        end = []
        no_start = []
        start = []
        ViewTournament.print_find_tournament(ViewTournament)
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
            ViewTournament.print_tournament_finished(ViewTournament, i)
        ViewTournament.print_space(ViewTournament)
        for i in no_start:
            ViewTournament.print_tournament_not_start(ViewTournament, i)
        for i in start:
            ViewTournament.print_tournament_start(ViewTournament, i)
        ViewTournament.print_space(ViewTournament)
        reponse = ViewTournament.print_input_selection_tournament(ViewTournament)
        return reponse


# set method used by the match class
class MethodeMatch:

    def display_list_matchs(self, list_match):
        ''' show match list request '''

        m = 0
        for list in list_match:
            m += 1
            ViewMatch.print_view_match_possition(ViewMatch, m)
            for i in list:
                ViewMatch.print_view_match(ViewMatch, i)
        return list_match

    def play_first_turn(self, list_match):
        ''' play the first round of the tournament '''

        resultat_total = {}
        resultat_tour1 = {}
        date_start = datetime.now()
        date = str(date_start)
        resultat_tour1.update({"debut round": date})
        ViewMatch.print_start_chrono(ViewMatch, date)
        for i in list_match:
            joueur1 = i[0]
            joueur2 = i[1]
            match = joueur1.get("pk") + " / " + joueur2.get("pk")
            resultat = MethodeControl.control_choice_resultat_match(MethodeControl, match, joueur1, joueur2)
            joueur1["meet"] = [joueur2.get("pk")]
            joueur2["meet"] = [joueur1.get("pk")]
            if resultat == 1:
                ViewMatch.print_player_winner(ViewMatch, joueur1)
                resultat_tour1 = Match.distribution_of_points_and_resultat(
                    Match(), joueur1, joueur2, match, resultat_tour1)
            elif resultat == 2:
                ViewMatch.print_player_winner(ViewMatch, joueur2)
                resultat_tour1 = Match.distribution_of_points_and_resultat(
                    Match(), joueur2, joueur1, match, resultat_tour1)
            elif resultat == 3:
                ViewMatch.print_player_pat(ViewMatch)
                resultat_tour1 = Match.distribution_of_points_and_resultat_pat(
                    Match(), joueur1, joueur2, match, resultat_tour1)
            else:
                ViewShare.print_error(ViewShare)
        ViewMatch.print_ending_first_round(ViewMatch)
        date_end = datetime.now()
        date = str(date_end)
        resultat_tour1.update({"fin round": date})
        resultat_total.update({"round 1": resultat_tour1})
        ViewMatch.print_ending_chrono(ViewMatch, date)
        return resultat_total

    def gestion_match(self, list_match, resultat_total, tour):
        ''' play rounds matches from the 2nd round '''

        resultat_tour = {}
        date_start = datetime.now()
        date = str(date_start)
        resultat_tour.update({"debut round": date})
        ViewMatch.print_start_chrono(ViewMatch, date)
        for i in list_match:
            joueur1 = i[0]
            joueur2 = i[1]
            match = joueur1.get("pk") + " / " + joueur2.get("pk")
            resultat = MethodeControl.control_choice_resultat_match(MethodeControl, match, joueur1, joueur2)
            joueur1["meet"] += [joueur2.get("pk")]
            joueur2["meet"] += [joueur1.get("pk")]
            if resultat == 1:
                ViewMatch.print_player_winner(ViewMatch, joueur1)
                resultat_tour = Match.distribution_of_points_and_resultat_other_round(
                    Match(), joueur1, joueur2, match, resultat_tour)
            elif resultat == 2:
                ViewMatch.print_player_winner(ViewMatch, joueur2)
                resultat_tour = Match.distribution_of_points_and_resultat_other_round(
                    Match(), joueur2, joueur1, match, resultat_tour)
            elif resultat == 3:
                ViewMatch.print_player_pat(ViewMatch)
                resultat_tour = Match.distribution_of_points_and_resultat_pat_other_round(
                    Match(), joueur1, joueur2, match, resultat_tour)
            else:
                ViewShare.print_error(ViewShare)
        ViewMatch.print_ending_other_round(ViewMatch, tour)
        date_end = datetime.now()
        date = str(date_end)
        resultat_tour.update({"fin round": date})
        ViewMatch.print_ending_chrono(ViewMatch, date)
        resultat_total.update({"round " + str(tour): resultat_tour})
        return resultat_total


class MethodeControl:

    def control_choice_resultat_match(self, match, joueur1, joueur2):
        # control that return on the match result is indeed an int between 1 and 3

        while True:
            try:
                while True:
                    answer = ViewMatch.print_menu_match_tournament(ViewMatch, match, joueur1, joueur2)
                    if 0 < answer < 4:
                        return answer
                    else:
                        ViewTournament.print_error_enter_selection(ViewTournament)
            except ValueError:
                ViewTournament.print_control_wrong_enter(ViewTournament)

    def control_enter_by_while(self, data, data2):
        # check that the entry is indeed one of the expected

        if 0 < data2 < 100:
            while True:
                try:
                    while True:
                        answer = ViewTournament.print_control_input(ViewTournament, data)
                        if 0 < answer <= data2:
                            return answer
                        else:
                            ViewTournament.print_control_wrong_number(ViewTournament, data2)
                except ValueError:
                    ViewTournament.print_control_wrong_enter(ViewTournament)
        elif 101 < data2 < 103:
            while True:
                try:
                    while True:
                        answer = ViewTournament.print_control_input_none_view(ViewTournament)
                        if 0 < answer <= data2:
                            return answer
                        else:
                            ViewTournament.print_control_wrong_number(ViewTournament, data)
                except ValueError:
                    ViewTournament.print_control_wrong_enter(ViewTournament)
        elif data2 > 105:
            while True:
                try:
                    while True:
                        answer = ViewTournament.print_control_input(ViewTournament, data)
                        if 1930 < answer < 2150:
                            return answer
                        else:
                            ViewTournament.print_error_enter_years(ViewTournament)
                except ValueError:
                    ViewTournament.print_control_wrong_enter(ViewTournament)
