"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders
application. There is no need for any additional classes in this module.  If
you need more classes, 99% of the time they belong in either the wave module or
the models module. If you are unsure about where a new class should go, post a
question on Piazza.

 Nick Veszelovits   nav7
 12/5/2018
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/
#setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for
    processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when
    the game started, paused, completed, etc. It keeps track of that in an
    attribute called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from
                consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
                STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and
                aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification
    for the method update.

    You may have more attributes if you wish (you might want an attribute to
    store any score across multiple waves). If you add new attributes, they need
    to be documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the game
        is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        # IMPLEMENT ME
        self._wave = None
        self._state = STATE_INACTIVE
        self._text = None

        text = GLabel(text='Press S to Play', font_size = 90, right=680,
        top=550)
        if self._state == STATE_INACTIVE:
            self._text = text

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in this
        state so long as the player never presses a key.

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the
        screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move
        the ship and fire laser bolts.  All of this should be handled inside of
        class Wave (NOT in this class).  Hence the Wave class should have an
        update() method, just like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the
        game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one
        animation frame before switching to STATE_ACTIVE.

        You are allowed to add more states if you wish. Should you do so, you
        should describe them here.

        STATE_COMPLETE: The game is over. The player
        may press a key to start another game

        STATE_WIN: The player won and is shown a congratulating message. The
        player wins by destroying all the aliens. The player may then press a
        key to switch to STATE_COMPLETE

        STATE_LOSE: The player lost and is greeted with an admonishing message.
        The player loses if they run out of lives or the aliens get past the
        defense line. The player may then press a key to switch to
        STATE_COMPLETE

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        key = self.input.is_key_down('s')
        if key is True and self._state == STATE_INACTIVE:
            self._state = STATE_NEWWAVE

        elif self._state == STATE_NEWWAVE:
            self._wave = Wave()
            self._state = STATE_ACTIVE

        elif self._state == STATE_ACTIVE:
            self.activestate(dt)
        elif self._state == STATE_COMPLETE:
            self.completestate(dt)
        elif self._state == STATE_WIN:
            self.winstate(dt)
        elif self._state == STATE_LOSE:
            self.losestate(dt)

        pausetext =  GLabel(text='Press S to Contine' , font_size = 90,
        x=GAME_WIDTH/2, top=550)
        if self._state == STATE_PAUSED:
            self._text = pausetext
            if key is True:
                self._wave.newship()
                self._state = STATE_ACTIVE

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.
        To draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to class
        Wave.  We suggest the latter.  See the example subcontroller.py from
        class.
        """
        # IMPLEMENT ME
        if self._state == STATE_INACTIVE and self._text is not None:
            self._text.draw(self.view)
        elif self._state == STATE_PAUSED and self._text is not None:
            self._text.draw(self.view)
        elif self._state == STATE_LOSE and self._text is not None:
            self._text.draw(self.view)
        elif self._state == STATE_WIN and self._text is not None:
            self._text.draw(self.view)
        elif self._state == STATE_COMPLETE and self._text is not None:
            self._text.draw(self.view)
        elif self._state == STATE_ACTIVE:
            self._text.draw(self.view)
            self._wave.draw(self.view)

    def activestate(self, dt):
        """
        Handles the game while it is in STATE_ACTIVE. It calls the
        update() function from Wave to make the game work. It also keeps track
        of the winning and losing conditions and switches the state to STATE_WIN
        or STATE_LOSE if an appropriate condition is met. Finally, this function
        keeps track of player lives

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """

        if self._wave is not None:
            activetext = GLabel(text='Score:'+str(self._wave.getscore())+
            '                                                            Lives:'
            +str(self._wave.getlives()),font_size = 25, left=10,
            top=GAME_HEIGHT-10)

        self._wave.update(self.input, dt)
        self._text = activetext
        if (self._wave.getship() is None) and (self._wave.getlives() >= 1):
            self._state = STATE_PAUSED
            self._wave.setlives(self._wave.getlives() - 1)
        if (self._wave.getship() is None) and (self._wave.getlives() == 0):
                self._state = STATE_LOSE
        if self._wave.getaliensbelow() == True:
                self._state = STATE_LOSE
        if self._wave.getaliensleft() == False:
            self._state = STATE_WIN

    def losestate(self, dt):
        """
        Handles the game while it is in STATE_LOSE. The player is shown a
        message and can press a key to switch to STATE_COMPLETE

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """

        losetext = GLabel(text="""Better Luck Next Time!
        Press S to Play Again""", font_size = 50, x=GAME_WIDTH/2, top=550)

        key = self.input.is_key_down('s')
        self._text = losetext
        if key is True:
            self._state = STATE_COMPLETE

    def winstate(self, dt):
        """
        Handles the game while it is in STATE_WIN. The player is shown a
        message and can press a key to switch to STATE_COMPLETE

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """

        wintext = GLabel(text="""Congratulations You Win!
        Press S to Play Again""", font_size = 50, x=GAME_WIDTH/2, top=550)

        key = self.input.is_key_down('s')
        if self._state == STATE_WIN:
            self._text = wintext
            if key is True:
                self._state = STATE_COMPLETE

    def completestate(self, dt):
        """
        Handles the game while it is in STATE_COMPLETE. The player is shown a
        message and can press a key to begin a new game.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """

        completetext = GLabel(text='Press S to Play Again' , font_size = 90,
        right=680, top=550)

        key = self.input.is_key_down('s')
        self._text = completetext
        if key is True:
            self._state = STATE_NEWWAVE
