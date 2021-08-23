
from player.model import Player
from player.view import ViewPlayer


# create class for intialized the menu
class MenuPlayer:

    def __init__(self):
        pass

    def menu_add_player(self):
        ''' management menu addition players '''

        player = ViewPlayer.print_add_player1(ViewPlayer)
        add_player = Player.add_players(Player, player)
        resultat = Player.duplicate_search(Player, add_player)
        serialized_player = resultat.get("valided")
        existing = resultat.get("no_valided")
        if not serialized_player == []:
            Player.save_player(Player, serialized_player)
            ViewPlayer.print_new_player_register1(ViewPlayer)
        if not existing == []:
            ViewPlayer.print_exicting_player1(ViewPlayer, existing)

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
                            modif = ViewPlayer.print_modif_player1(ViewPlayer, player)
                            Player.modification_of_player(Player, modif)
                            ViewPlayer.print_modif_ok1(ViewPlayer)
                        else:
                            ViewPlayer.print_display_player_list(ViewPlayer, player)
            ViewPlayer.print_display_player_nb(ViewPlayer, len(nb_players), resultat)
            MenuPlayer.menu_modif_player(self)
        else:
            for player in players:
                for k, v in player.items():
                    if v == resultat:
                        modif = ViewPlayer.print_modif_player1(ViewPlayer, player)
                        Player.modification_of_player(Player, modif)
                        ViewPlayer.print_modif_ok1(ViewPlayer)
