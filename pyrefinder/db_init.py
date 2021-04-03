import sqlite3

# SQLite DB Name
DB_Name = "pyrefinder.db"

TableSchema = """
drop table if exists fighter ;
create table fighter (
  id text primary key,
  latitude decimal not null,
  longitude decimal not null,
  last_status text
);
drop table if exists fighter_data ;
create table fighter_data (
  client_id text,
  status text not null,
  time text not null,
  foreign key(client_id) references fighter(id)
);
"""

conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

curs.close()
conn.close()