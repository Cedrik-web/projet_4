
from view import ViewMenu


#  method used in the main menu class
class MethodeForMenu:

    def selection_tournament(self):
        ''' allows to select a tournament in the dictionary '''

        from tournament.model import Tournament
        tournaments = Tournament.table_of_tournament(Tournament)
        liste_tournoi = []
        for i in tournaments:
            ViewMenu.print_list_tournament(ViewMenu, i)
            liste_tournoi.append(i.get("pk"))
        choix = CleanText.clean_input(CleanText, ViewMenu.print_choice_tournament(ViewMenu))
        while choix not in liste_tournoi:
            ViewMenu.print_error_id(ViewMenu)
            choix = ViewMenu.print_choice_tournament(ViewMenu)
        else:
            for i in tournaments:
                if i.get("pk") == choix:
                    tournament = i
                    return tournament

    def rapport_player_list_of_tournament_by_ranking(self):
        '''generate the list of players of a shosen tournament and display by rank in order from
            largest to smallest'''

        tournament = self.selection_tournament(self)
        players = tournament.get("players")
        player_list = []
        for i in players:
            for k, v in i.items():
                player_list.append(v)
        tri_player_rank = sorted(player_list, key=lambda k: k["ranking"], reverse=True)
        ViewMenu.print_classement_of_tournament(ViewMenu)
        p = 0
        for i in tri_player_rank:
            p += 1
            ViewMenu.print_tri_player_of_tournament_rank(ViewMenu, i, p)
        ViewMenu.print_pass_validation(ViewMenu)

    def rapport_player_list_of_tournament_by_alphabetical(self):
        '''generate the list of players of a chosen tournament and display in
            alphabetical order'''

        tournament = self.selection_tournament(self)
        players = tournament.get("players")
        player_list = []
        for i in players:
            for k, v in i.items():
                player_list.append(v)
        tri_player_alphabet = sorted(player_list, key=lambda k: k["pk"])
        ViewMenu.print_classement_player_of_tournament(ViewMenu)
        for i in tri_player_alphabet:
            ViewMenu.print_tri_player_of_tournament_alphabet(ViewMenu, i)
        ViewMenu.print_pass_validation(ViewMenu)

    def rapport_all_rounds_of_tournament(self):
        '''generates a list of all the rounds of a selected tournament, displays the number
            of rounds and the playing time of each round'''

        tournament = self.selection_tournament(self)
        resultat = tournament.get("resultat")
        ViewMenu.print_list_tournaments(ViewMenu, tournament)
        t = 0
        for k, v in resultat.items():
            t += 1
            ViewMenu.print_tournament_time(ViewMenu, t)
            list_tour = v
            match = []
            resultat = []
            for k, v in list_tour.items():
                match.append(k)
                resultat.append(v)
            ViewMenu.print_tournament_resultat(ViewMenu, resultat)
            ViewMenu.print_space1(ViewMenu)
        ViewMenu.print_pass_validation(ViewMenu)

    def rapport_all_matches_of_tournament(self):
        '''generate the list of all matches and result of a selected tournament'''

        tournament = self.selection_tournament(self)
        resultat = tournament.get("resultat")
        ViewMenu.print_list_match_by_tournament(ViewMenu, tournament)
        t = 0

        for k, v in resultat.items():
            t += 1
            ViewMenu.print_resultat_match(ViewMenu, t)
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
                ViewMenu.print_list_resultat_match(ViewMenu, i, j)
            ViewMenu.print_space1(ViewMenu)
        ViewMenu.print_pass_validation(ViewMenu)


class CleanText:

    def clean_input(self, data):
        ''' general function to protect the program from incorrect user input '''

        tiny = data.lower()
        text = tiny.replace(" ", "-")
        char = "!#$%&*()"
        for i in char:
            text = text.replace(i, "")
        accent = "éèêë"
        for a in accent:
            text = text.replace(a, "e")
        accent_a = text.replace("à", "a")
        accent_u = accent_a.replace("ù", "u")
        new_data = accent_u
        return new_data
