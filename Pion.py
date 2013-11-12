#! /usr/bin/env python
# -*- coding:Utf-8 -*-

'''
Created on 2013-11-08

@author: maximeblouin
'''

class Pion:
    '''Le pion se déplace vers l'avant d'une seule case à la fois, à l'exception du premier coup où il peut se deplacer de deux cases vers l'avant. Ce pion mange les autres pièces en diagonale directe vers l'avant.'''
        
    def __init__(self,x,y,couleur):
        '''Initialise un pion à la position (ligne,colonne) avec la bonne couleur 0 pour noir, 1 pour blanc'''
        self.pos = (x,y)
        self.color = couleur
        
    def deplacer(self,n_x,n_y,plateau):
        if self.deplacementValide(nouvPos,plateau):
            self.pos = nouvPos
        #else on ne change rien : on retourne la position courante
        #pour signifier que le changement a lieu... ou pas
        return self.pos

    def deplacementValide(self,pos_dep,pos_arr,plateau):
        '''La fonction permet de d'afficher les déplacements possibles d'un pion'''
        self.lp = [] #Car on a besoin d'une liste
        pos_dep=self.pos
        pieceArr=plateau.getpiece(pos_arr[0],pos_arr[1])
        if pieceArr!=None and pieceArr.color==self.color:
            return False
        #Pour le premier coup
        elif color==noir and y==6:
            self.lp.append([0,1]) #On ajoute 1 à la valeur verticale (y)
            self.lp.append([0,2]) #On ajoute 2 à la valeur verticale (y)      
        elif color==blanc and y==1:
            self.lp.append([0,-1]) #On enlève -1 à la valeur verticale (y)
            self.lp.append([0,-2]) #On enlève -2 à la valeur verticale (y)
        #Pour tout autre coup, on ajoute la case d'après(+1 en y)
        else:
            self.lp.append([0,y+1])
        
        #Pour les déplacements en diagonale pour manger d'autre pion
        if pieceArr!=None and pieceArr.color!=self.color:
        return self.lp #On retourne cette liste de coordonée possible
        
        
        
            for i in range (depart,arrivee):
                if plateau.getPiece(pos_dep[0],i) != None:
                plateau.getPiece(pos_dep[0],i).color == self.color:
                    return False
        #Pour les autres coups
        if
        
        
        
            for i in range (depart,arrivee):
                if plateau.getPiece(pos_dep[0],i) != None:
                plateau.getPiece(pos_dep[0],i).color == self.color:
                    return False
        
        
        
        else: #On a essaye un autre mouvement que d'avancer de un, de deux au premier coup ou bien de manger en diagonale
            return False
        
        