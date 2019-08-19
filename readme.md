#standardSQL   Average number of inventors per country  ?

```sql
SELECT AVG(num_inventors), COUNT(*) AS cnt, country_code, filing_year, STRING_AGG(publication_number LIMIT 10) AS example_publications
FROM (
  SELECT ANY_VALUE(publication_number) AS publication_number, ANY_VALUE(ARRAY_LENGTH(inventor)) AS num_inventors, ANY_VALUE(country_code) AS country_code, ANY_VALUE(CAST(FLOOR(filing_date / (5*10000)) AS INT64))*5 AS filing_year
  FROM `patents-public-data.patents.publications` AS pubs
  WHERE filing_date > 19000000 AND ARRAY_LENGTH(inventor) > 0
  GROUP BY application_number
)
GROUP BY filing_year, country_code
HAVING cnt > 100
ORDER BY filing_year
```