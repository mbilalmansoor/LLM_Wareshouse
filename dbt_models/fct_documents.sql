{{ config(materialized='table') }}

WITH base_data AS (
    -- Reads directly from your raw landing table
    SELECT * FROM {{ source('landing_zone', 'raw_documents') }}
),

deduplicated AS (
    SELECT
        b.*, -- Expands all columns from base_data explicitly
        -- Correctly hashes the row variable record structure tuple (b)
        ROW_NUMBER() OVER (
            PARTITION BY MD5(CAST(b AS TEXT)) 
            ORDER BY 1 -- Safe, fast deterministic sequencing placeholder
        ) as row_sequence
    FROM base_data b -- Added the explicit alias reference string link
)

-- Only output the unique, first occurrence of each row
SELECT
    * EXCLUDE (row_sequence)
FROM deduplicated
WHERE row_sequence = 1
