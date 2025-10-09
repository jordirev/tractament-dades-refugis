const fs = require('fs');
const path = require('path');

// File paths
const inputJsonPath = path.join(__dirname, 'refusInfo.json');
const outputJsonPath = path.join(__dirname, 'refusInfo_normalized.json');

try {
  // Read the JSON file
  const jsonContent = fs.readFileSync(inputJsonPath, 'utf8');
  const data = JSON.parse(jsonContent);
  
  // Normalize each node
  const normalizedNodes = data.nodes.map(node => {
    const normalizedNode = {};
    
    // Keep id, nom, derniere_modif as they are (lien will be moved to links array)
    normalizedNode.id = node.id;
    normalizedNode.nom = node.nom;
    // Extract only the date part from derniere_modif
    if (node.derniere_modif) {
      normalizedNode.derniere_modif = node.derniere_modif.split(' ')[0];
    }
    
    // Handle coordinates - separate altitude and keep lat/long
    if (node.coord) {
      normalizedNode.coord = {
        long: parseFloat(node.coord.long),
        lat: parseFloat(node.coord.lat)
      };
      
      // Add altitude as separate field
      if (node.coord.alt) {
        const altValue = parseInt(node.coord.alt, 10);
        normalizedNode.altitude = altValue === 0 ? null : altValue;
      } else {
        normalizedNode.altitude = null;
      }
    }
    
    // Simplify places - extract valeur
    if (node.places && node.places.valeur !== undefined) {
      normalizedNode.places = node.places.valeur;
    }
    
    // Simplify etat - extract valeur
    if (node.etat && node.etat.valeur !== undefined) {
      normalizedNode.etat = node.etat.valeur;
    }
    
    // Simplify remarque - extract valeur
    if (node.remarque && node.remarque.valeur !== undefined) {
      normalizedNode.remarque = node.remarque.valeur;
    }
    
    // Handle info_comp - simplify nested structures
    if (node.info_comp) {
      normalizedNode.info_comp = {};
      
      // List of fields to simplify (extract valeur)
      const fieldsToSimplify = [
        'manque_un_mur',
        'cheminee', 
        'poele',
        'couvertures',
        'latrines',
        'bois',
        'eau'
      ];
      
      fieldsToSimplify.forEach(field => {
        if (node.info_comp[field] && node.info_comp[field].valeur !== undefined) {
          let value = node.info_comp[field].valeur;
          // Convert numeric strings to numbers
          if (typeof value === 'string' && /^\d+$/.test(value.trim())) {
            value = parseInt(value.trim(), 10);
          }
          normalizedNode.info_comp[field] = value;
        }
      });
      
      // Handle places_matelas - simplify to just the number from nb
      if (node.info_comp.places_matelas) {
        let nbValue = 0; // Default value if no nb found
        if (node.info_comp.places_matelas.nb !== undefined) {
          // Convert to number if it's a numeric string and not empty
          if (typeof node.info_comp.places_matelas.nb === 'string' && 
              node.info_comp.places_matelas.nb.trim() !== '' && 
              /^\d+$/.test(node.info_comp.places_matelas.nb.trim())) {
            nbValue = parseInt(node.info_comp.places_matelas.nb.trim(), 10);
          } else if (typeof node.info_comp.places_matelas.nb === 'number') {
            nbValue = node.info_comp.places_matelas.nb;
          }
        }
        normalizedNode.info_comp.places_matelas = nbValue;
      }
    }
    
    // Keep description as is
    if (node.description !== undefined) {
      normalizedNode.description = node.description;
    }
    
    // Create links array from lien and site_officiel (without keeping original fields)
    normalizedNode.links = [];
    
    // Add lien if exists and is valid
    if (node.lien && typeof node.lien === 'string' && node.lien.trim() !== '') {
      normalizedNode.links.push(node.lien.trim());
    }
    
    // Add site_officiel from info_comp if exists and is valid
    if (node.info_comp && node.info_comp.site_officiel && node.info_comp.site_officiel.url) {
      const siteUrl = node.info_comp.site_officiel.url;
      if (typeof siteUrl === 'string' && siteUrl.trim() !== '') {
        normalizedNode.links.push(siteUrl.trim());
      }
    }
    
    return normalizedNode;
  });
  
  // Create the normalized result
  const normalizedResult = {
    nodes: normalizedNodes
  };
  
  // Write the normalized JSON to file
  fs.writeFileSync(outputJsonPath, JSON.stringify(normalizedResult, null, 2), 'utf8');
  console.log(`Normalization successful! Normalized JSON saved as ${outputJsonPath}`);
  console.log(`Original nodes: ${data.nodes.length}`);
  console.log(`Normalized nodes: ${normalizedNodes.length}`);
  
  // Show a sample of the first normalized node
  console.log('\nSample of first normalized node:');
  console.log(JSON.stringify(normalizedNodes[0], null, 2));
  
} catch (err) {
  console.error(`Error: ${err.message}`);
}