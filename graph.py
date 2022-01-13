from heapq import *


class Graph:
    nodes = dict()
    edges = 0
    def add_node(self, value):
        node = self.Node(value)
        self.nodes[node.nid] = node

    def get_value_of_node(self, node):
        return node.value

    def count_nodes(self):
        return len(self.nodes)

    def count_edges(self):
        return edges

    def get_neighbors_of_node(self,node):
        return node.neighbors

    def shortest_path_BFS(self, nmid1, nmid2):
        visited_nodes = set()
        node = self.nodes[nmid1]
        node.visited = True
        visited_nodes.add(node)
        queue = list()
        queue.append(node)
        # dette er en list av tuples
        shortest_path = list()
        while queue:
            node = queue.pop(0)
            for movie in node.value.movies:
                for actor in movie.actors:
                    neighbor = self.nodes[actor.nmid]
                    if not neighbor.visited:
                        queue.append(neighbor)
                        neighbor.previous = node
                        neighbor.edge_from_previous = movie
                        neighbor.visited = True
                        visited_nodes.add(neighbor)
                        if actor.nmid == nmid2:
                            tempmovie = None
                            shortest_path.append((neighbor, tempmovie))
                            while neighbor.previous:
                                tempmovie = neighbor.edge_from_previous
                                neighbor = neighbor.previous
                                shortest_path.append((neighbor,tempmovie))
                            for node in visited_nodes:
                                node.visited = False
                                node.previous = None
                                node.edge_from_previous = None
                            return shortest_path

    # Ettersom det bare er positive tall vil den foerste
    # vi finner korteste vei basert paa ratingen
    # veien vi finner vaere den korteste veien ettersom
    # vi per lag alltid gaar den korteste veien

    #vi bruker foreslått implementasjon fra heapq dokumentasjonen for å
    #oppdatere en  vilkårlig node i en heap ved hjelp av dict
    def dijkstra(self, nmid1, nmid2):
        heap = []
        heapify(heap)
        visited_nodes = set()
        count = 0
        node = self.nodes[nmid1]
        cheapest_path = list()
        node.distance = 0
        entry_finder = {}


        def _pop():
            # her maa vi poppe helt til vi finner et
            # element som ikke er none
            while heap:
                triple = heappop(heap)
                # hvis det var none maa vi poppe paa nytt
                if not triple[3]:
                    del entry_finder[triple[2]]
                    return triple[2]
            raise KeyError("pop fra tom priority queue")
        def _push(node,count):
            if node in entry_finder:
                _remove(node)
            count += 1
            # vi maa bruker count i tilfelle to noder
            # har samme avstand
            entry = [node.distance,count,node,False]
            entry_finder[node] = entry
            heappush(heap,entry)
        def _remove(node):
            # vi tar vekk noden fra dictet og
            # setter verdien i heapen til None
            entry = entry_finder.pop(node)
            entry[3] = True

        _push(node,count)

        # dette stjeler vi fra heapq documentation
        # lager lokale funksjoner som soerger for
        # at vi kan pushe og poppe mens vi soerger
        # for at heap invarianten blir opprettholdt,
        # men uten at vi maa sortere heapen hver gang,
        # som tar lang tid
        while heap:
            cheapest = _pop()

            visited_nodes.add(cheapest)
            # dersom dette er sant er vi ferdige, ettersom
            # alle verdier er positive
            if cheapest.nid == nmid2:
                tempmovie = None
                cheapest_path.append([cheapest, tempmovie])
                while cheapest.previous:
                    tempmovie = cheapest.edge_from_previous
                    cheapest = cheapest.previous
                    cheapest_path.append([cheapest, tempmovie])
                for node in visited_nodes:
                    node.previous = None
                    node.edge_from_previous = None
                    node.distance = float('inf')
                return cheapest_path

            # dersom vi kommer hit fant vi ikke noden og vi
            # maa gaa videre

            # vi bruker tuuple fordi tuple er et keyword i python
            for movie in cheapest.value.movies:
                for actor in movie.actors:
                    neighbor = self.nodes[actor.nmid]
                    new_dist = 10 - movie.rating
                    if cheapest.distance + new_dist < neighbor.distance:
                        neighbor.distance = cheapest.distance + new_dist
                        neighbor.previous = cheapest
                        neighbor.edge_from_previous = movie
                        visited_nodes.add(neighbor)
                        _push(neighbor,count)

    # det eneste vi trenger aa gjoere her er aa traversere
    # nodene langs kantene og ta dem ut etterhvert som vi
    # moeter dem. Gjoer vi dette til vi gaar tom for gyldige kanter
    # har vi en komponent. Gjoer vi dette til vi er tom noder
    # har vi telt alle komponenter
    def count_components(self):
        # vi bruker ikke bfs eller dfs ellernoe, vi bare
        # traverserer paa en tilfeldig maate, fordi det viktigste
        # er aa gjoere det raskt. Aa bruke et dict gir oss 
        # O(1) tid paa fjerning som er det vi oftest
        nodedict = dict(self.nodes)
        keylist = list(self.nodes)
        componentdict = dict()

        while nodedict:
            count = 0
            stack = set()

            # dette gir oss et element i nodedict, det er
            # irrelevant hvilket det er.
            stack.add(nodedict.pop(next(iter(nodedict))))
            while stack:
                lastpopped = stack.pop()
                count += 1
                # se paa naboene dens

                lastpopped.visited = True
                for movie in lastpopped.value.movies:
                    for actor in movie.actors:
                        if not self.nodes[actor.nmid].visited:
                            self.nodes[actor.nmid].visited = True
                            # saa hver gang vi legger til noe
                            # i stacken saa fjerner vi det ogsaa
                            # fra nodedictet
                            stack.add(self.nodes[actor.nmid])
                            nodedict.pop(actor.nmid)

            if count not in componentdict:
                componentdict[count] = 0
            componentdict[count] += 1
            # naa vil vi starte traversering paa nytt med en ny
            # komponent

        return componentdict

    class Node:
        def __init__(self, value):
            self.distance = float('inf')
            self.previous = None
            self.visited = False
            self.edge_from_previous = None
            self.value = value
            # vi bruker nid fordi id er en metode i python
            # allerede. nid betyr node id
            self.nid = value.nmid


        # vi implementer en maate for aa sammenligne
        # noder, slik at vi kan bruke dem direkte i
        # en heap for dijsktras algoritme
        def __lt__(self, node):
            return self.distance < node.distance
