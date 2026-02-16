from Model.Database import Database
from Exceptions.UserNotConnectedException import UserNotConnectedException
from Services.Service_Chat_Message import Service_Chat_Message

class Service_Chat:
    def __init__(self):
        pass

    def get_chat(self, chat_id, user_id, is_connected):
        db = Database()

        if is_connected == False:
            raise UserNotConnectedException("User not connected")
        
        try:
            chat = db.select_chat_by_id_and_user_id(chat_id, user_id)
            db.close()
        except Exception as e:
            db.close()
            raise e
        
        print(chat)
        return chat
    
    def create_chat(self, user_id, chat_title, chat_file_content, is_connected, model):
        db = Database()

        if is_connected == False:
            raise UserNotConnectedException("User not connected")
        
        try:
            db.begin_transaction()
            chat_id = db.insert_chat(user_id, chat_title, chat_file_content, model)
            db.commit_transaction() 
        except Exception as e:
            db.rollback_transaction() 
        finally:
            db.close()
        
        return chat_id
    
    def update_chat_file_content(self, user_id, chat_id, chat_file_content, is_connected):
        db = Database()

        if is_connected == False:
            raise UserNotConnectedException("User not connected")
        
        try:
            old_content = db.select_chat_by_id(chat_id)

            if old_content[3] != chat_file_content:
                chat_file_content = old_content[3] + " " + chat_file_content
                db.update_chat_file_content_by_id(chat_id, chat_file_content)

            db.close()
        except Exception as e:
            db.close()
            raise e
    
    def delete_chat(self, chat_id, is_connected, user_id):
        db = Database()
        serviceChatMessage = Service_Chat_Message()

        if is_connected == False:
            raise UserNotConnectedException("User not connected")
        
        try:
            serviceChatMessage.delete_chat_message(chat_id, is_connected)
            db.delete_chat_by_id_and_by_user_id(chat_id, user_id)
            db.close()
        except Exception as e:
            db.close()
            raise e
        
    def get_all_user_chats(self, user_id, is_connected):
        datas={}

        db = Database()
    
        if is_connected == False:
            raise UserNotConnectedException("User not connected")

        try:
            chats = db.select_all_user_chats(user_id)

            for chat in chats:
                data = {
                    'chat_id': chat[0],
                    'chat_title': chat[1],
                    'chat_file_content': chat[2],
                    'chat_date': chat[3],
                    'chat_model': chat[4]
                }

                datas.update({chat[0]: data})

            db.close()
        except Exception as e:
            db.close()
            raise e
        
        return datas

