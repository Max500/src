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
        self.lp = [] #Car on a besoin d'une liste de coup possible
        pos_dep=self.pos
        pieceArr=plateau.getpiece(pos_arr[0],pos_arr[1])
        if pieceArr!=None and pieceArr.color==self.color:
            return False
        elif pos_dep and pos_arr in plateau:
            
            #Pour interdire les déplacements de cote et vers l'arriere
            if 'blanc' in self.colour and pos_arr[0] < pos_dep[0]:
                return False
            elif 'noir' in self.colour and pos_arr[0] > pos_dep[0]:
                return False
            elif pos_dep[0] == pos_arr[0]:
                return False
            #Pour les déplacements en diagonale immédiate pour manger d'autres pieces
            elif pos_arr in plateau:
                if abs(pos_arr[1]-pos_dep[1]) == abs(pos_arr[0]-pos_dep[0]) == 1:
                    return True
                #Manière non testé
                #elif self.pos + (1,1) != self.color:
                    #pos_arr == self.pos + (1,1)
                    #self.lp.append(pos_arr)
                    #return True
                #elif self.pos + (-1,1)!=self.color:
                    #pos_arr == self.pos + (-1,1)
                    #self.lp.append(pos_arr)
                    #return True
            #Pour tout autre coup, on ajoute la case d'après(+1 en y)
            else:
                if pos_dep[1] == pos_arr[1]:
                #Deplacement normal d'une case
                    if abs(pos_arr[0]-pos_dep[0]) == 1:
                        return True
                    #Regle du premier deplacement, mouvement de deux cases permis
                    elif 'noir' in self.color and pos[1]==6:
                        self.lp.append([0,self.pos[1]+1]) or self.lp.append([0,self.pos[1]+2]) #On ajoute 1 ou 2à la valeur verticale (y)
                        return True
                    elif 'blanc' in self.color and pos[1]==1:
                        self.lp.append([0,self.pos[1]-1]) or self.lp.append([0,self.pos[1]-2]) #On enlève 1 ou 2à la valeur verticale (y)
                        return True
                        if abs(pos_arr[0]-pos_dep[0]) == 2:
                            return True
            #Le pion ne peut pas passer par dessus les autres pieces
            for i in range (pos_dep[0],pos_arr[0]):
                if plateau.getPiece(pos_dep[0],i) != None:
                plateau.getPiece(pos_dep[0],i).color == self.color:
                    return False
    
    def promotionpion(self, plateau, target):
        prom = 'vide'
        while prom.lower() not in ['Ca','F', 'T', 'Re']:
            prom = \
            raw_input("Vous pouvez promouvoir votre pion en:\n[Ca]valier [Re]ine [T]our [F]ou  : ")
        plateau[target].promouvoir(prom)
        