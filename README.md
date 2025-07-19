Jess Wall Python Fundamentals Project || 07/17/2025
This document goes over the different applications built within this project and their functionality.


----> ARCADE_APP <----


-- VIEWS.PY --
This powers the web-based retro game arcade built with ASCII-style games like Snake, Pong, and Tic-Tac-Toe.

-- ADMIN.PY --
Configures django interface

-- URLS.PY --
Stores all urls associated with the app

-- MODELS.PY --
Defines a django models, specifically, HighScore, which is used to store and manage player scores for the arcade

-- APPS.PY --
Used to configure & register django apps


---> ARCADE_APP/GAMES <---

-- PONG.PY --
Implements a simple ASCII-based Pong game with some basic AI for one paddle and keyboard-like input controls.
The core functions together implement the gameplay loop and interaction of the ASCII Pong game.

-- SNAKE.PY --
Simulates the Snake game on a 2D grid where the player controls a snake that moves around, eats food to grow longer,
and tries not to collide with itself or the walls. It keeps track of score and game state and
can render the game as ASCII art.

-- TIC_TAC_TOE.PY --







----> MY_ARCADE APP <----

-- SETTINGS.PY --
Stores general settings to power the entire app

-- URLS.PY --
Links back to internal apps (like arcade_app) to ensure all links work for webapp

----> STATIC DIRECTORY <----
Stores images used within webapp

----> TEMPLATES DIRECTORY <----

-- ARCADE_APP/INDEX.HTML --
Stores all the code to power the front end of the webapp
