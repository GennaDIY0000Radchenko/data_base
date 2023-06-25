INSERT INTO tests_results (uml_test_status, uml_test_ball100, uml_test_ball12, uml_test_ball,
                            ukr_test_status, ukr_test_ball100, ukr_test_ball12, ukr_test_ball,
                            hist_test_status, hist_test_ball100, hist_test_ball12, hist_test_ball,
                            math_test_status, math_test_ball100, math_test_ball12, math_test_ball,
                            phys_test_status, phys_test_ball100, phys_test_ball12, phys_test_ball,
                            chem_test_status, chem_test_ball100, chem_test_ball12, chem_test_ball,
                            bio_test_status, bio_test_ball100, bio_test_ball12, bio_test_ball,
                            geo_test_status, geo_test_ball100, geo_test_ball12, geo_test_ball,
                            eng_test_status, eng_test_ball100, eng_test_ball12, eng_test_ball,
                            fr_test_status, fr_test_ball100, fr_test_ball12, fr_test_ball,
                            deu_test_status, deu_test_ball100, deu_test_ball12, deu_test_ball,
                            sp_test_status, sp_test_ball100, sp_test_ball12, sp_test_ball,
                            student_id)
SELECT umlteststatus, umlball100, umlball12, umlball,
        ukrteststatus, ukrball100, ukrball12, ukrball,
        histteststatus, histball100, histball12, histball,
        mathteststatus, mathball100, mathball12, mathball,
        physteststatus, physball100, physball12, physball,
        chemteststatus, chemball100, chemball12, chemball,
        bioteststatus, bioball100, bioball12, bioball,
        geoteststatus, geoball100, geoball12, geoball,
        engteststatus, engball100, engball12, engball,
        frateststatus, fraball100, fraball12, fraball,
        deuteststatus, deuball100, deuball12, deuball,
        spateststatus, spaball100, spaball12, spaball,
        s.student_id
FROM zno_results as z
JOIN students as s ON z.outid = s.outid
                   AND z.birth = s.birth
                   AND z.sextypename = s.sextypename;


ALTER TABLE students
ADD COLUMN tests_results_id INT NULL;

ALTER TABLE students
ADD FOREIGN KEY (tests_results_id) REFERENCES tests_results(tests_id);


UPDATE students
SET tests_results_id = tests_results.tests_id
FROM tests_results
WHERE students.student_id = tests_results.student_id;
