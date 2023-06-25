CREATE INDEX idx_zno_results_outid_birth_sextypename
ON zno_results (outid, birth, sextypename);

CREATE INDEX idx_zno_results_Regname_AreaName_TerName
ON zno_results (regname, areaname, tername);

CREATE INDEX idx_zno_results_EOName_EOTypeName
ON zno_results (eoname, eotypename);

INSERT INTO locations(regname, areaname, tername, tertypename)
	SELECT DISTINCT regname, areaname, tername, tertypename FROM zno_results;

CREATE INDEX idx_locations_regname_areaname_tername
ON locations (regname, areaname, tername);
