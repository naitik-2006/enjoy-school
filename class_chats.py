"""
This is the module used for sending messages or reteriving them.

This module uses databse class_chats and stores the chats messages here.
class_chats Database columns -
1. sno - Used to store as a js cookie to indcate the presence of new messages..

2. User_email

3. msg

4.send_to - Tells whom should receive the message. Conatins a list of receipants' email...

5.date-time

Functions Useful -

1.get_class_chats() - Used to get the older messages...

2. add_message() - Adds the messages in the database along with deleting the older messages so that the msg would not exceed more than 200.

"""




from MySQLdb import _mysql
import user_classes as uc
import media_files as mf
import flash_errors as fe
from werkzeug.utils import secure_filename
import re

mysql_passwd = ''
mysql_user = "root"

def get_class_chats(classid):

    """
    This function will help us to get the older messages sent by the participants of the class so that no msg would lost, after the user exit the website and can read them when they come online...

    """


    try:
        dbase =_mysql.connect(db="class_chats", user = mysql_user , passwd = mysql_passwd)

        dbase.query(f"""SELECT `sno` , `user_email` , `user_name` , `msg` , `date-time` , `send_msg` FROM `{classid}_chats` """)

        chats_tp =  dbase.store_result().fetch_row(maxrows = 0)

        chats_li = [{"id" : sno.decode() , "participant_email" : user_email.decode() ,"participant_name" : user_name.decode()  , "message" : msg.decode() , "date-time" : date_time.decode() ,  "send-to" : send_to.decode()} for sno , user_email , user_name , msg , date_time , send_to in chats_tp ]

        return chats_li

    except Exception :
        return "Problem In Contacting"

def del_older_msg(classid , db):

    try:

        db.query(f"""SELECT  `sno` FROM `{classid}_chats`""")
        snos =  db.store_result().fetch_row(maxrows = 0)
        if len(snos) >= 200:

            db.query(f"""DELETE FROM `{classid}_chats` WHERE `{classid}_chats`.`sno` = '{snos[0][0].decode()}'""")

        return None
    
    except Exception:
        pass

def add_message(classid , participant_email , participant_name , data , msg_type , db , img_class , pdf_class , video_class , audio_class , doc_class):
    try:
        dbase =_mysql.connect(db="class_chats",user = mysql_user , passwd = mysql_passwd)

        del_older_msg(classid , dbase)

        current_participants = uc.get_participants_email(classid)
        if current_participants == "Problem In Contacting":
            fe.server_contact_error()
            return current_participants

        return_dict = {"user_email" : participant_email , "user_name" : participant_name}

        if msg_type == "msg_text" :

            message = data["message"]

            regex_to_match = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
            urls_finded = re.findall(regex_to_match , message)      
            urls = [x[0] for x in urls_finded]

            msg_inf = {"type" : msg_type , "msg" : message , "urls" : urls}
            msg_dict = str(msg_inf)
            return_dict.update(msg_inf)

            



        elif  msg_type == "media_file" :

            file = data["file"]
            filesize = int(file.size) / (1024 * 1024)
            file_content = data["message"]

            media_url , filetype = mf.upload_chat_file(file_content, secure_filename(file.name) , file.type , filesize , db , pdf_class , img_class, audio_class , video_class , doc_class) 

            if media_url in ("Problem In Contacting" , "fi"):
                return media_url

            filetype.replace("s" ,"")

            msg_inf = {"type" : filetype , "url" : media_url , "file_name" : secure_filename(file.filename) , "file_size" : filesize}
            msg_dict = str(msg_inf)
            return_dict.update(msg_inf)

        else :
            fe.some_went_wrong()
            return "swr"

        dbase.query(f"""INSERT INTO `{classid}_chats` (`user_email`, `user_name` ,`msg`, `send_msg` , `date-time`) VALUES ( '{participant_email}', '{participant_name}',"{msg_dict}", "{current_participants}" , current_timestamp())""")
        return return_dict

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"


if __name__ == "__main__":
    pass

