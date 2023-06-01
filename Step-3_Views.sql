
-- part-a -- 
-- creating views (in total, we created 7 views)
Drop view if exists low_democratized_countries;
Create view low_democratized_countries as
Select D.country, D.avg_liberal_dem_idx 
from (Select D2.iso_code as country, AVG(D2.liberal_dem) as avg_liberal_dem_idx
	  From Democracies_Governedby D2
      Group by D2.iso_code) as D
Where D.avg_liberal_dem_idx <= 0.408
Group by D.country;


Drop view if exists high_schooling_countries;
Create view high_schooling_countries as
Select A.country, A.avg_schooling_idx 
From (Select C4.iso_code as country, AVG(C4.schooling_index) as avg_schooling_idx 
	  FROM cs306_project.schooling_announces C4
	  Group by C4.iso_code) as A 
Where A.avg_schooling_idx >= 8.3 
Group by A.country;


Drop view if exists high_development_countries;
Create view high_development_countries as
Select hum.country, hum.avg_hum_dev_idx 
From (Select HD.iso_code as country, AVG(HD.hum_dev_index) as avg_hum_dev_idx
	  From cs306_project.humdev_reports HD
      Group by HD.iso_code) as hum
Where hum.avg_hum_dev_idx >= 0.711
Group by hum.country;


Drop view if exists high_corr_per_countries;
Create view high_corr_per_countries as
Select c.iso as country, c.aver as avg_corr_per_idx
From (Select Co.iso_code as country, AVG(co.corr_per_index) as aver From cs306_project.corruppercep_describes CO
	  Group By CO.iso_code ) as C
	  WHERE c.aver >= 42.805
Group by c.iso;


Drop view if exists high_bribery_countries;
Create view high_bribery_countries as
Select B.iso as country, B.aver as avg_bribe_payers_index
From (Select BH.iso_code as iso, Avg(BH.bribe_payers_index) as aver 
      From cs306_project.bribepayers_has BH 
      Group by BH.iso_code) as B
Where b.aver >= 7.872
Group by B.iso;

-- Extra views --
Drop view if exists high_democratized_countries;
Create view high_democratized_countries as
Select D.country, D.avg_liberal_dem_idx 
from (Select D2.iso_code as country, AVG(D2.liberal_dem) as avg_liberal_dem_idx
	  From Democracies_Governedby D2
      Group by D2.iso_code) as D
Where D.avg_liberal_dem_idx > 0.408
Group by D.country;


Drop view if exists low_corr_per_countries;
Create view low_corr_per_countries as
Select c.iso as country, c.aver as avg_corr_per_idx
From (Select Co.iso_code as country, AVG(co.corr_per_index) as aver From cs306_project.corruppercep_describes CO
	  Group By CO.iso_code ) as C
	  WHERE c.aver < 42.805
Group by c.iso;


-- part-b: intersect and inner join --
SELECT H.country FROM high_corr_per_countries H
INTERSECT
SELECT D.country FROM low_democratized_countries D;

SELECT H.country 
FROM high_corr_per_countries H 
JOIN low_democratized_countries D 
ON H.country = D.country;

-- part-c: in and exists --
-- select statement with "in" returns the country information for 
-- lowly democratized countries that also have a high bribery rate
SELECT L.country, L.avg_liberal_dem_idx, H.avg_bribe_payers_index
FROM low_democratized_countries L, high_bribery_countries H
WHERE L.country IN (SELECT H2.country 
					FROM high_bribery_countries H2);
                    
-- same select statement is written using "exists"
SELECT L.country, L.avg_liberal_dem_idx, H.avg_bribe_payers_index
FROM low_democratized_countries L, high_bribery_countries H
WHERE EXISTS (SELECT * 
			  FROM high_bribery_countries H2
              WHERE L.country = H2.country);
                    
-- Aggregate operators
-- SUM, AVG, COUNT, MIN, MAX

-- List the names and codes of the countries who have a high liberal democracy index and a low corruption perception index 
-- use the AVG operator

Select C.iso_code, C.name, AVG(D.liberal_dem) as avg_liberal_dem, MIN(D.liberal_dem) as min_liberal_dem, 
	MAX(D.liberal_dem) as max_liberal_dem
From Countries C, Democracies_Governedby D
Where C.iso_code = D.iso_code
Group by D.iso_code, C.name
Having COUNT(*) > 1;

