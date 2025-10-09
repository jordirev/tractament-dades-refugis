const fs = require('fs');
const path = require('path');

// File paths
const xmlFilePath = path.join(__dirname, 'refusInfoCompleta.xml');
const jsonFilePath = path.join(__dirname, 'refusInfoCompleta.json');

// Read the XML file
try {
  let xmlContent = fs.readFileSync(xmlFilePath, 'utf8');
  
  // Fix common XML issues
  // Replace unescaped & with &amp; if it's not already part of an entity
  xmlContent = xmlContent.replace(/&(?!amp;|lt;|gt;|apos;|quot;|#\d+;)/g, '&amp;');
  
  // Handle special characters
  xmlContent = xmlContent.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, ''); // Remove control characters
  
  // Parse XML to JSON using a simple approach
  const parseNode = (xml) => {
    // This is a simplified XML parser for this specific file structure
    // It assumes the XML is mostly well-formed with simple nesting
    
    const result = [];
    let currentNode = null;
    let currentTag = '';
    let collectingContent = false;
    let content = '';
    let depth = 0;
    
    // Create a simple state machine to parse the XML
    for (let i = 0; i < xml.length; i++) {
      const char = xml[i];
      
      if (char === '<') {
        if (xml[i+1] === '/') {
          // Closing tag
          const endTagPos = xml.indexOf('>', i);
          const tagName = xml.substring(i+2, endTagPos);
          
          if (tagName === 'node') {
            // End of a node
            if (currentNode) {
              result.push(currentNode);
              currentNode = null;
            }
          } else if (collectingContent) {
            // End of a content tag
            if (currentNode && currentTag) {
              currentNode[currentTag] = content.trim();
            }
            collectingContent = false;
            content = '';
            currentTag = '';
          }
          
          depth--;
          i = endTagPos;
        } else {
          // Opening tag
          const endTagPos = xml.indexOf('>', i);
          const tagName = xml.substring(i+1, endTagPos);
          
          if (tagName === 'nodes') {
            // Root tag, ignore
          } else if (tagName === 'node') {
            // Start of a new node
            currentNode = {};
            depth++;
          } else if (currentNode) {
            // Inner tag of a node
            currentTag = tagName;
            collectingContent = true;
            content = '';
            depth++;
          }
          
          i = endTagPos;
        }
      } else if (collectingContent) {
        content += char;
      }
    }
    
    return { nodes: result };
  };
  
  // Parse the XML
  const nodeRegex = /<node>[\s\S]*?<\/node>/g;
  const nodes = xmlContent.match(nodeRegex);
  
  if (!nodes) {
    console.error('No node tags found in the XML');
    process.exit(1);
  }
  
  const jsonResult = { nodes: [] };
  
  for (const nodeXml of nodes) {
    try {
      // Simple parsing for each node
      const nodeData = {};
      
      // Extract ID
      const idMatch = nodeXml.match(/<id>([^<]+)<\/id>/);
      if (idMatch) nodeData.id = idMatch[1];
      
      // Extract name
      const nameMatch = nodeXml.match(/<nom>([^<]+)<\/nom>/);
      if (nameMatch) nodeData.nom = nameMatch[1];
      
      // Extract link
      const linkMatch = nodeXml.match(/<lien>([^<]+)<\/lien>/);
      if (linkMatch) nodeData.lien = linkMatch[1];
      
      // Extract symbol
      const symMatch = nodeXml.match(/<sym>([^<]+)<\/sym>/);
      if (symMatch) nodeData.sym = symMatch[1];
      
      // Extract coordinates
      nodeData.coord = {};
      const altMatch = nodeXml.match(/<alt>([^<]+)<\/alt>/);
      if (altMatch) nodeData.coord.alt = altMatch[1];
      
      const longMatch = nodeXml.match(/<long>([^<]+)<\/long>/);
      if (longMatch) nodeData.coord.long = longMatch[1];
      
      const latMatch = nodeXml.match(/<lat>([^<]+)<\/lat>/);
      if (latMatch) nodeData.coord.lat = latMatch[1];
      
      // Extract type
      nodeData.type = {};
      const typeIdMatch = nodeXml.match(/<type>[^<]*<id>([^<]+)<\/id>/);
      if (typeIdMatch) nodeData.type.id = typeIdMatch[1];
      
      const typeValeurMatch = nodeXml.match(/<type>[^<]*<valeur>([^<]+)<\/valeur>/);
      if (typeValeurMatch) nodeData.type.valeur = typeValeurMatch[1];
      
      // Extract places - improved regex
      nodeData.places = {};
      const placesValeurMatch = nodeXml.match(/<places>[\s\S]*?<valeur>([\s\S]*?)<\/valeur>/);
      if (placesValeurMatch) nodeData.places.valeur = placesValeurMatch[1].trim();
      
      const placesNomMatch = nodeXml.match(/<places>[\s\S]*?<nom>([\s\S]*?)<\/nom>/);
      if (placesNomMatch) nodeData.places.nom = placesNomMatch[1].trim();
      
      // Extract etat - improved regex
      nodeData.etat = {};
      const etatValeurMatch = nodeXml.match(/<etat>[\s\S]*?<valeur>([\s\S]*?)<\/valeur>/);
      if (etatValeurMatch) nodeData.etat.valeur = etatValeurMatch[1].trim();
      
      const etatIdMatch = nodeXml.match(/<etat>[\s\S]*?<id>([\s\S]*?)<\/id>/);
      if (etatIdMatch) nodeData.etat.id = etatIdMatch[1].trim();
      
      // Extract remarque
      nodeData.remarque = {};
      const remarqueNomMatch = nodeXml.match(/<remarque>[^<]*<nom>([^<]+)<\/nom>/);
      if (remarqueNomMatch) nodeData.remarque.nom = remarqueNomMatch[1];
      
      // Use a better regex pattern for remarque/valeur that can handle multi-line content
      const remarqueValeurMatch = nodeXml.match(/<remarque>[\s\S]*?<valeur>([\s\S]*?)<\/valeur>/);
      if (remarqueValeurMatch) nodeData.remarque.valeur = remarqueValeurMatch[1].trim();
      
      // Extract info_comp
      nodeData.info_comp = {};
      
      // Site officiel - improved regex
      nodeData.info_comp.site_officiel = {};
      const siteNomMatch = nodeXml.match(/<site_officiel>[\s\S]*?<nom>([\s\S]*?)<\/nom>/);
      if (siteNomMatch) nodeData.info_comp.site_officiel.nom = siteNomMatch[1].trim();
      
      const siteUrlMatch = nodeXml.match(/<site_officiel>[\s\S]*?<url>([\s\S]*?)<\/url>/);
      if (siteUrlMatch) nodeData.info_comp.site_officiel.url = siteUrlMatch[1].trim();
      
      const siteValeurMatch = nodeXml.match(/<site_officiel>[\s\S]*?<valeur>([\s\S]*?)<\/valeur>/);
      if (siteValeurMatch) nodeData.info_comp.site_officiel.valeur = siteValeurMatch[1].trim();
      
      // Manque un mur - improved regex
      nodeData.info_comp.manque_un_mur = {};
      const murNomMatch = nodeXml.match(/<manque_un_mur>[\s\S]*?<nom>([\s\S]*?)<\/nom>/);
      if (murNomMatch) nodeData.info_comp.manque_un_mur.nom = murNomMatch[1].trim();
      
      const murValeurMatch = nodeXml.match(/<manque_un_mur>[\s\S]*?<valeur>([\s\S]*?)<\/valeur>/);
      if (murValeurMatch) nodeData.info_comp.manque_un_mur.valeur = murValeurMatch[1].trim();
      
      // Cheminee - improved regex
      nodeData.info_comp.cheminee = {};
      const chemineeNomMatch = nodeXml.match(/<cheminee>[\s\S]*?<nom>([\s\S]*?)<\/nom>/);
      if (chemineeNomMatch) nodeData.info_comp.cheminee.nom = chemineeNomMatch[1].trim();
      
      const chemineeValeurMatch = nodeXml.match(/<cheminee>[\s\S]*?<valeur>([\s\S]*?)<\/valeur>/);
      if (chemineeValeurMatch) nodeData.info_comp.cheminee.valeur = chemineeValeurMatch[1].trim();
      
      // Poele - improved regex
      nodeData.info_comp.poele = {};
      const poeleNomMatch = nodeXml.match(/<poele>[\s\S]*?<nom>([\s\S]*?)<\/nom>/);
      if (poeleNomMatch) nodeData.info_comp.poele.nom = poeleNomMatch[1].trim();
      
      const poeleValeurMatch = nodeXml.match(/<poele>[\s\S]*?<valeur>([\s\S]*?)<\/valeur>/);
      if (poeleValeurMatch) nodeData.info_comp.poele.valeur = poeleValeurMatch[1].trim();
      
      // Couvertures - improved regex
      nodeData.info_comp.couvertures = {};
      const couverturesNomMatch = nodeXml.match(/<couvertures>[\s\S]*?<nom>([\s\S]*?)<\/nom>/);
      if (couverturesNomMatch) nodeData.info_comp.couvertures.nom = couverturesNomMatch[1].trim();
      
      const couverturesValeurMatch = nodeXml.match(/<couvertures>[\s\S]*?<valeur>([\s\S]*?)<\/valeur>/);
      if (couverturesValeurMatch) nodeData.info_comp.couvertures.valeur = couverturesValeurMatch[1].trim();
      
      // Places matelas - improved regex
      nodeData.info_comp.places_matelas = {};
      const matelasNomMatch = nodeXml.match(/<places_matelas>[\s\S]*?<nom>([\s\S]*?)<\/nom>/);
      if (matelasNomMatch) nodeData.info_comp.places_matelas.nom = matelasNomMatch[1].trim();
      
      const matelasNbMatch = nodeXml.match(/<places_matelas>[\s\S]*?<nb>([\s\S]*?)<\/nb>/);
      if (matelasNbMatch) nodeData.info_comp.places_matelas.nb = matelasNbMatch[1].trim();
      
      const matelasValeurMatch = nodeXml.match(/<places_matelas>[\s\S]*?<valeur>([\s\S]*?)<\/valeur>/);
      if (matelasValeurMatch) nodeData.info_comp.places_matelas.valeur = matelasValeurMatch[1].trim();
      
      // Latrines - improved regex
      nodeData.info_comp.latrines = {};
      const latrinesNomMatch = nodeXml.match(/<latrines>[\s\S]*?<nom>([\s\S]*?)<\/nom>/);
      if (latrinesNomMatch) nodeData.info_comp.latrines.nom = latrinesNomMatch[1].trim();
      
      const latrinesValeurMatch = nodeXml.match(/<latrines>[\s\S]*?<valeur>([\s\S]*?)<\/valeur>/);
      if (latrinesValeurMatch) nodeData.info_comp.latrines.valeur = latrinesValeurMatch[1].trim();
      
      // Bois - improved regex
      nodeData.info_comp.bois = {};
      const boisNomMatch = nodeXml.match(/<bois>[\s\S]*?<nom>([\s\S]*?)<\/nom>/);
      if (boisNomMatch) nodeData.info_comp.bois.nom = boisNomMatch[1].trim();
      
      const boisValeurMatch = nodeXml.match(/<bois>[\s\S]*?<valeur>([\s\S]*?)<\/valeur>/);
      if (boisValeurMatch) nodeData.info_comp.bois.valeur = boisValeurMatch[1].trim();
      
      // Eau - improved regex
      nodeData.info_comp.eau = {};
      const eauNomMatch = nodeXml.match(/<eau>[\s\S]*?<nom>([\s\S]*?)<\/nom>/);
      if (eauNomMatch) nodeData.info_comp.eau.nom = eauNomMatch[1].trim();
      
      const eauValeurMatch = nodeXml.match(/<eau>[\s\S]*?<valeur>([\s\S]*?)<\/valeur>/);
      if (eauValeurMatch) nodeData.info_comp.eau.valeur = eauValeurMatch[1].trim();
      
      // Extract description - use better regex for multi-line content
      const descMatch = nodeXml.match(/<description>[\s\S]*?<valeur>([\s\S]*?)<\/valeur>/);
      if (descMatch) nodeData.description = descMatch[1].trim();
      
      jsonResult.nodes.push(nodeData);
    } catch (err) {
      console.warn(`Error parsing node: ${err.message}`);
      // Continue with next node
    }
  }
  
  // Write JSON to file
  fs.writeFileSync(jsonFilePath, JSON.stringify(jsonResult, null, 2), 'utf8');
  console.log(`Conversion successful! JSON file saved as ${jsonFilePath}`);
  
} catch (err) {
  console.error(`Error: ${err.message}`);
}
