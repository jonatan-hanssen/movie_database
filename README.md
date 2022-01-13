# Movie database
This was a project I worked on with another student for IN2010.
It involved creating a graph from a very large part of the IMDB database
(around 100k movies and 100k actors). The result is a graph with 100k nodes
(actors) and almost 5 million edges (an edge is created between to actors
if they played in the same movie). The rest of the project involved applying
different algorithms to the graph. Efficient algorithms was very important
and I'm very happy with our implementation of Dijkstra's algorithm for finding
the path between to actors with the highest rated movies. Using Numba we
have been able to complete the program in about 5 seconds.

To run the program simply run
```
python3 oblig2.py
```
