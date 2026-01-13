

-- Create guidelines table with primary key
CREATE TABLE public.guidelines (
    guideline_id SERIAL PRIMARY KEY,
    parameter VARCHAR(255) NOT NULL,
    soil_type VARCHAR(50),
    land_use VARCHAR(50),
    guideline_value TEXT,
    units VARCHAR(50),
    notes TEXT
);


-- Create samples table with primary key

CREATE TABLE public.samples (
    sample_id INT PRIMARY KEY,
    sample_name VARCHAR(255) NOT NULL,
    sample_type VARCHAR(50) DEFAULT 'regular', -- regular, duplicate, field_blank, trip_blank, equipment_blank
    original_sample_id INT REFERENCES public.samples(sample_id), -- points to original sample for dups/blanks
    depth_m NUMERIC,
    location VARCHAR(255),
    land_use VARCHAR(50),
    collection_date TIMESTAMP
);

-- Create results table with a primary key and foreign keys

CREATE TABLE public.results (
    result_id INT,
    sample_id INT,
    parameter VARCHAR(255) NOT NULL,
    concentration_value NUMERIC,
    detection_limit NUMERIC,
    soil_type VARCHAR(50),
    units VARCHAR(50),
    PRIMARY KEY (result_id, sample_id),
    FOREIGN KEY (sample_id) REFERENCES public.samples(sample_id)

);


-- Set ownership of the tables to the postgres user
ALTER TABLE public.guidelines OWNER to postgres;
ALTER TABLE public.samples OWNER to postgres;
ALTER TABLE public.results OWNER to postgres;


-- Create indexes for faster queries (optional)
CREATE INDEX idx_sample_id ON public.results (sample_id);
CREATE INDEX idx_parameter ON public.results(parameter);
CREATE INDEX idx_guidelines_lookup 
    ON public.guidelines(parameter, soil_type, land_use);
