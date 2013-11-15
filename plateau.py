'''
Created on 2013-11-15

@author: maximeblouin
'''
#! /usr/bin/env python
# -*- coding:Utf-8 -*-

"""
@file: plateau.py
@author:  C. Besse

Fichier contenant la classe Tour
"""

from chess.tour import tour

class Plateau:
    
    def __init__(self):
        """Initialise le plateau avec un damier vide"""
        self.damier = {
                          #Pions blancs
                          (0,0):Tour(0,0,0),
                          (0,1):Cavalier(0,1,0),
                          (0,2):Fou(0,2,0),
                          (0,3):Dame(0,3,0),
                          (0,4):Roi(0,4,0),
                          (0,5):Fou(0,5,0),
                          (0,6):Cavalier(0,6,0),
                          (0,7):Tour(0,7,0),
                          (1,0):Pion(1,0,0),
                          (1,1):Pion(1,1,0),
                          (1,2):Pion(1,2,0),
                          (1,3):Pion(1,3,0),
                          (1,4):Pion(1,4,0),
                          (1,5):Pion(1,5,0),
                          (1,6):Pion(1,6,0),
                          (1,7):Pion(1,7,0),
                          #Pions noirs
                          (6,0):Pion(1,0,0),
                          (6,1):Pion(1,1,0),
                          (6,2):Pion(1,2,0),
                          (6,3):Pion(1,3,0),
                          (6,4):Pion(1,4,0),
                          (6,5):Pion(1,5,0),
                          (6,6):Pion(1,6,0),
                          (6,7):Pion(1,7,0),
                          (7,0):Tour(7,0,1), 
                          (7,7):Tour(7,7,1),
                          (7,1):Cavalier(7,1,1),
                          (7,6):Cavalier(7,6,1),
                          (7,2):Fou(7,2,1),
                          (7,5):Fou(7,5,1),
                          (7,4):Roi(7,4,1),
                          (7,5):Dame(7,4,1)

                      }

        
    def getPiece(self,line,col):
        """Retourne la piece a la position (line,col) ou None sinon"""
        return self.damier.get((line,col))
    
    def affichage(self):
           for i in range (0, 8):
                print(8-i, " ", end="")  # Imprime le num��ro de la ligne 
                for j in range (0, 8):
                    print("[ ] ", end="")  # Imprime les ��l��ments d'une ligne
                print("\n")
            print("    1   2   3   4   5   6   7   8")  # Imprime le num��ro des colones

tableau = Plateau()
tableau.affichage()

from chess.reine import reine

from chess.roi import roi

from chess.fou import fou

from chess.cavalier import cavalier

from chess.pion import pion

    def deplacement:
        pos_dep=piece.pos
        if pos_dep != pos_arr:
            del self.damier[piece.pos]
            
        
    