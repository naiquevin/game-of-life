# "The Game of Life" in Clojure

This is the Clojure port of the Game of Life that works (almost)
similar to the Python implementation ``(../game_of_life.py)``

## Installation

[Leiningen](https://github.com/technomancy/leiningen) is required to
be installed for running this game and the tests

## Usage

Run following command from this directory

    $ lein run FILENAME

where ``FILENAME`` is a path to a ``.cells`` file eg.

    $ lein run ../cells/101.cells

## Running tests

    $ lein test

## Note

I know may not be idiomatic Clojure as I am still learning the
language. It's just an attempt to port something I had already written
in a more familiar language (Python), something like a warm up! But I
am open to any kind of suggestions/criticism. So please let me know if
there is anything.

## License

Copyright © 2013 Vineet Naik

Distributed under the Eclipse Public License, the same as Clojure.
