
import readline


# user input control class
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

    def activate(self, players):
        ''' manage autocomplementation '''

        text = []
        for i in players:
            text.append(i.get("pk"))
        completer = MyCompleter(text)
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')
