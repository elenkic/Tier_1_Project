import camelot
import pandas as pd
import re
import matplotlib.pyplot as plt


PDF_PATH = "/Applications/PostgreSQL 18/Developer/Tier_1_Project/pdf_file/albertatier1guidelines.pdf"
OUTPUT_CSV = "/Applications/PostgreSQL 18/Developer/Tier_1_Project/csv_files/alberta_tier1_soil_guidelines.csv"


# 1. Extract tables using Camelot
tables = camelot.read_pdf(
    PDF_PATH,
    pages="43-48",          
    flavor="lattice"
)
#camelot.plot(tables[0], kind='contour')
#plt.show()
rows = []

def split_vertical(cell):
    if not isinstance(cell, str):
        return []
            
    # 1. Remove commas inside numbers
    cell = re.sub(r"(?<=\d),(?=\d)", "", cell)  # "2,000" -> "2000"

    # 2. Split on newlines
    return [
        v.strip()
        for v in cell.split("\n")
        if v.strip() and v not in ["-", ".", "—"]
    ]


# 2. Process each table
for table in tables:
    df = table.df

    # Drop header rows (first 3 rows are always headers)
    df = df.iloc[3:].reset_index(drop=True)
    #print(df.head(35))

    
    
    last_notes = ""  # store last non-empty notes

    #iterating through the table
    for _, row in df.iterrows():
        #parameter = row[0].strip()

        #if not parameter:
        #    continue

        land_uses = [
            "Natural Area", "Agricultural",
            "Residential/Parkland", "Commercial", "Industrial"
        ]
   
# --- EXCEPTION: all numbers crammed into row[0] ---
        # inside the loop
        if row[1].strip() == "" and row[2].strip() == "" and row[3].strip() == "":
            parts = [p.strip() for p in row[0].split("\n") if p.strip()]
            param_name = parts[0]
            fine_values = parts[1:6]
            coarse_values = parts[6:11]
            notes_value = parts[11] if len(parts) > 11 else ""
        else:
            param_name = row[0].strip()
            fine_values = split_vertical(row[1])
            coarse_values = split_vertical(row[2])
            notes_value = row[3].strip() if isinstance(row[3], str) and row[3].strip() else ""


        #If Notes exists, it gets assigned.
        #If Notes is empty, notes_value is "".
        #Both Fine and Coarse rows use the same notes_value from that row, and it won’t carry over from previous rows.
        notes_value = row[3].strip() if isinstance(row[3], str) and row[3].strip() else ""
        #print(f"'{notes_value}'")  # quotes will show empty strings
       

        #fine_values = split_vertical(row[1])

        # Fine soil
        for value, land_use in zip(fine_values, land_uses):
            if value:
                rows.append({
                    "parameter": param_name,
                    "soil_type": "Fine",
                    "land_use": land_use,
                    "guideline_value": value,
                    "units": "mg/kg",
                    "notes": notes_value
                })

        #coarse_cols = split_vertical(row[2])
        # Coarse soil
        for value, land_use in zip(coarse_values, land_uses):
            if value:
                rows.append({
                    "parameter": param_name,
                    "soil_type": "Coarse",
                    "land_use": land_use,
                    "guideline_value": value,
                    "units": "mg/kg",
                    "notes": notes_value
                })


# 3. Create final DataFrame
clean_df = pd.DataFrame(rows)

# Clean text artifacts
clean_df = clean_df.applymap(
    lambda x: x.replace("\n", " ").strip() if isinstance(x, str) else x
)


# 4. Save CSV
clean_df.to_csv(OUTPUT_CSV, index=False)

print(f"Done! Saved to {OUTPUT_CSV}")