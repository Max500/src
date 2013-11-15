'''
Created on 2013-11-13

@author: maximeblouin
'''
#! /usr/bin/env python
# -*- coding:Utf-8 -*-

"""
@file: tour.py
@author:  C. Besse

Fichier contenant la classe Tour
"""
from chess.plateau import plateau

class tour:
    """Une tour est une piece d'echec qui peut se deplacer selon les lignes et les colonnes"""
    
    def __init__(self,line,col,couleur):
        """Initialise une tour a la position (ligne,colonne) avec la bonne couleur 0 pour noir, 1 pour blanc"""
        self.pos = (line,col)
        self.color = couleur
    
    def deplacer(self,n_line,n_col,plateau):
        if self.deplacementValide(nouvPos,plateau):
            self.pos = nouvPos
        #else on ne change rien : on retourne la position courante
        #pour signifier que le changement a lieu... ou pas
        return self.pos
 
    def deplacementValide(self,pos_dep,pos_arr,plateau):
        pos_dep=self.pos
        pieceArr=plateau.getpiece(pos_arr[0],pos_arr[1])
        if pieceArr!=None and pieceArr.color==self.color:
            return False
        #deplacement sur la meme ligne
        if (pos_dep[0]==pos_arr[0]):
            depart=min(pos_dep[1]+1,pos_arr[1])
            arrivee=max(pos_dep[1]-1,pos_arr[1])
            #si une piece est sur le chemin, la tour ne peut pas passer
            for i in range (depart,arrivee):
                if plateau.getPiece(pos_dep[0],i) != None:
            plateau.getPiece(pos_dep[0],i).color == self.color:
                    return False
                
            return True
        #deplacement sur la meme colonne
        elif (pos_dep[1] == pos_arr[0]):
            depart=min(pos_dep[1]+1,pos_arr[1])
            arrivee=max(pos_dep[1]-1,pos_arr[1])  
            #si une piece est sur le chemin, la tour ne peut pas passer
            for i in range (depart,arrivee):
                if plateau.getPiece(pos_dep[0],i) != None:
            plateau.getPiece(pos_dep[0],i).color == self.color:
                return False              
        return True
    
    else: #on a essaye autre chose que les lignes et les colonnes...
        return False

#-----------------
# FIN CLASSE TOUR
#-----------------

def test_pos():
        from chess.plateau import Plateau
        p = Plateau()
        tn1 = p.getPiece(0,0)
        tn2 = p.getPiece(0,7)
        tb1 = p.getPiece(7,0)
        tb2 = p.getPiece(7,7)
        
        print(tn1.deplacer(0,3,p))
        p.damier[(0,3)] = tn1
        p.damier.pop((0,0))
        print(tn2.deplacer(0,4,p)) 
        p.damier[(0,4)] = tn2
        p.damier.pop((0,7))
        print(tb1.deplacer(0,3,p)) # ne fais rien
        print(tb1.deplacer(0,0,p))
        p.damier[(0,0)] = tb1
        p.damier.pop((7,0))
        print(tb1.deplacer(0,3,p)) # On mange !
        p.damier[(0,3)] = tb1
        p.damier.pop((0,0)) 
        print(tn2.deplacer(0,3,p)) # On mange !
        p.damier[(0,3)] = tn2
        p.damier.pop((0,4)) 
        print(tb2.deplacer(0,3,p)) # Ne fais rien
        print(p.damier)
        
if __name__ == "__main__":
    
    test_pos()     
    test_pos2()     
        
        
        