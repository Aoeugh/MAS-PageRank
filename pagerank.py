import numpy as np

class Graphe:
    def __init__(self):
        self.listePages = []

    def contient(self, nom):
        for page in self.listePages:
            if(page.nom == nom):
                return True
        return False

    def trouver(self, nom):
        if(not self.contient(nom)):
            nouvellePage = Page(nom)
            self.listePages.append(nouvellePage)
            return nouvellePage
        else:
            return next(page for page in self.listePages if page.nom == nom)

    def ajouter_voisins(self, parent, enfant):
        pageParent = self.trouver(parent)
        pageEnfant = self.trouver(enfant)

        pageParent.lien_enfant(pageEnfant)
        pageEnfant.lien_parent(pageParent)


    def trier_pages(self):
        self.listePages.sort(key=lambda page: int(page.nom))

    def normaliser_pagerank(self):
        somme_pageranks = sum(page.pagerank for page in self.listePages)

        for page in self.listePages:
            page.pagerank /= somme_pageranks


    def recuperer_liste_pageranks(self):
        liste_pageranks = np.asarray([page.pagerank for page in self.listePages], dtype='float32')
        return np.round(liste_pageranks, 8)

class Page:
    def __init__(self, nom):
        self.nom = nom
        self.enfants = []
        self.parents = []
        self.pagerank = 1.0

    def lien_enfant(self, nouvelEnfant):
        for enfant in self.enfants:
            if(enfant.nom == nouvelEnfant.nom):
                return None
        self.enfants.append(nouvelEnfant)

    def lien_parent(self, nouveauParent):
        for parent in self.parents:
            if(parent.nom == nouveauParent.nom):
                return None
        self.parents.append(nouveauParent)

    def nouveau_pagerank(self, amortissement, n):
        voisins = self.parents
        somme_pageranks = sum((page.pagerank / len(page.enfants)) for page in voisins)
        random_saut = amortissement / n
        self.pagerank = random_saut + (1-amortissement) * somme_pageranks

def init_graphe(fname):
    with open(fname) as f:
        lignes = f.readlines()

    graphe = Graphe()

    for ligne in lignes:
        [parent, enfant] = ligne.strip().split(',')
        graphe.ajouter_voisins(parent, enfant)

    graphe.trier_pages()

    return graphe

def PageRank_boucle(graphe, amortissement):
    listePages = graphe.listePages
    for page in listePages:
        page.nouveau_pagerank(amortissement, len(graphe.listePages))
    graphe.normaliser_pagerank()

def PageRank(graphe, amortissement, iteration=100):
    for i in range(iteration):
        PageRank_boucle(graphe, amortissement)

if __name__ == '__main__':
    nbIterations = 2000
    amortissement = 0.15
    graphe = init_graphe('graphe.txt')

    PageRank(graphe, amortissement, nbIterations)
    print(graphe.recuperer_liste_pageranks())
