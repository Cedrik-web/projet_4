import readline

from tinydb import TinyDB
from tinydb.table import Document

from view import print_error_id
from player.view import print_elements_player, print_list_players_alphabet, print_new_player_register
from tournament.model import control_already_selection, table_of_tournament
from tournament.view import print_menu_ajout_players_fot_tournament, print_add_players_for_tournament, \
    print_save_players_for_tournament, print_add_players_for_tournament_new, print_add_player_impossible


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


def activate(players):
    ''' manage autocomplementation '''

    text = []
    for i in players:
        text.append(i.get("pk"))
    completer = MyCompleter(text)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')


# player model creation
class Player:

    def __init__(self, name, first_name, birth_date, sex=None, ranking=0):
        self.pk = name + "_" + first_name + "_" + birth_date[-4:]
        self.name = name
        self.first_name = first_name
        self.birth_date = birth_date
        self.sex = sex
        self.ranking = ranking


def add_players(players):
    ''' named parameters and serialization of players items '''

    serialized_player = []
    for i in players:
        new_player = i
        player = Player(
            name=new_player.get("name"),
            first_name=new_player.get("first_name"),
            birth_date=new_player.get("birth_date"),
            sex=new_player.get("sex"),
            ranking=new_player.get("ranking"),
        )
        serialized = {
            "pk": player.pk,
            "name": player.name,
            "first_name": player.first_name,
            "birth_date": player.birth_date,
            "sex": player.sex,
            "ranking": player.ranking,
        }
        serialized_player.append(serialized)
    return serialized_player


def save_player(serialized_player):
    ''' save players in the players table and save in the db.json file '''

    db = TinyDB("db.json")
    players_table = db.table("players")
    players_table.insert_multiple(serialized_player)


def table_of_player():
    ''' allows you to retrieve the players table from the db.json file '''

    db = TinyDB("db.json")
    players_table = db.table("players").all()
    return players_table


def modification_of_player(modif):
    ''' allows you to save changes to a player on db.json file '''

    players = table_of_player()
    db = TinyDB("db.json").table("players")
    for player in players:
        if player.get("pk") == modif.get("pk"):
            player_doc_id = player.doc_id
            db.upsert(Document(modif, doc_id=player_doc_id))


def duplicate_search(player):
    '''check ij the ID is not already referenced in the database '''

    players = table_of_player()
    nb_players = []
    valided = []
    no_valided = []
    dict = {"valided": valided,
            "no_valided": no_valided,
            }
    if len(player) > 1:
        for p in player:
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
            for p in player:
                for i in players:
                    if p.get("pk") == i.get("pk"):
                        no_valided.append(p)
                        break
                else:
                    valided.append(p)
        except:
            for i in players:
                for j in player:
                    if j == i.get("pk"):
                        no_valided.append(j)
                        break
            else:
                valided.append(j)
    return dict


def add_players_of_tournament(tournament):
    """ function to add players to the tournament
    access to the database or register a new player """

    players = table_of_player()
    retour_list = stat_classement()
    player_tri_alphabet = retour_list[1]
    nombre_de_tours = tournament[0].get("nb_players")
    participants = []
    compteur = 0
    for i in range(int(nombre_de_tours)):  # add all tournament players
        compteur += 1
        choix = print_menu_ajout_players_fot_tournament()
        if choix == 1:
            no_selection = False
            while no_selection == False:
                print_list_players_alphabet(player_tri_alphabet)
                activate(players)
                resultat = print_add_players_for_tournament()  # display the list of all players
                boucle = False
                while boucle == False:
                    for i in players:
                        if resultat == i.get("pk"):  # control if the player is not already recording
                            no_selection = control_already_selection(participants, i)
                            if no_selection == True:
                                participants.append(i)
                                print_save_players_for_tournament(compteur, nombre_de_tours)
                                boucle = True
                                break
                            else:
                                print_add_players_for_tournament_new()
                                boucle = True
                                break
                    else:
                        print_error_id()
                        resultat = print_add_players_for_tournament()
                        boucle = False
        elif choix == 2:  # create a new player and add player them to the tournament
            player = [print_elements_player()]
            add_player = add_players(player)
            player_valided = duplicate_search(add_player)
            seria = player_valided.get("valided")
            for s in seria:
                serialized_player = s
                if not serialized_player.get("pk") == None:
                    save_player([serialized_player])
                    print_new_player_register(serialized_player)
                    participants. append(serialized_player)
                    print_save_players_for_tournament(compteur, nombre_de_tours)
                    break
            ex = player_valided.get("no_valided")
            for i in ex:
                existing = i
                if not existing.get("pk") == None:
                    print_add_player_impossible(existing)
                    no_selection = control_already_selection(participants, i)
                    if no_selection == True:
                        participants.append(existing)
                        print_save_players_for_tournament(compteur, nombre_de_tours)
                        break
                    else:
                        print_add_players_for_tournament_new()
                        break
    return participants


def stat_classement():
    ''' returns a classification by rank or alphabetical '''

    players = table_of_player()
    tournaments = table_of_tournament()
    tri_rank = sorted(players, key=lambda k: k["ranking"], reverse=True)
    tri_alphabet = sorted(players, key=lambda k: k["pk"])
    player_tri_ranking = []
    player_tri_alphabet = []
    for i in tri_rank:
        player_tri_ranking.append(i)
    for j in tri_alphabet:
        player_tri_alphabet.append(j)
    return player_tri_ranking, player_tri_alphabet, tournaments