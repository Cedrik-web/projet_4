
from tinydb import TinyDB
from tinydb.table import Document

from player.model import Player
from settings import PLAYERS_OF_TOURNAMENT, TURNS


#  creation of the tournament class and manage tournaments
class Tournament:

    def __init__(self, name, location, date):
        self.pk = name + "_" + location + "_" + date
        self.name = name
        self.location = location
        self.date = date
        self.turns = TURNS
        self.nb_players = PLAYERS_OF_TOURNAMENT
        self.resultat = []

    def add_tournament(self, tour):
        ''' named parameter and serialization of tournament items '''

        serialized_tournament = []
        tournament = Tournament(
            name=tour.get("name"),
            location=tour.get("location"),
            date=tour.get("date"),
        )
        serialized = {
            "pk": tournament.pk,
            "name": tournament.name,
            "location": tournament.location,
            "date": tournament.date,
            "turns": tournament.turns,
            "nb_players": tournament.nb_players,
            "resultat": tournament.resultat,
        }
        serialized_tournament.append(serialized)
        return serialized_tournament

    def save_tournament(self, serialized_tournament):
        ''' save tournament in the tournament table and save in the db.json file '''

        db = TinyDB("db.json")
        tournament_table = db.table("tournament")
        tournament_table.insert(serialized_tournament)

    def save_resultat_tournament(self, serialized_resultat, tournament):
        ''' saves the modification of a tournament, etc result ... '''

        tournaments = self.table_of_tournament(self)
        db = TinyDB("db.json").table("tournament")
        serialized_resultat.update({"resultat": tournament})
        for t in tournaments:
            if t.get("pk") == serialized_resultat.get("pk"):
                tournoi_doc_id = t.doc_id
                db.upsert(Document(serialized_resultat, doc_id=tournoi_doc_id))

    def table_of_tournament(self):
        ''' allows you to retrieve the tournament table from the db.json file '''

        db = TinyDB("db.json")
        tournament_table = db.table("tournament").all()
        return tournament_table


