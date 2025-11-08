================================================================================
ELIMINACIÓ DE REFUGIS DUPLICATS
================================================================================

DESCRIPCIÓ
----------
Aquest procés identifica i fusiona refugis duplicats que es troben a menys de
100 metres de distància i tenen noms similars. Les dades provenen de dues fonts:
- refuges.info
- pyrenees-refuges.com

FITXERS
-------
- refugis_propers_noms_semblants_def.txt : Llista de 150 parelles de refugis duplicats
- data_refugis_updated_types.json        : Dades originals amb tots els refugis
- merge_duplicates.py                     : Script per fusionar els duplicats
- remove_remaining_duplicates.py         : Script per eliminar duplicats residuals
- data_refugis_sense_repetits.json       : Resultat final amb duplicats eliminats
- verify_merge.py                         : Script de verificació del merge
- verification_report.json                : Informe detallat de la verificació
- README.txt                              : Aquest fitxer

REGLES DE FUSIÓ
---------------
Les parelles (o triplets, com la parella #50) es fusionen seguint aquestes regles:

1. COORDENADES
   - S'utilitzen les coordenades del refugi de refuges.info
   - Això manté la consistència amb la font principal

2. ALTITUD
   - S'escull l'altitud més precisa (valor més alt quan ambdós existeixen)
   - Exemple: Si a1=1200 i a2=1235, s'escull 1235
   - Si un és null, s'escull el valor no null

3. INFO_COMP
   - Unió "OR" dels atributs (camp per camp)
   - Si qualsevol dels refugis té un atribut a 1, el resultat és 1
   - Comparteix tots els serveis/equipaments de tots els refugis

4. NAME I SURNAME
   - name: Nom del refugi de refuges.info
   - surname: Nom del refugi de pyrenees-refuges
   - Això preserva ambdues denominacions

5. REGION I DEPARTEMENT
   - Si un dels dos és null, s'escull el valor no null
   - Prioritza tenir informació completa

6. TYPE (TIPUS DE REFUGI)
   - Si qualsevol dels dos type == "fermée", llavors type = "fermée"
   - Si un dels dos type == "non gardé", s'escull l'altre type
   - Prioritza la informació més específica

7. PLACES (CAPACITAT)
   - S'escull el valor més gran (capacitat màxima)
   - Si un és null, s'escull el valor no null
   - Millor sobrestimar la capacitat que subestimarla

8. LINKS
   - Unió de tots els links en un sol vector
   - No hi ha duplicats, manté referències a ambdues fonts

9. DESCRIPTION
   - Unió de totes les descriptions en un sol vector
   - Ordre: primer description de refuges.info, després de pyrenees-refuges
   - Elimina descriptions duplicades

10. REMARQUE
    - Unió de totes les remarques en un sol vector
    - Ordre: primer remarque de refuges.info, després de pyrenees-refuges
    - Elimina remarques duplicades

11. MODIFIED_AT
    - S'escull el valor no null si n'hi ha un
    - Prioritza tenir informació de la darrera modificació

12. INFO_COUCHAGE I INFO_EAU
    - Es preserven aquests camps importants
    - Si un és null, s'escull el valor no null

13. REGLA GENERAL
    - Per qualsevol camp: si hi ha un valor null i un no null, sempre s'escull
      el valor no null
    - Maximitza la completitud de les dades

CAS ESPECIAL: PARELLA #50
--------------------------
La parella #50 té 3 refugis en lloc de 2. El procés els fusiona tots tres seguint
les mateixes regles, aplicant-les de forma iterativa a tots els refugis del grup.

NOTA: En el processament real, la parella #41 va resultar tenir 3 refugis.

DUPLICATS RESIDUALS
-------------------
Després del merge inicial, es van detectar 2 parelles de refugis amb coordenades
exactament iguals que no apareixien a la llista original:
1. Cabane des Masseys / Cabane de Masseys (42.8588, -0.2229)
2. Cabane du Sol del Bosc / Cabane sous les Rochers de Miglos (42.7702, 1.6116)

Aquests duplicats es van eliminar automàticament amb el script
remove_remaining_duplicates.py, mantenint només la primera ocurrència de cada parella.

RESULTATS
---------
- Refugis originals: 1662 refugis
- Parelles processades: 103 parelles (extretes de la llista)
- Duplicats eliminats per merge: 104 refugis
- Duplicats residuals eliminats: 2 refugis
- Total duplicats eliminats: 106 refugis
- Refugis finals: 1556 refugis

VERIFICACIÓ
-----------
El script verify_merge.py comprova:
1. Les coordenades són de refuges.info
2. L'altitud és la màxima
3. El camp info_comp existeix si existia als originals
4. Els noms són correctes (name i surname)
5. Region i departement no són null si existien als originals
6. Les regles de type s'han aplicat correctament
7. Places és el màxim
8. Tots els links s'han inclòs
9. Totes les descriptions s'han inclòs
10. Totes les remarques s'han inclòs
11. modified_at no és null si existia als originals
12. info_couchage i info_eau estan preservats
13. No queden duplicats de coordenades
14. El nombre de refugis eliminats és correcte

EXECUCIÓ
--------
1. Executar el merge:
   python merge_duplicates.py

2. Eliminar duplicats residuals:
   python remove_remaining_duplicates.py

3. Verificar el resultat:
   python verify_merge.py

4. Revisar l'informe:
   - Consola: Resum de verificació
   - verification_report.json: Detalls complets

NOTES
-----
- Les coordenades es comparen amb una tolerància de 0.0001 graus (~11 metres)
- Els refugis que no formen part de cap parella es mantenen sense canvis
- L'ordre dels refugis al fitxer final pot variar respecte a l'original
- Totes les descriptions i remarques es mantenen, encara que siguin similars
  (no es fa deduplicació semàntica, només exacta)

DATA DE CREACIÓ
----------------
2025-11-08

AUTOR
-----
Script generat automàticament per processar dades de refugis dels Pirineus
