Conway's Game of Life
=====================

What and Why?
-------------

This is an implementation of the famous
[Conway's Game of Life](http://en.wikipedia.org/wiki/Conway's_Game_of_Life)
in Python (Update: and Clojure). It's a result of Sunday afternoon boredom.

How to run?
-----------

First download ``.cells`` files from this
[game of life lexicon](http://www.bitstorm.org/gameoflife/lexicon/) by
running the ``lifeconfigs.sh`` script. This needs to be done only once.

```bash
    $ ./lifeconfigs.sh
```

It will take a while since there are many files to be downloaded. Once
it's done, run the ``game_of_life.py`` script,

```bash
    $ python game_of_life.py
```

A ``.cells`` file will be randomly selected from the ``cells/``
directory. You may also specify one by passing it as an argument to
the command,

```bash
    $ python game_of_life.py cells/101.cells
```

Demo
----

![Pulshuttle_V](../master/pulshuttle_V.gif?raw=true)

Languages
---------

Currently the game is implemented in,

* Python  (see game_of_life.py)  ✔
* Clojure (see gol_clj)          ✔

Implementions in other languages coming soon (whenever I am bored
again!)

