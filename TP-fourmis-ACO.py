import random as rd

class AntColony :
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha = 1, beta = 2):
        self.distances = distances
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.pheromones = [[1.0 for _ in range(len(distances))] for _ in range(len(distances))]
        self.meilleur_chemin = None
        self.meilleure_distance = float('inf')
    
    def calculer_distance_chemin(self, chemin) :
        S = 0
        for v in range(len(chemin)-1) :
            S = S + self.distances[chemin[v]][chemin[v+1]]
        return S
    
    def generer_tous_chemins(self) :
        tous_chemins = []
        for i in range(self.n_ants) :
            chemin = []
            ville = rd.uniform(0, len(self.distances))
            chemin.append(ville)
            while len(chemin) < len(self.distances) :
                probas = self.calculer_probabilites_mouvement(chemin)
                ville = self.choisir_ville_suivante(probas)
                chemin.append(ville)
            for c in chemin :
                tous_chemins.append((c, self.caculer_distance_chemin(c)))
        return tous_chemins

    def calculer_probabilites_mouvement(self, chemin) :
        derniere = chemin[-1]
        probas = []
        for i in range(len(self.distances)):
            if i in chemin :
                probas.append(0)
            else :
                heuristique = 1 / self.distances[i][derniere]
                pheromone = self.pheromones[i][derniere]
                P = pheromone^self.alpha * heuristique^self.beta
                probas.append(P)
        S = sum(probas)
        if S != 0 :
            for q in range(len(probas)):
                probas[q] = probas[q]/S
        return probas
    
    def choisir_ville_suivante(self, probas) :
        r = rd.random()
        for i in range(len(probas)):
            
        

    def deposer_pheromones(self, tous_chemins) :
        tous_chemins.sort(key = lambda x : x[1])
        for x in tous_chemins[:self.n_best] :
            for i in range(len(x[0])-1) :
                self.pheromones[x[i]][x[i+1]] += 1/x[1]
                self.pheromones[x[i+1]][x[i]] += 1/x[1]

    
    def evaporer_pheromones(self) :
        for i in range(len(self.pheromones)):
            for j in range(len(self.pheromones)):
                self.pheromones = self.pheromones * self.decay
    
    def run(self):
        
        for _ in range(self.n_iterations):
            tous_chemins = self.generer_tous_chemins()
            meilleur = min(tous_chemins, key = lambda x : x[1])
            if meilleur[1] < self.meilleure_distance :
                self.meilleur_chemin = meilleur[0]
                self.meilleure_distance = meilleur[1]
            self.deposer_pheromones(tous_chemins)
            self.evaporer_pheromones()



## Dans étape 5, créer fonctions 3, 6, 7, 9##