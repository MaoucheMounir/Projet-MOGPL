############################   Solution   #####################################################
import random as rd
import os

from Graphe import *


##Question 1

def bellmanFord(Graphe, source):
  G=Graphe.copy() 
  arborescence=dict()

  k=1; cpt=0
  nb_sommet=G[0]
  V=Graphe[1] #recuperer l'ensemble des sommets de G
  pred=dict() #enregistrer les predecesseurs de chaque sommet

  G[1]=dict()

  #mettre les etiquettes à l'infini pour tous les sommets de G
  for u in V :
    G[1].update({u : float('inf')})

  V=G[1] #recuperer l'ensemble des sommets de G
  E=G[3] #recuperer l'ensemble des aretes de G

  #initialiser l'etiquette de la source
  G[1].update({source : 0})


  while k<nb_sommet+1: #on admet une itération supplémentaire afin de tester si il existe un circuit absorbant
    cpt=0 #nombre de sommets mis à jour

    for e in E :

      poids_e=E.get(e) #recuperer le poids de l'arete e
      sommet1, sommet2=e
      etiquette_sommet1=V.get(sommet1)
      etiquette_sommet2=V.get(sommet2)

      if etiquette_sommet1 + poids_e < etiquette_sommet2:
        etiquette_new= etiquette_sommet1 + poids_e
        G[1].update({sommet2 : etiquette_new})
        pred.update({sommet2:sommet1})
        cpt +=1


    if(cpt==0): #l'algorithme a convergé car à un certain moment plus aucun sommet n'a changé d'étiquette
      break

    k +=1

  if(cpt!=0): #Le graphe comporte un circuit absorbant car on a dépassé n-1 itérations et les sommets continuent à etre modifiés

    return -1

  #---- construire l'arborescence

  #inverser les predecesseurs et les représenter sous forme d'arete
  pred_tuples=list(pred.items())
  i=0
  for t in pred_tuples :
    pred_tuples[i]=tuple(reversed(t))
    i+=1

  #associer à chaque arete son poids
  for e in pred_tuples:
    poids_e= E.get(e)
    arborescence.update({e:poids_e})

  #retroune G avec les étiquettes des sommets, l'arborescence des plus courts chemins et k le nombre d'itérations avant la convergence
  return G, arborescence, k 


##Question 2

def gloutonFas(Graphe):
  S1 = []
  S2 = []
  G = copy.deepcopy(Graphe)
  nb_sommets_G= G[0]


  while nb_sommets_G != 0:   #Tant que le graphe n'est pas vide

    u = getSource(G)

    while u != None :        #Tant que G contient une source
       S1.append(u)
       G = supprimerSommet(G, u)
       u = getSource(G)


    u = getPuits(G)

    while u != None :         #Tant que G contient un puits
       S1.append(u)
       G = supprimerSommet(G, u)
       u = getPuits(G)


    u = maxDifDeg(G)          #Si il n'y a pas de puits ou de source, supprimer le sommet pour lequel

    if u != None:             #la différence entre le degré positif et négatif est maximale
      S1.append(u)
      G = supprimerSommet(G, u)

    nb_sommets_G = G[0]


  return S1+S2


##Question 3

def getSource_V2(Graphe): #la source retournée par cette fonction verifie la condition que au moins |V|/2 sommets sont atteignables à partir d'elle
  G=copy.deepcopy(Graphe)

  verifie=False
  list_sommets_testes=[]

  source_potentielle=0
  sources_potentielles = getSources(G)
  i=0
  while not verifie and i < len(sources_potentielles):  #On verifie en priorite les sommets qui n'ont aucun predecesseur
    source_potentielle = sources_potentielles[i]
    if(source_potentielle != None) :
      list_sommets_testes.append(source_potentielle)

      list_sommets_atteints=[source_potentielle]

      sommets_atteignables= getSommetsAtteignables(G, source_potentielle, list_sommets_atteints)


      if len(sommets_atteignables) >= G[0]/2  :
        return source_potentielle
    i += 1



  while not verifie and source_potentielle != None: #Tant qu'on a pas encore trouvé de source qui verifie la condition que au moins |V|/2 sommets sont atteignables à partir d'elle

    source_potentielle=maxDegPos(G, list_sommets_testes)


    if(source_potentielle != None) :
      list_sommets_testes.append(source_potentielle) #ajouter le sommet aux sources deja testées et non concluantes

      list_sommets_atteints=[source_potentielle]

      sommets_atteignables= getSommetsAtteignables(G, source_potentielle, list_sommets_atteints)

      if len(sommets_atteignables) >= G[0]/2  :
        verifie = True
        return source_potentielle

  return -1 # dans le cas où aucun sommet du graphe ne verifie la condition que au moins |V|/2 sommets sont atteignables à partir de lui


