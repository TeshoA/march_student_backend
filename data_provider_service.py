import pymysql
from passlib.hash import sha256_crypt
import configparser


class DataProviderService:
    def __init__(self):
        """
        :creates: a new instance of connection and cursor
        reads the connection info from a config file
        """
        config = configparser.ConfigParser()
        config.read('db.ini')
                
        host = config['mysql']['host']
        port = 3306
        user = config['mysql']['user']
        password = config['mysql']['passwd']
        database = config['mysql']['db']
        
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, db=database)
        self.cursor = self.conn.cursor()

    # Insert new post
    def add_post(self, title, content, author_id=1):
        # defaults to author 1: guest
        sql_insert_post = """insert into post (title, content, author_id) values (%s, %s, %s)"""

        input_values = (title, content, int(author_id))

        try:
            self.cursor.execute(sql_insert_post, input_values)
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            print("Attempt to insert a new post: transaction was rolled back", exc)

        sql_new_post_id = "select LAST_INSERT_ID()"
        self.cursor.execute(sql_new_post_id)
        new_post_id = self.cursor.fetchone()
        return new_post_id

    # Get a single post by ID or all posts
    def get_post(self, post_id=None):
        all_posts = []

        if post_id is None:
            sql_all_posts = "SELECT * FROM post order by created desc"
            self.cursor.execute(sql_all_posts)
            all_posts = self.cursor.fetchall()
        else:
            sql_post_by_id = """Select * from post where id = %s"""

            input_values = (post_id,)
            self.cursor.execute(sql_post_by_id, input_values)
            all_posts = self.cursor.fetchone()

        return all_posts

    # Get a single post by ID or all posts, include author/user details
    def get_post_with_author(self, post_id=None):
        post_detail = []

        if post_id is None:
            sql_all_posts = "SELECT p.id, author_id, created, title, content, u.username FROM post as p inner join user_table as u on p.author_id = u.id  order by created desc"
            self.cursor.execute(sql_all_posts)
            post_detail = self.cursor.fetchall()
        else:
            sql_single_post_by_id = """SELECT p.id, author_id, created, title, content, u.username FROM post as p inner join user_table as u on p.author_id = u.id where p.id = %s order by created desc"""
            input_values = (post_id,)
            self.cursor.execute(sql_single_post_by_id, input_values)
            post_detail = self.cursor.fetchone()

        return post_detail

    # Update a post
    def update_post(self, post_id, new_post):
        updated_post = None
        current_post = DataProviderService().get_post(post_id=post_id)

        if current_post:
            sql_update_post = """update post set title = %s, content = %s where id = %s"""

            input_values = (new_post['title'], new_post['content'], post_id)

            try:
                self.cursor.execute(sql_update_post, input_values)
                self.conn.commit()
                updated_post = self.get_post(post_id)
            except pymysql.Error as exc:
                self.conn.rollback()
                print(exc)

        return updated_post

    # Confirm user can log in, compare hashed passwords
    def is_user_valid(self, username, passwd):
        sql = """select id, username, password from user_table where username = %s"""

        input_values = (username,)
        logged_in_user = None
        try:
            self.cursor.execute(sql, input_values)
            logged_in_user = self.cursor.fetchone()
        except pymysql.Error as exc:
            print(exc)

        same_password = sha256_crypt.verify(passwd, logged_in_user[2])
        if same_password:
            return logged_in_user
        else:
            return None

    # Confirm user exists in user table
    def is_logged_in_user_valid(self, user_id, username):
        sql_get_user = """select id, username from user_table where id = %s and username = %s"""

        input_values = (user_id, username)
        valid_user = None
        try:
            self.cursor.execute(sql_get_user, input_values)
            valid_user = self.cursor.fetchone()
        except Exception as exc:
            print(exc)

        return valid_user

    # Insert / register new user
    def add_user(self, username, passwd):
        sql_insert_user = """insert into user_table (username, password) values (%s, %s)"""

        hashed_passwd = sha256_crypt.hash(passwd)
        input_values = (username, hashed_passwd)

        try:
            self.cursor.execute(sql_insert_user, input_values)
            self.conn.commit()
        except pymysql.Error as exc:
            self.conn.rollback()

        sql_new_user_id = "select LAST_INSERT_ID()"
        self.cursor.execute(sql_new_user_id)
        new_user = self.cursor.fetchone()
        return new_user


