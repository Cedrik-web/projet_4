
from tinydb import TinyDB
from tinydb.table import Document


# player model creation
class Player:

    def __init__(self, name, first_name, birth_date, sex, ranking=0):
        self.pk = name + "_" + first_name + "_" + birth_date[-4:]
        self.name = name
        self.first_name = first_name
        self.birth_date = birth_date
        self.sex = sex
        self.ranking = ranking

    def add_players(self, players):
        ''' named parameters and serialization of players items '''

        from tournament.model import PlayTournament
        new_player = PlayTournament.control_type_function_list(PlayTournament, players)
        serialized_player = []
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

    def save_player(self, serialized_player):
        ''' save players in the players table and save in the db.json file '''

        db = TinyDB("db.json")
        players_table = db.table("players")
        players_table.insert_multiple(serialized_player)

    def table_of_player(self):
        ''' allows you to retrieve the players table from the db.json file '''

        db = TinyDB("db.json")
        players_table = db.table("players").all()
        return players_table

    def modification_of_player(self, modif):
        ''' allows you to save changes to a player on db.json file '''

        players = self.table_of_player(self)
        db = TinyDB("db.json").table("players")
        for player in players:
            if player.get("pk") == modif.get("pk"):
                player_doc_id = player.doc_id
                db.upsert(Document(modif, doc_id=player_doc_id))


# useful method for the player
class MethodePlayer:

    def duplicate_search(self, player):
        '''check ij the ID is not already referenced in the database '''

        players = Player.table_of_player(Player)
        nb_players = []
        valided = []
        no_valided = []
        dict = {"valided": valided, "no_valided": no_valided}
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
            except TypeError:
                for i in players:
                    for j in player:
                        if j == i.get("pk"):
                            no_valided.append(j)
                            break
                else:
                    valided.append(j)
        return dict

    def stat_classement(self):
        ''' returns a classification by rank or alphabetical '''

        players = Player.table_of_player(Player)
        tri_rank = sorted(players, key=lambda k: k["ranking"], reverse=True)
        tri_alphabet = sorted(players, key=lambda k: k["pk"])
        player_tri_ranking = []
        player_tri_alphabet = []
        for i in tri_rank:
            player_tri_ranking.append(i)
        for j in tri_alphabet:
            player_tri_alphabet.append(j)
        return player_tri_ranking, player_tri_alphabet
