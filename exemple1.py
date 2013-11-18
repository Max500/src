#!/usr/bin/env python
import os,sys,random

class joueur(object):
    allsquares = [(x, y) for x in range(8) for y in range(8)]
    dullmoves = 0
    def __init__(self, colour, nom):
        self.colour   = colour
        self.nom     = nom
        self.can_castle_long_this_tour  = False
        self.can_castle_short_this_tour = False
        self.playedturns = 0
    def __str__(self):
            return self.nom+' as '+self.colour
    def set_adversaire(self, adversaire):
        self.adversaire = adversaire
    def getpieces(self, plateau):
        return [pos for pos in plateau if plateau[pos].colour is self.colour]
    def deplacementpossible(self, joueurspieces):
        return [pos for pos in self.allsquares if pos not in joueurspieces]
    def kingpos(self, plateau):
        for mine in self.getpieces(plateau):
            if plateau[mine].piecenom is 'k':
                return mine
    def deplacementValide(self, plateau):
        self.set_castling_flags(plateau)
        mypieces=self.getpieces(plateau)
        for mine in mypieces:
            for target in self.deplacementpossible(mypieces):
                if self.canmoveto(plateau, mine, target):
                    if not self.makesuscheck(mine, target, plateau):
                        yield (mine, target)
    def set_castling_flags(self, plateau):
        kingpos = self.kingpos(plateau)
        if self.king_can_castle(plateau, kingpos):
            if self.rook_can_castle_long(plateau, kingpos):
                self.can_castle_long_this_tour = True
            else:
                self.can_castle_long_this_tour = False
            if self.rook_can_castle_short(plateau, kingpos):
                self.can_castle_short_this_tour = True
            else:
                self.can_castle_short_this_tour = False
        else:
            self.can_castle_long_this_tour = False
            self.can_castle_short_this_tour = False
    def king_can_castle(self, plateau, kingpos):
        if plateau[kingpos].nrofmoves is 0 and not self.isincheck(plateau):
            return True
    def rook_can_castle_long(self, plateau, kingpos):
        if self.longrook in plateau and plateau[self.longrook].nrofmoves is 0:
            if self.hasclearpath(self.longrook, kingpos, plateau):
                tmptarget = (kingpos[0],kingpos[1]-1)
                if not self.makesuscheck(kingpos, tmptarget, plateau):
                    return True
    def rook_can_castle_short(self, plateau, kingpos):
        if self.shortrook in plateau and plateau[self.shortrook].nrofmoves is 0:
            if self.hasclearpath(self.shortrook, kingpos, plateau):
                tmptarget = (kingpos[0],kingpos[1]+1)
                if not self.makesuscheck(kingpos, tmptarget, plateau):
                    return True
    def getposition(self, move):
        startcol  = int(ord(move[0].lower())-97)
        startrow  = int(move[1])-1
        targetcol = int(ord(move[2].lower())-97)
        targetrow = int(move[3])-1
        start     = (startrow, startcol)
        target    = (targetrow, targetcol)
        return start, target
    def reacheddraw(self, plateau):
        if not list(self.deplacementValide(plateau)) and not self.isincheck(plateau):
            return True
        if len(list(self.getpieces(plateau))) == \
           len(list(self.adversaire.getpieces(plateau))) == 1:
            return True
        if joueur.dullmoves/2 == 50:
            if raw_input("Call a draw? (yes/no) : ") in ['yes','y','Yes']:
                return True
    def ischeckmate(self, plateau):
        if not list(self.deplacementValide(plateau)) and self.isincheck(plateau):
            return True
    def tour(self, plateau):
       
        tourstring = "\n%s's turn," % self.nom
        warning = " *** Your King is in check *** "
        if self.isincheck(plateau):
            tourstring = tourstring + warning
        return tourstring
    def getmove(self, plateau):
        print "\n"
        while True:
            move=raw_input("\nMake a move : ")
            if move == 'exit':
                break
            else:
                start, target = self.getposition(move)
                if (start, target) in self.deplacementValide(plateau):
                    return start, target
                else:
                    raise IndexError
    def makesuscheck(self, start, target, plateau):
        # Make temporary move to test for check
        self.domove(plateau, start, target)
        retval = self.isincheck(plateau)
        
        # Undo temporary move
        self.unmove(plateau, start, target)
        return retval
    def isincheck(self, plateau):
        kingpos = self.kingpos(plateau)
        for enemy in self.adversaire.getpieces(plateau):
            if self.adversaire.canmoveto(plateau, enemy, kingpos):
                return True
    def domove(self, plateau, start, target):
        self.savedtargetpiece = None
        if target in plateau:
            self.savedtargetpiece = plateau[target]
        plateau[target] = plateau[start]
        plateau[target].position = target
        del plateau[start]
        plateau[target].nrofmoves += 1
        if plateau[target].piecenom is 'p' and not self.savedtargetpiece:
            if abs(target[0]-start[0]) == 2:
                plateau[target].tour_moved_twosquares = self.playedturns
            elif abs(target[1]-start[1]) == abs(target[0]-start[0]) == 1:
                # Pawn has done en passant, remove the victim
                if self.colour is 'white':
                    passant_victim = (target[0]-1, target[1])
                else:
                    passant_victim = (target[0]+1, target[1])
                self.savedpawn = plateau[passant_victim]
                del plateau[passant_victim]
        if plateau[target].piecenom is 'k':
            if target[1]-start[1] == -2:
                # King is castling long, move longrook
                self.domove(plateau, self.longrook, self.longrook_target)
            elif target[1]-start[1] == 2:
                # King is castling short, move shortrook
                self.domove(plateau, self.shortrook, self.shortrook_target)
    def unmove(self, plateau, start, target):
        plateau[start] = plateau[target]
        plateau[start].position = start
        if self.savedtargetpiece:
            plateau[target] = self.savedtargetpiece
        else:
            del plateau[target]
        plateau[start].nrofmoves -= 1
        if plateau[start].piecenom is 'p' and not self.savedtargetpiece:
            if abs(target[0]-start[0]) == 2:
                del plateau[start].tour_moved_twosquares
            elif abs(target[1]-start[1]) == abs(target[0]-start[0]) == 1:
                # We have moved back en passant Pawn, restore captured Pawn
                if self.colour is 'white':
                    formerpos_passant_victim = (target[0]-1, target[1])
                else:
                    formerpos_passant_victim = (target[0]+1, target[1])
                plateau[formerpos_passant_victim] = self.savedpawn
        if plateau[start].piecenom is 'k':
            if target[1]-start[1] == -2:
                # King's castling long has been unmoved, move back longrook
                self.unmove(plateau, self.longrook, self.longrook_target)
            elif target[1]-start[1] == 2:
                # King's castling short has been unmoved, move back shortrook
                self.unmove(plateau, self.shortrook, self.shortrook_target)
    def pawnpromotion(self, plateau, target):
        promoteto = 'empty'
        while promoteto.lower() not in ['kn','q']:
            promoteto = \
            raw_input("You may promote your pawn:\n[Kn]ight [Q]ueen : ")
        plateau[target].promote(promoteto)
    def hasclearpath(self, start, target, plateau):
        startcol, startrow = start[1], start[0]
        targetcol, targetrow = target[1], target[0]
        if abs(startrow - targetrow) <= 1 and abs(startcol - targetcol) <= 1:
            # The base case
            return True
        else:
            if targetrow > startrow and targetcol == startcol:
                # Straight down
                tmpstart = (startrow+1,startcol)
            elif targetrow < startrow and targetcol == startcol:
                # Straight up
                tmpstart = (startrow-1,startcol)
            elif targetrow == startrow and targetcol > startcol:
                # Straight right
                tmpstart = (startrow,startcol+1)
            elif targetrow == startrow and targetcol < startcol:
                # Straight left
                tmpstart = (startrow,startcol-1)
            elif targetrow > startrow and targetcol > startcol:
                # Diagonal down right
                tmpstart = (startrow+1,startcol+1)
            elif targetrow > startrow and targetcol < startcol:
                # Diagonal down left
                tmpstart = (startrow+1,startcol-1)
            elif targetrow < startrow and targetcol > startcol:
                # Diagonal up right
                tmpstart = (startrow-1,startcol+1)
            elif targetrow < startrow and targetcol < startcol:
                # Diagonal up left
                tmpstart = (startrow-1,startcol-1)
            # If no pieces in the way, test next square
            if tmpstart in plateau:
                return False
            else:
                return self.hasclearpath(tmpstart, target, plateau)
    def canmoveto(self, plateau, start, target):
        startpiece = plateau[start].piecenom.upper()
        if startpiece == 'R' and not self.check_rook(start, target):
            return False
        elif startpiece == 'KN' and not self.check_knight(start, target):
            return False
        elif startpiece == 'P' and not self.check_pawn(start, target, plateau):
            return False
        elif startpiece == 'B' and not self.check_bishop(start, target):
            return False
        elif startpiece == 'Q' and not self.check_queen(start, target):
            return False
        elif startpiece == 'K' and not self.check_king(start, target):
            return False
        # Only the 'Knight' may jump over pieces
        if startpiece in 'RPBQK':
            if not self.hasclearpath(start, target, plateau):
                return False
        return True
    def check_rook(self, start, target):
        # Check for straight lines of movement(start/target on same axis)
        if start[0] == target[0] or start[1] == target[1]:
            return True
    def check_knight(self, start, target):
        # 'Knight' may move 2+1 in any direction and jump over pieces
        if abs(target[0]-start[0]) == 2 and abs(target[1]-start[1]) == 1:
            return True
        elif abs(target[0]-start[0]) == 1 and abs(target[1]-start[1]) == 2:
            return True
    def check_pawn(self, start, target, plateau):
        # Disable backwards and sideways movement
        if 'white' in self.colour and target[0] < start[0]:
            return False
        elif 'black' in self.colour and target[0] > start[0]:
            return False
        if start[0] == target[0]:
            return False
        if target in plateau:
            # Only attack if one square diagonaly away
            if abs(target[1]-start[1]) == abs(target[0]-start[0]) == 1:
                return True
        else:
            # Make peasants move only one forward (except first move)
            if start[1] == target[1]:
                # Normal one square move
                if abs(target[0]-start[0]) == 1:
                    return True
                # 1st exception to the rule, 2 square move first time
                if plateau[start].nrofmoves is 0:
                    if abs(target[0]-start[0]) == 2:
                        return True
            # 2nd exception to the rule, en passant
            if start[0] == self.enpassantrow:
                if abs(target[0]-start[0]) == 1:
                    if abs(target[1]-start[1]) == 1:
                        if target[1]-start[1] == -1:
                            passant_victim = (start[0], start[1]-1)
                        elif target[1]-start[1] == 1:
                            passant_victim = (start[0], start[1]+1)
                        if passant_victim in plateau and \
                        plateau[passant_victim].colour is not self.colour and \
                        plateau[passant_victim].piecenom is 'p'and \
                        plateau[passant_victim].nrofmoves == 1 and \
                        plateau[passant_victim].tour_moved_twosquares == \
                        self.playedturns-1:
                            return True
    def check_bishop(self, start, target):
        # Check for non-horizontal/vertical and linear movement
        if abs(target[1]-start[1]) == abs(target[0]-start[0]):
            return True
    def check_queen(self, start, target):
        # Will be true if move can be done as Rook or Bishop
        if self.check_rook(start, target) or self.check_bishop(start, target):
            return True
    def check_king(self, start, target):
        # King can move one square in any direction
        if abs(target[0]-start[0]) <= 1 and abs(target[1]-start[1]) <= 1:
            return True
        # ..except when castling
        if self.can_castle_short_this_tour:
            if target[1]-start[1] == 2 and start[0] == target[0]:
                return True
        if self.can_castle_long_this_tour:
            if target[1]-start[1] == -2 and start[0] == target[0]:
                return True
