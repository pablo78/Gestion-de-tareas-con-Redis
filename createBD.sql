create database todolist;
use todolist;
create table tarea (
id int,
descripcion varchar(250),
completada varchar(5)
);
show tables;
insert into tarea (id, descripcion, completada) values (1, "Tarea 1 - Definición de TodoList", "False");
insert into tarea (id, descripcion, completada) values (2, "Tarea 2 - Analisis de TodoList", "False");
insert into tarea (id, descripcion, completada) values (3, "Tarea 3 - Diseño de TodoList", "False");
insert into tarea (id, descripcion, completada) values (4, "Tarea 4 - Construcción de TodoList", "False");
insert into tarea (id, descripcion, completada) values (5, "Tarea 5 - Pruebas unitarias TodoList", "False");
insert into tarea (id, descripcion, completada) values (6, "Tarea 6 - Pruebas integrales TodoList", "False");
insert into tarea (id, descripcion, completada) values (7, "Tarea 7 - Preparacion de entregable de TodoList", "False");
insert into tarea (id, descripcion, completada) values (8, "Tarea 8 - Documentación de TodoList", "False");
insert into tarea (id, descripcion, completada) values (9, "Tarea 9 - Manual de usuario TodoList", "False");
insert into tarea (id, descripcion, completada) values (10, "Tarea 10 - Manual de sistemas TodoList", "False");
