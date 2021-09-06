
from model import MyCompleter
from player.model import Player, MethodePlayer
from player.view import ViewPlayer
from tournament.controller import MethodeTournament
from tournament.view import ViewTournament


# create class for intialized the menu
class MenuPlayer:

    def menu_add_player(self):
        ''' management menu addition players '''

        player = MethodeTournament.elements_player(MethodeTournament)
        add_player = Player.add_players(Player, player)
        resultat = MethodePlayer.duplicate_search(MethodePlayer(), add_player)
        serialized_player = resultat.get("valided")
        existing = resultat.get("no_valided")
        if not serialized_player == []:
            Player.save_player(Player, serialized_player)
            ViewPlayer.print_new_player_register(ViewPlayer)
            MenuPlayer.ask_add_again_player(MenuPlayer)
        if not existing == []:
            ViewPlayer.print_exicting_player(ViewPlayer, existing)
            MenuPlayer.ask_add_again_player(MenuPlayer)

    def ask_add_again_player(self):
        # asks if the manager wants to re-enter a player

        reponse = ViewPlayer.print_add_player(ViewPlayer)
        if reponse == "oui":
            MenuPlayer.menu_add_player(MenuPlayer)
        else:
            from controller import MainMenu
            MainMenu.menu(MainMenu)

    def display_find_player(self):
        # manage player search

        resultat = ViewPlayer.print_find_player(ViewPlayer)
        while len(resultat) == 0:
            ViewPlayer.print_find_player_wrong(ViewPlayer)
        return resultat

    def menu_modif_player(self):
        ''' allows you to search for the player to modify by name which returns a list of
            all the players with this name or by ID to directly select the player to modify '''

        resultat = MenuPlayer.display_find_player(MenuPlayer)
        players = Player.table_of_player(Player)
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
                            modif = MenuPlayer.modif_element_player(MenuPlayer, player)
                            Player.modification_of_player(Player, modif)
                            from controller import MainMenu
                            MainMenu.menu(MainMenu)
                        else:
                            ViewPlayer.print_display_player_list(ViewPlayer, player)
            ViewPlayer.print_display_player_nb(ViewPlayer, len(nb_players), resultat)
            MenuPlayer.menu_modif_player(self)
        else:
            for player in players:
                for k, v in player.items():
                    if v == resultat:
                        modif = MenuPlayer.modif_element_player(MenuPlayer, player)
                        Player.modification_of_player(Player, modif)
                        from controller import MainMenu
                        MainMenu.menu(MainMenu)

    def modif_classement(self):
        ''' allows you to search for the player to modify by name which returns a list of all
            the players with this name or by ID to directly select the player to modify '''

        players = Player.table_of_player(Player)
        MyCompleter.activate(MyCompleter, players)  # manage autocomplementation
        resultat = MenuPlayer.display_find_player(MenuPlayer)
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
                            modif = self.display_modif_classement(self, player)
                            Player.modification_of_player(Player, modif)
                        else:
                            ViewPlayer.print_display_player_list(ViewPlayer, player)
            ViewPlayer.print_display_player_nb(ViewPlayer, len(nb_players), resultat)
            self.modif_classement(self)
        else:
            for player in players:
                for k, v in player.items():
                    if v == resultat:
                        modif = self.display_modif_classement(self, player)
                        Player.modification_of_player(Player, modif)

    def display_modif_classement(self, player):
        # asks if the manager wants to change the ranking

        reponse = ViewPlayer.print_modif_classement(ViewPlayer, player)
        ranking = player.get("ranking")
        if reponse == "oui":
            while ranking != int:
                try:
                    nb = ViewPlayer.print_modif_player_ranking_new_input(ViewPlayer)
                    ranking = nb
                    break
                except ValueError:
                    ViewPlayer.print_modif_classement_input_error(ViewPlayer)
        if not ranking == int(player.get("ranking")):
            player.update({"ranking": ranking})
            ViewPlayer.print_modif_player_ranking_answer(ViewPlayer, player)
            ViewPlayer.print_modif_ok(ViewPlayer)
        return player

    def modif_element_player(self, player):
        # manages the requests between the view and the modify player function

        a = ViewPlayer.print_modif_player_name(ViewPlayer, player)
        if not a == "":  # name change
            player.update({"name": a})
            ViewPlayer.print_modif_player_name_anwser(ViewPlayer, player)
        b = ViewPlayer.print_modif_player_first_name(ViewPlayer, player)
        if not b == "":  # first_name change
            player.update({"first_name": b})
            ViewPlayer.print_modif_player_first_name_anwser(ViewPlayer, player)
        reponse = ViewPlayer.print_modif_player_birth_date(ViewPlayer, player)
        if reponse == "oui":
            from tournament.controller import MethodeTournament
            c = MethodeTournament.print_date_controller(MethodeTournament)
        else:
            c = ""
        if c == player.get("birth_date"):  # birth date change
            player.update({"birth_date": c})
            ViewPlayer.print_modif_player_birth_date_answer(ViewPlayer, player)
        reponse = ViewPlayer.print_modif_player_sex(ViewPlayer, player)
        if reponse == "oui":
            d = ViewTournament.print_sex_control(ViewTournament)
        else:
            d = ""
        if d != player.get("sex"):  # sex change
            player.update({"sex": d})
            ViewPlayer.print_modif_player_sex_answer(ViewPlayer, player)
        reponse = ViewPlayer.print_modif_player_ranking(ViewPlayer, player)
        ranking = player.get("ranking")
        if reponse == "oui":
            while ranking != int:
                try:
                    nb = ViewPlayer.print_modif_player_ranking_new_input(ViewPlayer)
                    ranking = nb
                    break
                except ValueError:
                    ViewPlayer.print_modif_player_ranking_new_input_error(ViewPlayer)
        if not ranking == int(player.get("ranking")):  # ranking change
            player.update({"ranking": ranking})
            ViewPlayer.print_modif_player_ranking_answer(ViewPlayer, player)
        return player
