from flask import Flask
from Controllers.Controller_IA import prediction_blueprint
from Controllers.Controller_Database import signup_blueprint, login_blueprint, user_chat_history_blueprint, delete_chat_blueprint, chat_message_blueprint, get_chat_blueprint    
from Model.IA import IA

app = Flask(__name__)

ia = IA()

app.register_blueprint(prediction_blueprint)
app.register_blueprint(signup_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(user_chat_history_blueprint)
app.register_blueprint(delete_chat_blueprint)
app.register_blueprint(chat_message_blueprint)
app.register_blueprint(get_chat_blueprint)