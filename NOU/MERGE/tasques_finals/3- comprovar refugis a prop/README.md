# MERGE DE REFUGIS DUPLICATS

## Descripció del Procés

Aquest directori conté els scripts i dades per identificar i fusionar refugis duplicats que apareixen amb noms similars en les bases de dades de refuges.info i pyrenees-refuges.com.

## Fitxers

### Fitxers d'entrada
- `noms_parelles_semblants.txt` - Llista de 123 parelles de refugis amb noms similars identificats manualment
- `data_refugis_updated_types.json` - Base de dades de refugis amb tipus actualitzats (entrada)

### Scripts
- `merge_duplicates.py` - Script principal que fa el merge dels refugis duplicats
- `verify_merge_duplicates.py` - Script de verificació del procés de merge

### Fitxers de sortida
- `data_refugis_sense_repetits.json` - Base de dades final amb els refugis fusionats
- `informe_verificacio_merge.txt` - Informe detallat del procés de verificació
- `parelles_no_trobades.txt` - Llista de parelles que no s'han pogut trobar/fusionar

## Normes de Merge

El merge es fa seguint aquestes normes específiques per a cada camp:

### 1. COORDENADES
- S'utilitzen les coordenades del refugi de **refuges.info**
- Prioritza la font més fiable per a localització

### 2. ALTITUD
- S'escull l'altitud més precisa (valor amb més dígits o més gran)
- Si un valor és null, s'escull el valor no null
- Si un valor és 0, s'escull l'altre valor
- **Exemple**: Si a1=1200 i a2=1235, s'escull 1235

### 3. INFO_COMP (Informació de serveis/equipaments)
- Unió **OR** dels atributs (camp per camp)
- Si qualsevol dels refugis té un atribut a 1, el resultat és 1
- Comparteix tots els serveis/equipaments de tots els refugis
- Maximitza la informació sobre serveis disponibles

### 4. NAME I SURNAME
- **name**: Nom del refugi de refuges.info
- **surname**: Nom del refugi de pyrenees-refuges
- Això preserva ambdues denominacions per a futures referències

### 5. REGION I DEPARTEMENT
- Si un dels dos és null, s'escull el valor no null
- Prioritza tenir informació completa de localització

### 6. TYPE (Tipus de refugi)
- Si qualsevol dels dos `type == "fermée"`, llavors `type = "fermée"`
- Si un dels dos `type == "non gardé"`, s'escull l'altre type
- Prioritza la informació més específica sobre l'estat del refugi

### 7. PLACES (Capacitat)
- S'escull el valor més gran (capacitat màxima)
- Si un és null, s'escull el valor no null
- Maximitza la informació sobre capacitat

### 8. LINKS
- Unió de tots els links en un sol vector
- No hi ha duplicats
- Manté referències a ambdues fonts d'informació

### 9. DESCRIPTION
- Unió de totes les descriptions en un sol vector
- **Ordre**: primer description de refuges.info, després de pyrenees-refuges
- Preserva tota la informació descriptiva

### 10. REMARQUE
- Unió de totes les remarques en un sol vector
- **Ordre**: primer remarque de refuges.info, després de pyrenees-refuges
- Preserva tots els comentaris i observacions

### 11. MODIFIED_AT
- S'escull el valor no null si n'hi ha un
- Prioritza tenir informació de la darrera modificació

### 12. INFO_COUCHAGE I INFO_EAU
- Es preserven aquests camps importants
- Si un és null, s'escull el valor no null

### 13. REGLA GENERAL
- Per qualsevol camp: si hi ha un valor null i un no null, sempre s'escull el valor no null
- Maximitza la completitud de les dades

## Ús

### Executar el merge:
```bash
python merge_duplicates.py
```

Aquest script:
1. Llegeix les parelles de noms del fitxer `noms_parelles_semblants.txt`
2. Carrega la base de dades de refugis
3. Troba cada parella i fa el merge segons les normes
4. Elimina els refugis duplicats
5. Guarda el resultat a `data_refugis_sense_repetits.json`
6. Genera un informe de parelles no trobades (si n'hi ha)

### Verificar el resultat:
```bash
python verify_merge_duplicates.py
```

Aquest script:
1. Compara els números (original vs final)
2. Verifica l'estructura bàsica de les dades
3. Comprova característiques dels refugis fusionats
4. Analitza la qualitat de les dades
5. Mostra exemples de refugis fusionats
6. Genera un informe detallat

## Resultats Esperats

- **Parelles processades**: ~123 (amb tolerància de ±2)
- **Reducció de refugis**: ~123 refugis eliminats
- **Refugis amb name i surname**: ~123 (refugis fusionats)
- **Refugis amb ambdós links**: ~123 (links de refuges.info i pyrenees-refuges)

## Verificacions

El script de verificació comprova:

### Números
- Total de refugis abans i després
- Reducció esperada vs obtinguda
- Tolerància de ±2 parelles

### Estructura
- Percentatge de refugis amb cada camp omplert
- Completitud de les dades

### Fusió correcta
- Refugis amb name i surname (indicador de fusió)
- Refugis amb múltiples links (ambdues fonts)
- Refugis amb múltiples descriptions/remarques

### Qualitat
- Refugis sense coordenades
- Refugis sense altitud
- Refugis sense tipus
- Distribució de tipus de refugis

## Notes Importants

1. **Identificació de la font**: El script determina quin refugi ve de refuges.info consultant els links
2. **Preservació de dades**: El merge mai elimina informació, només la combina
3. **Ordre important**: En descriptions i remarques, es manté l'ordre (refuges.info primer)
4. **Tolerància**: Es permet una tolerància de 2 parelles no trobades
5. **Duplicats en links**: S'eviten duplicats en la unió de links

## Problemes Comuns

### Parelles no trobades
Si algunes parelles no es troben, pot ser perquè:
- Els noms no coincideixen exactament
- Un dels refugis ha estat eliminat o modificat prèviament
- Hi ha diferències en majúscules/minúscules o accents

### Verificació fallida
Si la verificació detecta problemes:
- Consultar `informe_verificacio_merge.txt` per detalls
- Revisar `parelles_no_trobades.txt` per veure què ha fallat
- Comprovar que els noms al fitxer de parelles coincideixen amb els de la base de dades

## Autor i Data

- **Data**: Novembre 2024
- **Procés**: Merge de refugis duplicats
- **Resultat**: Base de dades unificada sense duplicats
