INSERT INTO educational_organisations (eo_name, eo_type, location_id)
    SELECT DISTINCT eoname, eotypename, locations.location_id
    FROM zno_results

    JOIN locations ON zno_results.regname = locations.regname
        AND zno_results.areaname = locations.areaname
        AND zno_results.tername = locations.tername
        AND zno_results.tertypename = locations.tertypename;

    CREATE INDEX idx_educational_organisations_eo_name_eo_type
    ON educational_organisations (eo_name, eo_type);
