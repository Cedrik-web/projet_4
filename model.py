
from tournament.model import table_of_tournament



def clean_input(data):
    ''' general function to protect the program from
        incorrect user input '''

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


# class that supports text autocomplementation
class MyCompleter(object):  # Custom completer

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options
                                if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]
        # return match indexed by state
        try:
            return self.matches[state]
        except IndexError:
            return None


def selection_tournament():
    ''' allows to select a tournament in the dictionary '''

    tournaments = table_of_tournament()
    liste_tournoi = []
    for i in tournaments:
        print("ID du tournoi :", i.get("pk"))
        liste_tournoi.append(i.get("pk"))
    print("\nchoisis ton tournoi par l'ID")
    choix = input()
    while not choix in liste_tournoi:
        print("ERREUR vous avez mal saisie l'ID, reconnencer")
        choix = input()
    else:
        for i in tournaments:
            if i.get("pk") == choix:
                tournament = i
                return tournament


def tournament_find(TURNS):
    ''' alows you to search among the tournaments which have ended
        which are in progress and those which have not started '''

    tournaments = table_of_tournament()
    match = []
    tour = []
    end = []
    no_start = []
    start = []
    print("\nrecherche des tournois créer et non finaliser.\n")
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
        print("tournoi fini :", "le", i.get("name"), "de", i.get("location"), "du", i.get("date"))
    print()
    for i in no_start:
        print("tournoi non commencer voici leurs ID :", i.get("pk"))
        print(" - ", i.get("pk"))
    for i in start:
        print("tournoi non finaliser voici leurs ID :")
        print(" - ", i.get("pk"))
    print()
    reponse = input("entre l'ID ou appuie entrer pour sortir de la selection: ")
    return reponse


def tournaments_recovery(answer):
    ''' mamage the resumption of tournament and what turn it was '''

    tournaments = table_of_tournament()
    players = []
    tournament = []
    turn = 0
    for i in tournaments:
        if i.get("pk") == answer:
            serialized_tournament = i
            players_brut = i.get("players")
            tournament.append(i.get("resultat"))
            for p in players_brut:
                for k, v in p.items():
                    players.append(v)
    if tournament == [[]]:
        return players, serialized_tournament, turn
    else:
        for r in tournament:
            nb = len(r)
            if nb == 1:
                turn = 1
            elif nb == 2:
                turn = 2
            elif nb == 3:
                turn = 3
    return players, serialized_tournament, turn