# method used for tournament operation
class PlayTournament:

    def menu_manage_other_round(self, serialized_tournament, players_of_tournament, tour):
        '''manage all the others rounds'''

        resultat_total = serialized_tournament.get("resultat")
        resultat_total = self.nunber_turn(self, TURNS, players_of_tournament, resultat_total,
                                                serialized_tournament, tour)
        Tournament.save_resultat_tournament(Tournament, serialized_tournament, resultat_total)

    def gathers_tournament_dictionary(self, tournoi, players, remarks, timer_control):
        ''' add players to tournament elements '''

        for i in tournoi:
            tournament = i
        list_players = []
        nb = []
        for p in players:
            nb.append(p)
            player = {len(nb): p}
            list_players.append(player)
        tournament["players"] = list(list_players)
        tournament["remarks"] = list(remarks)
        tournament["timer_control"] = list(timer_control)
        return tournament

    def control_type_function(self, data):
        '''control and transform a data list and dictionary'''

        new_data = {}
        for i,j in data.items():
            new_data[i] = j
        return new_data

    def control_type_function_list(self, data):
        """control and transform data into a simple list"""

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

    def control_already_selection(self, list_participant, player):
        ''' checks if the player is in the list and answers true or false '''

        player_clean = self.control_type_function(self, player)
        for list in list_participant:
            for i in list:
                if player_clean.get("pk") == i.get("pk"):
                    valided = False
                    return valided
                else:
                    pass
        valided = True
        return valided

    def nunber_turn(self, turns, players_of_tournament, resultat_total, serialized_tournament, tour):
        ''' function that controls the course of laps from the 2nd ( by a loop) '''

        turn = turns - tour
        tour = tour
        for i in range(turn):
            tour += 1
            retour = Match.generation_next_round(Match(), players_of_tournament)
            list_matchs = retour[1]
            from tournament.controller import MethodeMatch
            list_match = MethodeMatch.display_list_matchs(MethodeMatch, list_matchs)
            from tournament.controller import MethodeTournament
            MethodeTournament.start_tournament(MethodeTournament)
            resultat_tournament = MethodeMatch.gestion_match(MethodeMatch(), list_match, resultat_total, tour)
            Tournament.save_resultat_tournament(Tournament, serialized_tournament, resultat_tournament)
        return resultat_tournament

    def tournaments_recovery(self, answer, tournaments):
        ''' manage the resumption of tournament and what turn it was '''

        players = []
        tournament = []
        serialized_tournament = []
        turn = 0
        for i in tournaments:
            if i.get("pk") == answer:
                serialized_tournament.append(i)
                players_brut = i.get("players")
                tournament.append(i.get("resultat"))
                for p in players_brut:
                    for k, v in p.items():
                        players.append(v)
        if tournament == [[]]:
            return players, serialized_tournament[0], turn
        else:
            for r in tournament:
                nb = len(r)
                if nb == 1:
                    turn = 1
                elif nb == 2:
                    turn = 2
                elif nb == 3:
                    turn = 3
            return players, serialized_tournament[0], turn

    def duplicate_search_player(self, new_player):  # TODO
        '''check ij the ID is not already referenced in the database '''

        players = Player.table_of_player(Player)
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
                else:
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
        ''' add players to the match and serialized them return the list of players '''

        player_of_tournament = []
        tour = 0
        for p in players:
            for i in p:
                tour += 1
                player = i
                point_tournament = 0
                match_win = 0
                match_lose = 0
                match_pat = 0
                serialized_players = {
                    "pk": player.get("pk"),
                    "ranking": player.get("ranking"),
                    "point_tournament": point_tournament,
                    "meet": [],
                    "match_win": match_win,
                    "match_lose": match_lose,
                    "match_pat": match_pat,
                }
                player_of_tournament.append(serialized_players)
        return player_of_tournament

    def generation_first_round(self, player_of_tournament):
        ''' generate the first matches then award points and update status
            match by players '''

        tri = sorted(player_of_tournament, key=lambda k: k["ranking"], reverse=True)
        nb_player = int(len(tri) / 2)
        list_player_a = tri[:nb_player]
        list_player_b = tri[nb_player:]
        list_match = []
        position = -1
        for i in range(TURNS):
            position += 1
            p1 = list_player_a[position]
            p2 = list_player_b[position]
            match = [p1, p2]
            list_match.append(match)
        return list_match

    def generation_next_round(self, player_of_tournament):
        ''' generates match pairs from the 2nd round '''

        list_player = []
        list_match = []
        tri_rank = sorted(player_of_tournament, key=lambda k: k["ranking"], reverse=True)
        tri_tour = sorted(tri_rank, key=lambda k: k["point_tournament"], reverse=True)
        position1 = -2
        position2 = -1
        t = 0
        for i in range(4):  # manage the matches
            t += 1
            position1 += 2
            position2 += 2
            joueur1 = tri_tour[position1]
            joueur2 = tri_tour[position2]
            answers = PlayMatch.find_player_already_play(PlayMatch, joueur1, joueur2, tri_tour, position2, list_player)
            player = answers[0]
            if player != joueur2:
                new_match = joueur1, player
                list_match.append(new_match)
            else:
                new_match = joueur1, joueur2
                list_match.append(new_match)
        return player_of_tournament, list_match

    def distribution_of_points_and_resultat_other_round(self, joueur1, joueur2, match, resultat_tour):
        '''distributed the points according to the player's result, is used to define the classification
            by tournament and thus to generate the peers'''

        joueur1["point_tournament"] = joueur1.get("point_tournament") + self.winner
        joueur1["match_win"] += 1
        joueur2["point_tournament"] = joueur2.get("point_tournament") + self.loser
        joueur2["match_lose"] += 1
        winner = joueur1.get("pk")
        resultat_tour.update({match: winner})
        return resultat_tour

    def distribution_of_points_and_resultat_pat_other_round(self, joueur1, joueur2, match, resultat_tour):
        '''distributed the points according to the player's result, is used to define the classification
            by tournament and thus to generate the peers'''

        joueur1["point_tournament"] = self.draw
        joueur1["match_pat"] += 1
        joueur2["point_tournament"] = self.draw
        joueur2["match_pat"] += 1
        winner = "pat match nul"
        resultat_tour.update({match: winner})
        return resultat_tour

    def distribution_of_points_and_resultat(self, joueur1, joueur2, match, resultat_tour1):
        '''distributed the points according to the player's result, is used to define the classification
            by tournament and thus to generate the peers'''

        joueur1["point_tournament"] = self.winner
        joueur1["match_win"] += 1
        joueur2["point_tournamant"] = self.loser
        joueur2["match_lose"] += 1
        winner = joueur1.get("pk")
        resultat_tour1.update({match: winner})
        return resultat_tour1

    def distribution_of_points_and_resultat_pat(self, joueur1, joueur2, match, resultat_tour1):
        '''distributed the points according to the player's result, is used to define the classification
            by tournament and thus to generate the peers'''

        joueur1["point_tournament"] = self.draw
        joueur1["match_pat"] += 1
        joueur2["point_tournament"] = self.draw
        joueur2["match_pat"] += 1
        winner = "pat match nul"
        resultat_tour1.update({match: winner})
        return resultat_tour1


# method used for the functioning of the matches
class PlayMatch:

    def find_player_already_play(self, joueur1, joueur2, tri_tour, position, list_player):
        ''' check if the player has already been selected '''

        list_player.append(joueur1.get("pk"))
        t = -1
        new_joueur = joueur2
        while new_joueur.get("pk") in joueur1.get("meet"):
            try:
                position += 2
                new_joueur = tri_tour[position]
            except IndexError:
                t += 2
                new_joueur = tri_tour[t]
            while new_joueur.get("pk") in list_player:
                try:
                    position += 2
                    new_joueur = tri_tour[position]
                except IndexError:
                    t += 2
                    new_joueur = tri_tour[t]
        new_player = new_joueur
        list_player.append(new_player.get("pk"))
        return new_player, list_player
