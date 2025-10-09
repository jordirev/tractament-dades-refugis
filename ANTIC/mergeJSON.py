import pandas as pd
import json
from rapidfuzz import process, fuzz

# Load the geojson file that has a "nodes" wrapper
with open("c:/Users/jordi/Desktop/UNI/TFG/INFO/refusPyrinees.geojson", 'r', encoding='utf-8') as f:
    data1 = json.load(f)
    df1 = pd.DataFrame(data1["nodes"])

# Load the regular json file that is a direct array
df2 = pd.read_json("c:/Users/jordi/Desktop/UNI/TFG/INFO/refusPyrineesCompleta.json")

df1["keyName"] = df1["name"].str.lower().str.strip()
df2["keyName"] = df2["name"].str.lower().str.strip()

df1["type"] = df1["type_hebergement"]
df1["places"] = df1["cap_ete"]
df2["places"] = df2["capete"]
df2["region"] = df2["ville"]

df1 = df1.drop(columns=["cap_hiver", "photo", "type_hebergement", "cap_ete"])
df2 = df2.drop(columns=["caphiv", "capete", "ville"])

#exclude all elements that has type = "ruine" or ""Refuge gardé toute l'année"
df1 = df1[~df1["type"].isin(["ruine", "Refuge gardé toute l'année"])]
df2 = df2[~df2["type"].isin(["ruine", "Refuge gardé toute l'année"])]

# Create an empty DataFrame to store merged results
merged = pd.DataFrame()

# For each row in df1, find the best match in df2
for _, row1 in df1.iterrows():
    name1 = row1["keyName"]
    # Find the best match in df2 using fuzz.ratio for similarity scoring
    match = process.extractOne(name1, df2["keyName"].tolist(), scorer=fuzz.ratio, score_cutoff=80)
    
    if match:  # If a match was found above the cutoff
        match_name, score, idx = match
        # Create a new row that combines data from both dataframes
        merged_row = row1.to_dict()
        # Add data from df2, excluding duplicated columns
        for col in df2.columns:
            if col not in df1.columns or col == "keyName":
                merged_row[col] = df2.iloc[idx][col]
            else:
                merged_row[f"{col}_right"] = df2.iloc[idx][col]
        merged = pd.concat([merged, pd.DataFrame([merged_row])], ignore_index=True)
    else:
        # No match found, just add the row from df1
        merged = pd.concat([merged, pd.DataFrame([row1.to_dict()])], ignore_index=True)

# Add rows from df2 that weren't matched to any in df1
matched_df2_keys = [m[0] for m in [process.extractOne(name, df1["keyName"].tolist(), scorer=fuzz.ratio, score_cutoff=80) or [None] for name in df2["keyName"]]]
unmatched_df2 = df2[df2["keyName"].apply(lambda x: x not in matched_df2_keys)]
merged = pd.concat([merged, unmatched_df2], ignore_index=True)
merged = merged.drop(columns=["keyName", "places_right", "name_right", "type_right", "region_right","altitude_right"])

# Save info in json
merged.to_json("c:/Users/jordi/Desktop/UNI/TFG/INFO/refusPyrineesMerged.json", orient="records")

# Save info in a more readable format for inspection
with open("c:/Users/jordi/Desktop/UNI/TFG/INFO/refusPyrineesMerged_pretty.json", 'w', encoding='utf-8') as f:
    json.dump(json.loads(merged.to_json(orient="records")), f, ensure_ascii=False, indent=4)
