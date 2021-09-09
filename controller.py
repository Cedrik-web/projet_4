
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
        # menu distribution function

        menuplayer = MenuPlayer()
        viewmenu = ViewMenu()
        resultat = viewmenu.print_accueil()
        try:
            resultat = viewmenu.print_choice_input_menu(resultat)
        except ValueError:
            viewmenu.print_error_enter_int()
            self.menu()
        if resultat == 1:  # adding player
            menuplayer.menu_add_player()
            self.menu()
        elif resultat == 2:  # player modification
            menuplayer.menu_modif_player()
            self.menu()
        elif resultat == 3:  # creation of a tournament
            tour = 1
            MenuTournament().play_tournament(tour)
            self.menu()
        elif resultat == 4:  # to see all tournaments create and play tournaments not finalized
            MethodeMainMenu().find_and_play_tournament()
            self.menu()
        elif resultat == 5:  # see the ranking
            retour_list = MethodePlayer().stat_classement()
            player_tri_ranking = retour_list[0]
            viewmenu.print_classement(player_tri_ranking)
            ViewToShare().print_pass_validation()
            self.menu()
        elif resultat == 6:  # allows the modification of rank points per players
            menuplayer.modif_classement()
            self.menu()
        elif resultat == 7:  # access to the report management menu
            MainMenu().menu_rapports()
            self.menu()
        elif resultat == 8:  # to exit the program
            sys.exit()
        else:
            viewmenu.print_error_enter_int()
            self.menu()

    def menu_rapports(self):
        # application report management menu

        viewmenu = ViewMenu()
        viewtoshare = ViewToShare()
        tournamentreport = TournamentReport()
        retourn_list = MethodeMainMenu().request_data_for_menu()
        choice = retourn_list[3]
        if choice == 1:  # tri players by ranking
            viewmenu.print_classement(retourn_list[0])
            viewtoshare.print_pass_validation()
            self.menu()
        elif choice == 2:  # tri players by aphabetical order
            viewmenu.print_classement_alphabet(retourn_list[1])
            viewtoshare.print_pass_validation()
            self.menu()
        elif choice == 3:  # player list of a tournament by ranking
            tournamentreport.rapport_player_list_of_tournament_by_ranking()
        elif choice == 4:  # player list of a tournament by alphabetical order
            tournamentreport.rapport_player_list_of_tournament_by_alphabetical()
        elif choice == 5:  # tournament list
            viewmenu.print_list_of_tournaments(retourn_list[2])
            viewtoshare.print_pass_validation()
        elif choice == 6:  # all the round of a tournament
            tournamentreport.rapport_all_rounds_of_tournament()
        elif choice == 7:  # all the matches of a tournaments
            tournamentreport.rapport_all_matches_of_tournament()
        elif choice == 8:  # for exit
            viewtoshare.print_space()
        else:
            viewmenu.print_menu_existing()


# useful fonction for main menu
class MethodeMainMenu:

    def find_and_play_tournament(self):
        # allows you to search the list of unfinished tounaments if there are any

        try:
            MenuTournament().menu_tournament()
            MainMenu().menu()
        except IndexError:
            ViewToShare().print_error_id()

    def request_data_for_menu(self):
        ''' returns lists used by the main menu '''

        viewmenu = ViewMenu()
        retour_list = MethodePlayer().stat_classement()
        player_tri_ranking = retour_list[0]
        player_tri_alphabet = retour_list[1]
        tournoi = Tournament().table_of_tournament()
        viewmenu.print_classement(player_tri_ranking)
        viewmenu.print_menu_stat()
        while True:
            choice = viewmenu.print_choice_input()
            try:
                while not 0 < int(choice) <= 8:
                    viewmenu.print_menu_existing()
                    choice = viewmenu.print_choice_input()
                resultat = int(choice)
                return player_tri_ranking, player_tri_alphabet, tournoi, resultat
            except ValueError:
                viewmenu.print_error_enter_int()


# miscellaneous reporting functions
class TournamentReport:

    def selection_tournament(self):
        # allows to select a tournament in the dictionary

        viewreport = ViewReport()
        tournaments = Tournament().table_of_tournament()
        liste_tournoi = []
        for i in tournaments:
            viewreport.print_list_tournaments(i)
            liste_tournoi.append(i.get("pk"))
        choix = CleanText().clean_input(viewreport.print_choice_tournament())
        while choix not in liste_tournoi:
            ViewToShare().print_error_id()
            choix = viewreport.print_choice_tournament()
        else:
            for i in tournaments:
                if i.get("pk") == choix:
                    tournament = i
                    return tournament

    def rapport_player_list_of_tournament_by_ranking(self):
        """generate the list of players of a shosen tournament and display by rank in order from
            largest to smallest"""

        viewreport = ViewReport()
        tournament = self.selection_tournament()
        players = tournament.get("players")
        player_list = []
        for i in players:
            player_list.append(i)
        tri_player_rank = sorted(player_list, key=lambda k: k["ranking"], reverse=True)
        viewreport.print_classement_of_tournament()
        p = 0
        for i in tri_player_rank:
            p += 1
            viewreport.print_tri_player_of_tournament_rank(i, p)
        ViewToShare().print_pass_validation()

    def rapport_player_list_of_tournament_by_alphabetical(self):
        """generate the list of players of a chosen tournament and display in
            alphabetical order"""

        viewreport = ViewReport()
        tournament = self.selection_tournament()
        players = tournament.get("players")
        player_list = []
        for i in players:
            player_list.append(i)
        tri_player_alphabet = sorted(player_list, key=lambda k: k["pk"])
        viewreport.print_classement_player_of_tournament()
        for i in tri_player_alphabet:
            viewreport.print_tri_player_of_tournament_alphabet(i)
        ViewToShare().print_pass_validation()

    def rapport_all_rounds_of_tournament(self):
        """generates a list of all the rounds of a selected tournament, displays the number
            of rounds and the playing time of each round"""

        viewtoshare = ViewToShare()
        viewreport = ViewReport()
        tournament = self.selection_tournament()
        resultat = tournament.get("resultat")
        viewreport.print_list_tournaments(tournament)
        t = 0
        for k, v in resultat.items():
            t += 1
            viewreport.print_tournament_time(t)
            list_tour = v
            match = []
            resultat = []
            for k, v in list_tour.items():
                match.append(k)
                resultat.append(v)
            viewreport.print_tournament_resultat(resultat)
            viewtoshare.print_space()
        viewtoshare.print_pass_validation()

    def rapport_all_matches_of_tournament(self):
        # generate the list of all matches and result of a selected tournament

        viewtoshare = ViewToShare()
        viewreport = ViewReport()
        tournament = self.selection_tournament()
        resultat = tournament.get("resultat")
        viewreport.print_list_match_by_tournament(tournament)
        t = 0
        for k, v in resultat.items():
            t += 1
            viewreport.print_resultat_match(t)
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
                    viewreport.print_list_resultat_match_for_pat(i, j)
                    viewreport.print_new_point_to_assign_for_pat(i)
                    viewtoshare.print_space()
                else:
                    viewreport.print_list_resultat_match(i, j)
                    viewreport.print_new_point_to_assign(j)
                    viewtoshare.print_space()
            viewtoshare.print_space()
        viewtoshare.print_pass_validation()
