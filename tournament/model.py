
from datetime import datetime
from tinydb import TinyDB
from tinydb.table import Document

from player.model import Player, MyCompleter
from settings import PLAYERS_OF_TOURNAMENT, TURNS
from tournament.view import ViewTournament


#  creation of the tournament class and manage tournaments
class Tournament(Player):

    def __init__(self, name, location, date):
        self.pk = name + "_" + location + "_" + date
        self.name = name
        self.location = location
        self.date = date
        self.turns = TURNS
        self.nb_players = PLAYERS_OF_TOURNAMENT
        self.resultat = []

    def add_players_of_tournament(self, tournament, players):
        """ function to add players to the tournament
        access to the database or register a new player """

        retour_list = self.stat_classement(self)
        player_tri_alphabet = retour_list[1]
        nombre_de_tours = tournament[0].get("nb_players")
        participants = []
        save_player = []
        compteur = 0
        for i in range(int(nombre_de_tours)):  # add all tournament players
            compteur += 1
            boucle = False
            while not boucle:
                choix = ViewTournament.print_menu_ajout_players_for_tournament(ViewTournament)
                if choix == 1:  # display player list by alphabetical order
                    try:
                        if len(player_tri_alphabet) != 0:
                            ViewTournament.print_list_players_alphabet(ViewTournament, player_tri_alphabet)
                            boucle = self.control_add_the_existing_player(self, players, participants, compteur,
                                                                          nombre_de_tours)
                    except ValueError:
                        ViewTournament.print_not_list_player_existing(ViewTournament)
                        self.create_and_add_new_player_of_tournament(self, participants, save_player, compteur,
                                                                     nombre_de_tours)
                        boucle = True
                elif choix == 2:  # create a new player and add player them to the tournament
                    self.create_and_add_new_player_of_tournament(self, participants, save_player, compteur,
                                                                 nombre_de_tours)
                    boucle = True
        return participants, save_player

    def print_date_controller(self):
        ''' control the input console for the birth date of the player '''

        day = ViewTournament.print_control_day(ViewTournament)
        month = ViewTournament.print_control_month(ViewTournament)
        year = ViewTournament.print_control_years(ViewTournament)
        day_str = str(day)
        month_str = str(month)
        if len(month_str) == 1:
            str_month = "0" + month_str
        else:
            str_month = str(month)
        if len(day_str) == 1:
            str_day = "0" + day_str
        else:
            str_day = str(day)
        birth_date = str_day + "/" + str_month + "/" + str(year)
        return birth_date

    def control_add_the_existing_player(self, players, participants, compteur, nombre_de_tours):
        '''check if the entry corresponds to an existing player'''

        MyCompleter.activate(MyCompleter, players)
        resultat = ViewTournament.print_add_players_for_tournament(ViewTournament)
        for i in players:  # control if the player is not already recording
            if resultat == i.get("pk"):
                no_selection = self.control_already_selection(self, participants, i)
                if no_selection:
                    participants.append(i)
                    ViewTournament.print_save_players_for_tournament(ViewTournament, compteur, nombre_de_tours)
                    break
                else:
                    ViewTournament.print_add_players_for_tournament_inpossible(ViewTournament)
                    ViewTournament.print_continue(ViewTournament)
                    return False
        else:
            ViewTournament.print_error_id_tournament(ViewTournament)
            return False

    def create_and_add_new_player_of_tournament(self, participants, save_player, compteur, nombre_de_tours):
        '''to create and add a new player in the tournament'''

        new_player = [ViewTournament.print_elements_player(ViewTournament)]
        add_player = Player.add_players(Player, new_player)
        player_valided = self.duplicate_search_player(self, add_player)
        seria = player_valided.get("valided")
        for s in seria:  # check if the player already exists
            serialized_player = s
            if not serialized_player.get("pk") is None:
                save_player.append(serialized_player)
                ViewTournament.print_new_player_register(ViewTournament)
                participants.append(serialized_player)
                ViewTournament.print_save_players_for_tournament(ViewTournament, compteur, nombre_de_tours)
                break
        ex = player_valided.get("no_valided")
        for i in ex:
            existing = i
            if not existing.get("pk") is None:
                ViewTournament.print_add_player_impossible(ViewTournament, existing)
                no_selection = self.control_already_selection(self, participants, i)
                if no_selection:
                    participants.append(existing)
                    ViewTournament.print_save_players_for_tournament(ViewTournament, compteur, nombre_de_tours)
                    break
                else:
                    ViewTournament.print_add_players_for_tournament_inpossible(ViewTournament)
                    ViewTournament.print_continue(ViewTournament)
                    break

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

    def start_tournament(self):
        ''' control the start of tournaments '''

        reponse = ViewTournament.print_start_tournament(ViewTournament)
        if reponse == "non":
            from controller import MainMenu
            MainMenu()
        else:
            pass

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

    def control_already_selection(self, list_participant, player):
        ''' checks if the player is in the list and answers true or false '''

        for i in list_participant:
            if player.get("pk") == i.get("pk"):
                valided = False
                return valided
        else:
            valided = True
            return valided

    def nunber_turn(self, turns, players_of_tournament, resultat_total, serialized_tournament, tour):
        ''' function that controls the course of laps from the 2nd ( by a loop) '''

        turn = turns - tour
        print("209", turn)
        print("210", players_of_tournament)
        tour = tour
        for i in range(turn):
            tour += 1
            retour = Match.generation_next_round(Match(), players_of_tournament)
            list_matchs = retour[1]
            list_match = Match.print_list_matchs(Match(), list_matchs)
            self.start_tournament(self)
            resultat_tournament = Match.gestion_match(Match(), list_match, resultat_total, tour)
            self.save_resultat_tournament(self, serialized_tournament, resultat_tournament)
        return resultat_tournament

    def tournament_find(self, TURNS, tournaments):
        ''' alows you to search among the tournaments which have ended
            which are in progress and those which have not started '''

        match = []
        tour = []
        end = []
        no_start = []
        start = []
        ViewTournament.print_find_tournament(ViewTournament)
        for i in tournaments:
            tour.append(i.get("resultat"))
            if tour == [[]]:
                match.append(i.get("pk"))
                no_start.append(i)
                tour.clear()
            else:
                for t in tour:
                    nb_turns = (len(t))
                    if nb_turns == TURNS:
                        end.append(i)
                        tour.clear()
                    else:
                        match.append(i.get("pk"))
                        start.append(i)
                        tour.clear()
        for i in end:
            ViewTournament.print_tournament_finished(ViewTournament, i)
        ViewTournament.print_space(ViewTournament)
        for i in no_start:
            ViewTournament.print_tournament_not_start(ViewTournament, i)
        for i in start:
            ViewTournament.print_tournament_start(ViewTournament, i)
        ViewTournament.print_space(ViewTournament)
        reponse = ViewTournament.print_input_selection_tournament(ViewTournament)
        return reponse

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
        for i in players:
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

    def generation_first_round(self, player_of_tournament, turns):
        ''' generate the first matches then award points and update status
            match by players '''

        tri = sorted(player_of_tournament, key=lambda k: k["ranking"], reverse=True)
        nb_player = int(len(tri) / 2)
        list_player_a = tri[:nb_player]
        list_player_b = tri[nb_player:]
        list_match = []
        position = -1
        for i in range(turns):
            position += 1
            p1 = list_player_a[position]
            p2 = list_player_b[position]
            match = [p1, p2]
            list_match.append(match)
        return list_match

    def print_list_matchs(self, list_match):
        ''' show match list request '''

        m = 0
        for list in list_match:
            m += 1
            ViewTournament.print_view_match_possition(ViewTournament, m)
            for i in list:
                ViewTournament.print_view_match(ViewTournament, i)
        return list_match

    def play_first_turn(self, list_match):
        ''' play the first round of the tournament '''

        resultat_total = {}
        resultat_tour1 = {}
        date_start = datetime.now()
        date = str(date_start)
        resultat_tour1.update({"debut round": date})
        ViewTournament.print_start_chrono(ViewTournament, date)
        for i in list_match:
            joueur1 = i[0]
            joueur2 = i[1]
            match = joueur1.get("pk") + " / " + joueur2.get("pk")
            resultat = ViewTournament.print_menu_match_tournament(ViewTournament, match, joueur1, joueur2)
            joueur1["meet"] = [joueur2.get("pk")]
            joueur2["meet"] = [joueur1.get("pk")]
            if resultat == 1:
                resultat_tour1 = self.distribution_of_points_and_resultat(joueur1, joueur2, match, resultat_tour1)
            elif resultat == 2:
                resultat_tour1 = self.distribution_of_points_and_resultat(joueur2, joueur1, match, resultat_tour1)
            elif resultat == 3:
                resultat_tour1 = self.distribution_of_points_and_resultat_pat(joueur1, joueur2, match, resultat_tour1)
            else:
                ViewTournament.print_error(ViewTournament)
        ViewTournament.print_ending_first_round(ViewTournament)
        date_end = datetime.now()
        date = str(date_end)
        resultat_tour1.update({"fin round": date})
        resultat_total.update({"round 1": resultat_tour1})
        ViewTournament.print_ending_chrono(ViewTournament, date)
        return resultat_total

    def distribution_of_points_and_resultat(self, joueur1, joueur2, match, resultat_tour1):
        '''distributed the points according to the player's result, is used to define the classification
            by tournament and thus to generate the peers'''

        ViewTournament.print_player_winner(ViewTournament, joueur1)
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

        ViewTournament.print_player_pat(ViewTournament)
        joueur1["point_tournament"] = self.draw
        joueur1["match_pat"] += 1
        joueur2["point_tournament"] = self.draw
        joueur2["match_pat"] += 1
        winner = "pat match nul"
        resultat_tour1.update({match: winner})

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
            answers = Match.find_player_already_play(self, joueur1, joueur2, tri_tour, position2, list_player)
            player = answers[0]
            if player != joueur2:
                new_match = joueur1, player
                list_match.append(new_match)
            else:
                new_match = joueur1, joueur2
                list_match.append(new_match)
        return player_of_tournament, list_match

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

    def gestion_match(self, list_match, resultat_total, tour):
        ''' play rounds matches from the 2nd round '''

        resultat_tour = {}
        date_start = datetime.now()
        date = str(date_start)
        resultat_tour.update({"debut round": date})
        ViewTournament.print_start_chrono(ViewTournament, date)
        for i in list_match:
            joueur1 = i[0]
            joueur2 = i[1]
            match = joueur1.get("pk") + " / " + joueur2.get("pk")
            resultat = ViewTournament.print_menu_match_tournament(ViewTournament, match, joueur1, joueur2)
            joueur1["meet"] += [joueur2.get("pk")]
            joueur2["meet"] += [joueur1.get("pk")]
            if resultat == 1:
                resultat_tour = self.distribution_of_points_and_resultat_other_round(joueur1, joueur2, match,
                                                                                     resultat_tour)
            elif resultat == 2:
                resultat_tour = self.distribution_of_points_and_resultat_other_round(joueur2, joueur1, match,
                                                                                     resultat_tour)
            elif resultat == 3:
                resultat_tour = self.distribution_of_points_and_resultat_pat_other_round(joueur1, joueur2, match,
                                                                                         resultat_tour)
            else:
                ViewTournament.print_error(ViewTournament)
        ViewTournament.print_ending_other_round(ViewTournament, tour)
        date_end = datetime.now()
        date = str(date_end)
        resultat_tour.update({"fin round": date})
        ViewTournament.print_ending_chrono(ViewTournament, date)
        resultat_total.update({"round " + str(tour): resultat_tour})
        return resultat_total

    def distribution_of_points_and_resultat_other_round(self, joueur1, joueur2, match, resultat_tour):
        '''distributed the points according to the player's result, is used to define the classification
            by tournament and thus to generate the peers'''

        ViewTournament.print_player_winner(ViewTournament, joueur1)
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

        ViewTournament.print_player_pat(ViewTournament)
        joueur1["point_tournament"] = joueur1.get("point_tournament") + self.draw
        joueur1["match_pat"] += 1
        joueur2["point_tournament"] = joueur2.get("point_tournament") + self.draw
        joueur2["match_pat"] += 1
        winner = "pat match nul"
        resultat_tour.update({match: winner})
        return resultat_tour
