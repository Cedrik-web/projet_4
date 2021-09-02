
import sys

from model import CleanText
from player.controller import MenuPlayer
from player.model import MethodePlayer
from tournament.controller import MenuTournament, MethodeTournament
from tournament.model import Tournament
from view import ViewMenu, ViewToShare, ViewReport


# class MainMenu to initialize the application menu
class MainMenu:

    def menu(self):
        ''' menu distribution function '''

        resultat = ViewMenu.print_accueil(ViewMenu)
        try:
            resultat = ViewMenu.print_choice_input_menu(ViewMenu, resultat)
        except ValueError:
            ViewMenu.print_error_enter_int(ViewMenu)
            self.menu(self)
        if resultat == 1:  # adding player
            MenuPlayer.menu_add_player(self)
            self.menu(self)
        elif resultat == 2:  # player modification
            MenuPlayer.menu_modif_player(self)
            self.menu(self)
        elif resultat == 3:  # creation of a tournament
            tour = 1
            MethodeTournament.play_tournament(MethodeTournament, tour)
            self.menu(self)
        elif resultat == 4:  # to see all tournaments create and play tournaments not finalized
            MethodeMainMenu.find_and_play_tournament(MethodeMainMenu)
            self.menu(self)
        elif resultat == 5:  # see the ranking
            retour_list = MethodePlayer.stat_classement(MethodePlayer)
            player_tri_ranking = retour_list[0]
            ViewMenu.print_classement(ViewMenu, player_tri_ranking)
            ViewToShare.print_pass_validation(ViewToShare)
            self.menu(self)
        elif resultat == 6:  # allows the modification of rank points per players
            MenuPlayer.modif_classement(MenuPlayer)
            self.menu(self)
        elif resultat == 7:  # access to the report management menu
            MainMenu.menu_rapports(self)
            self.menu(self)
        elif resultat == 8:  # to exit the program
            sys.exit()
        else:
            ViewMenu.print_error_enter_int(ViewMenu)
            self.menu(self)

    def menu_rapports(self):
        ''' application report management menu '''

        retourn_list = MethodeMainMenu.request_data_for_menu(MethodeMainMenu)
        choice = retourn_list[3]
        if choice == 1:  # tri players by ranking
            ViewMenu.print_classement(ViewMenu, retourn_list[0])
            ViewToShare.print_pass_validation(ViewToShare)
            self.menu(self)
        elif choice == 2:  # tri players by aphabetical order
            ViewMenu.print_classement_alphabet(ViewMenu, retourn_list[1])
            ViewToShare.print_pass_validation(ViewToShare)
            self.menu(self)
        elif choice == 3:  # player list of a tournament by ranking
            TournamentReport.rapport_player_list_of_tournament_by_ranking(TournamentReport)
        elif choice == 4:  # player list of a tournament by alphabetical order
            TournamentReport.rapport_player_list_of_tournament_by_alphabetical(TournamentReport)
        elif choice == 5:  # tournament list
            ViewMenu.print_list_of_tournaments(ViewMenu, retourn_list[2])
            ViewToShare.print_pass_validation(ViewToShare)
        elif choice == 6:  # all the round of a tournament
            TournamentReport.rapport_all_rounds_of_tournament(TournamentReport)
        elif choice == 7:  # all the matches of a tournaments
            TournamentReport.rapport_all_matches_of_tournament(TournamentReport)
        elif choice == 8:  # for exit
            ViewToShare.print_space(ViewToShare)
        else:
            ViewMenu.print_menu_existing(ViewMenu)


# useful fonction for main menu
class MethodeMainMenu:

    def find_and_play_tournament(self):
        ''''allows you to search the list of unfinished tounaments if there are any '''

        try:
            MenuTournament.menu_tournament(MenuTournament)
            MainMenu.menu(MainMenu)
        except IndexError:
            ViewToShare.print_error_id(ViewToShare)

    def request_data_for_menu(self):
        ''' returns lists used by the main menu '''

        retour_list = MethodePlayer.stat_classement(MethodePlayer)
        player_tri_ranking = retour_list[0]
        player_tri_alphabet = retour_list[1]
        tournoi = Tournament.table_of_tournament(Tournament)
        ViewMenu.print_classement(ViewMenu, player_tri_ranking)
        choice = int(ViewMenu.print_menu_stat(ViewMenu))
        return player_tri_ranking, player_tri_alphabet, tournoi, choice