Select C.iso_code, C.name, AVG(CP.corr_per_index) as avg_corr_per_idx, MIN(CP.corr_per_index) as min_corr_per_idx, 
	MAX(CP.corr_per_index) as max_corr_per_idx
From Countries C, CorrupPercep_Describes CP
Where C.iso_code = D.iso_code
Group by D.iso_code, C.name
Having COUNT(*) > 1;

Select CP.iso_code, C.name, SUM((CP.bribery_rate)*CP.population)/COUNT(CP.year_) as estimated_bribery_incidents
From cs306_project.Countries C, cs306_project.CorrupPercep_Describes CP
Where C.iso_code = CP.iso_code
Group by CP.iso_code, C.name;

-- How corrupt the countries are?
Select C.iso_code, C.name, MIN(H.hum_dev_index), MIN(S.schooling_index), MIN(D.liberal_dem), MAX(CP.corr_per_index),
	MAX(B.bribe_payers_index)
From Countries C, HumDev_Reports H, Schooling_Announces S, Democracies_Governedby D, CorrupPercep_Describes CP, 
	BribePayers_Has B
Where C.iso_code = H.iso_code AND C.iso_code = S.iso_code AND C.iso_code = D.iso_code AND 
	C.iso_code = CP.iso_code AND C.iso_code = B.iso_code
Group by H.iso_code, S.iso_code, D.iso_code, CP.iso_code, B.iso_code;

-- How virtuous the countries are?
Select C.iso_code, C.name, MAX(H.hum_dev_index), MAX(S.schooling_index), MAX(D.liberal_dem), MIN(CP.corr_per_index),
	MIN(B.bribe_payers_index)
From Countries C, HumDev_Reports H, Schooling_Announces S, Democracies_Governedby D, CorrupPercep_Describes CP, 
	BribePayers_Has B
Where C.iso_code = H.iso_code AND C.iso_code = S.iso_code AND C.iso_code = D.iso_code AND 
	C.iso_code = CP.iso_code AND C.iso_code = B.iso_code
Group by H.iso_code, S.iso_code, D.iso_code, CP.iso_code, B.iso_code;


-- Question 2: Constraints and Triggers
ALTER TABLE cs306_project.corruppercep_describes
ADD CONSTRAINT index_range_brib CHECK ( bribery_rate >= 0 AND bribery_rate <= 84);
INSERT INTO cs306_project.corruppercep_describes (bribery_rate) VALUES (85);


-- trigger for before insert
DELIMITER //
CREATE TRIGGER index_range_check_insert
BEFORE INSERT ON cs306_project.corruppercep_describes
FOR EACH ROW
BEGIN
    IF NEW.bribery_rate < 0 THEN
        SET NEW.bribery_rate = 0;
    ELSEIF NEW.bribery_rate > 84 THEN
        SET NEW.bribery_rate = 84;
    END IF;
END //
DELIMITER ;


-- trigger for before update
DELIMITER //
CREATE TRIGGER index_range_check_update
BEFORE update ON cs306_project.corruppercep_describes
FOR EACH ROW
BEGIN
    IF NEW.bribery_rate < 0 THEN
        SET NEW.bribery_rate = 0;
    ELSEIF NEW.bribery_rate > 84 THEN
        SET NEW.bribery_rate = 84;
    END IF;
END //
DELIMITER ;


-- Question 3: Stored Procedure
DELIMITER //
CREATE PROCEDURE corr_per_data (IN iso_code CHAR(11))
BEGIN
  IF iso_code = 'TUR' THEN
    SELECT * FROM corruppercep_describes C WHERE C.iso_code = 'TUR';
  ELSEIF iso_code = 'RUS' THEN
    SELECT * FROM corruppercep_describes C WHERE  C.iso_code = 'RUS';
  ELSEIF iso_code = 'USA' THEN
    SELECT * FROM corruppercep_describes C WHERE  C.iso_code = 'USA';
  ELSEIF iso_code = 'SWE' THEN
    SELECT * FROM corruppercep_describes C WHERE  C.iso_code = 'SWE';
  ELSE
    SELECT 'Invalid ISO code';
  END IF;
END //
DELIMITER ;

CALL corr_per_data('RUS');
CALL corr_per_data('TUR');
CALL corr_per_data('USA');
CALL corr_per_data('SWE');


