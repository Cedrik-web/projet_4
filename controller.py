from view import accueil, add_player, find_player, modif_player, error_enter_int
from view import display_player_list, display_player_nb, modif_ok
from view import elements_tournament, elements_player
from model import save_player, add_players, table_of_player, modification_of_player
from model import add_tournament, gathers_tournament_dictionary, save_tournament

def menu():
    ''' menu distribution function '''

    resultat = accueil()
    try:
        resultat = int(resultat)
    except:
        error_enter_int()
        menu()
    if resultat == 1:
        player = add_player()
        serialized = add_players(player)
        save_player(serialized)
        menu()
    if resultat == 2:
        modif_menu()
    if resultat == 3:
        elements = elements_tournament()
        tournament = add_tournament(elements)
        players = add_players_of_tournament(tournament)
        serialized_tournament = gathers_tournament_dictionary(tournament, players)
        save_tournament(serialized_tournament)
    if resultat == 4:
        pass
    if resultat == 5:
        pass
    if resultat == 6:
        pass
    if resultat == 7:
        pass
    else:
        error_enter_int()
        menu()

def modif_menu():
    ''' allows you to search for the player to modify by name
        which returns a list of all the players with this name
        or by ID to directly select the player to modify '''

    resultat = find_player()
    players = table_of_player()
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
                        modif = modif_player(player)
                        modification_of_player(modif)
                        modif_ok()
                        menu()
                    else:
                        display_player_list(player)
        display_player_nb(len(nb_players), resultat)
        modif_menu()
    else:
        for player in players:
            for k, v in player.items():
                if v == resultat:
                    modif = modif_player(player)
                    modification_of_player(modif)
                    modif_ok()
                    menu()

def add_players_of_tournament(tournament):
    for i in tournament:
        tournoi = i
    participants = []
    table_players = table_of_player()
    nb_str = tournoi.get("nb_players")
    nb_int = int(nb_str)
    for i in range(nb_int):
        player = []
        print("rentrer l'ID ou le nom du joueur participant")
        resultat = input()
        for i in table_players:
            if resultat == i.get("pk"):
                player.append(i)
            elif resultat == i.get("name"):
                player.append(i)
        if len(player) == 1:
            participants.append(player)
            print("participant enregistrer ! \n")
        else:
            print("il y a ", len(player), "joueurs enregister")
            participant = []
            for i in player:
                print(resultat, i.get("first_name"), " = ", i.get("pk"))
                participant.append(i)
            print("rentrer l'ID du joueur participant ou + pour creer un joueur")
            resultat = input()
            if len(resultat) > 10:
                for i in participant:
                    if resultat == i.get("pk"):
                        participants.append(i)
                        print("participant enregister ! \n")
            else:
                elements = elements_player()
                new_participant = add_players(elements)
                save_player(new_participant)
                participants.append(new_participant)
                print("participant creer et enregistrer ! \n")
    return participants



