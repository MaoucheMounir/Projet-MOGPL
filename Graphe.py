import random as rd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import copy


################################  GRAPHES  ####################################################

#Notre structure de graphe se presente sous la forme d'une liste de 4 elements, comme suit :
#le premier: le nombre de sommets,
#le deuxieme: un set des sommets du graphe
#le troisieme: le nombre d'arcs du graphe
#le quatrieme: un set des arcs du graphe, ou chaque arete est un tuple (sommet1, sommet2)

#Voici un exemple de graphe:
#[5, {0, 1, 2, 3, 4}, 6, {(0, 1):5, (1, 2):-1, (0, 3):3, (4, 2):6, (3, 2):-4, (4, 1):8}]


def genererGraphe (n, p, borneInterval=10):

  #verifier que n est un entier positif et p une proba entre 0 et 1
  if(n<0 or not isinstance(n,int)):
    raise Exception("Le premier paramètre 'n' doit etre un entier positif")
  if(p<=0 or p>=1):
    raise Exception("Le deuxième paramètre 'p' doit etre une valeur de probabilité entre 0 et 1")

  G=[0,set(),0,set()]
  for i in range(n):
    for j in range(n):
      if(i!=j): #une arete doit etre composée à partir de deux sommets distincts

        if(rd.random()<=p): #créer une arete entre i et j avec une probabilité de p
          #ajouter i et j à la liste des sommets de G
          G[1].add(i)
          G[1].add(j)
          G[0]=len(G[1]) #compter le nombre de sommets de G (dans un set)

          aretes=G[3].copy()
          if (j, i) not in G[3]:
            aretes.add((i,j)) #ajouter l'arete (i,j) à la liste des aretes de G
          G[3]=aretes.copy()
          G[2]=len(G[3]) #compter le nombre d'aretes de G (dans un set)

  aretes=G[3]
  for i in range(n):
    if( i not in G[1]): #traiter le cas ou il existe un sommet isolé dans G

      G[1].add(i) #ajouter le sommet i
      G[0]=len(G[1]) #compter le nombre de sommets de G (dans un set)

      j=rd.randint(0,n-1) #tirer un sommet aléatoirement
      while j == i:
        j=rd.randint(0,n-1) #tirer un sommet aléatoirement

      s=rd.randint(0,1)
      if(s==0):
        aretes.add((i,j)) #ajouter l'arete (i,j) à la liste des aretes de G
      else :
        aretes.add((j,i)) #ajouter l'arete (j,i) à la liste des aretes de G
      G[3]=aretes.copy()
      G[2]=len(G[3]) #compter le nombre d'aretes de G (dans un set)

  while(G[2]==0): #s'assurer que le graphe à retourner n'est pas vide
    G=genererGraphe(n,p, borneInterval)

  #ajouter les poids aux arcs
  E=G[3]
  E_poids=dict()
  for e in E:
    E_poids.update({e:0})
  G_final=copy.deepcopy(G)
  G_final[3]=  E_poids
  G_final= ajouter_poids(G_final, borneInterval)   ##Appel à ajouter_poids pour ajouter les poids
  return G_final

def ajouter_poids(Graphe, borneInterval=10):
  G=copy.deepcopy(Graphe)
  E=G[3]

  for arc in E:
    poids=rd.randint(-borneInterval, borneInterval) #poids tire de maniere uniforme et aleatoire parmi les entiers d’un intervalle
    G[3].update({arc:poids})

  return G

def supprimerSommet(G_init,v):
  G=G_init.copy()
  if G[0]>0 : #on considère qu'un graphe doit garder au moins un sommet

    if(v in G[1]): #on ne peut supprimer une arete que si elle existe dans G
      G[1].remove(v) #supprimer le sommet de la liste des sommets
      G[0] -=1 #mettre à jour le nombre de sommets de G

      #supprimer toutes les aretes pour lesquelles v est une
      aretes=G[3].copy() #créer une copie afin d'éviter de supprimer sur une liste qu'on itère
      for arete in G[3]:
        if v in arete :
          del aretes[arete] #supprimer l'arete de l'ensemble des aretes de G
          G[2] -=1 #mettre à jour le  nombre d'aretes de G
      G[3]=aretes.copy()
    else:
      raise Exception("Le sommet que vous souhaitez supprimer n'existe pas dans le graphe")
  else:
      raise Exception("Un graphe doit contenir au moins un sommet")
  return G

