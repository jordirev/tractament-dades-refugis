fes un codi en aquesta carpeta que faci el següent:
CONTEXT: en aquests dos documents json hi ha una llista de refugis. En aquests dos json poden haver-hi refugis iguals i refugis que nomes estan en un dels dos documents. El que vull que facis es que uneixis aquests dos json en un de sol de la següent manera:
- busca les parelles de refugis a través del camp "name". Tingues en compte que potser canvia per majuscules, espais o varia una mica el nom. Si no estas segur de que son el mateix refugi, compara també les coordenades del camp "coord" (poden diferir una mica) o bé la "altitude". Donam una llista abans d'executar el codi de les parelles que no estiguis segur. En cas d'ajuntar dos refugis, hi ha dades que decidirem de quin document ens quedem. Primer, queda't amb les coordenades (camp "coord") més precises entre els dos documents. Despres, quedat amb la "altitude" més alta. El "name" del refugi del document de refusInfo guarda'l com a "surname" i deixa l'altre "name" com esta. En el cas dels links, uneix-los tots en un sol "links":[], fes igual en el cas de "type", uneix-los en un sol "type":[], fes igual amb "description", uneix-los en un sol "description":[] i "remarque", uneix-los en un sol "remarque":[]. En el cas de "places", queda't amb el numero més gran. I en el cas de "info_comp", compara "cheminee" "bois" "eau" "matelas" que son els que estan compartits en els dos documents i fes una OR logica de tal manera que si hi ha el cas de 0 0, es queda a 0, 0 1 o 1 0, es queda 1 i 11 es queda a 1. La resta de camps de info_comp que nomes estan en un dels documents, afegeix-los a "info_comp" del resultat, de tal manera que quedaran tots els camps de "info_comp" dels dos documents en un de sol. un possible resultat de "info_comp" seria el següent:
"info_comp": {
    "manque_un_mur": 0,
      "cheminee": 1,
      "poele": 0,
      "couvertures": 0,
      "latrines": 0,
      "bois": 0,
      "eau": 1,
      "couchage": 1,
      "matelas": 1,
      "bas_flancs": 0,
      "lits": 0,
      "mezzanine/etage": 0
    }
La resta de camps que no estan compartits entre parelles (com region, departement, info_eau, modified_at, info_couchage), afegeix-los també al resultat per a tenir tots els camps desl dos documents en un de sol.

D'altra banda, en tots aquells refugis que nomes estiguin en un dels dos documents, afegeix-los al resultat de la següent manera:
- Afegeix els camps de "info_comp" que li faltin amb valor 0. 
- posa region i departement a null si no té aquests camps. 
- Si no te "modified_at", posali a null. 