class Piece(object):
    def __init__(self, piecenom, position, joueur):
        self.colour    = joueur.colour
        self.piecenom = piecenom
        self.position  = position
        self.nrofmoves = 0
    def __str__(self):
        if self.colour is 'white':
            if self.piecenom is 'p':
                return 'WP'
            else:
                return self.piecenom.upper()
        else:
            return self.piecenom
    def canbepromoted(self):
        if str(self.position[0]) in '07':
            return True
    def promote(self, to):
        self.piecenom = to.lower()
class Game(object):
    def __init__(self, joueura, joueurb):
        self.plateau = dict()
        for joueur in [joueura, joueurb]:
            if joueur.colour is 'white':
                brow, frow = 0, 1
                joueur.enpassantrow = 4
            else:
                brow, frow = 7, 6
                joueur.enpassantrow = 3
            joueur.longrook  = (brow, 0)
            joueur.longrook_target = \
            (joueur.longrook[0], joueur.longrook[1]+3)
            
            joueur.shortrook = (brow, 7)
            joueur.shortrook_target = \
            (joueur.shortrook[0], joueur.shortrook[1]-2)
            
            [self.plateau.setdefault((frow,x), Piece('p', (frow,x), joueur)) \
            for x in range(8)]
            [self.plateau.setdefault((brow,x), Piece('r', (brow,x), joueur)) \
            for x in [0,7]]
            [self.plateau.setdefault((brow,x), Piece('kn',(brow,x), joueur)) \
            for x in [1,6]]
            [self.plateau.setdefault((brow,x), Piece('b', (brow,x), joueur)) \
            for x in [2,5]]
            self.plateau.setdefault((brow,3),  Piece('q', (brow,3), joueur))
            self.plateau.setdefault((brow,4),  Piece('k', (brow,4), joueur))
    def printplateau(self):
        topbottom=['*','a','b','c','d','e','f','g','h','*']
        sides=['1','2','3','4','5','6','7','8']
        tbspacer=' '*6
        rowspacer=' '*5
        cellspacer=' '*4
        empty=' '*3
        print
        for field in topbottom:
            print "%4s" % field,
        print
        print tbspacer+("_"*4+' ')*8
        for row in range(8):
            print(rowspacer+(('|'+cellspacer)*9))
            print "%4s" % sides[row],('|'),
            for col in range(8):
                if (row, col) not in self.plateau:
                    print empty+'|',
                else:
                    print "%2s" % self.plateau[(row, col)],('|'),
            print "%2s" % sides[row],
            print
            print rowspacer+'|'+(("_"*4+'|')*8)
        print
        for field in topbottom:
            print "%4s" % field,
        print "\n"
    def refreshscreen(self, joueur):
        if joueur.colour is 'white':
            joueura, joueurb = joueur, joueur.adversaire
        else:
            joueura, joueurb = joueur.adversaire, joueur
        os.system('clear')
        print "   Now playing: %s vs %s" % (joueura, joueurb)
        self.printplateau()
    def run(self, joueur):
        self.refreshscreen(joueur)
        while True:
            print joueur.tour(self.plateau)
            try:
                start, target = joueur.getmove(self.plateau)
            except (IndexError, ValueError):
                self.refreshscreen(joueur)
                print "\n\nPlease enter a valid move."
            except TypeError:
                # No start, target if user exit
                break
            else:
                if target in self.plateau or self.plateau[start].piecenom is 'p':
                    joueur.dullmoves = 0
                else:
                    joueur.dullmoves += 1
                joueur.domove(self.plateau, start, target)
                joueur.playedturns += 1
                # Check if there is a Pawn up for promotion
                if self.plateau[target].piecenom is 'p':
                    if self.plateau[target].canbepromoted():
                        joueur.pawnpromotion(self.plateau, target)
                joueur = joueur.adversaire
                if joueur.reacheddraw(self.plateau):
                    return 1, joueur
                elif joueur.ischeckmate(self.plateau):
                    return 2, joueur
                else:
                    self.refreshscreen(joueur)
    def end(self, joueur, result):
        looser = joueur.nom
        winner = joueur.adversaire.nom
        if result == 1:
            endstring = "\n%s and %s reached a draw." % (winner, looser)
        elif result == 2:
            endstring = "\n%s put %s in checkmate." % (winner, looser)
        os.system('clear')
        self.printplateau()
        return endstring
