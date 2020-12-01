<p align="center">
    <!-- <img src="_x.png" alt="Logo" width=72 height=72> -->

  <h3 align="center">Algorithmes et structures de données pour l’indexation de grands volumes de données textuelles</h3>

</p>

## Table of contents

- [Quick start](#quick-start)
- [Context](#context)
- [What's included](#whats-included)
- [Creators](#creators)
- [Thanks](#thanks)

## Quick start

Use python3 !

1. Clone this project
2. Download [dataset files] to data/ and unzip
3. Remove  ```readchg.txt ``` and  ```readmela.txt ``` files in the data folder
4. Install the requierements dependencies

    ```pip3 install -r requirement.txt```
5. Create a new inverted index 

    ```python3 CreateIndex.py```
8. Or Make query using our saved PL.

    ```python3 main.py```

## Context

Les moteurs de recherche auxquels nous sommes habitués font appel à des structures de données et à des algorithmes toujours plus performants. Un index inversé est une correspondance entre du contenu, comme des mots ou des nombres, et une position dans un ensemble de données comme un document, un enregistrement de base de données, ou un corpus (sur le même principe qu'un index terminologique). Il permet de répondre rapidement à une recherche, moyennant un temps de calcul plus long en amont (création de l'index). Dans ce document, nous vous présenterons notre de moteur de recherche ainsi que nos méthodes d'indexation. Ensuite, nous montrerons que l'optimisation de l'index grâce à V-BYTE est particulièrement prometteuse.

## What's included

Pour mieux comprendre notre implémentation voici une déscription de l’architecture :

- ```Appearance```; Qui représente un élémentde  la  PL,  on  l’utilise  pour  créer  l’objectpuis le stocker dans un dict().
- ```Create Index```; Permet de créer l’invertedindex à partir de zéro, Il va créer un ob-ject Inverted index à partir de la classe enquestion puis réalise les étapes du schémade la figure 2, qui est en anglais car nousvoulions au début faire le rapport en an-glais.—Document; Défini un objet document, soitun numéro de document, son doc id et lebody d’un document.
- ```File Reader```; Permet de parser un fichierde dossier data et en extraire un tableaud’objects document.—Storage; Est un dictionaire qui permet degarder en mémoire les documents déja in-dexés.
- ```vbcode```; Permet l’encodage v-bit et le dé-codage d’une chaine de byte. C’est un codepartagé par Yuta Uekusa qui propose uneimplémentation simple et efficace en py-thon.
- ```main```; Ce fichier python permet de fairedes  recherches  dans  un  index  déja  créé.Nous allons d’abord récupérer les fichiersde l’index, puis nous allons faire des re-quetes en utilisant directement l’inverte

```text
OT1-Indexing_And_Querying_Text/
├── data/
│   └── documentfiles
│
├── src/
│    ├── Appearance.py
│    ├── CreateIndex.py
|    ├── Document.py
|    ├── FileReader.py
|    ├── InvertedIndex.py
|    ├── Storage.py
|    ├── vbcode.py
|    ├── mmap
|    ├── posting_list
│    └── main.py
│
└── .gitignore
```

## Creators

**Martin GERMAIN**

**Romain PERONNE**

**Joseph SIMONIN**


## Thanks

Merci, à notre professeur M. Portier pour l'accompagnement de notre groupe sur le sujet. Nous n'avons pas pu approfondir le sujet comme nous le souhaitions, mais nous avons appris et compris énormément sur la création et l'optimisation d'Inverted Index. Et nous comprenons mieux comment fonctionnent les moteurs de recherches que nous utilisons tous les jours.

## Copyright and license

Code and documentation copyright 2011-2018 the authors. Code released under the [MIT License](https://reponame/blob/master/LICENSE).

:metal:
