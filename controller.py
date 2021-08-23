
import sys

from model import MethodeForMenu
from player.controller import MenuPlayer
from player.model import Player
from tournament.controller import MenuTournament
from tournament.model import Tournament
from view import ViewMenu


# class MainMenu to initialize the application menu
class MainMenu(MethodeForMenu):

    def __init__(self):
        pass

    def menu(self):
        ''' menu distribution function '''

        resultat = ViewMenu.print_accueil(ViewMenu)
        try:
            resultat = ViewMenu.print_choice_input_menu(ViewMenu, resultat)
        except ValueError:
            ViewMenu.print_error_enter_int(ViewMenu)
            MainMenu.menu(self)
        if resultat == 1:  # adding player
            MenuPlayer.menu_add_player(self)
            MainMenu.menu(self)
        elif resultat == 2:  # player modification
            MenuPlayer.menu_modif_player(self)
            MainMenu.menu(self)
        elif resultat == 3:  # creation of a tournament
            tour = 1
            MenuTournament.play_tournament(MenuTournament, tour)
            MainMenu.menu(self)
        elif resultat == 4:  # to see all tournaments create and play tournaments not finalized
            self.menu_find_and_play_tournament(self)
            MainMenu.menu(self)
        elif resultat == 5:  # see the ranking
            retour_list = Player.stat_classement(Player)
            player_tri_ranking = retour_list[0]
            ViewMenu.print_classement(ViewMenu, player_tri_ranking)
            ViewMenu.print_pass_validation(ViewMenu)
            MainMenu.menu(self)
        elif resultat == 6:  # allows the modification of rank points per players
            Player.modif_classement(Player)
            MainMenu.menu(self)
        elif resultat == 7:  # access to the report management menu
            MainMenu.menu_rapports(self)
            MainMenu.menu(self)
        elif resultat == 8:  # to exit the program
            sys.exit()
        else:
            ViewMenu.print_error_enter_int(ViewMenu)
            MainMenu.menu()

    def menu_find_and_play_tournament(self):
        ''''allows you to search the list of unfinished tounaments if there are any '''

        try:
            MenuTournament.menu_tournament(MenuTournament)
            MainMenu.menu(self)
        except IndexError:
            ViewMenu.print_error_id(ViewMenu)

    def request_data_for_menu(self):
        ''' returns lists used by the main menu '''

        retour_list = Player.stat_classement(Player)
        player_tri_ranking = retour_list[0]
        player_tri_alphabet = retour_list[1]
        tournoi = Tournament.table_of_tournament(Tournament)
        ViewMenu.print_classement(ViewMenu, player_tri_ranking)
        choice = int(ViewMenu.print_menu_stat(ViewMenu))
        return player_tri_ranking, player_tri_alphabet, tournoi, choice

    def menu_rapports(self):
        ''' application report management menu '''

        retourn_list = self.request_data_for_menu(self)
        choice = retourn_list[3]
        if choice == 1:  # tri players by ranking
            ViewMenu.print_classement(ViewMenu, retourn_list[0])
            ViewMenu.print_pass_validation(ViewMenu)
            MainMenu.menu(self)
        elif choice == 2:  # tri players by aphabetical order
            ViewMenu.print_classement_alphabet(ViewMenu, retourn_list[1])
            ViewMenu.print_pass_validation(ViewMenu)
            MainMenu.menu(self)
        elif choice == 3:  # player list of a tournament by ranking
            self.rapport_player_list_of_tournament_by_ranking(self)
        elif choice == 4:  # player list of a tournament by alphabetical order
            self.rapport_player_list_of_tournament_by_alphabetical(self)
        elif choice == 5:  # tournament list
            ViewMenu.print_list_of_tournaments(ViewMenu, retourn_list[2])
            ViewMenu.print_pass_validation(ViewMenu)
        elif choice == 6:  # all the round of a tournament
            self.rapport_all_rounds_of_tournament(self)
        elif choice == 7:  # all the matches of a tournaments
            self.rapport_all_matches_of_tournament(self)
        elif choice == 8:  # for exit
            ViewMenu.print_space1(ViewMenu) * 50
        else:
            ViewMenu.print_menu_existing(ViewMenu)