# miscellaneous reporting functions
class TournamentReport:

    def selection_tournament(self):
        ''' allows to select a tournament in the dictionary '''

        tournaments = Tournament.table_of_tournament(Tournament)
        liste_tournoi = []
        for i in tournaments:
            ViewReport.print_list_tournament(ViewReport, i)
            liste_tournoi.append(i.get("pk"))
        choix = CleanText.clean_input(CleanText, ViewReport.print_choice_tournament(ViewReport))
        while choix not in liste_tournoi:
            ViewToShare.print_error_id(ViewToShare)
            choix = ViewReport.print_choice_tournament(ViewReport)
        else:
            for i in tournaments:
                if i.get("pk") == choix:
                    tournament = i
                    return tournament

    def rapport_player_list_of_tournament_by_ranking(self):
        '''generate the list of players of a shosen tournament and display by rank in order from
            largest to smallest'''

        tournament = self.selection_tournament(self)
        players = tournament.get("players")
        player_list = []
        for i in players:
            for k, v in i.items():
                player_list.append(v)
        tri_player_rank = sorted(player_list, key=lambda k: k["ranking"], reverse=True)
        ViewReport.print_classement_of_tournament(ViewReport)
        p = 0
        for i in tri_player_rank:
            p += 1
            ViewReport.print_tri_player_of_tournament_rank(ViewReport, i, p)
        ViewToShare.print_pass_validation(ViewToShare)

    def rapport_player_list_of_tournament_by_alphabetical(self):
        '''generate the list of players of a chosen tournament and display in
            alphabetical order'''

        tournament = self.selection_tournament(self)
        players = tournament.get("players")
        player_list = []
        for i in players:
            for k, v in i.items():
                player_list.append(v)
        tri_player_alphabet = sorted(player_list, key=lambda k: k["pk"])
        ViewReport.print_classement_player_of_tournament(ViewReport)
        for i in tri_player_alphabet:
            ViewReport.print_tri_player_of_tournament_alphabet(ViewReport, i)
        ViewToShare.print_pass_validation(ViewToShare)

    def rapport_all_rounds_of_tournament(self):
        '''generates a list of all the rounds of a selected tournament, displays the number
            of rounds and the playing time of each round'''

        tournament = self.selection_tournament(self)
        resultat = tournament.get("resultat")
        ViewReport.print_list_tournaments(ViewReport, tournament)
        t = 0
        for k, v in resultat.items():
            t += 1
            ViewReport.print_tournament_time(ViewReport, t)
            list_tour = v
            match = []
            resultat = []
            for k, v in list_tour.items():
                match.append(k)
                resultat.append(v)
            ViewReport.print_tournament_resultat(ViewReport, resultat)
            ViewToShare.print_space(ViewToShare)
        ViewToShare.print_pass_validation(ViewToShare)

    def rapport_all_matches_of_tournament(self):
        '''generate the list of all matches and result of a selected tournament'''

        tournament = self.selection_tournament(self)
        resultat = tournament.get("resultat")
        ViewReport.print_list_match_by_tournament(ViewReport, tournament)
        t = 0
        for k, v in resultat.items():
            t += 1
            ViewReport.print_resultat_match(ViewReport, t)
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
                if j == "pat match nul":
                    # controls the case where both players leave the winner list,which equals a tie
                    ViewReport.print_list_resultat_match_for_pat(ViewReport, i, j)
                    ViewReport.print_new_point_to_assign_for_pat(ViewReport, i)
                    ViewToShare.print_space(ViewToShare)
                else:
                    ViewReport.print_list_resultat_match(ViewReport, i, j)
                    ViewReport.print_new_point_to_assign(ViewReport, j)
                    ViewToShare.print_space(ViewToShare)
            ViewToShare.print_space(ViewToShare)
        ViewToShare.print_pass_validation(ViewToShare)
