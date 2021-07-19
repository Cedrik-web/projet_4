from model import Player

def accueil():
    print()
    print("Bienvenue sur le gestionnaire de jeu d'échec .")
    print("Selectionner le menu souhaiter .")
    print(" 1 : ajouter un joueur .")
    print(" 2 : modification d'un joueur .")
    print(" 3 : création d'un tournoi .")
    print(" 4 : classements .")
    print(" 5 : modification du classements .")
    print(" 6 : rapports .")
    print("Quelle est votre choix : ")
    resultat = input()
    return resultat

def elements_player():
    print("entrer le nom du joueur")
    name = input()
    print("entrer le prénom du joueur")
    first_name = input()
    print("entrer la date de naissance du joueur comme ceci ../../....")
    birth_date = input()
    print("entrer le sex du joueur")
    sex = input()
    print("entrer les points du joueur")
    ranking = input()
    elements = {
        'name': name,
        'first_name': first_name,
        'birth_date': birth_date,
        'sex': sex,
        'ranking': ranking,
        }
    return elements

def add_player():
    serialized_player = []
    serialized_player.append(elements_player())
    print("voulez vous rajouter un autre joueur ?")
    reponse = input()
    while reponse == "oui":
        serialized_player.append(elements_player())
        print("voulez vous rajouter un autre joueur ?")
        reponse = input()
    return serialized_player

def modif_player():
    print()
    print("recherche par ID ('non'_'premon'_'année de naissance'):")
    print("recherche par nom:")
    resultat = input()
    return resultat
