import reflex as rx
from models import City


# List of cities to insert
city_names_string = """Paris
Marseille
Lyon
Toulouse
Nice
Nantes
Montpellier
Strasbourg
Bordeaux
Lille
Rennes
Toulon
Reims
Saint-Étienne
Le Havre
Dijon
Grenoble
Angers
Villeurbanne
Saint-Denis
Nîmes
Aix-en-Provence
Clermont-Ferrand
Le Mans
Brest
Tours
Amiens
Annecy
Limoges
Metz
Boulogne-Billancourt
Perpignan
Besançon
Orléans
Rouen
Saint-Denis
Montreuil
Caen
Argenteuil
Mulhouse
Saint-Paul
Nancy
Tourcoing
Roubaix
Nanterre
Vitry-sur-Seine
Nouméa
Créteil
Avignon
Poitiers
Aubervilliers
Asnières-sur-Seine
Colombes
Dunkerque
Aulnay-sous-Bois
Saint-Pierre
Versailles
Le Tampon
Courbevoie
Béziers
La Rochelle
Rueil-Malmaison
Cherbourg-en-Cotentin
Champigny-sur-Marne
Pau
Mérignac
Saint-Maur-des-Fossés
Antibes
Fort-de-France
Ajaccio
Cannes
Saint-Nazaire
Mamoudzou
Drancy
Noisy-le-Grand
Issy-les-Moulineaux
Cergy
Levallois-Perret
Colmar
Calais
Pessac
Vénissieux
Évry-Courcouronnes
Clichy
Valence
Ivry-sur-Seine
Bourges
Quimper
Cayenne
Antony
Troyes
La Seyne-sur-Mer
Villeneuve-d'Ascq
Montauban
Pantin
Chambéry
Niort
Neuilly-sur-Seine
Sarcelles
Le Blanc-Mesnil
Maisons-Alfort
Lorient
Villejuif
Saint-André
Fréjus
Beauvais
Narbonne
Meaux
Hyères
Bobigny
La Roche-sur-Yon
Clamart
Vannes
Chelles
Cholet
Saint-Louis
Épinay-sur-Seine
Saint-Ouen-sur-Seine
Saint-Quentin
Bondy
Bayonne
Corbeil-Essonnes
Cagnes-sur-Mer
Vaulx-en-Velin
Les Abymes
Sevran
Fontenay-sous-Bois
Sartrouville
Massy
Arles
Saint-Laurent-du-Maroni
Albi
Laval
Saint-Herblain
Gennevilliers
Suresnes
Saint-Priest
Vincennes
Bastia
Martigues
Les Sables-d'Olonne
Grasse
Montrouge
Aubagne
Saint-Malo
Évreux
La Courneuve
Blois
Brive-la-Gaillarde
Charleville-Mézières
Meudon
Carcassonne
Choisy-le-Roi
Noisy-le-Sec
Livry-Gargan
Rosny-sous-Bois
Talence
Belfort
Alfortville
Chalon-sur-Saône
Salon-de-Provence
Sète
Istres
Mantes-la-Jolie
Saint-Germain-en-Laye
Saint-Brieuc
Tarbes
Alès
Châlons-en-Champagne
Bagneux
Puteaux
Caluire-et-Cuire
Bron
Rezé
Valenciennes
Châteauroux
Garges-lès-Gonesse
Castres
Arras
Melun
Thionville
Le Cannet
Bourg-en-Bresse
Anglet
Angoulême
Boulogne-sur-Mer
Wattrelos
Gap
Villenave-d'Ornon
Montélimar
Compiègne
Stains
Gagny
Colomiers
Poissy
Draguignan
Douai
Le Lamentin
Bagnolet
Marcq-en-Barœul
Saint-Joseph
Villepinte
Saint-Martin-d'Hères
Chartres
Pontault-Combault
Joué-lès-Tours
Annemasse
Oullins-Pierre-Bénitei
Neuilly-sur-Marne
Franconville
Savigny-sur-Orge
Tremblay-en-France
Thonon-les-Bains
Saint-Benoît
La Ciotat
Échirolles
Châtillon
Athis-Mons
Six-Fours-les-Plages
Creil
Saint-Raphaël
Conflans-Sainte-Honorine
Villefranche-sur-Saône
Meyzieu
Dumbéa
Sainte-Geneviève-des-Bois
Haguenau
Vitrolles
Villeneuve-Saint-Georges
La Possession
Saint-Chamond
Châtenay-Malabry
Palaiseau
Saint-Leu
Matoury
Auxerre
Roanne
Mâcon
Sainte-Marie
Le Perreux-sur-Marne
Schiltigheim
Les Mureaux
Trappes
Nogent-sur-Marne
Houilles
Montluçon
Le Port
Romainville
Marignane
Romans-sur-Isère
Nevers
Lens
Saint-Médard-en-Jalles
Agen
Pierrefitte-sur-Seine
Épinal
Koungou
Bezons
Aix-les-Bains
Montigny-le-Bretonneux
Herblay-sur-Seine
Saint-Martin
Cambrai
L'Haÿ-les-Roses
Plaisir
Pontoise
Châtellerault
Rillieux-la-Pape
Thiais
Vienne
Vigneux-sur-Seine
Viry-Châtillon
Saint-Laurent-du-Var
Le Chesnay-Rocquencourt
Baie-Mahault
Dreux
Bègles
Carpentras
Goussainville
Mont-de-Marsan
Villiers-sur-Marne
Cachan
Savigny-le-Temple
Menton
Villemomble
Malakoff
Liévin"""

