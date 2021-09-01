
from model import MyCompleter
from player.model import Player, MethodePlayer
from player.view import ViewPlayer


# create class for intialized the menu
class MenuPlayer:

    def menu_add_player(self):
        ''' management menu addition players '''

        player = ViewPlayer.print_add_player(ViewPlayer)
        add_player = Player.add_players(Player, player)
        resultat = MethodePlayer.duplicate_search(MethodePlayer(), add_player)
        serialized_player = resultat.get("valided")
        existing = resultat.get("no_valided")
        if not serialized_player == []:
            Player.save_player(Player, serialized_player)
            ViewPlayer.print_new_player_register(ViewPlayer)
        if not existing == []:
            ViewPlayer.print_exicting_player(ViewPlayer, existing)
            from controller import MainMenu
            MainMenu.menu(MainMenu)

    def menu_modif_player(self):
        ''' allows you to search for the player to modify by name which returns a list of
            all the players with this name or by ID to directly select the player to modify '''

        resultat = ViewPlayer.print_find_player(ViewPlayer)
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
                            modif = ViewPlayer.print_modif_player(ViewPlayer, player)
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
                        modif = ViewPlayer.print_modif_player(ViewPlayer, player)
                        Player.modification_of_player(Player, modif)
                        from controller import MainMenu
                        MainMenu.menu(MainMenu)

    def modif_classement(self):
        ''' allows you to search for the player to modify by name which returns a list of all
            the players with this name or by ID to directly select the player to modify '''

        players = self.table_of_player(self)
        MyCompleter.activate(MyCompleter, players)  # manage autocomplementation
        resultat = ViewPlayer.print_find_player(ViewPlayer)
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
                            modif = ViewPlayer.print_modif_classement(ViewPlayer, player)
                            self.modification_of_player(self, modif)
                            ViewPlayer.print_modif_ok(ViewPlayer)
                        else:
                            ViewPlayer.print_display_player_list(ViewPlayer, player)
            ViewPlayer.print_display_player_nb(ViewPlayer, len(nb_players), resultat)
            self.modif_classement(self)
        else:
            for player in players:
                for k, v in player.items():
                    if v == resultat:
                        modif = ViewPlayer.print_modif_classement(ViewPlayer, player)
                        self.modification_of_player(self, modif)
                        ViewPlayer.print_modif_ok(ViewPlayer)
