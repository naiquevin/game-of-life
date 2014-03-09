The Game of Life in Clojure
===========================

This works similar to the Python implementation that can be found
here - ``../game_of_life.py``.

Installation
------------

[Leiningen](https://github.com/technomancy/leiningen) is required to
for running the game.

Usage
-----

(First of all, make sure you have downloaded the cell configs from
http://www.bitstorm.org/gameoflife/lexicon/. You may do so by running
the `../lifeconfigs.sh` utility.)

Run following command from the current directory

```bash
    $ lein run ( FILENAME | DIR )
```

ie. the only command line argument this script accepts should be the
path to a `.cells` file or a directory containing at least 1 `.cells`
file.

```bash
    $ lein run ../cells/101.cells
```

```bash
    $ lein run ../cells
```

In second case, a `.cells` file will be randomly chosen from the dir.

Running tests
-------------

```bash
    $ lein test
```

Note
----

I know this may not be idiomatic Clojure as I am still learning the
language. It's just an attempt to port something I had already written
in a more familiar language (Python). But I am open to any kind of
suggestions. So please let me know if you have any thoughts on this.

License
-------

Copyright © 2013, Vineet Naik

Distributed under the Eclipse Public License, the same as Clojure.
