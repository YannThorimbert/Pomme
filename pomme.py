import random

val2points = {10:10, 11:2, 12:3, 13:4, 14:11}
def valeur2points(v):
    if v < 10:
        return 0
    else:
        return val2points[v]

class Carte:

    def __init__(self, couleur, valeur, rang):
        self.couleur = couleur
        self.valeur = valeur
        self.rang = rang
        self.points = valeur2points(valeur)
        self.forcee = False

    def copy(self):
        c = Carte(self.couleur, self.valeur, self.rang)
        c.points = self.points
        c.forcee = self.forcee
        return c

    def set_as(self, other):
        self.couleur = other.couleur
        self.valeur = other.valeur
        self.rang = other.rang
        self.points = other.points
        self.forcee = other.forcee

    def __str__(self):
        return self.couleur+str(self.valeur)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.valeur==other.valeur and self.couleur==other.couleur


class Jeu:

    def __init__(self):
        self.j = [[], []]
        self.j_known  =[[], []]
        self.u = [None, None]
        self.a_qui = None #tells who's turn to choose a card
        self.a_la_main = None #tells who's the first to choose a card in this turn
        self.choix_main = None
        self.choix_reponse = None
        self.all_cartes = []
        self.s = [0,0]
        self.cartes_mangees = [[], []]
        self.atout = None


    def c1_looses(self, c1, c2):
        if c1.forcee:
            return True
        elif c2.forcee:
            return False
        if c1.couleur == self.atout:
            if c2.couleur != self.atout: #c1 est un atout et pas c2
                return False
            else:
                return c1.rang < c2.rang #c1 et c2 sont des atout
        elif c2.couleur == self.atout: #c2 est un atout et pas c1
            return True
        else:
            return c1.rang < c2.rang #ni c1 ni c2 ne sont des atouts

    def check_validity(self, player, c):
        assert self.a_la_main != player
        if c.couleur != self.choix_main.couleur:
            if c.couleur != self.atout:
                for c2 in self.j_known[player]:
                    if c2.couleur == self.choix_main.couleur:
                        print("Couleur invalide mais joueur ok")
                        return False
                c.forcee = True
        return True

    def generate_initial_configuration(self, i):
        self.atout = None
        self.cartes_mangees = [[], []]
        self.s = [0,0]
        self.u = [None, None]
        self.a_qui = i
        self.a_la_main = i
        self.choix_main = unknown_carte.copy()
        self.choix_reponse = unknown_carte.copy()
        self.all_cartes = [c.copy() for c in all_cartes]
        random.shuffle(self.all_cartes)
        self.j[0] = self.all_cartes[0:len(self.all_cartes)//2]
        self.j[1] = self.all_cartes[len(self.all_cartes)//2:]
        self.j_known[0] = self.j[0][0:7]
        self.j_known[1] = self.j[1][0:7]

    def set_atout(self, couleur):
        self.atout = couleur
        for c in self.all_cartes:
            if c.couleur == couleur:
                if c.valeur == 11: #valais
                    c.points = 20
                    c.rang = 1000
                elif c.valeur == 9:
                    c.points = 14
                    c.rang = 999

    def choose_card(self, player, i_card, a_la_main):
        c = self.j_known[player].pop(i_card)
        if len(self.j[player]) > 7:
            self.j_known[player].insert(i_card, unknown_carte.copy())
            self.u[player] = i_card
        if a_la_main:
            self.choix_main = c
            self.a_qui = int(not self.a_qui)
        else:
            self.choix_reponse = c
            self.compare_choices()
            self.discover_unknown_cards()

    def choose_card_UI(self, player, i_card, a_la_main, ui_func):
        c = self.j_known[player].pop(i_card)
        if len(self.j[player]) > 7:
            self.j_known[player].insert(i_card, unknown_carte.copy())
            self.u[player] = i_card
        if a_la_main:
            self.choix_main = c
            self.a_qui = int(not self.a_qui)
        else:
            self.choix_reponse = c
            ui_func()
            self.compare_choices()
            self.discover_unknown_cards()

    def compare_choices(self):
        print("Main avant", self.a_la_main)
        if self.c1_looses(self.choix_main, self.choix_reponse):
            self.a_la_main = int(not self.a_la_main) #invert value of a_la_main
        print("Main apres", self.a_la_main)
        print("combat", self.choix_main.points, self.choix_reponse.points)
        self.s[self.a_la_main] += self.choix_main.points
        self.s[self.a_la_main] += self.choix_reponse.points
        self.cartes_mangees[self.a_la_main].extend([self.a_la_main, self.choix_reponse])
        self.choix_main = unknown_carte
        self.choix_reponse = unknown_carte
        self.a_qui = self.a_la_main

    def discover_unknown_cards(self):
        if self.u[0] is not None and self.u[1] is not None:
            self.j_known[0][self.u[0]].set_as(self.j[0].pop())
            self.j_known[1][self.u[1]].set_as(self.j[1].pop())
            self.u = [None, None]

    def is_finished(self):
        return len(self.j_known[0]) == len(self.j_known[1]) == 0



COULEURS = ["c", "l", "p", "t"]
valeurs = list(range(6, 15))
rangs = {valeurs[i]:i for i in range(len(valeurs))}
unknown_carte = Carte("u", -1, -1)
all_cartes = []
for couleur in COULEURS:
    for valeur in valeurs:
        rang = rangs[valeur]
        all_cartes.append(Carte(couleur, valeur, rang))


