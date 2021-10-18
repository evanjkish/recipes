from flask_app.config.mysqlconnection import connectToMySQL# model the class after the friend table from our database
from flask import flash
from flask_app import DATABASE

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.hash_pw = data['hash_pw']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users = []
    # Now we use class methods to query our database
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users ( first_name , last_name , email, hash_pw, created_at , updated_at ) \
        VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(hash_pw)s, NOW() , NOW() );"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(users) )
        return users

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return results
        return cls(results[0])

    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return results
        return cls(results[0])

    @classmethod
    def update_one(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, hash_pw=%(hash_pw)s"
    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM users WHERE id%(id)s"
        connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_login(data):
        is_valid = True

        if len(data['email']) < 1:
            is_valid = False
            flash('Email is required', 'error_login_email')

        if len(data['pw']) < 1:
            is_valid = False
            flash('Password is required', 'error_login_hash_pw')
        
        return is_valid

    @staticmethod
    def validate_registration(data):
        is_valid = True

        if len(data['first_name']) < 1:
            is_valid = False
            flash('First name is required', 'error_reg_first_name')

        if len(data['last_name']) < 1:
            is_valid = False
            flash('Last name is required', 'error_reg_last_name')

        if len(data['email']) < 1:
            is_valid = False
            flash('Email is required', 'error_login_email')

        if len(data['pw']) < 1:
            is_valid = False
            flash('Password is required', 'error_login_pw')
        elif data['pw'] != data['confirm_pw']:
            is_valid = False
            flash('Passwords do not match!', 'error_login_confirm_pw')

        return is_valid