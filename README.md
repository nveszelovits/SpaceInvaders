A mock version of the classic Space Invaders game I made for a school project.

app.py is contains the Invaders class which extends GameApp. It starts the game and manages the gamestate.
models.py contants the Ship, Alien and Bolt classes which all extend GImage. They mainly contain attributes and methods used by wave.
wave.py contains the class Wave. The Wave class does the bulk of the work in this program. It moves the sprites and handles all gameplay.
