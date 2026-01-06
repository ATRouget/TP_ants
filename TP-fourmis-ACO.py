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