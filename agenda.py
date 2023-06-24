#!/usr/bin/python3
from www import *
import os

nav.allowDL(["style.css"])

nbJours = 7
heureDebut = 8
heureFin = 20
nbHeures = heureFin - heureDebut


def init(table:list):
    table = [[""]*nbJours for i in range(nbHeures)]
    return table


def afficher(table:list):
    nav.write("""
    <table>
        <thead>
            <tr>
                <th> Agenda </th>
                <th> Lundi </th>
                <th> Mardi </th>
                <th> Mercredi </th>
                <th> Jeudi </th>
                <th> Vendredi </th>
                <th> Samedi </th>
                <th> Dimanche </th>
            </tr>
        </thead>
        <tbody>
    """)
    compteur = heureDebut
    for I in range(nbHeures):
        nav.write("""
            <tr>
                <th>""")
        value = str(compteur) + "h - " + str(compteur+1) +"h"
        nav.write(value)
        compteur += 1
        nav.write("""
                </th>
        """)
        for Y in range(nbJours):
            if table[I][Y] == '':
                nav.write("""
                                <td></td>
                """)
            else:
                nav.write("""
                                <td> """)
                nav.write(table[I][Y])
                nav.write("""
                                </td> """)
        nav.write("""
                    </th>
        """)
    nav.write("""
                </tbody>
    """)
    nav.write("""
                </table>
    """)
    return


def modification(table:list,ligne:int,colonne:int,valeur:str):
    table[ligne][colonne]+= " -"+valeur
    return

def sauvegarder(table:list,nom:str):
    with open(nom, "w") as fichier:
        for I in range(nbHeures):
            resultat = str(I)
            for J in range(nbJours):
                if table[I][J] != "":
                    resultat += " " + str(J) +table[I][J]
                    fichier.write(resultat+"\n")
                    resultat = str(I)

def importer(table:list,nom:str):
    with open(nom, "r") as fichier:
        tab = fichier.readlines()
        table = [[""]*nbJours for i in range(nbHeures)]
        for I in range(len(tab)):
            testeee = tab[I]
            resultat = int
            resultat2 = int
            resultat3 = ""
            resultat = testeee[0]
            if testeee[1] != " ":
                resultat += testeee[1]
                testeee = testeee[3:]
            else:
                testeee = testeee[2:]
            resultat = int(resultat)
            resultat2 = int(testeee[0])
            testeee = testeee[2:]
            resultat3 = testeee
            table[resultat][resultat2] = resultat3
    return table

#Codé par Bryan Lhomme
def echange2cases(table,ligne1,colonne1,ligne2,colonne2):
    tmp=table[ligne1][colonne1]
    table[ligne1][colonne1]=table[ligne2][colonne2]
    table[ligne2][colonne2]=tmp


#Codé par Axel Kleszewski
def gererSemaine(tab:list)->str:
    semaine=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
    listesemaine = []
    for i in range(nbJours):
        listejour = [semaine[i]]
        for j in range(nbHeures):
            if tab[j][i] != '':
                listejour.append(j+8)
                listejour.append(tab[j][i])
        listesemaine.append(listejour)
    return listesemaine

#Codé par Thibault Lombart
def copiercoupercoller(table,option,ligne,colonne):
   global tmp
   if option == 'copier':
       tmp = table[ligne][colonne]
   elif option == 'couper':
       tmp = table[ligne][colonne]
       table[ligne][colonne] = ''
   elif option == 'coller':
       table[ligne][colonne] += tmp


fini = False
tabl = []
tabl = init(tabl)
test=True


