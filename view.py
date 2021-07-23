from model import clean_input


def accueil():
    ''' menu printing and retrieval of menu choice '''

    print()
    print("Bienvenue sur le gestionnaire de jeu d'échec .")
    print("Selectionner le menu souhaiter .")
    print(" 1 : ajouter un joueur .")
    print(" 2 : modification d'un joueur .")
    print(" 3 : création d'un tournoi .")
    print(" 4 : classements .")
    print(" 5 : modification du classements .")
    print(" 6 : rapports .")
    print(" 7 : sortir du logiciel .")
    print("Quelle est votre choix : ")
    resultat = input()
    return resultat

def elements_player():
    ''' retrieving player items and putting all items in dictionary '''

    print("entrer le nom du joueur")
    name = clean_input(input())
    print("entrer le prénom du joueur")
    first_name = clean_input(input())
    print("entrer la date de naissance du joueur comme ceci ../../....")
    birth_date = clean_input(input())
    print("entrer le sex du joueur")
    sex = clean_input(input())
    print("entrer les points du joueur")
    ranking = input()
    elements = {
        "name": name,
        "first_name": first_name,
        "birth_date": birth_date,
        "sex": sex,
        "ranking": ranking,
        }
    return elements

def add_player():
    ''' function requesting the creation of a new player
        following a player creation and this as long as the users
        wants by answering yes '''

    serialized_player = []
    serialized_player.append(elements_player())
    print("voulez vous rajouter un autre joueur ?")
    reponse = clean_input(input())
    while reponse == "oui":
        serialized_player.append(elements_player())
        print("voulez vous rajouter un autre joueur ?")
        reponse = clean_input(input())
    return serialized_player

def find_player():
    ''' printing the search request for a player then retrieving the
        choice '''

    print()
    print("recherche par ID ('non'_'premon'_'année de naissance'):")
    print("recherche par nom:")
    resultat = clean_input(input())
    print()
    return resultat

def modif_player(player):
    ''' function displaying all the elements of a player and
        allowing to retrieve the possible change and return a dictionary
        with these elements '''

    print("modifier les valeurs que vous désirez à la suite de la valeur renseigner .")
    print("ou taper entrer pour passer . \n")
    a = clean_input(input("nom :" + player.get("name") + " -> "))
    if not a == "":
        player.update({"name": a})
        print("nouveau nom : " + player.get("name") + "\n")
    b = clean_input(input("prénom :" + player.get("first_name") + " -> "))
    if not b == "":
        player.update({"first_name": b})
        print("nouveau prénom : " + player.get("first_name") + "\n")
    c = clean_input(input("né le : " + player.get("birth_date") + " -> "))
    if not c == "":
        player.update({"birth_date": c})
        print("nouvelle date de naissance : " + player.get("birth_date") + "\n")
    d = clean_input(input("sex : " + player.get("sex") + " -> "))
    if not d == "":
        player.update({"sex": d})
        print("sex redéfini : " + player.get("sex") + "\n")
    e = clean_input(input("total de points : " + player.get("ranking") + " -> "))
    if not e == "":
        player.update({"ranking": e})
        print("nouveau total de points : " + player.get("ranking") + "\n")
    print()
    return player

def error_enter_int():
    ''' indicates to the user that he must enter a number '''

    print("\n ERREUR : vous devez entrer un chiffre correspondant à votre choix .")

def display_player_list(player):
    ''' printing a list of players with the same name '''

    print(player.get("name"), player.get("first_name"))
    print("son ID est : ", player.get("pk"), "\n")

def display_player_nb(nb_player, player):
    ''' print the number of existing players for the search then return
        to the menu to make a new request with ID '''

    print("il y a ", nb_player, " resultat pour la recherche : ", player)
    print("veuillez utiliser ID du joueur ")

def modif_ok():
    ''' printing modification to carry out '''

    print("modification effectuer avec succès !")

def elements_tournament():
    print("entrer le nom du tournoi")
    name = clean_input(input())
    print("entrer le lieu du tournoi")
    location = clean_input(input())
    print("entrer la date du tournoi")
    date = clean_input(input())
    elements = {
        "name": name,
        "location": location,
        "date": date,
        }
    return elements

def add_players_for_tournament():
    print("rentrer l'ID ou le nom du joueur participant")
    participant = clean_input(input())
    return participant