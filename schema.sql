CREATE DATABASE Project-2_db;

CREATE TABLE stocks (
    index INT PRIMARY KEY,
    date DATE NOT NULL,
    ticker VARCHAR NOT NULL,
    company VARCHAR NOT NULL,
    sector VARCHAR NOT NULL,
    open FLOAT NOT NULL,
    high FLOAT NOT NULL,
    low FLOAT NOT NULL,
    close FLOAT NOT NULL,
    adjclose FLOAT NOT NULL,
    stock FLOAT NOT NULL
);
	
	
CREATE TABLE covid_confirmed (
    date DATE PRIMARY KEY,
    per_delta FLOAT NOT NULL
);