def construire_Gi(Graphe, borneInterval=10): #Cette fonction ajoute des poids à un graphe
  G=copy.deepcopy(Graphe)
  E=G[3]

  for arc in E:
    poids=rd.randint(-borneInterval, borneInterval) #poids tiré de maniere uniforme et aleatoire parmi les entiers d’un intervalle
    G[3].update({arc:poids})

  return G


def construire_listGi(Graphe, Ni, borneInterval=10): #Ni = nombre de Gi a construire
  listGi=[]
  G=Graphe.copy()
  i=0
  while i <Ni:

    Gi=construire_Gi(G, borneInterval=10)

    source=getSource_V2(Gi)
    if(bellmanFord(Gi, source) !=-1): #S'assurer qu'il n'existe pas de circuit absorbant avec les valeurs actuelles de poids
      listGi.append(Gi)
      i +=1

  return listGi


## Question 4

def unionArborescence(listGi):
  list_arborescences=set()
  union_arborescences = []

  ## Calculer l'arborescence des plus courts chemins de chaque Gi, 
  ## et faire l'union de leurs aretes

  for Gi in listGi:         
    source = getSource_V2(Gi)
    Gi_etiq, arborescence_i, k_i=bellmanFord(Gi, source)
    #dessinerGraphe(arborescence_i) 
    list_arborescences=list_arborescences.union(set(arborescence_i.keys()))
    
  #Transformer l'union des arborescences en dictionnaire et affecter des poids de 1 aux aretes

  dict_arborescences = dict()    
  for k in list(list_arborescences):
    dict_arborescences.update({k:1})
  T=dict_arborescences
  return T



##Question 6

def bellmanFordOrdre(Graphe, ordre):  #Algorithme de Bellman Ford qui suit un ordre donné en entrée
  G=Graphe.copy()
  arborescence = dict()
  source = ordre[0]
  k=0; cpt=0
  nb_sommet = G[0]

  V=Graphe[1] #recuperer l'ensemble des sommets de G
  pred=dict()#enregistrer les predecesseurs de chcaque sommet

  G[1]=dict()  #Transformer G[1] en dict pour qu'il puisse recevoir les etiquettes des sommets

  #mettre les etiquettes à l'infini pour tous les sommets de G
  for u in V :
    G[1].update({u : float('inf')})

  V=G[1] #recuperer l'ensemble des sommets de G avec etiquettes
  E=G[3] #recuperer l'ensemble des aretes de G

  #initialiser l'etiquette de la source
  G[1].update({source : 0})


  while k<nb_sommet+1: #on admet une itération supplémentaire afin de tester si il existe un circuit absorbant
    cpt=0 #nombre de sommets mis à jour

    for sommet_ordre in ordre : #Iterer sur toutes les aretes du graphes 

      aretesEntrantes = getAretesEntrantes(G, sommet_ordre)

      for e in aretesEntrantes:
        poids_e = E.get(e)
        sommet_pred = e[0]
        etiq_pred = V.get(sommet_pred)
        etiq_sommetOrdre=V.get(sommet_ordre)

        if etiq_pred + poids_e < etiq_sommetOrdre:
            etiquette_new= etiq_pred + poids_e
            G[1].update({sommet_ordre : etiquette_new})
            pred.update({sommet_ordre : sommet_pred})
            cpt +=1


    if(cpt==0): #l'algorithme a convergé car à un certain moment plus aucun sommet n'a changé d'étiquette
      break

    k +=1

  if(cpt!=0): #Le graphe comporte un circuit absorbant car on a dépassé n-1 itérations et les sommets continuent à etre modifiés

    return -1

  #---- construire l'arborescence

  #inverser les predecesseurs et les représenter sous forme d'aretes pour avoir les chemins vers chaque sommet
  pred_tuples=list(pred.items())
  i=0
  for t in pred_tuples :
    pred_tuples[i]=tuple(reversed(t))
    i+=1

  #associer à chaque arete son poids
  for e in pred_tuples:
    poids_e= E.get(e)
    arborescence.update({e:poids_e})

  #retroune G avec des etiquettes sur les sommets, l'arborescence des plus courts chemins et k le nombre d'itteration avant la convergence
  return G, arborescence, k 


