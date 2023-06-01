
USE CS306_project_schema;


CREATE TABLE Countries (
	iso_code CHAR(11),
   	name VARCHAR(50),
    year_ INTEGER,
    population INTEGER,
	PRIMARY KEY (iso_code)
);


CREATE TABLE Democracies_Governedby (
	iso_code CHAR(11) NOT NULL,
	d_id INTEGER AUTO_INCREMENT,
	year_ INTEGER,
	deliberative_dem DECIMAL,
	liberal_dem DECIMAL,
	electoral_dem DECIMAL,
	egalitarian_dem DECIMAL,
	participiary_dem DECIMAL,
	PRIMARY KEY(d_id, iso_code),
	FOREIGN KEY (iso_code) REFERENCES Countries (iso_code) ON DELETE CASCADE
);


CREATE TABLE BribePayers_Has (
	iso_code CHAR(11) NOT NULL,
	b_id  INTEGER AUTO_INCREMENT,
	year_ INTEGER,
	bribe_payers_index REAL,
	PRIMARY KEY(b_id, iso_code),
	FOREIGN KEY (iso_code) REFERENCES Countries (iso_code) ON DELETE CASCADE
);


CREATE TABLE Schooling_Announces (
	iso_code CHAR(11) NOT NULL,
	s_id INTEGER AUTO_INCREMENT,
	year_ INTEGER,
    schooling_index REAL,
	population INTEGER,
    PRIMARY KEY(s_id, iso_code),
	FOREIGN KEY (iso_code) REFERENCES Countries (iso_code) ON DELETE CASCADE
);


CREATE TABLE HumDev_Reports (
	iso_code CHAR(11) NOT NULL,
	h_id INTEGER AUTO_INCREMENT,
	year_ INTEGER,
    hum_dev_index REAL,
	population INTEGER,
    PRIMARY KEY(h_id, iso_code),
	FOREIGN KEY (iso_code) REFERENCES Countries (iso_code) ON DELETE CASCADE
);


CREATE TABLE CorrupPercep_Describes (
	iso_code CHAR(11) NOT NULL,
	c_id INTEGER AUTO_INCREMENT,
	year_ INTEGER,
    corr_per_index REAL,
	bribery_rate DECIMAL,
    population INTEGER,
    PRIMARY KEY(c_id, iso_code),
	FOREIGN KEY (iso_code) REFERENCES Countries (iso_code) ON DELETE CASCADE
);

