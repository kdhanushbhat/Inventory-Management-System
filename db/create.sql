
create database root_try3_root;
use root_try3_root;
create table itmtype(typid int auto_increment,typnm varchar(20),primary key(typid));
create table item(iid int auto_increment,iname varchar(20),typid int ,
cstprc float,selprc float,quantity varchar(10),primary key(iid),foreign key(typid) references itmtype(typid) on delete cascade);
create table customer(cid int auto_increment,cname varchar(20),phone int,address varchar(50),email varchar(20), primary key(cid));
create table orders(ordid int auto_increment,cid int,amount float,odate date,status boolean,
primary key(ordid),foreign key(cid) references customer(cid) on delete cascade on update cascade);
create table ord_det(ordid int,iid int,quant varchar(15),amount float,
foreign key(ordid) references orders(ordid) on delete cascade on update cascade,
foreign key(iid) references item(iid) on delete cascade on update cascade);
create table sales(iid int,quant int,quantval varchar(3),amnt int,
foreign key(iid) references item(iid) on delete cascade on update cascade);
select * from item;