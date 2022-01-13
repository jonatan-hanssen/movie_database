class Movie:
    def __init__(self, ttid, title, rating):
        self.ttid = ttid
        self.title = title
        self.rating = rating
        self.actors = set()
        self.edges = 0

    def add_actor(self, actor):
        self.actors.add(actor)

    def set_edges(self):
        self.edges = ((len(self.actors)-1)/2)*len(self.actors)
        return int(self.edges)
