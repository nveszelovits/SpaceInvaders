"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special class
for it.  Unless you need something special for your extra gameplay features,
Ship and Aliens could just be an instance of GImage that you move across the
screen. You only need a new class when you add extra features to an object. So
technically Bolt, which has a velocity, is really the only model that needs to
have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is
because there are a lot of constants in consts.py for initializing the objects,
and you might want to add a custom initializer.  With that said, feel free to
keep the pass underneath the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

Nick Veszelovits nav7
12/5/2018
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
#than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a ship
    just means changing the x attribute (which you can do directly), you want
    to prevent the player from moving the ship offscreen.  This is an ideal
    thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We do not
    require this.  You could put this method in Wave if you wanted to.  But the
    advantage of putting it here is that Ships and Aliens collide with
    different bolts.  Ships collide with Alien bolts, not Ship bolts.  And
    Aliens collide with Ship bolts, not Alien bolts. An easy way to keep this
    straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those inherited
    by GImage. You would only add attributes if you needed them for extra
    gameplay features (like animation). If you add attributes, list them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    def sety(self, value):
        """
        Sets self.y to value

        Parameter value: the value self._lives is set to
        Precondition: value is int or float
        """
        self.y = value

    def setx(self, value):
        """
        Sets self._lives to value

        Parameter value: the value self._lives is set to
        Precondition: value is int or float
        """
        self.x = value

    def gety(self):
        """
        Returns self.y
        """
        return self.y

    def getx(self):
        """
        Returns self.x
        """
        return self.x

    def gettop(self):
        """
        Returns self.top
        """
        return self.top

    def getbottom(self):
        """
        Returns self.bottom
        """
        return self.bottom

    def collides(self, bolt):
        """
        This function returns True if bolt overlaps with the ship and bolt was
        fired from an alien. It False otherwise
        Using the contains method inherited from GImage, all four corners of
        bolt are tested to see if they overlap with the ship. The attribute
        _fromship of bolt is also tested.
        """

        shipbolt = bolt.getfromship()
        if shipbolt == True:
            return False
        else:
            result1 = self.contains((bolt.getright(),bolt.getbottom()))
            result2 = self.contains((bolt.getleft(),bolt.getbottom()))
            result3 = self.contains((bolt.getright(),bolt.gettop()))
            result4 = self.contains((bolt.getright(),bolt.gettop()))
            return max(result1, result2, result3, result4)


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We do
    not require this.  You could put this method in Wave if you wanted to.  But
    the advantage of putting it here is that Ships and Aliens collide with
    different bolts.  Ships collide with Alien bolts, not Ship bolts.  And
    Aliens collide with Ship bolts, not Alien bolts. An easy way to keep this
    straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those inherited
    by GImage. You would only add attributes if you needed them for extra
    gameplay features (like giving each alien a score value). If you add
    attributes, list them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    def sety(self, value):
        """
        Sets self.y to value

        Parameter value: the value self._lives is set to
        Precondition: value is int or float
        """
        self.y = value

    def setx(self, value):
        """
        Sets self._lives to value

        Parameter value: the value self._lives is set to
        Precondition: value is int or float
        """
        self.x = value

    def gety(self):
        """
        Returns self.y
        """
        return self.y

    def getx(self):
        """
        Returns self.x
        """
        return self.x

    def gettop(self):
        """
        Returns self.top
        """
        return self.top

    def getbottom(self):
        """
        Returns self.bottom
        """
        return self.bottom

    def getright(self):
        """
        Returns self.right
        """
        return self.right

    def getleft(self):
        """
        Returns self.bottom
        """
        return self.left

    def collides(self, bolt):
        """
        This function returns True if bolt overlaps with the alien and bolt was
        fired from the Ship. It returns False otherwise
        Using the contains method inherited from GImage, all four corners of
        bolt are tested to see if they overlap with the alien. The attribute
        _fromship of bolt is also tested.
        """
        shipbolt = bolt.getfromship()
        if shipbolt == False:
            return False
        else:
            result1 = self.contains((bolt.getright(),bolt.getbottom()))
            result2 = self.contains((bolt.getleft(),bolt.getbottom()))
            result3 = self.contains((bolt.getright(),bolt.gettop()))
            result4 = self.contains((bolt.getright(),bolt.gettop()))
            return max(result1, result2, result3, result4)


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles.  The size of the bolt is
    determined by constants in consts.py. We MUST subclass GRectangle, because
    we need to add an extra attribute for the velocity of the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a helper.

    You also MIGHT want to create a method to move the bolt.  You move the bolt
    by adding the velocity to the y-position.  However, the getter allows Wave
    to do this on its own, so this method is not required.

    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
        _fromship: True the bolt is from the player ship, False if the bolt
                    is from an Alien [bool]

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    def getVelocity(self):
        """
        Returns self._velocity
        """
        return self._velocity

    def sety(self, value):
        """
        Sets self.y to value

        Parameter value: the value self._lives is set to
        Precondition: value is int or float
        """
        self.y = value

    def gety(self):
        """
        Returns self.y
        """
        return self.y

    def gettop(self):
        """
        Returns self.top
        """
        return self.top

    def getbottom(self):
        """
        Returns self.bottom
        """
        return self.bottom

    def getright(self):
        """
        Returns self.right
        """
        return self.right

    def getleft(self):
        """
        Returns self.bottom
        """
        return self.left

    def getfromship(self):
        """
        Returns self._fromship
        """
        return self._fromship

    def  __init__(self, x, y, fromship):
        """
        This function initializes a new instance of Bolt.
        The __init__ method inherited from GRectangle is called and the
        necessary attributes are assigned from consts.py. Attribute _velocity
        is postive if the bolt is fired from a ship and negative if fired from
        an alien.

        Parameter x: The x-coordinate of the center of the bolt
        Precondition: x is an int or float

        Parameter y: The y-coordinate of the center of the bolt
        Precondition: y is an int or float

        Parameter fromship: True if the bolt is fired from a Ship and False if
                            fired from an alien.
        Precondition: fromship is a bool
        """

        GRectangle.__init__(self)
        self._velocity = BOLT_SPEED
        if fromship is False:
            self._velocity = 0 - BOLT_SPEED

        self.x = x
        self.bottom = y
        self.width = BOLT_WIDTH
        self.height = BOLT_HEIGHT
        self.fillcolor = 'blue'
        self._fromship = fromship



    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
