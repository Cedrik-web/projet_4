
from model import CleanText


class ViewPlayer:

    def print_find_player(self):
        ''' printing the search request for a player then retrieving the choice '''

        print()
        print("recherche par ID ('non'_'premon'_'année de naissance') ou par nom:")
        resultat = CleanText.clean_input(CleanText, input())
        return resultat

    def print_find_player_wrong(self):
        # displays information and retrieves an entry

        print("vous devez entrer un ID ou un nom.")
        resultat = CleanText.clean_input(CleanText, input())
        print()
        return resultat

    def print_display_player_list(self, player):
        ''' printing a list of players with the same name '''

        print(player.get("name"), player.get("first_name"))
        print("son ID est : ", player.get("pk"), "\n")

    def print_display_player_nb(self, nb_player, player):
        ''' print the number of existing players for the search then return
            to the menu to make a new request with ID '''

        print("il y a ", nb_player, " resultat pour la recherche : ", player)
        print("veuillez utiliser ID du joueur ")

    def print_modif_ok(self):
        ''' printing modification to carry out '''

        print("modification effectuée avec succès !")

    def print_modif_classement(self, player):
        ''' displays the rank of a player requesting and takes charge of the rank change then returns it '''

        print("total de points : " + str(player.get("ranking")) + " , tapez oui pour modifier -> ")
        reponse = CleanText.clean_input(CleanText, input())
        return reponse

    def print_modif_classement_input_error(self):
        # displays information

        print("\nERREUR , veuillez entrer un nombre entier")
        print("recomencez")

    def print_add_player(self):
        ''' function requesting the creation of a new player following a player creation
            and this as long as the users wants by answering yes '''

        print("\nvoulez vous ajouter un autre joueur ?")
        reponse = CleanText.clean_input(CleanText, input())
        print()
        return reponse

    def print_new_player_register(self):
        ''' display a message in console '''

        print("le joueur a été enregisté.")

    def print_exicting_player(self, existing):
        ''' display a message in console '''

        for i in existing:
            print()
            print("le joueur:", i.get("name"), i.get("first_name"), "est déjà enregistré.")
            input("appuyer sur entrée pour continuer ......")
            print("\n" * 20)

    def print_modif_player_name(self, player):
        ''' function displaying all the elements of a player and allowing to retrieve
            the possible change and return a dictionary with these elements '''

        print("modifiez les valeurs que vous désirez à la suite de la valeur renseignée .")
        print("ou tapez ENTRER pour passer . \n")
        a = CleanText.clean_input(CleanText, input("nom :" + player.get("name") + " -> "))
        return a

    def print_modif_player_name_anwser(self, player):
        # information for the modif player function

        print("nouveau nom : " + player.get("name") + "\n")

    def print_modif_player_first_name(self, player):
        # information for the modif player function

        b = CleanText.clean_input(CleanText, input("prénom :" + player.get("first_name") + " -> "))
        return b

    def print_modif_player_first_name_anwser(self, player):
        # information for the modif player function

        print("nouveau prénom : " + player.get("first_name") + "\n")

    def print_modif_player_birth_date(self, player):
        # information for the modif player function

        print("né.e le " + player.get("birth_date") + " , tapez oui pour modifer ->")
        reponse = CleanText.clean_input(CleanText, input())
        return reponse

    def print_modif_player_birth_date_answer(self, player):
        # information for the modif player function

        print("nouvelle date de naissance : " + player.get("birth_date") + "\n")

    def print_modif_player_sex(self, player):
        # information for the modif player function

        print("sex : " + player.get("sex") + " , tapez oui pour modifier ->")
        reponse = CleanText.clean_input(CleanText, input())
        return reponse

    def print_modif_player_sex_answer(self, player):
        # information for the modif player function

        print("sex redéfini : " + player.get("sex") + "\n")

    def print_modif_player_ranking(self, player):
        # information for the modif player function

        print("total des points : " + str(player.get("ranking")) + " , tapez oui pour modifier -> ")
        reponse = CleanText.clean_input(CleanText, input())
        return reponse

    def print_modif_player_ranking_new_input(self):
        # information for the modif player function

        nb = int(input(": "))
        return nb

    def print_modif_player_ranking_new_input_error(self):
        # information for the modif player function

        print("\nERREUR , veuillez entrer un nombre entier")
        print("recomencer")

    def print_modif_player_ranking_answer(self, player):
        # information for the modif player function

        print("\nnouveau total de points : " + str(player.get("ranking")))
