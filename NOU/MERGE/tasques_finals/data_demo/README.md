# Selecció de Refugis Demo

Aquest directori conté scripts per generar un dataset demo de 100 refugis variats a partir del fitxer complet `data_refugis_sense_repetits.json`.

## Objectiu

Crear un subset representatiu de refugis que inclogui:
- **Varietat de tipus**: Assegurant que els 4 tipus principals estiguin presents
  - `non gardé`
  - `fermée`
  - `cabane ouverte mais ocupee par le berger l ete`
  - `orri`
- **Varietat d'atributs**: Diferents rangs de places, altituds, regions, departaments, info_comp i links
- **Format simplificat**: Eliminant el camp `remarque` i convertint `description` d'array a string

## Fitxers

### Scripts

#### `select_varied_refuges.py`
Script principal que selecciona 100 refugis variats del dataset complet.

**Funcionalitats:**
- Carrega tots els refugis de `data_refugis_sense_repetits.json`
- Categoritza refugis per múltiples criteris (tipus, altitud, places, info_comp, links, regió, departament)
- Selecciona refugis assegurant representació de tots els tipus requerits
- Dins de cada tipus, selecciona refugis amb varietat d'altres atributs
- Aplica transformacions:
  - Elimina el camp `remarque`
  - Converteix `description` d'array a string (seleccionant el primer element)
- Genera estadístiques de la selecció
- Guarda el resultat a `data_demo.json`

**Ús:**
```bash
python select_varied_refuges.py
```

**Estratègia de selecció:**
1. Divideix els 100 refugis equitativament entre els 4 tipus requerits (~25 per tipus)
2. Dins de cada tipus, selecciona refugis amb varietat d'altituds (baixa/mitjana/alta)
3. Assegura diversitat en:
   - Places (null, 0, 1-5, 6-10, 11-20, 20+)
   - Altitud (<1000, 1000-1500, 1500-2000, 2000-2500, >2500)
   - Info_comp (0, 1-2, 3-4, 5+ característiques)
   - Links (0, 1, 2, 3+)
   - Regions i departaments diferents

#### `verify_selection.py`
Script de verificació que comprova la correcció de la selecció i les transformacions aplicades.

**Funcionalitats:**
- Verifica que el camp `remarque` s'ha eliminat de tots els refugis
- Verifica que `description` és un string (no un array)
- Comprova que els 4 tipus requerits estan presents
- Analitza la diversitat en tots els camps (places, altitud, links, info_comp, regió, departament)
- Genera un informe detallat amb estadístiques i possibles errors
- Mostra un resum per consola

**Ús:**
```bash
python verify_selection.py
```

**Output:**
- Informe escrit a `verificacio_data_demo.txt`
- Resum per consola amb estat de les verificacions

### Fitxers de dades

#### `data_refugis_sense_repetits.json` (input)
Dataset complet de refugis sense duplicats.

#### `data_demo.json` (output)
Dataset demo de 100 refugis seleccionats i processats.

**Transformacions aplicades:**
- Camp `remarque`: **ELIMINAT**
- Camp `description`: Convertit de `["text"]` a `"text"` (primer element de l'array)

#### `verificacio_data_demo.txt` (output)
Informe de verificació amb:
- Verificació de transformacions (remarque eliminat, description convertit)
- Estadístiques de varietat per cada camp
- Errors i advertències (si n'hi ha)
- Conclusió sobre l'èxit de la selecció

## Flux de treball

1. **Generar dataset demo:**
   ```bash
   python select_varied_refuges.py
   ```
   Això crearà `data_demo.json` amb 100 refugis seleccionats i processats.

2. **Verificar resultats:**
   ```bash
   python verify_selection.py
   ```
   Això crearà `verificacio_data_demo.txt` amb un informe complet de verificació.

## Criteris de qualitat

El dataset demo es considera correcte si:
- ✓ Té exactament 100 refugis
- ✓ No hi ha cap camp `remarque`
- ✓ Tots els camps `description` són strings (no arrays)
- ✓ Els 4 tipus requerits estan presents
- ✓ Hi ha varietat en places, altitud, links, info_comp
- ✓ Hi ha múltiples regions i departaments representats

## Nota tècnica

Els scripts utilitzen una llavor aleatòria (`random.seed(42)`) per garantir reproducibilitat. Això significa que executar el script múltiples vegades amb les mateixes dades d'entrada produirà sempre el mateix resultat.

## Estadístiques esperades

Distribució aproximada (pot variar lleugerament):
- **Tipus**: ~25 refugis per cada tipus
- **Altitud**: Distribució entre <1500m, 1500-2000m, 2000-2500m, >2500m
- **Places**: Varietat des de null fins a 20+
- **Links**: Mix de refugis amb 0, 1, 2 o 3+ links
- **Info_comp**: Des de 0 fins a 5+ característiques
- **Regions**: Múltiples regions representatives
- **Departaments**: Múltiples departaments representatius
