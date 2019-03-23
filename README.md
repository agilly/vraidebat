# Analyse de la base de données du Vrai Débat

Le [Vrai Débat](https://le-vrai-debat.fr) est un site participatif de collecte de revendications politiques lancé parallèlement au site du gouvernement français "Le Grand Débat National".
La grande différence est la forme totalement libre et non guidée des revendications, ce qui les rend plus intéressantes mais d'autant plus difficiles à analyser.

![](tsne.all.perp50.jpg)

## Finalité

Les propositions soumises sur le site sont très nombreuses, et de nombreux doublons sont présent. Lóbjectif global est de synthétiser les revendications. En pratique, on va essayer:
* de trouver une façon de rapprocher les propositions très similaires et les doublons
* d'agréger les mesures d'opinion (votes pour ou contre) sur les propositions similaires

## Résultats

La structure des données a été clarifiée:
1. les propositions sont soit atomiques soit composées (une proposition très différente par paragraphe, à la manière d'une constitution)
2. les propositions sont structurées en très nombreux clusters à cardinalité faible mais plus ou moins constante (il y a toujours environ le même nombre de doublons pour une proposition)
3. la distribution des votes est très fortement biaisée: un petit nombre de propositions dépassent toutes les autres, mais il y a une "fat tail" de petites propositions qui composent une part non négligeable des votes


Au vu de ces remarques, il devient clair (1.) que le pré-traitement est important, que (2.) les algorithmes de classification auront du mal avec ce jeu de données à cause de sa structure très granulaire, et (3) qu'il n'est pas souhaitable de procéder à du filtrage à moins d'ignorer une grande partie des revendications. 

Em termes d'analyse:
* une transformation performante qui rapproche les propositions similaires et les doublons (Word Loadings + t-SNE) a été trouvée
* il a été impossible dans le peu de temps imparti, de trouver une méthode de classification qui découperait automatiquement le jeu de données en paquets de propositions similaires
* un outil d'exploration destiné à faciliter l'annotation et la classification manuelles du jeu de données a été programmé en Python à l'aide de la librairie `bokeh`.

### Outils d'exploration
Les outils sont présents aux adresses suivantes, pour chaque thème:
* [Démocratie, Institutions](http://vmi251326.contaboserver.net:5006/Institutions)
* [Economie, Finances, Travail, Comptes publics](http://vmi251326.contaboserver.net:5006/Economie)
* [Justice, Police, Armée](http://vmi251326.contaboserver.net:5006/Police)
* [Transition Ecologique et Solidaire, Agriculture & Alimentation, Transport](http://vmi251326.contaboserver.net:5006/Ecologie)
* [Santé, Solidarité, Handicap](http://vmi251326.contaboserver.net:5006/Handicap)
* [Europe, Affaires Etrangères, Outre-mer](http://vmi251326.contaboserver.net:5006/Europe)
* [Education, jeunesse, Enseignement Supérieur, Recherche et Innovation](http://vmi251326.contaboserver.net:5006/Education)
* [Expression Libre & Sujets de société](http://vmi251326.contaboserver.net:5006/Libre)
* [Sport, Culture](http://vmi251326.contaboserver.net:5006/Culture)

## Prochaines étapes
Certaines perspectives prometteuses n'ont pas pu être explorées faute de temps:
* Granulariser les propositions composées
* Explorer plus avant les possibilités de clustering automatique
* Explorer l'approche itérative, consistant à identifier les clusters aux marges, les synthétiser, ensuite re-transformer et re-classifier jusqu'à ce que le jeu de données soit vide.

## Étapes de l'analyse

### Analyse exploratoire

L'analyse exploratoire est décrite dans [ce notebook](Analyse_Preliminaire.ipynb). Il s'agit surtout de se familiariser avec les données et de tester quelques formes de classification.
L'analyse préliminaire contient:
* exploration des étapes nécessaires au contrôle qualité
* TF-IDF, suivi de clustering hiérarchique
* Allocation de Dirichlet Latente
* Word loadings et t-SNE
* Exploration de méthodes de clusering: DBSCAN

Après avoir abouti à une pipeline d'analyse robuste, l'analyse définitive se poursuit dans [cet autre notebook](Analyse%20Finale.ipynb).

### Contrôle qualité
Le contrôle qualité final effectue les étapes suivantes:

* transformation en minuscules
* suppression des balises HTML
* suppression des liens hypertexte
* suppression des caractères spéciaux HTML
* suppression des "stop words"
* suppression de la ponctuation
* suppression du whitespace
* précorrection des fautes touchant des mots spécifiques 
* correction automatique avec hunspell
* création du dictionnaire de lemmatisation
* lemmatisation
* suppression des suggestions de lemmes alternatifs
* suppression des mots peu informatifs
* suppression des mots d'une ou deux lettres

### Analyse proprement dite

* projection du jeu de données nettoyé sur les word loadings pré-entraînés sur le jeu frWac, gracieusement mis à disposition par M. Fauconnier (http://fauconnier.github.io/). Il s'agit du corpus frWac (>1 milliard de textes), avec une limite d'au moins 50 occurrences, entraîné avec l'algorithme SKIP et projeté sur 700 dimensions.
* réduction de dimension à l'aide de l'algorithme t-SNE



