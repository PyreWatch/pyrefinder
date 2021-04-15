import json
import logging
import sqlite3
from datetime import datetime

from . import utils

DB_Name = "pyrefinder.db"


class DatabaseManager():
    """ Database manager class that manages an instance of the connection to the database
    """
    def __init__(self):
        """Connects to sqlite database and makes sure foreign keys are enabled"""
        self.conn = sqlite3.connect(DB_Name)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def modify_db(self, sql_query, args=()):
        """Run the given SQL query, with the provided args

        Args:
            sql_query (str): the SQL query string 
            args (tuple, optional): value arguments to add into the query. Defaults to ().
        """
        self.cur.execute(sql_query, args)
        self.conn.commit()

    def query_db(self, sql_query, args=()):
        """Query databse with the given query and args

        Args:
            sql_query (str): the SQL query string 
            args (tuple, optional): value arguments to add into the query. Defaults to ().

        Returns:
            [dict of tuples]: dictionary of tuples representing each row of the result 
        """
        self.cur.execute(sql_query, args)
        return self.cur.fetchall()

    def __del__(self):
        """Closes cursor and connection objects to database"""
        self.cur.close()
        self.conn.close()


def add_fighter(topic, jsondict):
    """Add a fighter to fighter table to keep track of fighters

    Args:
        topic (str): the topic the message was sent from
        jsondict (json): the payload in dictionary form from the json fighter status

    Returns:
        [bool]: status of the insertion; true if inserted, exception printed and false if failed
    """
    client = utils.client_from_topic(topic)
    lat = jsondict['latitude']
    lng = jsondict['longitude']

    try:
        db = DatabaseManager()
        db.modify_db(
            "insert into fighter (id, latitude, longitude) values (?,?,?)",
            [client, lat, lng])
        del db
        logging.debug(
            f"Inserted new fighter: {client}, {lat}, {lng} into the fighter table"
        )
        return True
    except Exception as e:
        logging.error("Exception produced while adding fighter: %d", e)
        return False


def add_fighter_status(topic, jsondict):
    """Add a status data point to the fighter data log table

    Args:
        topic (str): top of the message sent
        jsondata (dict): the payload in dictionary form from the json fighter status

    Returns:
        [bool]: inserts status point into database, and adds fighter if not in fighter table
            Note: will retrun a true or false status and log the exception
    """
    client = utils.client_from_topic(topic)
    status = jsondict['status']
    now = datetime.now()

    try:
        db = DatabaseManager()
        fighters = db.query_db("select id from fighter where id=?", [client])

        if fighters == []:
            add_fighter(topic, jsondict)

        db.modify_db(
            "insert into fighter_data (client_id, time, status) values (?,?,?)",
            [client, now, status])
        logging.debug(
            f"Inserted new status: {client}, {now}, {status} into the fighter data table"
        )

        del db
        return True
    except Exception as e:
        logging.error("Exception produced while adding fighter: %d", e)
        return False


def update_image_path(path):
    """Updates the image path for a fighter given the image filepath

    Args:
        filename (str): the filename of the image, i.e images/fire/name_time.jpg

    Returns:
        [bool]: returns whether or not the update was without error
        Note: if fighter is not in database, this fails silently atm
    """
    path_splits = path.split("/")

    filename = path_splits[2]

    filename_splits = filename.split("_")

    client_id = filename_splits[0]

    logging.debug(client_id)

    try:
        db = DatabaseManager()
        db.modify_db(
            "update fighter set last_image_path = ? where fighter.id = ?",
            [path, client_id])
        logging.debug(f"Updated {client_id}'s last image file path to {path}")
        del db
        return True
    except Exception as e:
        logging.error(
            "Exception produced while updating last image file path: %d", e)
        return False