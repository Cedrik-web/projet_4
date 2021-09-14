
from tinydb import TinyDB
from tinydb.table import Document

from player.model import Player
from settings import PLAYERS_OF_TOURNAMENT, TURNS


#  creation of the tournament class and manage tournaments
class Tournament:

    def __init__(self):
        self.pk = None
        self.name = None
        self.location = None
        self.date = None
        self.turns = TURNS
        self.nb_players = PLAYERS_OF_TOURNAMENT
        self.resultat = []
        self.players = []
        self.remarks = []
        self.timer_control = []

    def add_tournament(self, tournament):
        # named parameter and serialization of tournament items

        serialized = {
            "pk": tournament.get("name") + "_" + tournament.get("location") + "_" + tournament.get("date"),
            "name": tournament.get("name"),
            "location": tournament.get("location"),
            "date": tournament.get("date"),
            "turns": self.turns,
            "nb_players": self.nb_players,
            "resultat": self.resultat,
            "players": tournament.get("players"),
            "remarks": tournament.get("remarks"),
            "timer_control": tournament.get("timer_control"),
        }
        return serialized

    def save_tournament(self, serialized_tournament):
        # save tournament in the tournament table and save in the db.json file

        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        tournament_table.insert(serialized_tournament)

    def save_resultat_tournament(self, serialized_resultat, tournament):
        # saves the modification of a tournament, etc result ...

        tournaments = self.table_of_tournament()
        db = TinyDB("db.json").table("tournament")
        serialized_resultat.update({"resultat": tournament})
        for t in tournaments:
            if t.get("pk") == serialized_resultat.get("pk"):
                tournoi_doc_id = t.doc_id
                db.upsert(Document(serialized_resultat, doc_id=tournoi_doc_id))

    def table_of_tournament(self):
        # allows you to retrieve the tournament table from the db.json file

        db = TinyDB("db.json")
        tournament_table = db.table("tournament").all()
        return tournament_table


# method used for tournament operation
class PlayTournament:

    def __init__(self):
        # initiates players into the tournament
        self.pk = None
        self.name = None
        self.first_name = None
        self.birth_date = None
        self.sex = None
        self.ranking = 0

    def add_players_tournament(self, player):
        # named parameters and serialization of players items

        serialized_player = {
            "pk": player.get("pk"),
            "name": player.get("name"),
            "first_name": player.get("first_name"),
            "birth_date": player.get("birth_date"),
            "sex": player.get("sex"),
            "ranking": player.get("ranking"),
        }
        return serialized_player

    def menu_manage_other_round(self, serialized_tournament, players_of_tournament, tour):
        # manage all the others rounds

        tournament = Tournament()
        resultat_total = serialized_tournament.get("resultat")
        resultat_total = self.nunber_turn(TURNS, players_of_tournament, resultat_total, serialized_tournament, tour)
        tournament.save_resultat_tournament(serialized_tournament, resultat_total)

    def control_type_function(self, data):
        # control and transform a data list and dictionary

        new_data = {}
        for i, j in data.items():
            new_data[i] = j
        return new_data

    def control_type_function_list(self, data):
        # control and transform data into a simple list

        if data != []:
            if type(data) == list:
                for i in data:
                    new_data = i
                    return new_data
            else:
                new_data = data
                return new_data
        else:
            return data

    @classmethod
    def control_already_selection(cls, list_participant, data):
        # checks if the "pk" data ( player or tournament ) is in the list and answers true or false

        for i in list_participant:
            if data.get("pk") == i.get("pk"):
                valided = False
                return valided
            else:
                pass
        valided = True
        return valided

    def nunber_turn(self, turns, players_of_tournament, resultat_total, serialized_tournament, tour):
        # function that controls the course of laps from the 2nd ( by a loop)

        global resultat_tournament
        turn = turns - tour
        # get the tour and turns attribute in order to determine how many turns remains to be done
        # compared to what the manager has to determine in settings.py

        for i in range(turn):
            tour += 1
            retour = Match.generation_next_round(Match(), players_of_tournament)
            #   generate the list of matches to be played
            list_matchs = retour[1]
            from tournament.controller import MethodeMatch
            list_match = MethodeMatch().display_list_matchs(list_matchs, tour)
            from tournament.controller import MethodeTournament
            MethodeTournament().start_tournament()
            resultat_tournament = MethodeMatch().play_turn(list_match, resultat_total, tour)
            Tournament().save_resultat_tournament(serialized_tournament, resultat_tournament)
        return resultat_tournament

    def tournaments_recovery(self, answer, tournaments):
        # manage the resumption of tournament and what turn it was return the tournament

        serialized_tournament = []
        for i in tournaments:
            if i.get("pk") == answer:
                serialized_tournament.append(i)
        return serialized_tournament

    def tournaments_recovery2(self, tournament):
        """return the number of the turn"""

        tournoi = []
        for i in tournament:
            tour = i.get("resultat")
            tournoi.append(tour)
        if tournoi == []:
            turn = 0
            return turn
        else:
            for r in tournoi:
                nb = len(r)
                if nb == 1:
                    turn = 1
                    return turn
                elif nb == 2:
                    turn = 2
                    return turn
                elif nb == 3:
                    turn = 3
                    return turn

    def duplicate_search_player(self, new_player):
        # check ij the ID is not already referenced in the database

        players = Player.table_of_player()
        nb_players = []
        valided = []
        no_valided = []
        dict = {"valided": valided, "no_valided": no_valided}
        if len(new_player) > 1:
            for p in new_player:
                for k, v in p.items():
                    if k == "pk":
                        nb_players.append(v)
                nb_str = len(nb_players)
                nb_int = nb_str
                if nb_int == 1:
                    for i in players:
                        if p.get("pk") == i.get("pk"):
                            no_valided.append(p)
                            break
                    else:
                        valided.append(p)
                else:
                    for i in players:
                        if p.get("pk") == i.get("pk"):
                            no_valided.append(p)
                            break
                    else:
                        valided.append(p)
        else:
            try:
                for p in new_player:
                    for i in players:
                        if p.get("pk") == i.get("pk"):
                            no_valided.append(p)
                            break
                    else:
                        valided.append(p)
            except TypeError:
                for i in players:
                    for j in new_player:
                        if j == i.get("pk"):
                            no_valided.append(j)
                            break
                        else:  # TODO
                            valided.append(j)
        return dict


