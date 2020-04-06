-- course_catalog_init.sql

-- Initializes the course_catalog database

/* WARNING !! 
----------------------
This script will drop tables!


It can be used to reset the database if needed.
*/


/* CLEANUP
---------------*/
DROP TABLE course;
DROP TABLE catalog;
DROP TABLE credit_type;
DROP TABLE catalog_year;
DROP TABLE school;
DROP TABLE system_user;


-- system_user table
/*
This table will be for admin users who will have the ability to 
add and edit information. 
*/
CREATE TABLE system_user 
( system_user_id        SERIAL 
, email                 VARCHAR(60)     NOT NULL
, first_name            VARCHAR(60)     NOT NULL
, last_name             VARCHAR(60)     NOT NULL
, password              VARCHAR(250)
, salt                  VARCHAR(250)
, CONSTRAINT system_user_pk PRIMARY KEY (system_user_id)
);

INSERT INTO system_user 
( email 
, first_name 
, last_name 
, password 
, salt )
VALUES 
( 'admin@admin'
, 'Admin'
, 'Admin'
, ''
, '');

-- catalog_year table
/*
This table will organize all of the school courses by year.
*/
CREATE TABLE catalog_year
( catalog_year_id       SERIAL 
, name                  VARCHAR(30)     NOT NULL
, endyear               INT             NOT NULL
, active                INT             NOT NULL    DEFAULT 1
, CONSTRAINT catalog_year_pk PRIMARY KEY (catalog_year_id)
);


INSERT INTO catalog_year 
( name 
, endyear
, active )
VALUES 
( '19-20'
, 2020
, 1);


-- school table
/*
This table will hold the data for schools
*/
CREATE TABLE school 
( school_id             SERIAL 
, number                INT             NOT NULL
, name                  VARCHAR(60)     NOT NULL
, abbreviation          VARCHAR(6)      NOT NULL
, active                INT             NOT NULL    DEFAULT 1
, CONSTRAINT school_pk PRIMARY KEY (school_id)
);

INSERT INTO school 
( number 
, name 
, abbreviation
, active )
VALUES 
( '1202056'
, 'Shire High School'
, 'SHS'
, 1);



-- credit_type table
/*
This table will hold the various types of credit.
*/
CREATE TABLE credit_type 
( credit_type_id        SERIAL 
, name                  VARCHAR(30)     NOT NULL
, code                  VARCHAR(6)      NOT NULL
, CONSTRAINT credit_type_pk PRIMARY KEY (credit_type_id)
);

INSERT INTO credit_type 
( name 
, code )
VALUES 
  ( 'Math', 'MAT')
, ( 'English', 'ENG')
, ( 'Science', 'SCI')
, ( 'Social Studies', 'SOC')
, ( 'Vocational', 'VOC')
, ( 'Fine Arts', 'ART')
, ( 'Physical Education', 'PHYS')
, ( 'Elective', 'ELEC');



-- catalog table
/*
This will contain the data for a catalog
*/
CREATE TABLE catalog 
( catalog_id            SERIAL 
, school_id             INT             NOT NULL
, catalog_year_id       INT             NOT NULL
, name                  VARCHAR(30)     NOT NULL
, CONSTRAINT catalog_pk PRIMARY KEY (catalog_id)
, CONSTRAINT catalog_fk_1 FOREIGN KEY (school_id) REFERENCES school(school_id)
, CONSTRAINT catalog_fk_2 FOREIGN KEY (catalog_year_id) REFERENCES catalog_year(catalog_year_id)
);

INSERT INTO catalog 
( school_id
, catalog_year_id 
, name )
VALUES 
( (SELECT school_id FROM school WHERE number = 1202056)
, (SELECT catalog_year_id FROM catalog_year WHERE active = 1)
, 'SHS 19-20');


-- course table 
/*
This table will hold the course data
*/
CREATE TABLE course 
( course_id             SERIAL 
, catalog_id            INT             NOT NULL
, number                VARCHAR(20)     NOT NULL
, name                  VARCHAR(60)     NOT NULL
, description           TEXT
, video_link            VARCHAR(250)
, credits               NUMERIC
, credit_type_id        INT
, active                INT             NOT NULL    DEFAULT 1
, CONSTRAINT course_pk PRIMARY KEY (course_id)
, CONSTRAINT course_fk_1 FOREIGN KEY (catalog_id) REFERENCES catalog(catalog_id)
, CONSTRAINT course_fk_2 FOREIGN KEY (credit_type_id) REFERENCES credit_type(credit_type_id)
);

INSERT INTO course 
( catalog_id 
, number 
, name 
, description )
VALUES 
( (SELECT cat.catalog_id 
  FROM catalog cat INNER JOIN school sch 
  ON cat.school_id = sch.school_id 
  INNER JOIN catalog_year cy 
  ON cat.catalog_year_id = cy.catalog_year_id
  WHERE sch.number = 1202056
  AND cy.active = 1)
, 'CS101'
, 'Introduction to Web Development'
, 'An introduction to full-stack web development with Flask.');