ligne = 0
colonne = 0
valeur = ""
tour = True
while not(fini):
    nav.beginPage()
    nav.write("""
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="style.css" />
                <title>Agenda</title>
            </head>
            <body>
                <h1> Agenda </h1>
    """)
    if not(tour):
        if "importer" in nav.form:
            nom = nav.form["importer"]
            nom = nom+'.txt'
            listefichier=os.listdir(os.getcwd())
            if nom in listefichier:
                tabl = importer(tabl,nom)
            else:
                nav.write("""
                    <h3> Erreur dans l'importation, il n'y a pas ce fichier</h3>
                """)

        if "sauvegarder" in nav.form:
            nom = nav.form["sauvegarder"] + ".txt"
            listefichier=os.listdir(os.getcwd())
            if not(nom in listefichier):
                sauvegarder(tabl,nom)
            else:
                nav.write("""
                    <h3> Erreur dans la sauvegarde, Il y a deja un fichier de ce nom</h3>
                """)
                
        if "colonne1" in nav.form:
            colonne1 = int(nav.form["colonne1"])
            ligne1 = int(nav.form["ligne1"])
            colonne2 = int(nav.form["colonne2"])
            ligne2 = int(nav.form["ligne2"])
            echange2cases(tabl,ligne1,colonne1,ligne2,colonne2)
            
        if "valeur" in nav.form:
            valeur = str(nav.form['valeur'])
            ligne = int(nav.form['ligne'])
            colonne = int(nav.form['colonne'])
            modification(tabl,ligne,colonne,valeur)
            ligne = int
            colonne = int
            valeur = str
        
        if "choix" in nav.form:
            choix = str(nav.form["choix"])
            ligne = int(nav.form['lignechoix'])
            colonne = int(nav.form['colonnechoix'])
            copiercoupercoller(tabl,choix,ligne,colonne)
            
    nav.write("""
              <div class="Formulaires">
                    <div class="gauche">
                            <form method="POST">
                                Entrez les informations : 
                                <select name="colonne" id="" required>
                                    <option value="">Jour</option>
                                    <option value="0">Lundi</option>
                                    <option value="1">Mardi</option>
                                    <option value="2">Mercredi</option>
                                    <option value="3">Jeudi</option>
                                    <option value="4">Vendredi</option>
                                    <option value="5">Samedi</option>
                                    <option value="6">Dimanche</option>
                                </select>
                                <select name="ligne" id="" required>
                                    <option value="">Heure</option>
                                    <option value="0">8h - 9h</option>
                                    <option value="1">9h - 10h</option>
                                    <option value="2">10h - 11h</option>
                                    <option value="3">11h - 12h</option>
                                    <option value="4">12h - 13h</option>
                                    <option value="5">13h - 14h</option>
                                    <option value="6">14h - 15h</option>
                                    <option value="7">15h - 16h</option>
                                    <option value="8">16h - 17h</option>
                                    <option value="9">17h - 18h</option>
                                    <option value="10">18h - 19h</option>
                                    <option value="11">19h - 20h</option>
                                </select>
                                <input type="text" name="valeur" placeholder="Ajout" required> 
                                <input type="submit" name="Valider">
                            </form>
                            <form method="POST">
                                Si vous voulez importer (uniquement le nom demande):
                                <input type="text" name="importer" placeholder="Nom du fichier(dans le dossier local)">
                                <input type="submit" name="Valider">
                            </form>
                            <form method="POST">
                                Si vous voulez sauvegarder (uniquement le nom demande):
                                <input type="text" name="sauvegarder" placeholder="Nom du fichier(dans le dossier local)">
                                <input type="submit" name="Valider">
                            </form>
                            <form method="POST">
                                Echange de cases : 
                                <select name="colonne1" id="" required>
                                    <option value="">Jour</option>
                                    <option value="0">Lundi</option>
                                    <option value="1">Mardi</option>
                                    <option value="2">Mercredi</option>
                                    <option value="3">Jeudi</option>
                                    <option value="4">Vendredi</option>
                                    <option value="5">Samedi</option>
                                    <option value="6">Dimanche</option>
                                </select>
                                <select name="ligne1" id="" required>
                                    <option value="">Heure</option>
                                    <option value="0">8h - 9h</option>
                                    <option value="1">9h - 10h</option>
                                    <option value="2">10h - 11h</option>
                                    <option value="3">11h - 12h</option>
                                    <option value="4">12h - 13h</option>
                                    <option value="5">13h - 14h</option>
                                    <option value="6">14h - 15h</option>
                                    <option value="7">15h - 16h</option>
                                    <option value="8">16h - 17h</option>
                                    <option value="9">17h - 18h</option>
                                    <option value="10">18h - 19h</option>
                                    <option value="11">19h - 20h</option>
                                </select>
                                Avec :
                                <select name="colonne2" id="" required>
                                    <option value="">Jour</option>
                                    <option value="0">Lundi</option>
                                    <option value="1">Mardi</option>
                                    <option value="2">Mercredi</option>
                                    <option value="3">Jeudi</option>
                                    <option value="4">Vendredi</option>
                                    <option value="5">Samedi</option>
                                    <option value="6">Dimanche</option>
                                </select>
                                <select name="ligne2" id="" required>
                                    <option value="">Heure</option>
                                    <option value="0">8h - 9h</option>
                                    <option value="1">9h - 10h</option>
                                    <option value="2">10h - 11h</option>
                                    <option value="3">11h - 12h</option>
                                    <option value="4">12h - 13h</option>
                                    <option value="5">13h - 14h</option>
                                    <option value="6">14h - 15h</option>
                                    <option value="7">15h - 16h</option>
                                    <option value="8">16h - 17h</option>
                                    <option value="9">17h - 18h</option>
                                    <option value="10">18h - 19h</option>
                                    <option value="11">19h - 20h</option>
                                </select>
                                <input type="submit" name="Valider">
                            </form>
                            <form method="POST">
                                Voulez vous Copier, Couper ou coller ? 
                                <select name="choix" id="" required>
                                    <option value="">Choix</option>
                                    <option value="copier">Copier</option>
                                    <option value="couper">Couper</option>
                                    <option value="coller">Coller</option>
                                </select>
                                <select name="colonnechoix" id="" required>
                                    <option value="">Jour</option>
                                    <option value="0">Lundi</option>
                                    <option value="1">Mardi</option>
                                    <option value="2">Mercredi</option>
                                    <option value="3">Jeudi</option>
                                    <option value="4">Vendredi</option>
                                    <option value="5">Samedi</option>
                                    <option value="6">Dimanche</option>
                                </select>
                                <select name="lignechoix" id="" required>
                                    <option value="">Heure</option>
                                    <option value="0">8h - 9h</option>
                                    <option value="1">9h - 10h</option>
                                    <option value="2">10h - 11h</option>
                                    <option value="3">11h - 12h</option>
                                    <option value="4">12h - 13h</option>
                                    <option value="5">13h - 14h</option>
                                    <option value="6">14h - 15h</option>
                                    <option value="7">15h - 16h</option>
                                    <option value="8">16h - 17h</option>
                                    <option value="9">17h - 18h</option>
                                    <option value="10">18h - 19h</option>
                                    <option value="11">19h - 20h</option>
                                </select>
                                <input type="submit" name="Valider">
                            </form>
                        </div>
                        <div class="droite">
    """)
    resultat = gererSemaine(tabl)
    vide = True
    print(resultat)
    for I in range(len(resultat)):
        if len(resultat[I]) > 1:
            vide = False
    
    if vide:
        nav.write("<h3> Vous n'avez rien a faire cette semaine </h3>")
    else:
        nav.write("<h3> Vous avez a faire cette semaine : </h3>")
        while len(resultat) != 0:
            if len(resultat[0]) != 1:
                date = str(resultat[0].pop(0))
                conc = "<h4>" + date + " : " + "</h4>"
                nav.write(conc)
                while len(resultat[0]) > 0:
                    heure = resultat[0].pop(0)
                    heure2 = str(heure+1)
                    heure = str(heure)
                    activite = str(resultat[0].pop(0))
                    condense = "<p> De "+heure+"h a "+heure2+"h : "+activite+"</p>"
                    nav.write(condense)
                resultat.pop(0)
            else:
                resultat.pop(0)
    
    nav.write("""
              </div>
            </div>
    """)
            
    
    afficher(tabl)
    nav.write("""
            </body>
        </html>
    """)
    nav.endPage()
    tour = False