#############################################

def getDegres (G): #retourne un tableau de tuple tel que chaque sommet et associé à son degré_pos= nombre d'arcs sortants degré_neg= nombre d'arcs entrants
  degres = []

  for sommet in G[1]: #parcourir tous les sommets de G
    degre_pos=0
    degre_neg=0
    for arete in G[3]: #compter le nombre de fois ou chaque sommet apparait en tant qu'extrémité d'une arete
      if sommet in arete :
        if sommet == arete[0]:
          degre_pos +=1
        if sommet == arete[1]:
          degre_neg +=1

    degres.append((sommet, degre_pos, degre_neg)) #créer un tuple pour représenté le degré de chaque sommet de G

  return degres

def maxDifDeg(G):
  degres = getDegres (G)
  dmax = 0
  smax = None

  for d in degres:
    diff_d = d[1] - d[2]
    if diff_d >= dmax:
      dmax = diff_d
      smax = d[0]

  return smax

def maxDegPos(G, list_sommets_testes=[]):
  degres = getDegres (G)
  dmax = 0
  smax = None

  for d in degres:
    diff_d = d[1]
    if diff_d > dmax and  d[0] not in list_sommets_testes :
      dmax = diff_d
      smax = d[0]

  return smax

def getAretesEntrantes(G, sommet):
    listeAretes = []
    for e in G[3]:     #Recuperer une arete qui commence par le sommet au premier rang dans l'ordre
        if e[1] == sommet:
            listeAretes.append(e)

    return listeAretes

#############################################

def getSource(Graphe):
  G = Graphe.copy()

  degres = getDegres(G)

  for d in degres:
    if d[2] == 0:   #Le degre negatif est nul donc le sommet n'a aucun arc entrant, c'est donc une source
      return d[0]
  return None

def getSources(Graphe):
  G = Graphe.copy()
  sources = []
  degres = getDegres(G)

  for d in degres:
    if d[2] == 0:   #Le degre negatif est nul donc le sommet n'a aucun arc entrant, c'est donc une source
      sources.append(d[0])


  return sources

def getPuits(Graphe):
  G = Graphe.copy()

  degres = getDegres(G)

  for d in degres:
    if d[1] == 0:   #Le degre positif est nul donc le sommet n'a aucun arc sortant, c'est donc un puits
      return d[0]
  return None

#############################################

#Cette fonction retourne les sucesseurs d'un sommet donne dans un graphe G
def getSuccesseurs(G,sommet):
  E=G[3]
  voisins=[]
  for i,j in E :
    if i==sommet:
      voisins.append(j)

  return set(voisins)

def getSommetsAtteignables(G, source_potentielle, list_sommets_atteints):
  successeurs_source_potentielle=getSuccesseurs(G,source_potentielle)

  sommets_atteignables = set()
  for successeur in list(successeurs_source_potentielle):
    sommets_atteignables.update({successeur})

    if successeur not in list_sommets_atteints: #il faut que la source donnée initialement soit différente d'un des sommets à considérer comme successeurs
      for s in list(sommets_atteignables):
        list_sommets_atteints.append(s)

      sommets_atteignables.update(getSommetsAtteignables(G, successeur, list_sommets_atteints))


  return sommets_atteignables

#############################################

def dessinerGraphe(arborescence):
  # créer un graphe avec la bibliotheque NetworkX
  G_nx = nx.DiGraph()

  #ajouter les arcs avec les poids au graphe
  for arc, poids in arborescence.items():
      G_nx.add_edge(arc[0], arc[1], weight=poids)

  #dessiner le graphe
  pos = nx.spring_layout(G_nx)
  nx.draw(G_nx, pos, with_labels=True, font_weight='bold', node_size=700, node_color='black', font_size=8, font_color='white')

  #ajouter les étiquettes de poids sur les arcs
  labels = nx.get_edge_attributes(G_nx, 'weight')
  nx.draw_networkx_edge_labels(G_nx, pos, edge_labels=labels)

  #afficher le graphe
  plt.show()

def transformer_Arbo_Graphe(arborescence):  #Creer une structure de graphe a partir d'une arborescence
  G = []
  V = set()
  for sommet1, sommet2  in arborescence.keys() :
    V.add(sommet1)
    V.add(sommet2)

  G.append(len(V))
  G.append(V)
  G.append(len(arborescence))
  G.append(arborescence)

  return G
