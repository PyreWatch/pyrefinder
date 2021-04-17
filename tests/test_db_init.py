import sqlite3
import os


def test_creation_of_db():
    """ Makes sure that database is created
    """
    os.system('python -m pyrefinder.db_init')
    assert os.path.isfile("pyrefinder.db")


def test_tables_are_present():
    """ Asserts that two tables are created: fighter and fighter_data
    """
    conn = sqlite3.connect("pyrefinder.db")
    cur = conn.cursor()

    cur.execute("select name from sqlite_master where type='table';")

    tables = [v[0] for v in cur.fetchall() if v[0] != "sqlite_sequence"]

    assert tables == ["fighter", "fighter_data"]


def test_triggers_are_present():
    """ Asserts that two triggers are created: update_status and update_time
    """
    conn = sqlite3.connect("pyrefinder.db")
    cur = conn.cursor()

    cur.execute("select name from sqlite_master where type='trigger';")

    triggers = [v[0] for v in cur.fetchall() if v[0] != "sqlite_sequence"]

    assert triggers == ["update_status", "update_time"]