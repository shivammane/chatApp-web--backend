create table users(
userid int AUTO_INCREMENT PRIMARY KEY,
firstname varchar(20) NOT NULL,
lastname varchar(20) not null,
email varchar(30) not null UNIQUE,
password varchar(20) not null,
connection_id varchar(20)
);

-- drop table users;

-- TRUNCATE TABLE users;

create table messeges(
messegeid int AUTO_INCREMENT PRIMARY KEY,
sender int ,
messege TEXT,
receiver int,
FOREIGN KEY (sender) REFERENCES users(userid),
FOREIGN KEY (receiver) REFERENCES users(userid)
);

-- drop table messeges;

-- important query for selecting messeges 
-- select u.firstname as sender ,m.messege,k.firstname as receiver from messeges m
-- join users u on u.userid = m.sender
-- JOIN users k on k.userid = m.receiver;

