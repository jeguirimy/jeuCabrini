import pyxel, random


class PileMonstre:

    def __init__(self):
        self.valeurs = []

    def empiler(self, valeur):
        self.valeurs.append(valeur)

    def depiler(self):
        if self.valeurs:
            return self.valeurs.pop()

    def estVide(self):
        return len(self.valeurs) == 0

    def __str__(self):
        ch = ''
        for x in self.valeurs:
            ch = "|\t" + str(x) + "\t|" + "\n" + ch
        ch = "\nEtat de la pile:\n" + ch
        return ch

# On crée une classe pour le héros
class Heros :
    def __init__(self, x, y):

         # Définitions des attributs :vitesse et position initiale du héros
        self.x = x
        self.y = y
        self.vitesse= 1

        # on initiatlise le nombre de vies

    def draw(self) :
        # on charge le modèle de notre héros depuis notre fichier images
        #Change l'aspect tous les 1/10 de seconde, coef peut valoir 0,1 ou 2. Ca donne l'impression que notre monstre bouge
        coef = pyxel.frame_count //5% 3
        #pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8)
        pyxel.blt(self.x, self.y, 0, 16, 32, 8, 8)

    def deplacement(self) :
        """déplacement avec les touches de directions ou souris """
        if pyxel.mouse_x>0 and pyxel.mouse_x<120 and pyxel.mouse_y>0 and pyxel.mouse_y<120:
            self.x=pyxel.mouse_x
            self.y=pyxel.mouse_y
        else :
            if pyxel.btn(pyxel.KEY_RIGHT) and self.x < 120 :
                self.x += self.vitesse
            if pyxel.btn(pyxel.KEY_LEFT) and self.x>0:
                self.x += -self.vitesse
            if pyxel.btn(pyxel.KEY_DOWN) and self.y<120:
                self.y += self.vitesse
            if pyxel.btn(pyxel.KEY_UP) and self.y>0:
                self.y += -self.vitesse

# On crée une classe pour les monstres
class Monstre :
    def __init__(self, x, y,bi,xi,yi,th,tv) :
        self.x = x
        self.y = y
        self.bi = bi
        self.xi = xi
        self.yi = yi
        self.th = th
        self.tv = tv
        self.alive = True

    def draw(self):
        #Change l'aspect tous les 1/10 de seconde, coef peut valoir 0,1 ou 2. Ca donne l'impression que notre monstre bouge
        coef = pyxel.frame_count //3% 3

        #pyxel.blt(x, y, numéro banque, x(image), y(image), taille horizontale, taille verticale, [couleur de transparence])
        #pyxel.blt(self.x, self.y, 0, self.xi, self.yi + 4*coef,self.th,self.tv) # si on veut que ca bouge
        pyxel.blt(self.x, self.y, self.bi, self.xi, self.yi,self.th,self.tv)

    def deplacement(self):
        self.y += 1
        if  self.y>128:
            self.alive = False
            return True
        else :
            return False

# On crée une classe pour les tirs
class Tir :
    def __init__(self, x, y,bi,xi,yi,th,tv) :
        self.x = x
        self.y = y
        self.bi = bi
        self.xi = xi
        self.yi = yi
        self.th = th
        self.tv = tv
        self.alive = True

    def draw(self):
        pyxel.blt(self.x, self.y, self.bi, self.xi, self.yi,self.th,self.tv)

    def deplacement(self):
        self.y -= 1
        if  self.y < -8:
            self.alive = False

    def collision(self, monstre):
        """disparition d'un monstre et d'un tir si contact"""
        if monstre.x <= self.x+8 and monstre.x+8 >= self.x and monstre.y+8 >= self.y:
            self.alive = False
            return True
        else :
            return False

