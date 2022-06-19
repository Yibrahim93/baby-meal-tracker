from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Meal:
    db_name="meals_usersdb"
    def __init__(self,data):
        self.id = data["id"]
        self.meal=data["meal"]
        self.date=data["date"]
        self.time=data["time"]
        self.liked=data["liked"]
        self.description=data["description"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.user_id=data['user_id']
        self.user = None

    @classmethod
    def save(cls, data): 
        query = "INSERT INTO meals (meal, date, time, liked, description, user_id) VALUES (%(meal)s, %(date)s, %(time)s,  %(liked)s,  %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_meals(cls):
            query = "SELECT * FROM meals JOIN users on user_id = users.id;"
            results= connectToMySQL(cls.db_name).query_db(query)
            meals = []
            for row in results:
                meal = cls(row)
                user_data ={
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'relation': row['relation'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at':row['created_at'],
                    'updated_at': row['updated_at'],
                }
                meal.user = user.User(user_data)
                meals.append(meal)
            return meals

    @classmethod
    def get_onemeal(cls, data):
            query = "SELECT * FROM meals JOIN users ON meals.user_id = users.id WHERE meals.id = %(id)s;"
            results= connectToMySQL(cls.db_name).query_db(query, data)
            print (results)
            meals = []
            for row in results:
                meal = cls(results[0])
                print (results[0]['users.id'])
                user_data ={
                    'id': results[0]['users.id'],
                    'first_name': results[0]['first_name'],
                    'last_name': results[0]['last_name'],
                    'relation': results[0]['relation'],
                    'email': results[0]['email'],
                    'password': results[0]['password'],
                    'created_at':results[0]['created_at'],
                    'updated_at': results[0]['updated_at'],
                }
                meal.user = user.User(user_data)
            return meal

    @classmethod
    def edit_meal(cls, data):
        query = "UPDATE meals SET meal = %(meal)s, date = %(date)s, time = %(time)s,  liked = %(liked)s,  date = %(date)s,  description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def delete_meal(cls, id):
        data={
            'id':id
        }
        query = "DELETE FROM meals WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod #validations
    def validate_newmeal(form_data):
            is_valid = True
            print(form_data)
            if len (form_data ["meal"]) < 2:
                is_valid =False
                flash("MEAL MUST BE AT LEAST 3 CHARACTERS", "meal")
            if len (form_data ["date"]) < 2:
                is_valid =False
                flash("INVALID DATE", "meal")
            if len (form_data ["time"]) < 1:
                is_valid =False
                flash("INVALID TIME", "meal")
            if len (form_data ["liked"]) < 1:
                is_valid =False
                flash("LIKED FIELD REQUIRED!", "meal")
            if len (form_data ["description"]) < 1:
                is_valid =False
                flash("SHORT DESCRIPTION IS REQUIRED!", "meal")
            return is_valid
