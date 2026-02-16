from Model.Database import Database
from Exceptions.UserExistsException import UserExistsException
from Exceptions.UserOrPasswordIncorrectException import UserOrPasswordIncorrectException
import bcrypt

class Service_User:

    def __init__(self):
        pass

    ### Signup user
    def signup_user(self, username, password):
        db = Database()

        if db.user_exists(username):
            db.close()
            raise UserExistsException("User already exists")

        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            db.insert_user(username, str(hashed_password))
            db.close()
        except Exception as e:
            db.close()
            raise e
        
        return "Account created successfully"

    ### Login user
    def login_user(self, username, password):
        db = Database()
        user_info = db.select_user_by_name(username)
        
        if user_info is None:
            db.close()
            raise UserOrPasswordIncorrectException("User or Password incorrect.")

        try:
            hashed_password_from_db = user_info[2]

            if hashed_password_from_db.startswith("b'") and hashed_password_from_db.endswith("'"):
                hashed_password_from_db = hashed_password_from_db[2:-1].encode('utf-8')
            elif isinstance(hashed_password_from_db, str):
                hashed_password_from_db = hashed_password_from_db.encode('utf-8')

            password_match = bcrypt.checkpw(password.encode('utf-8'), hashed_password_from_db)

            db.close()
        except Exception as e:
            db.close()
            raise e
        
        if password_match == False:
            raise UserOrPasswordIncorrectException("User or Password incorrect.")
        
        return {
            'user_id': user_info[0],
            'user_name': user_info[1],
            'user_is_connected': True,
            'password_match': password_match
        }