postal_codes_string = """75056
13055
69123
31555
6088
44109
34172
67482
33063
59350
35238
83137
51454
42218
76351
21231
38185
49007
69266
97411
30189
13001
63113
72181
29019
37261
80021
74010
87085
57463
92012
66136
25056
45234
76540
93066
93048
14118
95018
68224
97415
54395
59599
59512
92050
94081
98818
94028
84007
86194
93001
92004
92025
59183
93005
97416
78646
97422
92026
34032
17300
92063
50129
94017
64445
33281
94068
6004
97209
2A004
6029
44184
97611
93029
93051
92040
95127
92044
68066
62193
33318
69259
91228
92024
26362
94041
18033
29232
97302
92002
10387
83126
59009
82121
93055
73065
79191
92051
95585
93007
94046
56121
94076
97409
83061
60057
11262
77284
83069
93008
85191
92023
56260
77108
49099
97414
93031
93070
2691
93010
64102
91174
6027
69256
97101
93071
94033
78586
91377
13004
97311
81004
53130
44162
92036
92073
69290
94080
2B033
13056
85194
6069
92049
13005
35288
27229
93027
41018
19031
8105
92048
11069
94022
93053
93046
93064
33522
90010
94002
71076
13103
34301
13047
78361
78551
22278
65440
30007
51108
92007
92062
69034
69029
44143
59606
36044
95268
81065
62041
77288
57672
6030
1053
64024
16015
62160
59650
5061
33550
26198
60159
93072
93032
31149
78498
83050
59178
97213
93006
59378
97412
93078
38421
28085
77373
37122
74012
69149
93050
95252
91589
93073
74281
97410
13028
38151
92020
91027
83129
60175
83118
78172
69264
69282
98805
91549
67180
13117
94078
97408
42207
92019
91477
97413
97307
89024
42187
71270
97418
94058
67447
78440
78621
94052
78311
3185
97407
93063
13054
26281
58194
62498
33449
47001
93059
88160
97610
95063
73008
78423
95306
97801
59122
94038
78490
95500
86066
69286
94073
38544
91657
91687
6123
78158
97103
28134
33039
84031
95280
40192
94079
94016
77445
6083
93077
92046
62510"""


def insert_cities():
    """Script to insert cities in the sqlite database."""

    print("Inserting cities in the database")
    # Import the string as a list of cities to insert
    cities_list = city_names_string.split("\n")
    # Import the string as a list of postal codes to insert
    postal_codes_list = postal_codes_string.split("\n")

    with rx.session() as session:
        cities = session.exec(City.select()).all()
        if cities:
            print("Cities already inserted")
            return
        for city in cities_list:
            city = City(
                name=city,
                postal_code=postal_codes_list[cities_list.index(city)]
            )
            session.add(city)
        session.commit()

    print("Inserting cities - Done")

    print("Testing the insertion")
    # Test the insertion
    with rx.session() as session:
        cities = session.exec(City.select()).all()
        for city in cities:
            print(city.name)


def delete_cities():
    """Script to delete all cities in the database."""

    print("Deleting cities in the database")
    with rx.session() as session:
        cities = session.exec(City.select()).all()
        session.delete(cities)
        session.commit()

    print("Deleting cities - Done")


def main():
    insert_cities()


if __name__ == "__main__":
    main()
