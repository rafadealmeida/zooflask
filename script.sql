create database zooflask;

use zooflask;

create table animal(
  id int primary key auto_increment,
  nome_popular varchar(80) NOT NULL,
  nome_cientifico varchar(60) NOT NULL,
  habitos_noturnos LONGTEXT NOT NULL
);


create table avaliacao(
  id int primary key auto_increment,
  texto LONGTEXT NOT NULL,
  polaridade LONGTEXT NOT NULL
);


select * from animal;
select * from avaliacao;