# Create class Match who initiates the characteristics to ask for the match
class Match:

    def __init__(self):
        self.nb_players = 2
        self.winner = 1.0
        self.loser = 0.0
        self.draw = 0.5
        self.point = self.winner + self.loser + self.draw

    def match_generation(self, players):
        # add players to the match and serialized them return the list of players

        player_of_tournament = []
        tour = 0
        for i in players:
            tour += 1
            player = i
            point_tournament = 0
            match_win = 0
            match_lose = 0
            match_pat = 0
            player["point_tournament"] = point_tournament
            player["meet"] = player.get("pk")
            player["match_win"] = match_win
            player["match_lose"] = match_lose
            player["match_pat"] = match_pat
            player_of_tournament.append(player)
        return player_of_tournament

    def transform_list(self, list_joueur):
        """transforms the list of players numbered by position generated by
        the object and list to be supported for peer generation"""

        player_of_tournament = []
        for i in list_joueur:
            for k, v in i.items():
                player_of_tournament.append(v)
        return player_of_tournament

    def generation_first_round(self, player_of_tournament):
        """generate the first matches then award points and update status
            match by players"""

        tri = sorted(player_of_tournament, key=lambda k: k["ranking"], reverse=True)
        #   sort the list in order from highest to lowest rank
        nb_player = int(len(tri) / 2)
        #   divide the list sort into two
        list_player_a = tri[:nb_player]
        list_player_b = tri[nb_player:]
        #   build two lists with the first one that was split
        list_match = []
        position = -1
        for i in range(TURNS):
            position += 1
            p1 = list_player_a[position]
            p2 = list_player_b[position]
            update = PlayMatch().update_meet_list(p1, p2)
            joueur1 = update[0]
            joueur2 = update[1]
            match = [joueur1, joueur2]
            list_match.append(match)
            # generate the first matches by taking the first ones from each list to then compete
            # against each other the second etc ... until all the desired matches are generated and return
            # a match list with these elements
        return list_match

    def generation_next_round(self, player_of_tournament):
        # generates match pairs from the 2nd round

        playmatch = PlayMatch()
        list_player = []
        list_match = []
        tri_rank = sorted(player_of_tournament, key=lambda k: k["ranking"], reverse=True)
        tri_tour = sorted(tri_rank, key=lambda k: k["point_tournament"], reverse=True)
        #   sort first in order of highest to lowest rank, and sort by tournament point from highest to lowest
        position1 = -2
        position2 = -1
        #   initial position defined in order to generate a dynamic position after the for loop
        t = 0
        for i in range(4):  # manage the matches
            t += 1
            position1 += 2
            position2 += 2
            joueur1 = tri_tour[position1]
            joueur2 = tri_tour[position2]
            #  dynamic position of the players select from the list sort the first meet the second and so on
            #  checks that the match has not already been played and returns another player if necessary
            player1 = playmatch.control_first_player1_in_list(joueur1, tri_tour, list_player)
            player2 = playmatch.control_valided_player2(player1, joueur2, tri_tour, list_player, tour=0)
            #  checks that the match has not already been played and returns another player if necessary
            update = playmatch.update_meet_list(player1, player2)
            player1 = update[0]
            player2 = update[1]
            new_match = player1, player2
            list_match.append(new_match)
        return player_of_tournament, list_match

    def distribution_of_points_and_resultat(self, joueur1, joueur2, match, resultat_tour):
        """distributed the points according to the player's result, is used to define the classification"""
        """by tournament and thus to generate the peers"""

        joueur1.update(point_tournament=joueur1.get("point_tournament") + self.winner)
        joueur1.update(match_win=+1)
        joueur2.update(point_tournament=joueur2.get("point_tournament") + self.winner)
        joueur2.update(match_win=+1)
        winner = joueur1.get("pk")
        resultat_tour.update({match: winner})
        return resultat_tour

    def distribution_of_points_and_resultat_pat(self, joueur1, joueur2, match, resultat_tour):
        """distributed the points according to the player's result, is used to define the classification
            by tournament and thus to generate the peers"""

        joueur1.update(point_tournament=joueur1.get("point_tournament") + self.draw)
        joueur1.update(match_win=+1)
        joueur2.update(point_tournament=joueur2.get("point_tournament") + self.draw)
        joueur2.update(match_win=+1)
        winner = "pat match nul"
        resultat_tour.update({match: winner})
        return resultat_tour


