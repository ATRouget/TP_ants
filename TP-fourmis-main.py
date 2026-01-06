import flet as ft
import random as rd
from math import *

def main(page):
    page.title = "Algorithme de colonie de fourmis"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    titre = ft.Text("Visualisation de l'Algorithme", size=24)

    
    bouton = ft.Button("Cliquez", on_click=lambda e: print("cliqué !"))
    createur = ft.Button("Générer le graphe", on_click=lambda e: generer_nodes())

    page.add(ft.Column([titre, bouton]))

    champ1 = ft.TextField(label = 'Nombre de noeuds', value = '20', width = 150)
    champ2 = ft.TextField(label = 'Nombre de fourmis', value = '15', width = 150)
    champ3 = ft.TextField(label = "Nombre de d'itérations", value = '100', width = 150)
    

    zone = ft.Container(width = 600, height =  500, bgcolor = 'lightblue', border = ft.border.all(2,'blue'))

    statut = ft.Text("Prêt à démarrer", color = 'green', size = 16)

    page.add(ft.Column([ft.Text("Paramètres de l'algorithme", size = 16), ft.Row([champ1,champ2,champ3]), createur, ft.Divider(), statut, zone]))

    nodes = []
    def generer_nodes():
        try:
            N = int(champ1.value)
        except ValueError: N=20
        for _ in range(N):
            x = rd.uniform(50,550)
            y = rd.uniform(50,450)
            nodes.append((x,y))
        distances = calculer_distances()
        
        dessiner_graphe()

        print(f"{len(nodes)} nœuds générés")
        print(f"Distance entre nœud 0 et 1 : {distances[0][1]:.2f}")
    
    def dessiner_graphe():
        shapes = []
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


    

ft.run(main)