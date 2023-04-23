CREATE USER IF NOT EXISTS 'safestatUser'@'%' IDENTIFIED WITH mysql_native_password BY 'safestat123';
DROP DATABASE IF EXISTS `safestat`;
SET default_storage_engine=InnoDB;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS safestat
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;
-- GRANT SELECT, INSERT, UPDATE, DELETE, FILE ON *.* TO 'safestatUser'@'%';
-- GRANT ALL PRIVILEGES ON `safestat`.* TO 'safestatUser'@'%';
GRANT ALL PRIVILEGES ON *.* TO 'safestatUser'@'%';

-- UPDATE mysql.user SET host='%' WHERE user='safestatUser';
FLUSH PRIVILEGES;

USE safestat;
CREATE TABLE Crimes (
                            link VARCHAR(150) NOT NULL,
                            published VARCHAR(50) NOT NULL,
                            tag VARCHAR(20) NOT NULL,
                            news_text VARCHAR(200),
                            PRIMARY KEY (link)
);

CREATE TABLE Tags (
                           tag VARCHAR(20) NOT NULL,
                           PRIMARY KEY (tag)
);

CREATE TABLE Locs (
                           loc VARCHAR(50) NOT NULL,
                           PRIMARY KEY (loc)
);

CREATE TABLE LocCrimes (
                            link VARCHAR(150) NOT NULL,
                            loc VARCHAR(50) NOT NULL,
                            PRIMARY KEY (link, loc)
);