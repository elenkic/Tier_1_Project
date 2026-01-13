COPY guidelines(parameter, soil_type, land_use, guideline_value, units, notes)
FROM '/Applications/PostgreSQL 18/Developer/Tier_1_Project/csv_files/alberta_tier1_soil_guidelines.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

COPY results
FROM '/Applications/PostgreSQL 18/Developer/Tier_1_Project/csv_files/results.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

COPY samples
FROM '/Applications/PostgreSQL 18/Developer/Tier_1_Project/csv_files/samples.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

/*
COPY command means to copy contents to a specific file. so we want to copy data into company_dim
FROM where the csv is living
*/
SELECT * FROM samples;