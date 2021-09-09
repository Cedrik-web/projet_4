
from model import MyCompleter
from player.model import Player, MethodePlayer
from player.view import ViewPlayer
from tournament.controller import MethodeTournament


# create class for intialized the menu
class MenuPlayer:

    def menu_add_player(self):
        """management menu addition players"""

        viewplayer = ViewPlayer()
        player = MethodeTournament().elements_player()
        cplayer = Player(**player)
        add_player = cplayer.add_players(player)
        resultat = MethodePlayer().duplicate_search(add_player)
        serialized_player = resultat.get("valided")
        existing = resultat.get("no_valided")
        if not serialized_player == []:
            cplayer.save_player(serialized_player)
            viewplayer.print_new_player_register()
            self.ask_add_again_player()
        if not existing == []:
            viewplayer.print_exicting_player(existing)
            self.ask_add_again_player()

    def ask_add_again_player(self):
        # asks if the manager wants to re-enter a player

        reponse = ViewPlayer().print_add_player()
        if reponse == "oui":
            MenuPlayer().menu_add_player()
        else:
            from controller import MainMenu
            MainMenu().menu()

    def display_find_player(self):
        # manage player search

        viewplayer = ViewPlayer()
        resultat = viewplayer.print_find_player()
        while len(resultat) == 0:
            viewplayer.print_find_player_wrong()
            resultat = viewplayer.print_find_player()
        return resultat

    def menu_modif_player(self):
        """allows you to search for the player to modify by name which returns a list of
            all the players with this name or by ID to directly select the player to modify"""

        menuplayer = MenuPlayer()
        viewplayer = ViewPlayer()
        players = Player.table_of_player()
        MyCompleter.activate(players)  # manage autocomplementation
        resultat = menuplayer.display_find_player()
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
                            modif = menuplayer.modif_element_player(player)
                            Player(**modif).modification_of_player(modif)
                            from controller import MainMenu
                            MainMenu().menu()
                        else:
                            viewplayer.print_display_player_list(player)
            viewplayer.print_display_player_nb(len(nb_players), resultat)
            menuplayer.menu_modif_player()
        else:
            for player in players:
                for k, v in player.items():
                    if v == resultat:
                        modif = menuplayer.modif_element_player(player)
                        Player(**modif).modification_of_player(modif)
                        from controller import MainMenu
                        MainMenu().menu()

    def modif_classement(self):
        """allows you to search for the player to modify by name which returns a list of all
            the players with this name or by ID to directly select the player to modify"""

        viewplayer = ViewPlayer()
        players = Player.table_of_player()
        MyCompleter.activate(players)  # manage autocomplementation
        resultat = MenuPlayer().display_find_player()
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
                            modif = self.display_modif_classement(player)
                            Player(**modif).modification_of_player(modif)
                        else:
                            viewplayer.print_display_player_list(player)
            viewplayer.print_display_player_nb(len(nb_players), resultat)
            self.modif_classement()
        else:
            for player in players:
                for k, v in player.items():
                    if v == resultat:
                        modif = self.display_modif_classement(player)
                        Player(**modif).modification_of_player(modif)

    def display_modif_classement(self, player):
        # asks if the manager wants to change the ranking

        viewplayer = ViewPlayer()
        reponse = viewplayer.print_modif_classement(player)
        ranking = player.get("ranking")
        if reponse == "oui":
            while ranking != int:
                try:
                    nb = viewplayer.print_modif_player_ranking_new_input()
                    ranking = nb
                    break
                except ValueError:
                    viewplayer.print_modif_classement_input_error()
        if not ranking == int(player.get("ranking")):
            player.update({"ranking": ranking})
            viewplayer.print_modif_player_ranking_answer(player)
            viewplayer.print_modif_ok()
        return player

    def modif_element_player(self, player):
        # manages the requests between the view and the modify player function

        self.ask_change_name(player)
        self.ask_change_first_name(player)
        self.ask_change_birth_date(player)
        self.ask_change_sex(player)
        self.ask_change_rank(player)
        return player

    def ask_change_name(self, player):
        # ask and change the name

        viewplayer = ViewPlayer()
        a = viewplayer.print_modif_player_name(player)
        if not a == "":  # name change
            player.update({"name": a})
            viewplayer.print_modif_player_name_anwser(player)

    def ask_change_first_name(self, player):
        # ask and change the first name

        viewplayer = ViewPlayer()
        b = viewplayer.print_modif_player_first_name(player)
        if not b == "":  # first_name change
            player.update({"first_name": b})
            viewplayer.print_modif_player_first_name_anwser(player)

    def ask_change_birth_date(self, player):
        # ask and change the birth date

        viewplayer = ViewPlayer()
        reponse = viewplayer.print_modif_player_birth_date(player)
        try:
            if reponse == "oui":
                from tournament.controller import MethodeTournament
                c = MethodeTournament().print_date_controller()
                if not c == player.get("birth_date"):  # birth date change
                    player.update({"birth_date": c})
                    viewplayer.print_modif_player_birth_date_answer(player)
        except ValueError:
            pass

    def ask_change_sex(self, player):
        # ask and change the sex

        viewplayer = ViewPlayer()
        reponse = viewplayer.print_modif_player_sex(player)
        try:
            if reponse == "oui":
                from tournament.controller import MethodeTournament
                d = MethodeTournament().control_sex_player()
                if not d == player.get("sex"):  # sex change
                    player.update({"sex": d})
                    viewplayer.print_modif_player_sex_answer(player)
        except ValueError:
            pass

    def ask_change_rank(self, player):
        # ask and change the rank

        viewplayer = ViewPlayer()
        reponse = viewplayer.print_modif_player_ranking(player)
        ranking = player.get("ranking")
        try:
            if reponse == "oui":
                while ranking != int:
                    try:
                        nb = viewplayer.print_modif_player_ranking_new_input()
                        ranking = nb
                        if not ranking == int(player.get("ranking")):  # ranking change
                            player.update({"ranking": ranking})
                            viewplayer.print_modif_player_ranking_answer(player)
                        break
                    except ValueError:
                        viewplayer.print_modif_player_ranking_new_input_error()
        except ValueError:
            pass
