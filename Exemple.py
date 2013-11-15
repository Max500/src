#! /usr/bin/env python
# -*- coding:Utf-8 -*-
'''
Created on 2013-11-12

@author: maximeblouin
'''
# -*- coding: utf-8 -*-
 
from __future__ import print_function
 
###############################################################################
# fonctions utilitaires et constantes globales
 
NOIR  = 0
BLANC = 1
 
VIDE = None
 
SYMBOLE_PION = '*'
SYMBOLE_TOUR = 'T'
SYMBOLE_CAVALIER = 'C'
SYMBOLE_FOU = 'F'
SYMBOLE_REINE = '&'
SYMBOLE_ROI = '@'
 
COULEUR_SURLIGNE = '\033[7m'
COULEUR_STOP = '\033[0m'
 
def surligne(texte):
    """
    Surligne le texte dans la console (affiche en noir sur blanc)
    Fonctionne sur toutes les plate-formes
    (sous windows, il faut s'assurer que ansi.sys est activé)
 
    """
    return '{0}{1}{2}'.format(COULEUR_SURLIGNE, texte, COULEUR_STOP)
 
###############################################################################
 
class Piece(object):
    """
    Interface commune à toutes les pièces.
    Ne s'utilise pas directement.
 
    """
    def __init__(self, echiquier, couleur, symbole):
        """
        Construit une pièce.
        echiquier : echiquier sur lequel se trouve la pièce
        couleur : NOIR ou BLANC.
        symbole : caractère symbolisant la pièce.
         
        """
        self.__echiquier = echiquier
        self.__couleur = couleur
        self.__symbole = symbole
 
    def get_mouvements_possibles(self, pos_x, pos_y):
        """
        Retourne la liste des cases que peut atteindre la pièce sachant qu'elle
        se trouve actuellement en (pos_x, pos_y).
         
        """
        # return []
        raise NotImplementedError(
            "{0}.get_mouvements_possibles".format(self.nom)
            )
 
    def is_mouvement_possible(self, pos_x, pos_y, dest_x, dest_y):
        """
        Retourne True si la pièce, actuellement (pos_x, pos_y) peut se
        déplacer vers (dest_x, dest_y) en un tour.
 
        """
        # Il est possible, suivant le type de la pièce, d'utiliser des règles
        # de calcul plus efficaces que de parcourir linéairement la liste des
        # mouvements possibles...
        return (dest_x, dest_y) in self.get_mouvements_possibles(pos_x, pos_y)
 
    def get_attaques_possibles(self, pos_x, pos_y):
        """
        Retourne une liste des mouvements d'attaque possible.
        Concrêtement, la pièce peut se déplacer différemment quand elle attaque
        ou quand elle bouge simplement (le pion, par exemple).
        Cette méthode permet donc de retourner les cases sur lesquelles la
        pièce peut attaquer.
 
        """
        # cas général, la pièce attaque exactement comme elle bouge
        return self.get_mouvements_possibles(pos_x, pos_y)
 
    def is_attaque_possible(self, pos_x, pos_y, dest_x, dest_y):
        """
        True si la pièce peut attaquer la case dest_x, dest_y depuis pos_x,
        pos_y.
        False sinon.
        """
        return (dest_x, dest_y) in self.get_attaques_possibles(pos_x, pos_y)
 
    @property
    def nom(self):
        """
        Retourne le nom de la pièce sous forme de chaîne de caractères.
 
        Par exemple:
        >>> p = Reine()
        >>> p.nom
        'Reine'
        """
        return type(self).__name__
 
    @property
    def couleur(self):
        return self.__couleur
     
    def __str__(self):
        """
        Retourne une représentation de la pièce et de sa couleur sur un
        caractère (Noir sur blanc si la pièce est noire, blanc sur noir si la
        pièce est blanche).
        """
        return surligne(self.__symbole) if self.__couleur == NOIR \
                else self.__symbole
 
    def __repr__(self):
        return "Piece({0}, {1})".format(self.nom, self.couleur)
 
###############################################################################
# classes dérivées de Piece
 
class Tour(Piece):
    def __init__(self, echiquier, couleur):
        Piece.__init__(self, echiquier, couleur, SYMBOLE_TOUR)
 
class Pion(Piece):
    def __init__(self, echiquier, couleur):
        Piece.__init__(self, echiquier, couleur, SYMBOLE_PION)
 
class Cavalier(Piece):
    def __init__(self, echiquier, couleur):
        Piece.__init__(self, echiquier, couleur, SYMBOLE_CAVALIER)
 
