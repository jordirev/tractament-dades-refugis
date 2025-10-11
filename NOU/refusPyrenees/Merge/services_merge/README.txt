Primer volem saber quins tipus hi ha de cada servei (analyse_service_values). Despres, classifiquem els tipus de couchage de la se¨guent manera amb el codi (classify_couchage):

Afegeix al codi refusPyrenees_finished_services al final de tot un codi per a canviar els valors del camp "couchage" de la següent manera:
- crea els camps "matelas", "bas_flancs", "lits", "mezzanine/etage" al mateix nivell que "couchage", amb valor inicial a 0. (mou-los també a dins de "info_comp")
- tots els refugis que estiguin al grup SOL/TERRE, NÉGATIF o bé NUMÉRIC amb valor "0", posa "couchage" a 0.
- a partir dels grups de refugis que hi ha al txt classificacio_couchage (on apareix el nom dels refugis en grups), En els refugis dels grups de MATELAS, BAS FLANCS, LITS, MEZZANINE/ÉTAGE i NUMÉRIC (que no siguin "0") crea un camp a la altura de "type" anomenat "info_couchage" que tingui el valor que actualment té "couchage". Després, posa "couchage" a 1.
- a partir dels grups de refugis que hi ha al txt classificacio_couchage (on apareix el nom dels refugis en grups), posa el camp "matelas" a 1 dels refugis que estiguin al grup MATELAS. Fes el mateix per als refugis que estan al grup BAS FLANCS, "bas_flancs" a 1. Igual amb "lits" al grup LITS i amb "mezzanine/etage" amb el grup de refugis MEZZANINE/ÉTAGE.
- escriu el resultat a refusPyrenees_finished_services.json
finalment, fes un codi per a verificar que tot hagi anat be.

un cop classificats, executem el codi per a normalitzar els serveis i binaritzar-los (refusPyrenees_finished_services). També s'afegeix els camps "info_eau" i "info_couchage" per a donar mes informació. Aquests contenen el text que hi havia abans de binaritzar aquells serveis.

finalment, verifiquem que tot estigui correcte amb verify_couchage_processing que comprova el següent:
- Tots els refugis tenen l'estructura correcta
- Tots els valors són vàlids (0 o 1 per camps binaris)
- No hi ha inconsistències (refugis amb info_couchage però couchage = 0)
- Els serveis bàsics (cheminee, bois, eau) mantenen la normalització binària