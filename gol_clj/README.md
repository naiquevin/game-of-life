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

Run following command from this directory

```bash
    $ lein run FILENAME
```

where ``FILENAME`` is a path to a ``.cells`` file eg.

```bash
    $ lein run ../cells/101.cells
```

Running tests
-------------

```bash
    $ lein test
```

Note
----

I know may not be idiomatic Clojure as I am still learning the
language. It's just an attempt to port something I had already written
in a more familiar language (Python), something like a warm up! But I
am open to any kind of suggestions/criticism. So please let me know if
there is anything.

License
-------

Copyright © 2013 Vineet Naik

Distributed under the Eclipse Public License, the same as Clojure.
