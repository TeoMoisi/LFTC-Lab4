class Grammar:
    def __init__(self):
        self.N = []  # non-terminals list
        self.E = []  # terminals list
        self.P = {}  # productions dictionary
        self.S = None  # starting symbol

    def read_grammar_file(self, file):
        f = open(file, "r")

        self.N = f.readline().strip("\n").split(",")
        self.E = f.readline().strip("\n").split(",")
        self.S = f.readline().strip("\n")
        self.P = {}

        line = f.readline().strip("\n")
        i = 0
        while line != "":
            line = line.split("->")
            if line[0] not in self.P:
                self.P[line[0]] = []
            rhs = line[1].split("|")
            for elem in rhs:
                self.P[line[0]].append((elem, i))
                i += 1
            line = f.readline().strip("\n")

    def get_productions_for_non_terminal(self, non_terminal):
        if non_terminal not in self.P:
            return None
        return self.P[non_terminal]
