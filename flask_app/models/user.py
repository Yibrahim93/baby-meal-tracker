from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.config.mysqlconnection import connectToMySQL
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash, request


class User:
    db_name="meals_usersdb"
    def __init__(self,data):
        self.id = data["id"]
        self.first_name=data["first_name"]
        self.last_name=data["last_name"]
        self.email=data["email"]
        self.relation=data["relation"]
        self.password=data["password"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.meal = []


    @classmethod
    def register(cls,data):
        query = "INSERT INTO users (first_name, last_name, relation, email, password) VALUES (%(first_name)s, %(last_name)s, %(relation)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def grab_userid(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results= connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])

    @classmethod
    def grab_useremail(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results= connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])
    @staticmethod #validations
    def validate_newuser(form_data):
        is_valid = True

        if len (form_data["first_name"]) < 2:
            is_valid =False
            flash("FIRST NAME MUST BE AT LEAST 2 CHARACTERS", "register")
        if len (form_data ["last_name"]) < 2:
            is_valid =False
            flash("LAST NAME MUST BE AT LEAST 2 CHARACTERS", "register")
        if len (form_data ["relation"]) < 2:
            is_valid =False
            flash("RELATION TO BABY IS REQUIRED!!", "register")
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("ENTER A VALID EMAIL", "register")
            is_valid = False
        if len (form_data["password"]) < 5:
            is_valid =False
            flash("PASSWORD MUST BE AT LEAST 5 CHARACTERS", "register")
        if not form_data ["password"] == form_data["confirm_password"]:
            is_valid = False
            flash("PASSWORD DOES NOT MATCH", "register")
        return is_valid

    @staticmethod
    def validate_login(form_data):
        is_valid = True
        email_data = {
        "email": form_data["email"]
        }
        found_user = User.grab_useremail(email_data)
        if not found_user:
            flash("INVALID LOGIN CREDENTIALS", "login")
            return False
        if not bcrypt.check_password_hash(found_user.password, form_data['password']):
            flash ("INVALID LOGIN CREDENTIALS", "login")
            is_valid = False
        return is_valid