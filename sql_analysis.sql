-- Average price by location
SELECT 
    Location, 
    ROUND(AVG(Price), 2) as Average_Price,
    COUNT(*) as Property_Count
FROM properties
GROUP BY Location
ORDER BY Average_Price DESC;

-- Property-type analysis
SELECT 
    Property_Type, 
    ROUND(AVG(Price), 2) as Average_Price,
    COUNT(*) as Property_Count
FROM properties
GROUP BY Property_Type
ORDER BY Average_Price DESC;

-- Price-per-square-foot analysis by Location and Property Type
SELECT 
    Location,
    Property_Type,
    ROUND(AVG(Price_per_sqft), 2) as Avg_Price_Per_Sqft
FROM properties
GROUP BY Location, Property_Type
ORDER BY Location, Avg_Price_Per_Sqft DESC;