def newgame():
    os.system('clear')
    print """
      Please type in the nom of the contestants.
      If you want to play against the computer, leave one nom blank
      and press [Enter].
      """
    joueura, joueurb = getjoueurs()
    joueura.set_adversaire(joueurb)
    joueurb.set_adversaire(joueura)
    game = Game(joueura, joueurb)
    infostring = \
    """
    Very well, %s and %s, let's play.
    
    joueur A: %s (uppercase)
    joueur B: %s (lowercase)
    (Use moves on form 'a2b3' or type 'exit' at any time.) """
    print infostring % (joueura.nom, joueurb.nom, joueura, joueurb)
    raw_input("\n\nPress [Enter] when ready")
    # WHITE starts
    joueur = joueura
    try:
        result, joueur = game.run(joueur)
    except TypeError:
        # No result if user exit
        pass
    else:
        print game.end(joueur, result)
        raw_input("\n\nPress any key to continue")
def getjoueurs():
    nom1 = raw_input("\njoueur A (white): ")
    joueura = joueur('white', nom1)
    nom2 = raw_input("\njoueur B (black): ")
    joueurb = joueur('black', nom2)
    return joueura, joueurb
def main():
    """ Kickstart everything. Display menu after game has ended. """
    
    menu="""
    Thanks for playing the Chessmastah, would you like to go again?
    Press [Enter] to play again or type 'exit'.  >>  """
    try:
        while True:
            newgame()
            choice=raw_input(menu)
            if choice == 'exit':
                print "\nAs you wish. Welcome back!"
                break
    except KeyboardInterrupt:
        sys.exit("\n\nOkok. Aborting.")
if __name__ == '__main__':
    #cProfile.run('main()')
    main()