# method used for the functioning of the matches
class PlayMatch:

    def update_meet_list(self, joueur1, joueur2):
        """updates the player's encounter key in the other round"""

        update1 = []
        update2 = []
        for i in joueur1.get("meet"):
            update1.append(i)
        for j in joueur2.get("meet"):
            update2.append(j)
        update1.append(joueur2.get("pk"))
        update2.append(joueur1.get("pk"))
        joueur1.update(meet=update1)
        joueur2.update(meet=update2)
        return joueur1, joueur2

    def control_first_player1_in_list(self, joueur1, tri_tour, list_player):
        """test if the player has not already played on the turn"""

        t = 0
        try:
            joueur_valided = joueur1
            while joueur_valided.get("pk") in list_player:
                # test if the player has already played during this round
                t += 1
                new_position = t
                joueur_valided = tri_tour[new_position]
            list_player.append(joueur_valided.get("pk"))
            return joueur_valided
        except ValueError:
            from tournament.controller import MethodeControl
            MethodeControl().unexpected_error()

    def control_valided_player2(self, joueur1, joueur2, tri_tour, list_player, tour):
        """test if the player has not already played on the turn and has not already met his opponent"""

        try:
            player_meet = joueur1.get("meet")
            while True:
                # test if the player has already met his opponent
                if joueur2.get("pk") in player_meet:
                    tour += 1
                    joueur2 = tri_tour[tour]
                    while True:  # test if the player has already played during this round
                        if joueur2.get("pk") in list_player:
                            tour += 1
                            joueur2 = tri_tour[tour]
                        else:
                            break
                else:
                    break
            list_player.append(joueur2.get("pk"))
            return joueur2
        except ValueError:
            from tournament.controller import MethodeControl
            MethodeControl().unexpected_error()
