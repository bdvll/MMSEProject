drop table if exists employees;
create table employees (
  id integer primary key autoincrement,
  name text not null,
  pass text not null,
  position text not null
);
drop table if exists events;
create table events (
  id integer primary key autoincrement,
  event_name text not null,
  event_date text not null,
  client_name text not null,
  budget integer
);
drop table if exists tasks;
create table tasks (
  id integer primary key autoincrement,
  client_name text not null,
  task_date text not null,
  task_name text not null,
  budget integer not null
);
drop table if exists reports;
create table reports (
  id integer primary key autoincrement,
  creator text not null,
  content text not null
);
