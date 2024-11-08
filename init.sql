create database telegram_bot_db;
use telegram_bot_db;

create table users (
    id int primary key auto_increment,
    name varchar(255) not null,
    username varchar(255) not null,
    password varchar(255) not null,
    is_active tinyint(1) not null,
    role varchar(255) not null
);

insert into users (name, username, password, is_active, role) values ("adm","adm","scrypt:32768:8:1$ZjnHI75BJDnhP1XU$d6196d74f79f5354c99b9b573226576b3825012ea72eec782b9f956ad9594e3ddb582f4afa62ad66f17ee884137ceb466d92af1729327857be81abd570f4d7c6",1,"Admin");