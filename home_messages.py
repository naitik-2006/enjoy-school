"""
Useful Functions ---

1. get_messages() - Helps us to get the messages ...
2. get_latest_message_sno() - Helps us to show the red mark on the home option by returning the latest message sno...

"""


# import pymysql
# pymysql.install_as_MySQLdb()
from MySQLdb import _mysql


def get_messages(user_email):

    """This function will helps us to get the messages form the messages table of classrooms db...
    
    
    Returns a dictionary in which the key is is sno of message according to table messages and the value is another dioctionary..
    
    In that dictionary there are three key-value pairs..
    1. message or subject
    2. type (or importance)
    3. sno of the message according to the table...
    
    """

    try:

        db =_mysql.connect(db="classrooms",user = "root" , passwd = 'mainhoondon')

        db.query(f"""SELECT  `sno` ,  `msg` , `type` FROM messages WHERE email = '{user_email}' """)
        msg_tp =  db.store_result().fetch_row(maxrows = 0)
        msg_dict = {sno.decode() : {"message":msg.decode(),'importance' : imp.decode(),'sno':sno.decode()} for sno , msg , imp in msg_tp }


        if msg_dict:
            return msg_dict
        return None

    except Exception:
        return "Problem In Contacting"


def get_latest_message_sno(user_email):

    """This function will return the latest message sno . So we will store it in the js cookies and then after an interval will check the sno in b oth the places- js cokkies and the return value of this function..
    
    
    According to this we will create a red highlightion mark  on the home option for the user in vertical navbar to indicate the new message..
    
    Examples of this function...
    
    12
    523
    500"""

    try:
        db =_mysql.connect(db="classrooms",user = "root" , passwd = 'mainhoondon')

        db.query(f"""SELECT  `sno` FROM messages WHERE email = '{user_email}' ORDER BY sno DESC LIMIT 1 """)

        msg_sno =  db.store_result().fetch_row(maxrows = 0)[-1][-1].decode()

        return msg_sno

    except Exception:
        return "Problem In Contacting"



def del_prev_msg(user_email , db):
    db.query(f"""SELECT  `sno` FROM messages WHERE email = '{user_email}' """)
    snos =  db.store_result().fetch_row(maxrows = 0)
    if len(snos) >= 20:

        db.query(f"""DELETE FROM `messages` WHERE `messages`.`sno` = '{snos[0][0].decode()}'""")

    return


def add_approve_req_message(user_email , class_name):
    try:

        db =_mysql.connect(db="classrooms",user = "root" , passwd = 'mainhoondon')
        del_prev_msg(user_email , db)

        db.query(f"""INSERT INTO `messages` (`email`, `msg`, `type`) VALUES ('{user_email}', "Your request for joining {class_name} has been approved.", 'Request Approved')""")

    except Exception:
        return "Problem In Contacting"


def add_decline_req_message(user_email , class_name):
    try:

        db =_mysql.connect(db="classrooms",user = "root" , passwd = 'mainhoondon')
        del_prev_msg(user_email , db)

        db.query(f"""INSERT INTO `messages` (`email`, `msg`, `type`) VALUES ('{user_email}', "Your request for joining {class_name} has been declined.", 'Request Declined')""")

    except Exception:
        return "Problem In Contacting"


def add_rmovd_frm_cls_message(user_email , class_name):
    try:

        db =_mysql.connect(db="classrooms",user = "root" , passwd = 'mainhoondon')
        del_prev_msg(user_email , db)

        db.query(f"""INSERT INTO `messages` (`email`, `msg`, `type`) VALUES ('{user_email}', "Your have been removed from {class_name}.", 'Removed frm Cls')""")

    except Exception:
        return "Problem In Contacting"

def add_lvd_frm_cls_message(user_email , class_name):
    try:

        db =_mysql.connect(db="classrooms",user = "root" , passwd = 'mainhoondon')
        del_prev_msg(user_email , db)

        db.query(f"""INSERT INTO `messages` (`email`, `msg`, `type`) VALUES ('{user_email}', "Your have Leaved {class_name}.", 'Lvd Cls')""")
    except Exception:
        return "Problem In Contacting"

def add_class_del_message(class_name , user_emails):
    try:

        db =_mysql.connect(db="classrooms",user = "root" , passwd = 'mainhoondon')

        for user_email in user_emails:

            del_prev_msg(user_email , db)
            db.query(f"""INSERT INTO `messages` (`email`, `msg`, `type`) VALUES ('{user_email}', "{class_name} has been deleted.", 'Class Del')""")

    except Exception:
        return "Problem In Contacting"
        

if __name__ == "__main__":
    

    pass
