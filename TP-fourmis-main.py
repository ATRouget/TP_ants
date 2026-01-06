import flet as ft

def main(page):
    page.title = "Algorithme de colonie de fourmis"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    titre = ft.Text("Visualisation de l'Algorithme", size=24)

    
    bouton = ft.Button("Cliquez", on_click=lambda e: print("cliqué !"))
    
    page.add(ft.Column([titre, bouton]))

    champ1 = ft.TextField(label = 'Nombre de noeuds', value = '20', width = 150)
    champ2 = ft.TextField(label = 'Nombre de fourmis', value = '15', width = 150)
    champ3 = ft.TextField(label = "Nombre de d'itérations", value = '100', width = 150)
    

    zone = ft.Container(width = 600, height =  500, bgcolor = 'lightblue', border = ft.border.all(2,'blue'))

    statut = ft.Text("Prêt à démarrer", color = 'green', size = 16)

    page.add(ft.Column([ft.Text("Paramètres de l'algorithme", size = 16), ft.Row([champ1,champ2,champ3]), ft.Divider(), statut, zone]))

ft.run(main)