##Question 7  

def getOrdreAleatoire0(G):
    V = list(G[1])
    rd.shuffle(V)
    return V

def getOrdreAleatoire(G, source):
    V = list(G[1])
    V.remove(source)
    rd.shuffle(V)
    
    V = [source] + (V)
    return V


##Question 8

def meilleur_resultat(resultatOrdreTotal, resultatOrdreAleatoire):
    if resultatOrdreTotal < resultatOrdreAleatoire:
        print("Bellman Ford avec ordre total est meilleur qu'avec un ordre aleatoire")
    elif resultatOrdreTotal > resultatOrdreAleatoire:
        print("Bellman Ford avec ordre aleatoire est meilleur qu'avec un ordre total")
    else:
        print("Les résultats sont égaux")
#######

def verifierSource_V2(G, n, p, borneInterval):     #Verifie si le graphe possede une source qui permet d'atteindre au moins |V|/2 sommets, si non il regenere un autre graphe qui en possede une
  source = getSource_V2(G)

  while source == -1 :
    G = genererGraphe(n, p, borneInterval)
    source = getSource_V2(G)
  
  G.append(source)
  return G

def verifierCircuitAbsorbant(G):    #Verifie qu'il n'existe pas de circuit absorbant, si oui retourne le meme graphe avec un autre ensemble de poids
    bf = bellmanFord(G, getSource_V2(G))

    while bf == -1:
        G = construire_Gi(G)
        bf = bellmanFord(G, getSource_V2(G))

    return G

def genererGrapheValide(n, p, borneInterval=10):  #Retourne un graphe avec source V2 et sans circuit absorbant
    G = genererGraphe(n, p, borneInterval)
    G = verifierSource_V2(G, n, p, borneInterval)
    G = verifierCircuitAbsorbant(G)

    return G

#######


##Question 9    

def get_nbIterations_ordre_total(G, H, Ni):
    liste_Gi = construire_listGi(G, Ni)

    T = unionArborescence(liste_Gi)
    T = transformer_Arbo_Graphe(T)
    ordre = gloutonFas(T)
    #print("ordre total utilise:", ordre)
    #bf = bellmanFordOrdre(H, ordre)
    _, _, k_ordre = bellmanFordOrdre(H, ordre)
    source = ordre[0]      #Recuperer la source utilisee pour utiliser la meme pour l'ordre aleatoire

    return k_ordre, source

def get_nbIterations_ordre_aleatoire(H, source):
    ordre = getOrdreAleatoire(H, source)
    #print("Ordre aleatoire utilise :", ordre)
    _, _, k_aleatoire = bellmanFordOrdre(H, ordre)

    return k_aleatoire

#######

def comparer_ordre_total_aleatoire(tailles, probas, bornesIntervals, Ni):
    resultats = np.empty((len(tailles), len(probas), len(bornesIntervals)), dtype=object)

    for i_n in range(len(tailles)):    #Faire varier le nombre de sommets de G
        n=tailles[i_n]
        
        for i_p in range(len(probas)):        #Faire varier la densité de G
            p=probas[i_p]
            
            for i_borneInterval in range(len(bornesIntervals)):    #Faire varier les bornes des intervalles
                borneInterval=bornesIntervals[i_borneInterval]
                
                
                G = genererGrapheValide(n, p, borneInterval)     #Generer le graphe de depart
                H = construire_listGi(G, 1)[0]                   #Generer le graphe de test
                k_ordre, source = get_nbIterations_ordre_total(G, H, Ni)     #Récupérer le nombre d'itérations retourné par Bellman-Ford en utilisant l'ordre total, ainsi que la source utilisee

                k_aleatoire = get_nbIterations_ordre_aleatoire(H, source) #Récupérer le nombre d'itérations retourné par Bellman-Ford en utilisant un ordre aléatoire
                
                resultats[i_n, i_p, i_borneInterval]=(H, k_ordre, k_aleatoire)
    
    return resultats

