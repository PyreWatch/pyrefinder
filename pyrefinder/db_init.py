import sqlite3

# SQLite DB Name
DB_Name = "pyrefinder.db"

TableSchema = """
drop table if exists fighter ;
create table fighter (
  id text primary key,
  latitude decimal not null,
  longitude decimal not null,
  last_fire_status text,
  last_time text,
  last_image_path text
);
drop table if exists fighter_data ;
create table fighter_data (
  client_id text,
  status text not null,
  time text not null,
  image_path text,
  foreign key(client_id) references fighter(id)
);
create trigger update_status after insert on fighter_data
begin
  update fighter set last_fire_status = new.status where fighter.id = new.client_id;
end;
create trigger update_time after insert on fighter_data
begin
  update fighter set last_time = new.time where fighter.id = new.client_id;
end;
"""

conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

curs.close()
conn.close()
