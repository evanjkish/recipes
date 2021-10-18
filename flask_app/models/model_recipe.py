from flask_app.config.mysqlconnection import connectToMySQL# model the class after the friend table from our database
from flask import flash
from flask_app import DATABASE
class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.under_thirty = data['under_thirty']
        self.instruction = data['instruction']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    # Now we use class methods to query our database
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes ( name , description , under_thirty, instruction, date_made, created_at , updated_at, user_id ) \
        VALUES ( %(name)s , %(description)s , %(under_thirty)s , %(instruction)s, %(date_made)s , NOW() , NOW(), %(user_id)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of friends
        all_recipes = []
        # Iterate over the db results and create instances of friends with cls.
        for row in results:
            print(row['date_made'])
            all_recipes.append(cls(row))
        return all_recipes

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results[0])

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    # @classmethod
    # def get_one_by_email(cls, data):
    #     query = "SELECT * FROM recipes WHERE email = %(email)s;"
    #     results = connectToMySQL(DATABASE).query_db(query, data)
    #     if not results:
    #         return results
    #     return cls(results[0])

    @classmethod
    def update_one(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, under_thirty=%(under_thirty)s, instruction=%(instruction)s"
        return connectToMySQL(DATABASE).query_db(query, data)
    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM recipes WHERE id%(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True

        if len(recipe['name']) < 3:
            is_valid = False
            flash('Name is required to be at least 3 characters', 'recipe')

        if len(recipe['description']) < 3:
            is_valid = False
            flash('Description is required to be at least 3 characters', 'recipe')
        
        if len(recipe['instruction']) < 3:
            is_valid = False
            flash('Instructions are required to be at least 3 characters', 'recipe')

        if recipe['date_made'] == "":
            is_valid=False
            flash('Please enter a date', 'recipe')
        return is_valid
