"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the
Alien Invaders game.  Instances of Wave represent a single wave.  Whenever you
move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a
complicated issue.  If you do not know, ask on Piazza and we will answer.

# Nick Veszelovits  nav7
# 12/6/2018
"""
from game2d import *
from consts import *
from models import *
import app
import random
import time

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
#permitted
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you should create a NEW instance of Wave
    (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This class
    will be similar to than one in how it interacts with the main class
    Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien
                 or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly
                 empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]


    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in class Invaders. It is okay if you do, but you
    MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter
    for any attribute that you need to access in Invaders.  Only add the getters
    and setters that you need for Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example,
    may want to keep track of the score.  You also might want some label objects
    to display the score and number of lives. If you make changes, please list
    the changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _aliendir: the direction the aliens are marching, 0 for right 1 for left
                   [int >=0, <=1]
        _boltsteps: number of alien steps till they fire a bolt [int >=0,
                    <=BOLT_RATE]
        _aliensbelow: True if an alien get below the defense line, False
                     otherwise [bool]
        _noaliens: True if all aliens are shot, False otherwise [bool]
        _score: Score of Game. Increases by 100 for each alien shot. [int >=0]
        _speed: How many seconds between alien steps [0 < float <= 1]
            """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getlives(self):
        """
        Returns self._lives
        """
        return self._lives

    def setlives(self, value):
        """
        Sets self._lives to value

        Parameter value: the value self._lives is set to
        Precondition: value is 0 <= int <= SHIP_LIVES
        """
        self._lives = value

    def getship(self):
        """
        Returns self._ship
        """
        return self._ship

    def setship(self, value):
        """
        Sets self._ship to value

        Parameter value: the value self._ship is set to
        Precondition: value is a Ship object
        """
        self._ship = value

    def getaliensbelow(self):
        """
        Returns self._aliensbelow
        """
        return self._aliensbelow

    def getaliensleft(self):
        """
        Returns self._aliensleft
        """
        return self._aliensleft

    def getscore(self):
        """
        Returns self._score
        """
        return self._score

    def setscore(self, value):
        """
        Sets self._score to value

        Parameter value: the value self._score is set to
        Precondition: value is an int >= 0
        """
        self._score = value

    def __init__(self):
        """
        Initializes a new Wave object. This function call self.createaliens()
        to create a series of Alien objects to fill self._aliens. It sets all
        the attributes of Wave objects to their initial values
        """

        self._ship = Ship(x=GAME_WIDTH/2, bottom=SHIP_BOTTOM,
        height=SHIP_HEIGHT, width=SHIP_WIDTH, source='ship.png')
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
        linewidth=2, linecolor='black')
        self._time = 0
        self._lives = SHIP_LIVES
        self._aliendir = 0
        self._bolts = []
        self._boltsteps = random.randint(0, BOLT_RATE)
        self._aliensbelow = False
        self._aliensleft = True
        self._score = 0
        self._speed = ALIEN_SPEED
        self._aliens = []
        self.createaliens()

    def update(self, input, dt):
        """
        This function calls on a variety of helper functions to update many
        factors in the game including alien movement, ship movement, and bolts.
        This function also increases the _time attribute by dt every time it
        is called finds the right and left most coordinate of an alien on
        screen.

        Parameter input: The current input recived by the PC
        Precondition: input is an instance of GInput

        Parameter dt: The time is seconds since last update
        Precondition: dt is a number int or float

        """
        self.shipmove(input)
        self._time += dt

        hirite = 0
        hileft = GAME_WIDTH
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    r = alien.getright()
                    l = alien.getleft()
                    if r > hirite:
                        hirite = r
                    if l < hileft:
                        hileft = l
        if (hirite > GAME_WIDTH - ALIEN_H_SEP) and (self._time >= self._speed):
            self.alienmovedownatright()
        elif (hileft < ALIEN_H_SEP) and (self._time >= self._speed):
            self.alienmovedownatleft()
        elif self._time >= self._speed:
            self.alienmove()

        self.shipfire(input)
        self.alienfire()
        self.boltmove()
        self.aliencollide()
        self.shipcollide()
        self.alienbelowtest()
        self.alientracker()

    def draw(self, view):
        """
        This methods draws all instances of Alien, Ship, and Bolt if they are
        not None, using the draw method inherited from GImage. The defense line
        is drawn the same way.
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.draw(view)
        if self._ship is not None:
            self._ship.draw(view)


        self._dline.draw(view)

        for bolts in self._bolts:
            bolts.draw(view)

    def newship(self):
        """
        This method creates a new Ship object and assigns it to attribute _ship
        """
        self._ship = Ship(x=GAME_WIDTH/2, bottom=SHIP_BOTTOM,
        height=SHIP_HEIGHT, width=SHIP_WIDTH, source='ship.png')

    def createaliens(self):
        """
        This function creates ALIEN_ROWS rows of Alien objects with
        ALIENS_IN_ROW Aliens in each row. Each row of aliens is added to
        self._aliens
        """

        alienrow = []
        rowcount = ALIEN_ROWS - 1
        for x in range(ALIEN_ROWS):
            rowcount2 = x+rowcount
            imgcount = int(rowcount2/2)
            imgremain = imgcount % len(ALIEN_IMAGES)

            for n in range(ALIENS_IN_ROW):
                p = Alien(left=ALIEN_H_SEP+n*(ALIEN_H_SEP+ALIEN_WIDTH),
                top=GAME_HEIGHT-ALIEN_CEILING-x*(ALIEN_V_SEP+ALIEN_HEIGHT),
                source=ALIEN_IMAGES[imgremain], width=ALIEN_WIDTH,
                height=ALIEN_HEIGHT)
                alienrow.append(p)
            rowcount = rowcount - 2
            self._aliens.append(alienrow)
            alienrow = []

    def shipmove(self, input):
        """
        This function moves the player ship.

        If the right key is pressed the
        ship moves SHIP_MOVEMENT pixels right. If the left key is pressed the
        ship moves SHIP_MOVEMENT pixels left. The ship is not able to move
        offscreen

        Parameter input: The currect input recived by the PC
        Precondition: input is an instance of GInput
        """

        if self._ship is not None:
            if input.is_key_down('left') and self._ship.left > 0:
                self._ship.setx(self._ship.getx() - SHIP_MOVEMENT)
            if input.is_key_down('right') and self._ship.right < GAME_WIDTH:
                self._ship.setx(self._ship.getx() + SHIP_MOVEMENT)

    def shipfire(self, input):
        """
        This function creates a Bolt object originating at the player ships

        Parameter input: The currect input recived by the PC
        Precondition: input is an instance of GInput
        """
        isplayerbolt = 0
        for bolts in self._bolts:
            isplayerbolt += bolts.getfromship()

        if self._ship is not None:
            if input.is_key_down('spacebar') and isplayerbolt == 0:
                bolt = Bolt(self._ship.getx(), self._ship.gettop(), True)
                self._bolts.append(bolt)

    def alienfire(self):
        """
        This function controls the firing of bolts by the aliens.

        First it picks a random nonempty column of aliens and chooses the
        lowest alien in that column. Then it subtracts 1 from self._boltsteps
        everytime the aliens move untill self._boltsteps == 0. At that point
        a Bolt object is created at the location of the chosen alien and
        self._boltsteps is assigned a random number between 1 and BOLT_RATE
        """
        col = random.randint(0, ALIENS_IN_ROW-1)
        empty = self._aliens[0][col] == None
        while empty == True:
            for x in range(ALIEN_ROWS):
                empty = empty and self._aliens[x][col] == None
            col = random.randint(0, ALIENS_IN_ROW-1)

        bottom = GAME_HEIGHT
        i = 2
        botalien = self._aliens[ALIEN_ROWS-1][col]
        while (botalien is None) and (i <= ALIEN_ROWS):
            try:
                botalien = self._aliens[ALIEN_ROWS - i][col]
                i = i + 1
            except:
                i = i+1

        for x  in range(0-ALIEN_ROWS):
            if self._aliens[x][col] is not None:
                if (self._aliens[x][col].gety()) < bottom:
                    botalien = self._aliens[x][col]

        if self._boltsteps == 0:
            if botalien is not None:
                albolt = Bolt(botalien.getx(), (botalien.getbottom()
                 - BOLT_HEIGHT/2), False)
                self._bolts.append(albolt)
                self._boltsteps = random.randint(1, BOLT_RATE)

    def boltmove(self):
        """
        This function moves Bolt objects aross the screen.

        Each time this function is called all current bolt's y attributes
        changes self._velocity pixels. This function also deletes Bolts that
        reach the bottom or top of the screen.
        """
        for bolts in self._bolts:
            vel = bolts.getVelocity()
            y = bolts.gety()
            bolts.sety(y + vel)
            pos = self._bolts.index(bolts)
            if bolts.getbottom() > GAME_HEIGHT or bolts.gettop() < 0:
                del self._bolts[pos]

    def alienmove(self):
        """
        This function moves the aliens left or right ALIEN_H_WALK pixels each
        time it is called depending on attribute _aliendir. It also resets
        attribute _time to 0 and reduces attribute _boltsteps by 1.
        """
        if self._aliendir == 0:
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        alien.setx(alien.getx() + ALIEN_H_WALK)

        elif self._aliendir == 1:
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        alien.setx(alien.getx() - ALIEN_H_WALK)

        self._time = 0
        self._boltsteps -= 1

    def alienmovedownatright(self):
        """
        This function moves the aliens when they reach the right side of the
        screen.
        All aliens are moved ALIEN_V_WALK pixels down and ALIEN_H_WALK pixels
        left. This function also resets attribute _time to 0, reduces
        attribute _boltsteps by 1, and switches the direction the aliens move to
        left.
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.sety(alien.gety() - ALIEN_V_WALK)
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.setx(alien.getx() - ALIEN_H_WALK)
        self._time = 0
        self._aliendir = 1
        self._boltsteps -= 1

    def alienmovedownatleft(self):
        """
        This function moves the aliens when they reach the left side of the
        screen.
        All aliens are moved ALIEN_V_WALK pixels down and ALIEN_H_WALK pixels
        right. This function also resets attribute _time to 0, reduces
        attribute _boltsteps by 1, and switches the direction the aliens move to
        right.
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.sety(alien.gety() - ALIEN_V_WALK)
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.setx(alien.getx() + ALIEN_H_WALK)
        self._time = 0
        self._aliendir = 0
        self._boltsteps -= 1

    def aliencollide(self):
        """
        This function tests if any bolts fired have hit an alien. If an alien is
        hit, the alien and bolt are removed and attribute score increases.
        This function uses method collides from the Alien class to test if any
        bolts from the player ship have hit an alien.

        """
        for x in range(len(self._aliens)):
            for aliens in self._aliens[x]:
                if aliens is not None:
                    for bolts in self._bolts:
                        collide = aliens.collides(bolts)
                        if collide == True:
                            xlist = self._aliens[x]
                            pos = xlist.index(aliens)
                            self._aliens[x][pos] = None
                            pos = self._bolts.index(bolts)
                            del self._bolts[pos]
                            self._score += 100

    def shipcollide(self):
        """
        This function tests if any bolts fired have hit the player ship. If the
        ship is hit, the ship and bolt are removed.
        This function uses method collides from the Ship class to test if any
        bolts from the an alien have hit the ship.

        """
        for bolts in self._bolts:
            if self._ship is not None:
                collide = self._ship.collides(bolts)
                if collide == True:
                    self._ship = None
                    pos = self._bolts.index(bolts)
                    del self._bolts[pos]

    def alienbelowtest(self):
        """
        This method tests if any aliens have gotten below DEFENSE_LINE. If an
        alien has gotten below the defense line attribute _aliensblow is changed
        to True.
        """
        for rows in self._aliens:
            for aliens in rows:
                if aliens is not None:
                    if aliens.getbottom() <= DEFENSE_LINE:
                        self._aliensbelow = True

    def alientracker(self):
        """
        This function tracks how many aliens are left, and how many have been
        shot. It also decreases attribute ._speed depending on how many aliens
        have been shot. Finally, if no aliens are left this function updates
        attribute _aliensleft to False
        """
        aliensleft = ALIEN_ROWS*ALIENS_IN_ROW
        alienskilled = 0
        for rows in self._aliens:
            for aliens in rows:
                if aliens is None:
                    aliensleft -= 1
                    alienskilled += 1

        self._speed = ALIEN_SPEED*(0.97**alienskilled)

        if aliensleft == 0:
            self._aliensleft = False
