import datetime

from pyrefinder import db


def test_add_fighter():
    DB = db.DatabaseManager()
    topic = "dt/fighter/bob"
    message = {"latitude": 100, "longitude": 100}

    db.add_fighter(topic, message)

    result = DB.query_db(
        "select id from fighter where id=? and latitude=? and longitude=?",
        ["bob", 100, 100])

    del DB

    assert result != None


def test_add_fighter_status_with_no_fighter():
    DB2 = db.DatabaseManager()
    topic = "dt/fighter/bobby"
    message = {"status": "FIRE", "latitude": 100, "longitude": 100}

    db.add_fighter_status(topic, message)

    fighter_result = DB2.query_db(
        "select id from fighter where id=? and latitude=? and longitude=?",
        ["bob", 100, 100])

    fighter_data_result = DB2.query_db(
        "select client_id from fighter_data where client_id=? and time=? and status=?",
        ["bobby", datetime.datetime.now(), "FIRE"])

    # For cleaning up
    DB2.modify_db("delete from fighter_data where client_id=?", ["bobby"])
    DB2.modify_db("delete from fighter where id=?", ["bobby"])

    del DB2

    assert fighter_result != None and fighter_data_result != None


def test_update_last_time_of_fighter():
    DB3 = db.DatabaseManager()
    now = datetime.datetime.now()

    topic = "dt/fighter/sam"
    message = {"status": "NOFIRE", "latitude": 100, "longitude": 100}

    db.add_fighter(topic, message)

    message = {"status": "FIRE", "latitude": 100, "longitude": 100}
    db.add_fighter_status(topic, message)

    fighter_time_result = DB3.query_db(
        "select last_time from fighter where id=? and last_time=?",
        ["sam", now])

    DB3.modify_db("delete from fighter_data where client_id=?", ["sam"])
    DB3.modify_db("delete from fighter where id=?", ["sam"])

    del DB3

    assert fighter_time_result != (now, )


def test_update_of_last_status():
    DB4 = db.DatabaseManager()
    now = datetime.datetime.now()

    topic = "dt/fighter/sam"
    message = {"status": "NOFIRE", "latitude": 100, "longitude": 100}

    db.add_fighter(topic, message)

    message = {"status": "FIRE", "latitude": 100, "longitude": 100}
    db.add_fighter_status(topic, message)

    fighter_status_result = DB4.query_db(
        "select last_fire_status from fighter where id=? and last_time=?",
        ["sam", now])

    DB4.modify_db("delete from fighter_data where client_id=?", ["sam"])
    DB4.modify_db("delete from fighter where id=?", ["sam"])

    del DB4

    assert fighter_status_result != ("FIRE", )


def test_update_image_path():
    topic = "dt/fighter/bob"
    message = {"status": "NOFIRE", "latitude": 100, "longitude": 100}

    db.add_fighter_status(topic, message)

    imagepath = "images/fire/bob_4173930.jpg"
    db.update_image_path(imagepath)

    DB5 = db.DatabaseManager()
    results = DB5.query_db("select last_image_path from fighter where id=?",
                           ["bob"])

    del DB5

    assert results == [(imagepath, )]
