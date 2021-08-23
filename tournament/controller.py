
from player.model import Player
from settings import TURNS
from tournament.model import Match, Tournament
from tournament.view import ViewTournament


#  the tournament menu class manages the creation or search of an existing tournament to the management
#  of rounds and matches then saving.
class MenuTournament(Player):

    def play_tournament(self, tour):
        ''' management menu for create a tournament and saving it '''

        player = Player.table_of_player(Player)
        elements = ViewTournament.print_elements_tournament(ViewTournament)
        tournament = Tournament.add_tournament(Tournament, elements)
        retour = Tournament.add_players_of_tournament(Tournament, tournament, player)
        players = retour[0]
        save_player = retour[1]
        Player.save_player(Player, save_player)
        remarks = ViewTournament.print_add_genaral_remarks(ViewTournament)
        timer_control = ViewTournament.print_add_timer_control(ViewTournament)
        players_of_tournament = Match.match_generation(Match(), players)
        serialized_tournament = Tournament.gathers_tournament_dictionary(
            Tournament, tournament, players_of_tournament, remarks, timer_control)
        self.menu_manage_save_tournament(self, serialized_tournament, players_of_tournament, tour)

    def menu_manage_save_tournament(self, serialized_tournament, players_of_tournament, tour):
        '''manage the save elements of tournament'''

        Tournament.save_tournament(Tournament, serialized_tournament)
        list_matchs = Match.generation_first_round(Match(), players_of_tournament, TURNS)
        list_match = Match.print_list_matchs(Match(), list_matchs)
        Tournament.start_tournament(Tournament)
        resultat_total = Match.play_first_turn(Match(), list_match)
        Tournament.save_resultat_tournament(Tournament, serialized_tournament, resultat_total)
        Tournament.nunber_turn(Tournament, TURNS, players_of_tournament, resultat_total, serialized_tournament, tour)
        Tournament.save_resultat_tournament(Tournament, serialized_tournament, resultat_total)

    def menu_tournament(self):
        ''' menu to retrieve the ID of the tournament register to start
            or finish '''

        tournaments = Tournament.table_of_tournament(Tournament)
        reponse = Tournament.tournament_find(Tournament, TURNS, tournaments)  # return ID input
        if reponse != "":
            retour = Tournament.tournaments_recovery(Tournament, reponse, tournaments)
            players_of_tournament = retour[0]
            serialized_tournament = retour[1]
            turn = retour[2]
            if turn == 0:  # turn has for value an integer which corresponds to the
                ViewTournament.print_starting_round(ViewTournament, tour=0)
                self.menu_manage_first_round(self, players_of_tournament, serialized_tournament)
            elif turn == 1:
                tour = 1
                ViewTournament.print_starting_round(ViewTournament, tour)
                self.menu_mange_other_round(self, serialized_tournament, players_of_tournament, tour)
            else:
                tour = turn
                ViewTournament.print_starting_round(ViewTournament, tour)
                self.menu_mange_other_round(self, serialized_tournament, players_of_tournament, tour)
        else:
            ViewTournament.print_error(ViewTournament)

    def menu_manage_first_round(self, players_of_tournament, serialized_tournament):
        '''manage the first round'''

        list_matchs = Match.generation_first_round(Match(), players_of_tournament, TURNS)
        list_match = Match.print_list_matchs(Match(), list_matchs)
        Tournament.start_tournament(Tournament)
        resultat_total = Match.play_first_turn(Match(), list_match)
        Tournament.save_resultat_tournament(Tournament, serialized_tournament, resultat_total)
        Tournament.nunber_turn(Tournament, TURNS, players_of_tournament, resultat_total, serialized_tournament, tour=1)
        Tournament.save_resultat_tournament(Tournament, serialized_tournament, resultat_total)

    def menu_mange_other_round(self, serialized_tournament, players_of_tournament, tour):
        '''manage all the others rounds'''

        resultat_total = serialized_tournament.get("resultat")
        resultat_total = Tournament.nunber_turn(Tournament, TURNS, players_of_tournament, resultat_total,
                                                serialized_tournament, tour)
        Tournament.save_resultat_tournament(Tournament, serialized_tournament, resultat_total)
