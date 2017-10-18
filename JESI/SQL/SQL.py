from pathlib import Path
import json
import logging
import os
import shutil
import sqlite3
import time

from ..EVE import Item

class SQL:
    c = None
    conn = None
    log = logging.getLogger('JESI').getChild(__name__)


    def __init__(self):
        dbFile = Path('local_cache.db')
        if not dbFile.is_file():
            self.initalize()
        if self.conn is None:
            self.log.info("Attempt to connect to SQL local db")
            self.conn = sqlite3.connect('local_cache.db')
            self.conn.row_factory = self.dict_factory
            self.c = self.conn.cursor()
            self.c.arraysize = 300
            self.log.info("Connected")


    def commit(self):
        self.conn.commit()


    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


    def initalize(self):
        # Init the connection

        self.conn = sqlite3.connect('local_cache.db')
        self.conn.row_factory = self.dict_factory
        self.c = self.conn.cursor()

        # Add tables as needed
        self.log.info("Create config table")
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS config
            (
                key text UNIQUE NOT NULL,
                value TEXT NOT NULL
            )
            """)

        self.log.info("Create regions table")
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS regions
            (
                region_id INTEGER UNIQUE NOT NULL,
                name TEXT UNIQUE,
                constellations TEXT,
                description TEXT
            )
            """)

        self.log.info("Create items table")
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS items
            (
                type_id INTEGER UNIQUE ON CONFLICT FAIL NOT NULL,
                name TEXT,
                capacity REAL,
                description TEXT,
                dogma_attributes TEXT,
                dogma_effects TEXT,
                group_id INTEGER,
                graphic_id INTEGER,
                icon_id INTEGER,
                market_group_id INTEGER,
                mass REAL,
                packaged_volume REAL,
                portion_size INTEGER,
                published BOOLEAN,
                radius REAL,
                volume REAL
            )
            """)
        self.c.execute("""
            CREATE INDEX IF NOT EXISTS itemsIname
            ON items(name)
            """)
        self.c.execute("""
            CREATE INDEX IF NOT EXISTS itemsItypeid
            ON items(type_id)
            """)

        self.log.info("Create prices table")
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS  prices
            (
                type_id INTEGER UNIQUE NOT NULL,
                adjusted_price REAL,
                average_price REAL,
                recorded REAL
            )
            """)

        # TODO: I'm pretty sure this doesn't exist....
        # self.log.info("Create regionPrices table")
        # self.c.execute("""
        #     CREATE TABLE IF NOT EXISTS  regionPrices
        #     (
        #         type_id INTEGER NOT NULL,
        #         region_id INTEGER NOT NULL,
        #         adjusted_price REAL,
        #         average_price REAL,
        #         recorded REAL

        #     )
        #     """)

        self.log.info("Create orders table")
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS  orders
            (
                order_id INTEGER UNIQUE NOT NULL,
                duration INTEGER,
                is_buy_order BOOLEAN,
                issued REAL,
                location_id INTEGER,
                min_volume INTEGER,
                price REAL,
                range TEXT,
                recorded REAL,
                region_id INTEGER NOT NULL,
                type_id INTEGER,
                volume_remain INTEGER,
                volume_total INTEGER
            )
            """)
        self.c.execute("""
            CREATE INDEX IF NOT EXISTS ordersItypeid
            ON orders(type_id)
            """)
        self.c.execute("""
            CREATE INDEX IF NOT EXISTS ordersIregionid
            ON orders(region_id)
            """)
        self.c.execute("""
            CREATE INDEX IF NOT EXISTS ordersIcombo
            ON orders(type_id,region_id)
            """)

        self.log.info("Create histories table")
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS  histories
            (
                type_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                highest REAL,
                lowest REAL,
                order_count INTEGER,
                volume INTEGER
            )
            """)
        self.conn.commit()


    ##################
    ## Item methods ##
    ##################
    def _item_make_good(self, item):
        """Take wide range of valid inputs, turn into an Item
        """
        # TODO Finish this!
        if isinstance(item,int):
            return Item.Item(type_id=item)
        elif isinstance(item,str):
            self.c.execute("SELECT * FROM items WHERE name=?",(item,))
        elif isinstance(item,str):
            self.c.execute("SELECT * FROM items WHERE name=?",(item,))
        elif isinstance(item,Item.Item):
            if item.type_id is not None:
                self.c.execute("SELECT * FROM items WHERE type_id=?",(item.type_id,))
            elif item.name is not None:
                self.c.execute("SELECT * FROM items WHERE name=?",(item.name,))
            else:
                ValueError(f"Item {item} didn't have a type_or or name")
        elif isinstance(item,dict):
            if 'type_id' in item and item['type_id'] is not None:
                self.c.execute("SELECT * FROM items WHERE type_id=?",(item['type_id'],))
            if 'name' in item and item['name'] is not None:
                self.c.execute("SELECT * FROM items WHERE name=?",(item['name'],))
            else:
                ValueError(f"dict {item} didn't have a type_or or name")
        else:
            raise TypeError(f"Item {item} is of type {type(item)}, not {Item.Item}")

    def clean_items(self):
        """Drop items from the items table

        Keyword Arguments:
        filter -- If given, function to return true on rows that are valid
        """
        self.c.execute("DELETE FROM items")

    def get_item(self, item):
        """Try to get item from db

        Keyword Arguments:
        item -- Accepts several types, and will check the db accordingly
            dict() -- Assumed to be a dict that has a type_id or name key
            int() -- Assumed to be a type_id
            Item() -- Assume to be an Item class, will check item.id then item.name
            str() -- Assume to be the full name

        Returns:
        Item()

        Raises:
        KeyError - Given item was not in the DB
        TypeError - Given argument isn't a valid type
        ValueError - Given item is not in the db
        """
        if isinstance(item,int):
            self.c.execute("SELECT * FROM items WHERE type_id=?",(item,))
        elif isinstance(item,str):
            self.c.execute("SELECT * FROM items WHERE name=?",(item,))
        elif isinstance(item,str):
            self.c.execute("SELECT * FROM items WHERE name=?",(item,))
        elif isinstance(item,Item.Item):
            if item.type_id is not None:
                self.c.execute("SELECT * FROM items WHERE type_id=?",(item.type_id,))
            elif item.name is not None:
                self.c.execute("SELECT * FROM items WHERE name=?",(item.name,))
            else:
                ValueError(f"Item {item} didn't have a type_or or name")
        elif isinstance(item,dict):
            if 'type_id' in item and item['type_id'] is not None:
                self.c.execute("SELECT * FROM items WHERE type_id=?",(item['type_id'],))
            if 'name' in item and item['name'] is not None:
                self.c.execute("SELECT * FROM items WHERE name=?",(item['name'],))
            else:
                ValueError(f"dict {item} didn't have a type_or or name")
        else:
            raise TypeError(f"Item {item} is of type {type(item)}, not {Item.Item}")

        data = self.c.fetchall()
        if len(data) == 0:
            raise ValueError
        return data[0]

    def get_items(self, filter=None):
        """Check if given item is in the db

        Keyword Arguments:
        filter -- If given, function to return true on rows that are valid

        Returns:
        [Item()...] 

        Raises:
        TypeError - Filter was given, but is not a valid function
        ValueError - Given item didn't have an id or name
        """
        self.c.execute("SELECT * FROM items")
        data = self.c.fetchall()
        return data

    def has_item(self, item):
        """Check if given item is in the db

        Keyword Arguments:
        item -- Accepts several types, and will check the db accordingly
            dict() -- Assumed to be a dict that has a type_id or name key
            int() -- Assumed to be a type_id
            Item() -- Assumed to be an Item class, will check item.id then item.name
            str() -- Assumed to be the full name

        Returns:
        bool() -- True/False if item is in the db

        Raises:
        TypeError - Given argument isn't a valid type
        ValueError - Given item didn't have an id or name
        """
        if isinstance(item,int):
            self.c.execute("SELECT * FROM items WHERE type_id=?",(item,))
        elif isinstance(item,str):
            self.c.execute("SELECT * FROM items WHERE name=?",(item,))
        elif isinstance(item,str):
            self.c.execute("SELECT * FROM items WHERE name=?",(item,))
        elif isinstance(item,Item.Item):
            if item.type_id is not None:
                self.c.execute("SELECT * FROM items WHERE type_id=?",(item.type_id,))
            elif item.name is not None:
                self.c.execute("SELECT * FROM items WHERE name=?",(item.name,))
            else:
                ValueError(f"Item {item} didn't have a type_or or name")
        elif isinstance(item,dict):
            if 'type_id' in item and item['type_id'] is not None:
                self.c.execute("SELECT * FROM items WHERE type_id=?",(item['type_id'],))
            if 'name' in item and item['name'] is not None:
                self.c.execute("SELECT * FROM items WHERE name=?",(item['name'],))
            else:
                ValueError(f"dict {item} didn't have a type_or or name")
        else:
            raise TypeError(f"Item {item} is of type {type(item)}, not {Item.Item}")

        data = self.c.fetchall()
        if len(data) == 0:
            return False
        return True

    def insert_item(self, item):
        """Check if given item is in the db

        Keyword Arguments:
        item -- Accepts several types, and will check the db accordingly
            dict() -- Valid dict with at least a type_id
            Item() -- Assume to be an Item class, will check item.id then item.name

        Returns:
        None

        Raises:
        TypeError - Given argument isn't a valid type
        ValueError - Given item didn't have an id or name
        """        
        self.log.debug(f"Inserting {item}")

        if isinstance(item,Item.Item):
            item = item.dict()
        elif not isinstance(item,dict):
            raise TypeError

        self.log.debug(f"Inserting {item['name']}")
        if 'dogma_attributes' in item:
            item['dogma_attributes'] = json.dumps(item['dogma_attributes'])
        if 'dogma_effects' in item:
            item['dogma_effects'] = json.dumps(item['dogma_effects'])

        keys = ",".join([x for x in item])
        values = [item[x] for x in item]
        questionMarks = ",".join( list( "?" * len(item) ) )
        sqlCmd = f"""
            INSERT OR FAIL INTO items 
            ({keys})
            VALUES 
            ({questionMarks})
        """
        # self.log.debug(sqlCmd)
        try:
            self.c.execute(sqlCmd, values)
        except sqlite3.IntegrityError:
            self.log.error(f"Failed to insert {item}")
            self.log.error("Continuing")

