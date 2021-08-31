
from tournament.view import ViewTournament
from model import CleanText


class ViewPlayer:

    def print_find_player(self):
        ''' printing the search request for a player then retrieving the choice '''

        print()
        print("recherche par ID ('non'_'premon'_'année de naissance') ou par nom:")
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
        ranking = player.get("ranking")
        if reponse == "oui":
            while ranking != int:
                try:
                    nb = int(input(": "))
                    ranking = nb
                    break
                except ValueError:
                    print("\nERREUR , veuillez entrer un nombre entier")
                    print("recomencez")
        print(ranking)
        if not ranking == int(player.get("ranking")):
            player.update({"ranking": ranking})
            print("nouveau total de points : " + str(player.get("ranking")) + "\n")
        print()
        return player

    def print_add_player(self):
        ''' function requesting the creation of a new player following a player creation
            and this as long as the users wants by answering yes '''

        serialized_player = []
        serialized_player.append(ViewTournament.print_elements_player(ViewTournament))
        print("voulez vous ajouter un autre joueur ?")
        reponse = CleanText.clean_input(CleanText, input())
        while reponse == "oui":
            serialized_player.append(ViewTournament.print_elements_player(ViewTournament))
            print("voulez vous ajouter un autre joueur ?")
            reponse = CleanText.clean_input(CleanText, input())
        return serialized_player

    def print_new_player_register(self):
        ''' display a message in console '''

        print("le joueur a été enregisté.")

    def print_modif_player(self, player):
        ''' function displaying all the elements of a player and allowing to retrieve
            the possible change and return a dictionary with these elements '''

        print("modifiez les valeurs que vous désirez à la suite de la valeur renseignée .")
        print("ou tapez ENTRER pour passer . \n")
        a = CleanText.clean_input(CleanText, input("nom :" + player.get("name") + " -> "))
        if not a == "":  # name change
            player.update({"name": a})
            print("nouveau nom : " + player.get("name") + "\n")
        b = CleanText.clean_input(CleanText, input("prénom :" + player.get("first_name") + " -> "))
        if not b == "":  # first_name change
            player.update({"first_name": b})
            print("nouveau prénom : " + player.get("first_name") + "\n")
        print("né.e le " + player.get("birth_date") + " , tapez oui pour modifer ->")
        reponse = CleanText.clean_input(CleanText, input())
        if reponse == "oui":
            from tournament.model import Tournament
            c = Tournament.print_date_controller(Tournament)
        else:
            c = ""
        if c == player.get("birth_date"):  # birth date change
            player.update({"birth_date": c})
            print("nouvelle date de naissance : " + player.get("birth_date") + "\n")
        print("sex : " + player.get("sex") + " , tapez oui pour modifier ->")
        reponse = CleanText.clean_input(CleanText, input())
        if reponse == "oui":
            d = ViewTournament.print_sex_control(ViewTournament)
        else:
            d = ""
        if d != player.get("sex"):  # sex change
            player.update({"sex": d})
            print("sex redéfini : " + player.get("sex") + "\n")
        print("total des points : " + str(player.get("ranking")) + " , tapez oui pour modifier -> ")
        reponse = CleanText.clean_input(CleanText, input())
        ranking = player.get("ranking")
        if reponse == "oui":
            while ranking != int:
                try:
                    nb = int(input(": "))
                    ranking = nb
                    break
                except ValueError:
                    print("\nERREUR , veuillez entrer un nombre entier")
                    print("recomencer")
        print(ranking)
        if not ranking == int(player.get("ranking")):  # ranking change
            player.update({"ranking": ranking})
            print("nouveau total de points : " + str(player.get("ranking")) + "\n")
        print()
        return player
