INSERT INTO students (year_of_passing, outid, birth, sextypename)
    SELECT year, outid, birth, sextypename
    FROM zno_results;

ALTER TABLE students
ADD FOREIGN KEY (location_id) REFERENCES locations(location_id);

ALTER TABLE students
ADD FOREIGN KEY (eo_id) REFERENCES educational_organisations(eo_id);

UPDATE students
SET location_id = loc.location_id,
    eo_id = eo.eo_id
FROM zno_results as z
JOIN locations as loc ON z.regname = loc.regname
                     AND z.areaname = loc.areaname
                     AND z.tername = loc.tername
JOIN educational_organisations as eo ON z.eoname = eo.eo_name
                                    AND z.eotypename = eo.eo_type
WHERE students.location_id IS NULL AND students.eo_id IS NULL
  AND students.outid = z.outid
  AND students.birth = z.birth
  AND students.sextypename = z.sextypename;


CREATE INDEX idx_students_location_id
ON students (location_id);

CREATE INDEX idx_students_eo_id
ON students (eo_id);

CREATE INDEX idx_students_outid_birth_sextypename
ON students (outid, birth, sextypename);
