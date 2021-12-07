USE ManageUser;

CREATE TABLE InfoAddRowDatabase
(
	Id INT PRIMARY KEY AUTO_INCREMENT,
	NameDatabase nchar(100),
    NameTable nchar(100)
);

SHOW COLUMNS FROM  quangbdhz_abcda.Datatype;
INSERT INTO quangbdhz_adduser.test(Id, name, avg) VALUES (3, 'ac', NULL);
INSERT INTO quangbdhz_myDatabase.user(Id, FullName, UserName, Password) VALUES (5, '22', '32', '5');

SELECT * FROM quangbdhz_abcda.Datatype

INSERT INTO InfoAddRowDatabase(NameDatabase, NameTable) 
VALUES ('abcda', 'Datatype');

SELECT * FROM ManageUser.InfoAddRowDatabase;

UPDATE ManageUser.InfoAddRowDatabase SET NameDatabase = 'a', NameTable = 'b' WHERE Id = 1;
SET SQL_SAFE_UPDATES = 0;
SELECT id FROM quangbdhz_abcda.Datatype ORDER BY id DESC LIMIT 1;

DROP DATABASE quangbdhz_oneShot;
INSERT INTO quangbdhz_myDatabase.user(Id, FullName, UserName, Password) VALUES (2, "2", "2", "2")

CREATE DATABASE yukino_Oregairu;
SELECT * FROM  quangbdhz_myDatabase.user;
INSERT INTO quangbdhz_adduser.users(FullName, UserName) VALUES ("quangbdhz", "12345");	
USE quangbdhz_oneShot;

UPDATE quangbdhz_adduser.user SET Id = '3', FullName = 'quangbdhz', UserName = '12345' WHERE Id = '2', FullName = 'quangbdhz', UserName = '12345'

UPDATE quangbdhz_adduser.users SET FullName = 'quang', UserName = '12345' where UserName = '1234' and Id = '1';


SELECT * FROM quangbdhz_dataTestABC.user;
SELECT * FROM ManageUser.InfoAddRowDatabase;


CREATE TABLE quangbdhz_adduser.users
(
	Id INT PRIMARY KEY AUTO_INCREMENT,
    FullName NVARCHAR(200),
    UserName CHAR(100)
);

INSERT INTO users(FullName, UserName) 
VALUES ('Tran Quang', 'quangbdhz');

INSERT INTO users(FullName, UserName) 
VALUES ('Tran Quang 1', 'quangbdhz');

INSERT INTO users(FullName, UserName) 
VALUES ('Tran Quang 2', 'quangbdhz');

INSERT INTO users(FullName, UserName) 
VALUES ('Tran Quang 3', 'quangbdhz');


SELECT * FROM TypeTable;

SELECT * FROM users;

INSERT INTO users(FullName, UserName, Password, Email, Phone, IsAdmin, Active, Avatar) 
VALUES ('Tran Quang', 'quangbdhz', '12345', 'tranquangbdhz@gmail.com', '0708046010', 1, 1, 'https://res.cloudinary.com/https-deptraitd-blogspot-com/image/upload/v1638089975/UserManageDatabase/932465_bdfdlk.png');

INSERT INTO users(FullName, UserName, Password, Email, Phone, IsAdmin, Active, Avatar) 
VALUES ('Hachiman', 'hiki', '12345', 'oregairu@gmail.com', '0708046010', 0, 1, 'https://res.cloudinary.com/https-deptraitd-blogspot-com/image/upload/v1638090045/UserManageDatabase/1001923_e7vhfv.jpg');

INSERT INTO users(FullName, UserName, Password, Email, Phone, IsAdmin, Active, Avatar) 
VALUES ('Yukino', 'yukino', '12345', '19110443@student.hcmute.edu.vn', '0708046010', 0, 1, 'https://res.cloudinary.com/https-deptraitd-blogspot-com/image/upload/v1638090055/UserManageDatabase/hachiman_lfdirh.png');
	
CREATE TABLE Users
(
	Id INT PRIMARY KEY AUTO_INCREMENT,
    FullName NVARCHAR(200),
    UserName CHAR(100),
    Password CHAR(200),
    Email CHAR(200) NOT NULL,
    Phone CHAR(20),
    IsAdmin INT NOT NULL DEFAULT 0,
    Active INT NOT NULL DEFAULT 1,
	Avatar NCHAR(200)
);

DROP TABLE users;
DROP TABLE TypeTable;

CREATE TABLE TypeTable
(Id INT PRIMARY KEY AUTO_INCREMENT, Datatypes CHAR(50) NOT NULL, CheckInput INT NOT NULL);

use quangbdhz_abcda;

SELECT * FROM ManageUser.TypeTable;

CREATE TABLE Datatype
(Id INT PRIMARY KEY AUTO_INCREMENT,Name CHAR(50) NOT NULL,CheckInputNumber INT NOT NULL, Active INT);

INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('INT', 0, 1);
INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('FLOAT', 0, 1);
INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('DOUBLE', 0, 1);
INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('CHAR()', 1, 1);
INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('VARCHAR()', 1, 1);
INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('TEXT()', 1, 1);
INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('DECIMAL()', 1, 1);
INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('DATETIME', 0, 1);
INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('BLOB', 0, 1);
INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('BINARY()', 1, 1);
INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('BLOB()', 1, 1);
INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('VARBINARY()', 1, 1);
INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('TIME()', 1, 1);
INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('TIMESTAMP', 1, 1);
INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('DECIMAL', 0, 1);
INSERT INTO Datatype(Name, CheckInputNumber, Active) VALUES ('JSON', 0, 1);