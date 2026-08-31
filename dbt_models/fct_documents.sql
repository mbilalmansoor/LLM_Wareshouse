{{ config(materialized='table') }}

WITH base_data AS (
    -- Reads directly from your raw landing table
    SELECT * FROM {{ source('landing_zone', 'raw_documents') }}
),

deduplicated AS (
    SELECT
        *,
        -- Generates a deterministic hash of the entire row to flag duplicates
        ROW_NUMBER() OVER (
            PARTITION BY MD5(CAST(base_data AS TEXT)) 
            ORDER BY (SELECT NULL)
        ) as row_sequence
    FROM base_data
)

-- Only output the unique, first occurrence of each row
SELECT
    * EXCLUDE (row_sequence)
FROM deduplicated
WHERE row_sequence = 1