# la classe principale : jeu
class Jeu:
    def __init__(self):

        # taille de la fenetre 128x128 pixels
        pyxel.init(128, 128, title="Je suis un Héros !")

        # on crée un heros en instanciant la classe Heros
        self.heros = Heros(60, 60)
        self.pileMonstre=PileMonstre()

        #vies
        self.vies = 5
        self.vitesse= 1
        self.compteur = 0

        # initialisation des tirs
        self.tirs_liste = []

        # initialisation des monstres
        self.monstres_liste = []

        # initialisation des explosions
        self.explosions_liste=[]

        # liste des récompenses
        self.recompenses_liste=["vie","vie","vie","amelioration2","vitesse","amelioration1"]
        self.coffres_liste=[]
        self.amelioration1=False
        self.amelioration2=False


        # chargement des images des monstres, du héros qu'on a dessiné en pixel et de la musi
        pyxel.load("images.pyxres")
        pyxel.load("sons.pyxres", False, False, True, True)

        #Lancement de la musique
        pyxel.playm(0, loop=True)

        pyxel.run(self.update, self.draw)


    def tirs_creation(self):
        """création d'un tir avec la barre d'espace ou la souris, l''arme change en fonction du score """
        if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            #dans le cas basique le tir est simple
            if self.amelioration1==True :
                self.tirs_liste.append(Tir(self.heros.x+4, self.heros.y-8,0, 8, 0, 8, 8)) # tir double
            elif self.amelioration2==True :
                self.tirs_liste.append(Tir(self.heros.x+4, self.heros.y-8,0, 16, 0, 8, 8)) # tir étoile
            else  :
                self.tirs_liste.append(Tir(self.heros.x+4, self.heros.y-8,0, 8, 8, 8, 8)) # tir simple

    def tirs_deplacement(self):
        """déplacement des tirs vers le haut et suppression s'ils sortent du cadre"""
        for tir in  self.tirs_liste:
            tir.deplacement()
            if not tir.alive :
                self.tirs_liste.remove(tir)


    def monstres_creation(self):
        """création aléatoire des monstres"""
        # On appelle la classe monstre, pour créer 2 monstres. Un monstre par seconde
        if (pyxel.frame_count % 30 == 2):
           self.monstres_liste.append(Monstre(random.randint(0, 110),0, 0, 8, 48, 8, 8))
        if (pyxel.frame_count % 30 == 5):
           self.monstres_liste.append(Monstre(random.randint(0, 120),0, 0, 0, 72, 8, 8))



    def monstres_deplacement(self):
        for monstre in self.monstres_liste:
            monstre.deplacement()
            if not monstre.alive :
                self.monstres_liste.remove(monstre)



    # On supprime le monstre s'il est touché
    def monstres_suppression(self):
        for monstre in self.monstres_liste:
            for tir in self.tirs_liste:
                if tir.collision(monstre) and monstre in self.monstres_liste :
                        self.monstres_liste.remove(monstre)

                        # on ajoute l'explosion
                        self.explosions_creation(monstre.x, monstre.y)

                        #faire un compteur pour compter le nombre de monstres tués et on crée des positions de bonus sur la grille
                        self.compteur += 1
                        self.drop_coffre(random.randint(20, 110),random.randint(20, 120))


    def heros_suppression(self):
        """disparition d''une vie du héros et d'un monstre si contact"""
        for monstre in self.monstres_liste:
                if monstre.x <= self.heros.x+8 and monstre.y <= self.heros.y+8 and monstre.x+8 >= self.heros.x and monstre.y+8 >= self.heros.y:
                    self.monstres_liste.remove(monstre)
                    self.vies -= 1
                    # on ajoute l'explosion
                    self.explosions_creation(self.heros.y, self.heros.y)

    def explosions_creation(self, x, y):
        """explosions aux points de collision entre deux objets"""
        self.explosions_liste.append([x, y, 0])


    def explosions_animation(self):
        """animation des explosions"""
        for explosion in self.explosions_liste:
            explosion[2] +=1
            if explosion[2] == 12:
                self.explosions_liste.remove(explosion)

    # on crée une liste pour placer les bonus dans la grille
    def drop_coffre(self,x,y) :
        prob_coffre=random.randint(0,99)
        if prob_coffre < 20:
            self.coffres_liste.append([x,y])


    # si le heros touche le cadeau il récupère une récompense : soit des vies en plus, soit une amélioration de son arme, soit de la vitesse
    def recup_coffre(self):
        for coffre in self.coffres_liste:
            if coffre[0] <= self.heros.x+8 and coffre[1] <= self.heros.y+8 and coffre[0]+8 >= self.heros.x and coffre[1]+8 >= self.heros.y:
                self.coffres_liste.remove(coffre)
                recompense=random.randint(0,len(self.recompenses_liste)-1)

                if self.recompenses_liste[recompense]=="vie":
                    self.vies += 5

                elif self.recompenses_liste[recompense]=="vitesse":
                    self.recompenses_liste.remove("vitesse")
                    self.vitesse=self.vitesse*4

                elif self.recompenses_liste[recompense]=="amelioration1":
                     self.tirs_liste.append(Tir(self.heros.x+4, self.heros.y-8,0, 8, 0, 8, 8)) # tir double
                     self.recompenses_liste.remove("amelioration1")
                     self.amelioration1=True

                elif self.recompenses_liste[recompense]=="amelioration2":
                    self.tirs_liste.append(Tir(self.heros.x+4, self.heros.y-8,0, 16, 0, 8, 8)) # tir étoile
                    self.recompenses_liste.remove("amelioration2")
                    self.amelioration2=True




    # =====================================================
    # == UPDATE :met à jour les variables
    # =====================================================
    def update(self):
        """mise à jour des variables (30 fois par seconde)"""

        # deplacement du heros
        self.heros.deplacement()

        # creation des tirs en fonction de la position du heros
        self.tirs_creation()

        # mise a jour des positions des tirs
        self.tirs_deplacement()

        # creation des monstres
        self.monstres_creation()

        # mise a jour des positions des monstres
        self.monstres_deplacement()

        # suppression des monstres et tirs si contact
        self.monstres_suppression()

        # suppression du heros et monstre si contact
        self.heros_suppression()

        # evolution de l'animation des explosions
        self.explosions_animation()

        # suppression du coffre si contact
        self.recup_coffre()


    # =====================================================
    # == DRAW :crée et positionne les objets, elle permet de dessiner sur l’écran
    # =====================================================
    def draw(self):
        """création et positionnement des objets (30 fois par seconde)"""

        # vide la fenetre
        pyxel.cls(0)
        # si le héros possede des vies le jeu continue
        if self.vies > 0:

            # affichage des vies
            pyxel.text(5,5, 'VIES:'+ str(self.vies), 7)
            pyxel.text(5,15, 'SCORE:'+ str(self.compteur), 7)

            # Mon Personnage HEROS
            self.heros.draw()

            # tirs
            for tir in self.tirs_liste:
                tir.draw()

            # monstres
            #Monstre 1, appelle de la classe Monstre
            for monstre in self.monstres_liste:
                monstre.draw()


            #coffres pour les bonus
            for coffre in self.coffres_liste:
              pyxel.blt(coffre[0], coffre[1], 0, 8, 24, 8, 8)

            # explosions (cercles de plus en plus grands)
            for explosion in self.explosions_liste:
                pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3)

        # sinon: GAME OVER
        else:
            pyxel.text(45,64, 'GAME OVER', 7)
            pyxel.text(45,75, ' SCORE:'+ str(self.compteur), 7)



Jeu()