def get_moyenne_taille(tailles, probas, bornesIntervals, resultats):
    moyenne_tailles_Tot=[]
    moyenne_tailles_Al=[]
    for i_n in range(len(tailles)):    #Faire varier le nombre de sommets de G
        n=tailles[i_n]
        moyenne_tailles_i_nbIterOrdreTot=0
        moyenne_tailles_i_nbIterOrdreAl=0
        somme_tailles_nbIterordreTot=0
        somme_tailles_nbIterordreAl=0
        for i_p in range(len(probas)):                   #Faire varier la densité de G
            p=probas[i_p]
            for i_borneInterval in range(len(bornesIntervals)):    #Faire varier les bornes des intervalles
                somme_tailles_nbIterordreTot += resultats[i_n, i_p, i_borneInterval][1]
                somme_tailles_nbIterordreAl += resultats[i_n, i_p, i_borneInterval][2]
        moyenne_tailles_i_nbIterOrdreTot=somme_tailles_nbIterordreTot/(len(probas)*len(bornesIntervals))
        moyenne_tailles_Tot.append(moyenne_tailles_i_nbIterOrdreTot)

        moyenne_tailles_i_nbIterOrdreAl=somme_tailles_nbIterordreAl/(len(probas)*len(bornesIntervals))
        moyenne_tailles_Al.append(moyenne_tailles_i_nbIterOrdreAl)

    return moyenne_tailles_Tot, moyenne_tailles_Al

def get_moyenne_probas(tailles, probas, bornesIntervals, resultats):
    moyenne_Tot=[]
    moyenne_Al=[]
    for i_p in  range(len(probas)):    #Faire varier la densité de G
        p=probas[i_p]
        moyenne_i_nbIterOrdreTot=0
        moyenne_i_nbIterOrdreAl=0
        somme_nbIterordreTot=0
        somme_nbIterordreAl=0

        for i_n in range(len(tailles)):          #Faire varier le nombre de sommets de G
            n=tailles[i_n]
            for i_borneInterval in range(len(bornesIntervals)):    #Faire varier les bornes des intervalles
                somme_nbIterordreTot += resultats[i_n, i_p, i_borneInterval][1]
                somme_nbIterordreAl += resultats[i_n, i_p, i_borneInterval][2]
        moyenne_i_nbIterOrdreTot=somme_nbIterordreTot/(len(tailles)*len(bornesIntervals))
        moyenne_Tot.append(moyenne_i_nbIterOrdreTot)

        moyenne_i_nbIterOrdreAl=somme_nbIterordreAl/(len(tailles)*len(bornesIntervals))
        moyenne_Al.append(moyenne_i_nbIterOrdreAl)

    return moyenne_Tot, moyenne_Al

def get_moyenne_bornesIntervals(tailles, probas, bornesIntervals, resultats):
    moyenne_Tot=[]
    moyenne_Al=[]
    for i_borneInterval in  range(len(bornesIntervals)):    #Faire varier la densité de G
        borneInterval = bornesIntervals[i_borneInterval]
        moyenne_i_nbIterOrdreTot=0
        moyenne_i_nbIterOrdreAl=0
        somme_nbIterordreTot=0
        somme_nbIterordreAl=0

        for i_n in range(len(tailles)):          #Faire varier le nombre de sommets de G
            n=tailles[i_n]
            for i_p in range(len(probas)):    #Faire varier les probas
                somme_nbIterordreTot += resultats[i_n, i_p, i_borneInterval][1]
                somme_nbIterordreAl += resultats[i_n, i_p, i_borneInterval][2]
        moyenne_i_nbIterOrdreTot=somme_nbIterordreTot/(len(tailles)*len(bornesIntervals))
        moyenne_Tot.append(moyenne_i_nbIterOrdreTot)

        moyenne_i_nbIterOrdreAl=somme_nbIterordreAl/(len(tailles)*len(bornesIntervals))
        moyenne_Al.append(moyenne_i_nbIterOrdreAl)

    return moyenne_Tot, moyenne_Al

