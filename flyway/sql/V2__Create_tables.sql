CREATE TABLE locations (
	location_id SERIAL PRIMARY KEY,
	regname VARCHAR(1000) NOT NULL,
	areaname VARCHAR(1000) NOT NULL,
	tername VARCHAR(1000) NOT NULL,
	tertypename VARCHAR(1000) NOT NULL
);

CREATE TABLE educational_organisations(
	eo_id SERIAL PRIMARY KEY,
	eo_name VARCHAR(1000) NOT NULL,
	eo_type VARCHAR(1000) NOT NULL,
	location_id INT,
	FOREIGN KEY(location_id) REFERENCES locations(location_id)
);

CREATE TABLE students(
	student_id SERIAL PRIMARY KEY,
	year_of_passing CHAR(4) NOT NULL,
	outid VARCHAR(100) NOT NULL,
	birth NUMERIC NOT NULL,
	sextypename CHAR(8) NOT NULL,
	location_id INT NULL,
	eo_id INT NULL
);

CREATE TABLE tests_results(
	tests_id SERIAL PRIMARY KEY,
    uml_test_status VARCHAR(25),
    uml_test_ball100 DECIMAL,
    uml_test_ball12 DECIMAL,
    uml_test_ball DECIMAL,
    ukr_test_status VARCHAR(25),
    ukr_test_ball100 DECIMAL,
    ukr_test_ball12 DECIMAL,
    ukr_test_ball DECIMAL,
    hist_test_status VARCHAR(25),
    hist_test_ball100 DECIMAL,
    hist_test_ball12 DECIMAL,
    hist_test_ball DECIMAL,
    math_test_status VARCHAR(25),
    math_test_ball100 DECIMAL,
    math_test_ball12 DECIMAL,
    math_test_ball DECIMAL,
    phys_test_status VARCHAR(25),
    phys_test_ball100 DECIMAL,
    phys_test_ball12 DECIMAL,
    phys_test_ball DECIMAL,
    chem_test_status VARCHAR(25),
    chem_test_ball100 DECIMAL,
    chem_test_ball12 DECIMAL,
    chem_test_ball DECIMAL,
    bio_test_status VARCHAR(25),
    bio_test_ball100 DECIMAL,
    bio_test_ball12 DECIMAL,
    bio_test_ball DECIMAL,
    geo_test_status VARCHAR(25),
    geo_test_ball100 DECIMAL,
    geo_test_ball12 DECIMAL,
    geo_test_ball DECIMAL,
    eng_test_status VARCHAR(25),
    eng_test_ball100 DECIMAL,
    eng_test_ball12 DECIMAL,
    eng_test_ball DECIMAL,
    fr_test_status VARCHAR(25),
    fr_test_ball100 DECIMAL,
    fr_test_ball12 DECIMAL,
    fr_test_ball DECIMAL,
    deu_test_status VARCHAR(25),
    deu_test_ball100 DECIMAL,
    deu_test_ball12 DECIMAL,
    deu_test_ball DECIMAL,
    sp_test_status VARCHAR(25),
    sp_test_ball100 DECIMAL,
    sp_test_ball12 DECIMAL,
    sp_test_ball DECIMAL,
    student_id INT NULL,
	FOREIGN KEY(student_id) REFERENCES students(student_id)
);