class Fou(Piece):
    def __init__(self, echiquier, couleur):
        Piece.__init__(self, echiquier, couleur, SYMBOLE_FOU)
 
class Reine(Piece):
    def __init__(self, echiquier, couleur):
        Piece.__init__(self, echiquier, couleur, SYMBOLE_REINE)
 
class Roi(Piece):
    def __init__(self, echiquier, couleur):
        Piece.__init__(self, echiquier, couleur, SYMBOLE_ROI)
 
###############################################################################
 
POS_PIECES = [Tour, Cavalier, Fou, Roi, Reine, Fou, Cavalier, Tour]
 
class Echiquier(object):
    """
    Echiquier.
    Tient à jour l'échiquier de la partie : l'état du jeu
    """
    def __init__(self):
        """
        Initialise l'échiquier en plaçant les pièces à leur position initiale.
 
        """
        self.__plateau = [[VIDE for _ in range(8)] for _ in range(8)]
        # initialisation des pions
        for x in range(8):
            self.__plateau[x][0] = POS_PIECES[x](self, BLANC)
            self.__plateau[x][1] = Pion(self, BLANC)
            self.__plateau[x][6] = Pion(self, NOIR)
            self.__plateau[x][7] = POS_PIECES[7-x](self, NOIR)
 
        # ...
     
    def get(self, x, y):
        """
        Retourne la pièce à la position x, y
 
        """
        return self.__plateau[x][y]
 
    def put(self, piece, x, y):
        """
        Place une pièce à la position x, y
 
        """
        self.__plateau[x][y] = piece
 
    def libre(self, x, y):
        """
        retourne True si la case aux coordonnées (x, y) est libre
 
        """
        return self.piece_at(x, y) is VIDE
 
    def mouvement(self, pos_x, pos_y, dest_x, dest_y):
        """
        Bouge la pièce aux coordonnées pos_x, pos_y vers la position dest_x,
        dest_y.
 
        """
        if not self.libre(pos_x, pos_y):
            piece = self.get(pos_x, pos_y)
            if piece.is_mouvement_possible(pos_x, pos_y, dest_x, dest_y):
                self.put(piece, dest_x, dest_y)
                self.put(VIDE, pos_x, pos_y)
 
    def attaque(self, pos_x, pos_y, dest_x, dest_y):
        """
        Attaque la pièce en position (dest_x, dest_y) avec la pièce en position
        (pos_x, pos_y)
 
        """
        raise NotImplementedError('Plateau.attaque')
 
    def __str__(self):
        """
        Retourne une représentation de l'échiquier affichable dans la console.
 
        """
        str_plateau = ''
        for yc in range(23,-1,-1):
            y = yc // 3
            if yc % 3 == 1:
                str_plateau += ' ' + str(y+1) + '  '
            else:
                str_plateau += '    '
 
            for xc in range(48):
                x = xc // 6
                if xc % 6 == 2 and yc % 3 == 1:
                    piece = self.__plateau[x][y]
                    if piece is not None:
                        str_plateau += str(piece)
                    else:
                        str_plateau += surligne(' ') if (x + y) % 2 else ' '
                else:
                    str_plateau += surligne(' ') if (x + y) % 2 else ' '
            str_plateau += '\n'
        str_plateau += '\n      A     B     C     D     E     F     G     H\n'
        return str_plateau
 
###############################################################################
 
class Jeu(object):
    """
    Classe permettant de gérer une partie.
 
    """
    def __init__(self):
        """
        initialise une partie.
 
        """
        self.selection_x = -1
        self.selection_y = -1
        self.tour_actuel = BLANC
        self.echiquier = Echiquier()
        # ...
 
    def selectionner_piece(self, pos_x, pos_y):
        """
        Sélectionne la pièce avec laquelle jouer.
        Vérifie qu'elle appartient bien au joueur dont c'est le tour de
        jouer...
 
        """
        raise NotImplementedError("jeu.selectionner_piece")
 
    def jouer_case(self, pos_x, pos_y):
        """
        Joue la case (pos_x, pos_y) avec la pièce sélectionnée.
 
        """
        raise NotImplementedError("jeu.jouer_case")
 
    def verifier_echec_mat(self):
        """
        Vérifie si le joueur actuel est en position d'echec et mat.
        """
        raise NotImplementedError("jeu.verifier_echec_mat")
 
 
if __name__ == '__main__':
    ech = Echiquier()
    print(ech)