#######

def plotGraphe(X, Y, x_label = 'x', y_label='y', labels=["Ordre total", "Ordre aleatoire"]) :

    for i in range(len(Y)):
        plt.plot(X, Y[i], label = labels[i])
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend()

    title = x_label + " en fonction de " + y_label
    plt.title(title)

    # vérifier si le dossier "plots" existe, sinon le créer
    if not os.path.exists("plots"):
        os.makedirs("plots")

    # enregistrer le graphe
    nom_fichier = "Graphe_NbIter_" + x_label
    chemin= 'plots/'
    plt.savefig(chemin + nom_fichier + '.png')

    plt.show()


## Question 10


def eval_Ni(G,list_Ni, borneInterval):
    list_k_ordre=[]
    list_k_aleatoire=[]
    
    for Ni in list_Ni :
        moy_k_ordre=0
        moy_k_aleatoire=0
        N_repetitions=10
        for i in range(N_repetitions): #prendre un nombre d'itérations moyen à chaque Ni
            # A partir de G construire les Gi ainsi que H en s'assurant qu'ils ne contiennent pas de circuit négatif
            listGi = construire_listGi(G, Ni, borneInterval=borneInterval)     ##Créer les Ni de Gi

            H = construire_listGi(G, 1, borneInterval=borneInterval)[0]  #Créer H (le graphe de test) séparement
            k_ordre, source = get_nbIterations_ordre_total(G, H, Ni)     #Récupérer le nombre d'itérations retourné par Bellman-Ford en utilisant l'ordre total, ainsi que la source utilisee
            k_aleatoire = get_nbIterations_ordre_aleatoire(H, source) #Récupérer le nombre d'itérations retourné par Bellman-Ford en utilisant un ordre aléatoire
            moy_k_ordre+=k_ordre
            moy_k_aleatoire+=k_aleatoire
            
        moy_k_ordre=round(moy_k_ordre/ N_repetitions,2)
        moy_k_aleatoire=round(moy_k_aleatoire/ N_repetitions,2)
        
        list_k_ordre.append(moy_k_ordre)
        list_k_aleatoire.append(moy_k_aleatoire)
        
    return list_k_ordre, list_k_aleatoire           


## Question 11

def genererGrapheNiveau(nb_niveaux, borneInterval=10):
    G = [nb_niveaux*4, {i for i in range(nb_niveaux*4)}]
    E = {}
    for i in range(1, nb_niveaux, 1):
        for j in range(4):
            nb_pred = rd.randint(1,4)
            sommet_courant = 4*i+j
            list_pred = [l for l in range(4*(i-1), 4*(i))]
            rd.shuffle(list_pred)
            
            for pred in list_pred[:nb_pred]:
                arc = (pred, sommet_courant)
                poids = rd.randint(-borneInterval, borneInterval)
                E.update({arc:poids})
                
    G.append(len(E))   #calculer le nombre d'aretes
    G.append(E)        #Ajouter l'ensemble des aretes
    source = rd.randint(0,3)  #prendre une source aleatoire
    G.append(source)            #Coller la source
    return G

#######

def get_moyenne_niveaux(niveaux):
    moyennes_tot = []
    moyennes_al = [] 

    for nv in niveaux:
        iter_tot = []
        iter_al = []
        
        for i in range(5):
            Gn = genererGrapheNiveau(nv)   
            Hn = construire_listGi(Gn, 1)[0]                              #Generer le graphe de test
            
            k_ordre, source = get_nbIterations_ordre_total(Gn, Hn, 3)     #Récupérer le nombre d'itérations retourné par Bellman-Ford en utilisant l'ordre total, ainsi que la source utilisee
            
            k_aleatoire = get_nbIterations_ordre_aleatoire(Hn, source)   #Récupérer le nombre d'itérations retourné par Bellman-Ford en utilisant un ordre aléatoire

            iter_tot.append(k_ordre) 
            iter_al.append(k_aleatoire) 

        moyennes_tot.append(np.mean(iter_tot))
        moyennes_al.append(np.mean(iter_al))
        
    return (moyennes_tot, moyennes_al)
