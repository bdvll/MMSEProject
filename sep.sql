create table employees (
  id integer primary key autoincrement,
  name text not null,
  position text not null
);

create table events (
  id integer primary key autoincrement,
  event_name text not null,
  event_date text not null,
  client_name text not null,
  budget integer
);

create table tasks (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);

create table reports (
  id integer primary key autoincrement,
  creator text not null,
  content text not null
);