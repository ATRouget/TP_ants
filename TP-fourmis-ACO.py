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
        

    def deposer_pheromones(self, tous_chemins) :
    
    
    def evaporer_pheromones(self) :
        for i in range(len(self.pheromones)):
            for j in range(len(self.pheromones)):
                self.pheromones = self.pheromones * self.decay
    
    def run(self):
        

