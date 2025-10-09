A partir del fitxer refusPyrinees_merged_filtered.json analitzem quins tipus de valors prenen els camps cap_ete i cap_hiver que representen les capacitats dels refugis a l'estiu i hivern amb el codi analyze_filed_values.py i s'obté el txt analisi_capacitats_refugis.

Amb aquest txt podem fer un analisi de les capacitats i unir en un camp "places" la máxima capacitat del refugi tant a l'estiu com a l'hivern, ja que molts d'aquests camps prenen valors raros i tenen text en comptes de nomes un numero. 

A partir del codi refusPyrenees_merged_filtered_normalized.py, obtenim aquest valor "places" i amb el codi verify.py comprovem els casos raros s'hagin fet be. També, el codi refusPyrenees_merged_filtered_normalized.py transforma l'altitud en numero i posa a null si no es coneix o es 0. 