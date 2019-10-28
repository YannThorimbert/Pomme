import thorpy, pygame
import pomme

W_CARTE, H_CARTE = 100, 40
COULEUR_CARTE = 200,200,200
CARTE_FONT_SIZE = 20

couleur2texte = {"c":"<3", "p":">>", "l":"<>", "t":"*", "u":"?"}
couleur2couleur = {"c":(255,0,0), "l":(255,0,0), "p":(0,0,0), "t":(0,0,0), "u":(0,0,0)}
val2txt = {11:"J", 12:"Q", 13:"K", 14:"A", "-1":"?"}
def valeur2texte(valeur):
    if valeur < 0:
        return "??"
    elif valeur < 11:
        return str(valeur)
    else:
        return val2txt[valeur]

class Carte(pomme.Carte):

    def __init__(self, carte):
        self.carte = carte
##        texte = couleur2texte[carte.couleur] + "  " + valeur2texte(carte.valeur)
        texte = carte.couleur.capitalize()+valeur2texte(carte.valeur)
        self.e = thorpy.make_button(texte)
##        self.e.set_main_color()
        self.e.set_font_color(couleur2couleur[carte.couleur])
        self.e.set_font_size(CARTE_FONT_SIZE)
        self.e.set_size((W_CARTE, H_CARTE))
        self.e.user_func = carte_func_ui
        self.e.user_params = {"c":carte}
        self.texte = texte

    def __str__(self):
        return self.texte + " --- " + str(self.carte)


def carte_func_ui(c):
    print("CLICKED:", c.couleur, c.rang, c.points)
    ok = str(c) in [str(c2) for c2 in jeu.j_known[jeu.a_qui]]
    if not ok:
        print("Pas a ce joueur")
        return
    if jeu.choix_main.valeur > 0 and jeu.choix_reponse.valeur < 0:
        if not jeu.check_validity(jeu.a_qui, c):
            return
    a_la_main = False
    player = 0 if c in jeu.j_known[0] else 1
    if jeu.a_la_main == player:
        a_la_main = True
    i = jeu.j_known[player].index(c)
    jeu.choose_card_UI(player,i,a_la_main, show_anim_choose_response)
    show_jeu()
    if jeu.is_finished():
        thorpy.launch_blocking_alert("Fin du jeu", "Joueur 1 : "+str(jeu.s[1])+"\nJoueur 2 : "+str(jeu.s[2]))
    else:
        print("Joueur 1 : "+str(jeu.s[0])+"\nJoueur 2 : "+str(jeu.s[1]))
    for card in all_cartes:
        if str(card) in [str(c2) for c2 in jeu.j_known[jeu.a_qui]]:
            all_cartes[card].set_active(True)
        else:
            all_cartes[card].set_active(False)



def show_cards(x0, y0, cartes):
    i = 0
    x,y = x0, y0
    for i,c in enumerate(cartes):
        cui = all_cartes[str(c)]
        cui.set_topleft((x,y))
        if i == 3:
            cui.set_topleft((x,y+H_CARTE//2))
            x = x0
            y += H_CARTE + 10
        else:
            x += W_CARTE + 10

def show_jeu():
    for c in b.get_elements():
        c.set_topleft((-300,-300))
    show_cards(100, 100, jeu.j_known[0])
    show_cards(100, 400, jeu.j_known[1])
    show_choices()
    e_s1.stick_to("screen", "top", "top")
    e_s2.stick_to("screen", "bottom", "bottom")
    e_s1.set_text("Score j1 : " + str(jeu.s[0]))
    e_s2.set_text("Score j2 : " + str(jeu.s[1]))
    b.unblit_and_reblit()
    pygame.display.flip()

h1,h2 = 200,300
x1 = 600
def show_choices():
    #choix main ################################################################
    if jeu.choix_main.valeur < 0:
        e_none1.set_topleft((x1,h1))
    else:
        all_cartes[str(jeu.choix_main)].set_topleft((x1,h1))
    #choix reponse #############################################################
    if jeu.choix_reponse.valeur < 0:
        e_none2.set_topleft((x1,h2))
    else:
        all_cartes[str(jeu.choix_reponse)].set_topleft((x1,h2))

def show_anim_choose_response():
    if jeu.choix_main.valeur > 0 and jeu.choix_reponse.valeur > 0:
        c1 = all_cartes[str(jeu.choix_main)]
        c2 = all_cartes[str(jeu.choix_reponse)]
        c2.set_topleft((x1,h2))
        c1_loose = jeu.c1_looses(jeu.choix_main, jeu.choix_reponse)
        j1_main = jeu.a_la_main == 0
        if c1_loose and j1_main: #j1 loose ==> down
            sgn = 1
        elif c1_loose: #j1 win ==> up
            sgn = -1
        elif j1_main: #j1 win ==> up
            sgn = -1
        else:
            sgn = 1
        for i in range(30):
            c1.move((0,sgn*10))
            c2.move((0,sgn*10))
            b.unblit_and_reblit()
            pygame.display.flip()
            pygame.time.wait(20)


app = thorpy.Application((800,600), "Pomme d'API")


jeu = pomme.Jeu()
jeu.generate_initial_configuration(0)
jeu.set_atout("c")

all_cartes = {str(c):Carte(c).e for c in jeu.all_cartes}
all_cartes[str(pomme.unknown_carte)] = Carte(pomme.unknown_carte).e
all_cartes[str(pomme.unknown_carte)].set_main_color((100,100,100))
e_none1 = Carte(pomme.Carte("u",-1,-1)).e
e_none1.get_image().fill((50,)*3)
e_none2 = Carte(pomme.Carte("u",-1,-1)).e
e_none2.get_image().fill((50,)*3)
e_s1 = thorpy.make_text("Score j1 : 0 points")
e_s2 = thorpy.make_text("Score j2 : 0 points")

b = thorpy.Background(elements=[e_s1,e_s2,e_none1,e_none2]+list(all_cartes.values()))
show_jeu()
m = thorpy.Menu(b)
m.play()

app.quit()