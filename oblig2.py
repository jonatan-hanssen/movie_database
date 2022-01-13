from actor import Actor
from graph import Graph
from movie import Movie
import time

def main():
    start = time.time()
    totstart = start
    
    graph = Graph()

    ###############
    # LESE MOVIES #
    ###############

    #aapner filen for aa lese verdiene
    moviefile = open("movies.tsv", 'r',encoding="UTF-8")
    # vi lagrer movies i et dict fordi det er lett
    # aa legge til movies til skuespillere ved aa bruke
    # ttid
    movies = dict()
    line = moviefile.readline()
    while line:
        splitline = line.strip().split("\t")
        # lagrer movies som movieobjekter med ttid som key
        movies[splitline[0]] = Movie(splitline[0],splitline[1],float(splitline[2]))
        line = moviefile.readline()

    moviefile.close()
    ###############
    # LESE ACTORS #
    ###############

    actorfile = open("actors.tsv", 'r',encoding="UTF-8")
    line = actorfile.readline()
    while line:
        splitline = line.strip().split("\t")
        actormovies = set()

        # legger til verdiene fra 2 til n som
        # movieobjekter
        actor = Actor(splitline[0],splitline[1])
        for i in range(2,len(splitline)):
            # her gjoer vi sjekken for at filmen faktisk
            # er i movies.tsv, hvis den ikke er det blir den
            # ikke lagt til.
            if splitline[i] in movies:
                actormovies.add(movies[splitline[i]])
                movies[splitline[i]].add_actor(actor)
        actor.movies = actormovies
        graph.add_node(actor)
        line = actorfile.readline()

    actorfile.close()

    edges = 0
    for movie in movies.values():
        edges += movie.set_edges()



    print("Oppgave 1\n")
    print(f"Nodes: {graph.count_nodes()}")
    print(f"Edges: {edges}", end = "\n")

    end = time.time()
    print(f"\nKjøretid: {end - start:.2f} sekunder", end = "\n\n")
    start = time.time()

    print("Oppgave 2\n")

    print_path(graph.shortest_path_BFS("nm2255973","nm0000460"),graph)
    print_path(graph.shortest_path_BFS("nm0424060","nm0000243"),graph)
    print_path(graph.shortest_path_BFS("nm4689420","nm0000365"),graph)
    print_path(graph.shortest_path_BFS("nm0000288","nm0001401"),graph)
    print_path(graph.shortest_path_BFS("nm0031483","nm0931324"),graph)

    end = time.time()
    print(f"\nKjøretid: {end - start:.2f} sekunder", end = "\n\n")
    start = time.time()

    print("Oppgave 3\n")

    print_path(graph.dijkstra("nm2255973","nm0000460"),graph)
    print_path(graph.dijkstra("nm0424060","nm0000243"),graph)
    print_path(graph.dijkstra("nm4689420","nm0000365"),graph)
    print_path(graph.dijkstra("nm0000288","nm0001401"),graph)
    print_path(graph.dijkstra("nm0031483","nm0931324"),graph)


    end = time.time()
    print(f"\nKjøretid: {end - start:.2f} sekunder", end = "\n\n")
    start = time.time()

    print("Oppgave 4\n")

    print_components(graph.count_components())


    end = time.time()
    print(f"\nKjøretid: {end - start:.2f} sekunder", end = "\n\n")

    print(f"\nTotal kjøretid: {end - totstart:.2f} sekunder", end = "\n\n")


def print_path(path,graph):
    for pair in path[::-1]:
        print(pair[0].value.name)
        if pair[1]:
            print(f"=== [ {pair[1].title} ({pair[1].rating}) ] ===>", end = ' ')
    print("")

def print_components(components):
    #printer dictet fra flest components til faerrest
    compList = list(components)
    compList.sort()
    compList = compList[::-1]
    for key in compList :
        print(f"Det er {components[key]} componenter med {key} noder.")

main()
