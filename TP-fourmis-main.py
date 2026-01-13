import flet as ft
import random as rd
from math import *
import threading
from AntColony import AntColony


def main(page):
    page.title = "Algorithme de colonie de fourmis"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    titre = ft.Text("Visualisation de l'Algorithme", size=24)

    createur = ft.Button("Générer le graphe", on_click=lambda e: generer_nodes())


    champ1 = ft.TextField(label = 'Nombre de noeuds', value = '20', width = 150)
    champ2 = ft.TextField(label = 'Nombre de fourmis', value = '15', width = 150)
    champ3 = ft.TextField(label = "Nombre de d'itérations", value = '100', width = 150)
    

    zone = ft.Container(width = 600, height =  500, bgcolor = 'lightblue', border = ft.border.all(2,'blue'))

    statut = ft.Text("Prêt à démarrer", color = 'green', size = 16)


    iteration_text = ft.Text("Itération: 0", size=16)
    pheromone_text = ft.Text("Phéromones moyennes: ", size=14)
    path_text = ft.Text("Meilleur chemin: ", size=14)





    page.add(ft.Column([titre, ft.Text("Paramètres de l'algorithme", size = 16), ft.Row([champ1,champ2,champ3]), createur, ft.Divider(), statut, zone]))

    nodes = []




    distances = []
    pheromones = []
    best_path = []
    iteration = 0
    running = False
    stop_event = threading.Event()

    best_field = ft.TextField(label="Meilleures fourmis", value="3", width=150)
    decay_field = ft.TextField(label="Decay", value="0.95", width=150)
    alpha_field = ft.TextField(label="Alpha", value="1", width=150)
    beta_field = ft.TextField(label="Beta", value="2", width=150)

    def create_line(x1, y1, x2, y2, colour, thickness) : 
        dx = x2 - x1
        dy = y2 - y1
        length = sqrt(dx*dx + dy*dy)
        angle = atan2(dy, dx)
        return ft.Container(width=length,
            height=thickness,
            bgcolor= colour,
            left=x1,
            top=y1 - thickness / 2,
            rotate=ft.Rotate(
                angle=angle,
                alignment=ft.alignment.Alignment(-1, 0)))



    def generer_nodes():
        try:
            N = int(champ1.value)
        except ValueError: N=20
        for _ in range(N):
            x = rd.uniform(50,550)
            y = rd.uniform(50,450)
            nodes.append((x,y))
        distances = calculer_distances()
        pheromones = [[1.0 for _ in range(len(distances))] 
                  for _ in range(len(distances))]
        
        dessiner_graphe()

        print(f"{len(nodes)} nœuds générés")
        print(f"Distance entre nœud 0 et 1 : {distances[0][1]:.2f}")
    
    def dessiner_graphe():
        shapes = []

        if pheromones and len(pheromones) > 0:
            # Valeur maximale des phéromones (pour normalisation)
            max_pheromone = max(max(row) for row in pheromones) if pheromones else 1
            # Parcours de toutes les paires de nœuds
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    # Seuil minimal pour éviter l’encombrement visuel
                    if pheromones[i][j] > 0.1:
                        # Opacité proportionnelle à la quantité de phéromones
                        opacity = min(1, pheromones[i][j] / max_pheromone)

                        # Épaisseur proportionnelle aux phéromones
                        thickness = max(1, (pheromones[i][j] / max_pheromone) * 3)

                        # Création de la ligne entre les deux nœuds
                        line = create_line(
                            nodes[i][0], nodes[i][1],
                            nodes[j][0], nodes[j][1],
                            ft.Colors.with_opacity(opacity, ft.Colors.BLUE),
                            thickness)
                        shapes.append(line)
        
        # Dessin du meilleur chemin courant

        if best_path:
            for i in range(len(best_path) - 1):
                start_idx = best_path[i]
                end_idx = best_path[i + 1]

                # Vérification de sécurité
                if start_idx < len(nodes) and end_idx < len(nodes):
                    line = create_line(
                        nodes[start_idx][0], nodes[start_idx][1],
                        nodes[end_idx][0], nodes[end_idx][1],
                        "red",   # Couleur du meilleur chemin
                        3        # Épaisseur renforcée
                    )
                    shapes.append(line)
        
        for i in range(len(nodes)) :
            x,y = nodes[i]
            noeud = ft.Container(border_radius = 10,
                                 height = 20,
                                 width = 20,
                                 left = x-10,
                                 top = y-10,
                                 content = ft.Text(f"{i}"),
                                 bgcolor = "green")
            shapes.append(noeud)
        zone.content = ft.Stack(controls = shapes, 
                                width = 600, height = 500)
        page.update()

    def calculer_distances() :
        M = [[0 for _ in range(len(nodes))] for _ in range(len(nodes))]
        for i in range(len(nodes)) :
            for j in range(len(nodes)) :
                xi,yi = nodes[i]
                xj,yj = nodes[j]
                d = sqrt((xi-xj)**2 + (yi-yj)**2)
                M[i][j] = d
        return M
    
    def update_callback(iter_num, current_best_path, current_pheromones):
        
        #Callback appelé par l’algorithme à chaque itération
        #pour mettre à jour l’interface graphique.

        nonlocal iteration, best_path, pheromones

        # Mise à jour des variables globales
        iteration = iter_num
        best_path = current_best_path[0] if current_best_path else []
        pheromones = current_pheromones

        async def update_ui():
            # Affichage du numéro d’itération
            iteration_text.value = f"Itération: {iteration}"

            # Affichage du meilleur chemin et de sa longueur
            if current_best_path:
                path_text.value = (
                    f"Meilleur chemin: {best_path} "
                    f"(longueur: {current_best_path[1]:.2f})")

            # Calcul de la moyenne des phéromones
            avg = sum(sum(row) for row in pheromones) / (len(nodes) ** 2)
            pheromone_text.value = f"Phéromones moyennes: {avg:.4f}"

            # Redessiner le graphe
            dessiner_graphe()

        # Lancement asynchrone pour ne pas bloquer l’UI
        page.run_task(update_ui)


    

ft.run(main)