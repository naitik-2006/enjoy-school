"""
Useful Functions---

1. get_user_classes() - Helps to get the information about the user classes. (suitable for : student)

2. get_more_info_classes() - Helps to get the additional information about the user classes. (suitable for : teacher)

3. create_new_class() - Helps to create new class... (using form post request) (suitable for : teacher)

4. add_joining_req() - Helps us to let send requests to teacher so that they can join the students in thier class. (suitable for : student)

5.approve_req() - Coming Soon. (suitable for : teacher)
"""

"""
Databases used -  

1. Db- classrooms

"""






from MySQLdb import _mysql , _exceptions
import string
from random import choice
import flash_errors as fe
import home_messages as hm


mysql_passwd = ''
db_user = "root"

def get_user_classes(user_email):

    """This function will return user classes as a list of dictionaries..
    
    In those dictionaries there are two key-value pairs one is class name and other is class id of that class for making reqests to enter that class...

    Example - 
    
    [{'class_name': "Naitik's History Class", 'classid': 'gipn3bcspn5wphm'},
    {'class_name': "Naitik's Maths Class", 'classid': 'mngfdhr54hjuyd6'}]"""

    try:

        db =_mysql.connect(db="classrooms",user = db_user , passwd = mysql_passwd )
    
        db.query(f"""SELECT  `classid` ,  `class_name`FROM joined_classes WHERE email = '{user_email}' """)
        cls_tp =  db.store_result().fetch_row(maxrows = 0)

        
        class_li = [{"class_name" : class_name.decode() , "classid" : classid.decode() } for classid , class_name in cls_tp ]

        if class_li:
            class_li.sort(key = lambda x : x["class_name"]) 
            return class_li
        return None

    except Exception:
        return "Problem In Contacting"

def get_more_info_classes(user_email):

    """ This is the imporved function of the get_user_classes()...
    This function will also return user classes as a list of dictionaries..
    
    In those dictionaries there are three key-value pairs. The two key-values are same as of the above function but the additional key-value pairs gives the information about the class standard...

    Example - 

    [{'class_name': "Naitik's History Class", 'classid': 'gipn3bcspn5wphm', 'class_standard':'10 B'} , {'class_name': "Naitik's Maths Class", 'classid': 'mngfdhr54hjuyd6' , 'class_standard : '11 D'}]
    
    """

    try:


        db = _mysql.connect(db="class_inf",user = db_user , passwd = mysql_passwd)
        
        class_li = get_user_classes(user_email)
        print(class_li)

        if class_li in (None , "Problem In Contacting"):
            return class_li

        class_mr_li = []

        for user_class in class_li:

            classid = user_class["classid"]

            db.query(f"""SELECT  `class_standard` FROM basic_information WHERE class_id = '{classid}' """)
            print("more info")
            class_standard =  db.store_result().fetch_row()[-1][-1].decode()
            print(class_standard)
            class_mr_li.append({"class_name" : user_class["class_name"] , "classid" : classid , "class_standard" : class_standard})

        return class_mr_li


    except Exception:
        return "Problem In Contacting"



def get_class_cards(user_email):

    """This function is helpful When we want to display classes cards on home screen...
    
    This Function returns list of dictionaries. Maily based on get_user_classes().
    
    
    Example - 
    
    [{'class_name': "Naitik's Hindi Class", 'classid': '03neblduab6u0fm', 'class_standard': '12 B', 'teacher': 'Naitik Agrawal'}, {'class_name': "Naitik's Hindi Class", 'classid': '5uzgiwo2uvbobk0', 'class_standard': '12 B', 'teacher': 'Naitik Agrawal'}]
    """

    try:

        db = _mysql.connect(db="class_inf",user = db_user , passwd = mysql_passwd)

        db2 = _mysql.connect(db="class_information",user = db_user , passwd = mysql_passwd)
        
        class_li = get_user_classes(user_email)

        if class_li in (None , "Problem In Contacting"):
            return class_li

        class_mr_li = []

        for user_class in class_li:

            classid = user_class["classid"]

            db.query(f"""SELECT  `class_name` , `class_standard` FROM basic_information WHERE `class_id` = '{classid}' """)
            result = db.store_result().fetch_row()[-1]

            db2.query(f"""SELECT `name` FROM `{classid}` WHERE `role` = 'Teacher'""")
            result2 = db2.store_result().fetch_row()[-1]

            class_name , te_name , class_standard =  result[0].decode() , result2[0].decode(), result[1].decode()

            class_mr_li.append({"class_name" : user_class["class_name"] , "classid" : classid , "class_standard" : class_standard , "teacher" : te_name})

        return class_mr_li


    except Exception:
        return "Problem In Contacting"


def get_participants(classid):

    """This function Will help us to get the name of the participants and their email...
    Returns a dict of two key-value pairs one teacher and other student...
    
    Example - 
    
    {'teacher': {'name' : "Naitik Agrawal' , 'email' = 'Naitikagrawal65789@gmail.com'}, 'students': [{'name' : "Naitik Agrawal' , 'email' : 'naitiktoobta@gmail.com'}, {'name' : "Lalit' , 'email' : 'lalit459@gmail.com'}]}
    
    """

    try:

        db3 = _mysql.connect(db="class_information",user = db_user , passwd = mysql_passwd)

        db3.query(f"""SELECT  `name` , `email` FROM {classid} WHERE `role`  = 'Teacher' """)
        result = db3.store_result().fetch_row()[-1]
        teacher_name , teacher_email =  result[0].decode() , result[1].decode()

        db3.query(f"""SELECT  `name` , `email` FROM {classid} WHERE `role`  = 'Student' """)
        students = []
        result = db3.store_result()

        while True:
            row = result.fetch_row()
            if row:
                students.append({ "name" : row[-1][0].decode() , "email" :row[-1][1].decode() })
            else:
                break
        
        students.sort(key = lambda x: x["name"])

        participants = {"teacher" : {"name" : teacher_name , "email" : teacher_email} , "students" : students} 
        return participants

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"

def get_participants_dict(classid):

    """
    This function s used to get the participants name and email in the format of dictionary rather than list...

    Format of dictionary - {"participant-email" : "participant-name"}
    """

    try:

        dbase = _mysql.connect(db="class_information",user = db_user , passwd = mysql_passwd)

        dbase.query(f"""SELECT  `name` , `email` FROM {classid} """)
        result = dbase.store_result()

        participants_dict = {}

        
        while True:
            row = result.fetch_row()
            if row:
                participants_dict[f"{row[-1][1].decode()}"]  = row[-1][0].decode()
            else:
                break


        return participants_dict

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"

def get_participants_email(classid):
    try:

        db3 = _mysql.connect(db="class_information",user = db_user , passwd = mysql_passwd)

        db3.query(f"""SELECT  `email` FROM {classid}""")
        result = db3.store_result().fetch_row(maxrows = 0)
        email_tp =  result
        email_li = [ email[-1].decode() for email in email_tp ]

        return email_li

    except Exception:
        return "Problem In Contacting"

def get_uni_cls_id():

    """
    This function will helps to get a new classid for creatinga new class. 
    
    This function will search in the joined_classes named table to find an existing classid.

    This will always return unique id for  the class acrroding to joined classes but not to the existing tables of same classid...

    """

    try:

        db =_mysql.connect(db="class_inf",user = db_user , passwd = mysql_passwd)

        classid =  ''.join(choice(string.ascii_lowercase  + string.digits) for x in range(15))
        while True:
            db.query(f"""SELECT  `class_name` FROM basic_information WHERE class_id = '{classid}' """)
            if not (db.store_result().fetch_row()):
                return classid
            classid =  ''.join(choice(string.ascii_lowercase + string.digits) for x in range(15))
    except Exception:
        return "Problem In Contacting"

def check_len_classes(user_email):

    """
    This function will help us to know that the person is eligible or not for joining any other class or creating a new class.

    Maxium class allowed = 20

    """

    classes = get_user_classes(user_email)
    if classes == "Problem In Contacting":
        return classes
    elif classes == None:
        return True
    else:
        return len(classes) < 20

def try_del_tables(classid):

    """
    This function will helps us to delete existing tables with a classid .. 
    
    As It was due to some server or intenet problem that the tables are created but the class is not registered in joined_classes table.
    
    So this function will help us to delete that tables...
    """

    try:
        dbase =_mysql.connect(db="class_chats",user = db_user , passwd = mysql_passwd)

        dbase2 =_mysql.connect(db="class_information",user = db_user , passwd = mysql_passwd)

        dbase3 =_mysql.connect(db="class_other",user = db_user , passwd = mysql_passwd)

        dbase4 = _mysql.connect(db="class_pd_req",user = db_user , passwd = mysql_passwd)

        dbase5 = _mysql.connect(db="class_inf",user = db_user , passwd = mysql_passwd)
         
        try: 
            dbase.query(f"""DROP TABLE `{classid}_chats`""")
        except Exception:
            pass

        try: 
            dbase2.query(f"""DROP TABLE `{classid}`""")
        except Exception:
            pass

        try: 
            dbase3.query(f"""DROP TABLE `{classid}_other`""")
        except Exception:
            pass

        try: 
            dbase4.query(f"""DROP TABLE `{classid}_pd_req`""")
        except Exception:
            pass

        try: 
            dbase5.query(f"""DELETE FROM `basic_information` WHERE `class_id` = '{classid}'""")
        except Exception:
            pass

        return None
        
    except Exception:
        return "Problem In Contacting"

def create_tables(dbase , dbase2 , dbase3 , dbase4 , classid , name , email , class_standard):
    
    """
    This function will create tables for the classes by using thier classid for chats , useful informations , meetings , assignments etc.. 

    This function will also add a row when a new class  will be created  class_information database table which will contain some useful information about the teacher..."""


    try:

        dbase.query(f"""CREATE TABLE `class_chats`.`{classid}_chats` ( `sno` INT(5) NOT NULL AUTO_INCREMENT ,  `user_email` VARCHAR(200) NOT NULL , `user_name` VARCHAR(200) NOT NULL , `send_msg` TEXT NOT NULL,  `msg` TEXT NOT NULL , `date-time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ,    PRIMARY KEY  (`sno`)) ENGINE = InnoDB;""")


        dbase.query(f"""INSERT INTO `{classid}_chats` (`sno`, `user_email`, `send_msg`, `msg` , `date-time`) VALUES (1 , 'None', 'None' '[]', 'None' , current_timestamp());""")
        dbase.commit()


        dbase2.query(f"""CREATE TABLE `class_information`.`{classid}` ( `email` VARCHAR(400) NOT NULL ,  `name` TEXT NOT NULL ,  `role` TEXT NOT NULL , `statics` TEXT NOT NULL ,    PRIMARY KEY  (`email`)) ENGINE = InnoDB;""")

        dbase2.query(f"""INSERT INTO `{classid}` (`email`, `name`, `role`, `statics`) VALUES ('{email}', '{name}', 'Teacher', '{"{}"}');""")

        dbase2.commit()
        
        dbase3.query(f"""CREATE TABLE `class_other`.`{classid}_other` ( `sno` INT(5) NOT NULL AUTO_INCREMENT , `type` VARCHAR(30) NOT NULL , `details` TEXT NOT NULL , `st_details` TEXT NOT NULL,  PRIMARY KEY (`sno`)) ENGINE = InnoDB;""")

        dbase3.query(f"""INSERT INTO `{classid}_other` (`sno`, `type`, `details`, `st_details`) VALUES (1 , 'None', 'None' , 'None');""")
        dbase3.commit()

        dbase4.query(f"""CREATE TABLE `class_pd_req`.`{classid}_pd_req` ( `email` VARCHAR(400) NOT NULL ,  `name` TEXT NOT NULL, PRIMARY KEY  (`email`)) ENGINE = InnoDB;""")
        
        dbase4.commit()

        return None

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"

def create_new_class(user_email , class_name , name , class_standard , description):
    
    """
    This is the main function which will do all the tasks to create  a new class.  We have to just call this...
    
    First of all this will check the number of classes created and then generate a unique classid. If there is any problem in connection to mysql then will return None by flashing the server_conatct_message error ...


    Then it will try to delete the tables if they exist of the same classid as they are created due to  connection problem because it is very rare that tables are created but not registered in the joined_classes tables.

    Return None if there is problem in connecting and flash the mnessage. It always try to delete tables seprately so we can identify the error type in try_del_tables() function...


    Then will create four tables... 
    1. classid_chats in class_chats (for storage of the chats)
    2. classid in class_information (for general information like can send message or not , class-standard) 
    3. classid_other in class_other (to store meetings assignments , etc...)
    4. classid_pd_req in class_pd_req (for class joining requests)

    At last it will append the entry to the joined classes...

    There is a main reason behind these algo as we will do all the tasks before adding entry to the joined_classes. 
    Because if consider there can be a server problem between the whole process. So if entry is added to joined classes but the four 
    tables are not constructed successfully then it will show that the teacher has created this class and he/she can also enter the class. 
    Then there will be problem. So by considering this probelm we have used this algo... 

    At last returns classid..

    Note: This function will return None or classid. So if it returns None then there is problem in server connection else the whole process is successfull...

    """


    no_classes = check_len_classes(user_email)
    classid = get_uni_cls_id()


    if not(no_classes):
        fe.not_create_moreclass()
        return None

    elif "Problem In Contacting" in (no_classes , classid):
        fe.server_contact_error()
        return None
  
    del_tables = try_del_tables(classid)

    if del_tables == "Problem In Contacting":
        fe.server_contact_error()
        return None

    try:

        dbase =_mysql.connect(db="classrooms",user = db_user , passwd = mysql_passwd)

        db =_mysql.connect(db="class_chats",user = db_user , passwd= mysql_passwd)

        db2 = _mysql.connect(db="class_information",user = db_user , passwd = mysql_passwd)

        db3 = _mysql.connect(db="class_other",user = db_user , passwd = mysql_passwd)

        db4 = _mysql.connect(db="class_pd_req",user = db_user , passwd = mysql_passwd)

        db5 = _mysql.connect(db="class_inf",user = db_user , passwd = mysql_passwd)

        cr_tab = create_tables(db , db2, db3 , db4 , classid , name , user_email , class_standard)

        if cr_tab == "Problem In Contacting":
            return None

        db5.query(f"""INSERT INTO `basic_information` (`class_id`, `class_name`, `teacher`, `class_standard` , `description`) VALUES ('{classid}', "{class_name}", '{user_email}', '{class_standard}' , '{description}');""")
        
        dbase.query(f"""INSERT INTO `joined_classes` (`role`, `classid`, `email`, `class_name`) VALUES  ('Teacher', '{classid}', '{user_email}', "{class_name}")""")
        
        dbase.commit()
        db5.commit()
        return classid

    except Exception:
        fe.server_contact_error()
        return None


def check_already_presence(classid , user_email):
     
    """
    [{'class_name': "Naitik's History Class", 'classid': 'gipn3bcspn5wphm'},
    {'class_name': "Naitik's Maths Class", 'classid': 'mngfdhr54hjuyd6'}]"""

    classes = get_user_classes(user_email)
    
    if classes == "Problem In Contacting":
        return classes
    elif classes == None:
        return False

    for st_class in classes:
        if st_class["classid"] == classid:
            return True
    return False



def add_joining_req(email , name ,  classid):

    no_class = check_len_classes(email)

    if not(no_class):
        fe.no_more_join()
        return "Max joined"

    if no_class == "Problem In Contacting":
        fe.server_contact_error()
        return no_class

    check_already_presence_res = check_already_presence(classid , email)

    if check_already_presence_res == "Problem In Contacting":
        fe.server_contact_error()
        return check_already_presence_res

    elif check_already_presence_res == True:
        fe.already_joined()
        return "Already Joined"

    try:
        dbase = _mysql.connect(db="class_pd_req",user = db_user , passwd = mysql_passwd)

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"
        
    try:
        dbase.query(f"""INSERT INTO `{classid}_pd_req` (`email`, `name`) VALUES ('{email}', '{name}');""")

    except _exceptions.ProgrammingError:
        fe.no_class_found()
        return "No class found"

    except _exceptions.IntegrityError:
        fe.already_req()
        return "Already Requested"

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"
        
    return None


def get_join_req(classid):

    """ This function will help us to get all the pending requests for joining the class...
    
    Returns a list of dicts...
    
    Example - 
    
    [{'email': 'agrawalNaitik13@gmail.com', 'name': 'Naitik Agrawal'} ,{'email': 'Naitik1789@gmail.com', 'name': 'Naitik'}]
    
    """

    try:
        dbase = _mysql.connect(db="class_pd_req",user = db_user , passwd = mysql_passwd)

        dbase.query(f"""SELECT * FROM `{classid}_pd_req`""")

        req_tp  =  dbase.store_result().fetch_row(maxrows = 0)

        req_li = [{"email" : email.decode() , "name" : name.decode()} for email, name in req_tp ]

        return req_li

    except Exception:
        return "Problem In Contacting"



def get_class_name(classid):

    """This function helps us to know the name of the The Class using classid...
    
    Returns None if Classid Is Wrong or connection to db is not successfull....
    """


    try:
        dbase =  _mysql.connect(db="class_inf",user = db_user , passwd = mysql_passwd)

        dbase.query(f"""SELECT  `class_name` FROM basic_information WHERE `class_id` = '{classid}' """)

        return dbase.store_result().fetch_row()[-1][-1].decode()
        
    except Exception:
        return None
        
def check_max_participants(classid):
    participants = get_participants_email(classid)
    if participants == "Problem In Contacting":
        return participants
    return len(participants) < 51


def approve_request(user_email , classid ):
    """
    Function adds Student To The class...
    
    First of all get the class name using classid and also check that classid is right or not...
    
    Making ConnectionsTo Dbases...
    After That Get Student Request For Joining In DB With Email. Proceed Only If The Request Is Present IN db..
    If Not then return "Request Not Found"
    
    Then Checks in joined_classes Table of classrooms Db about that the user is already joined the class or not...
    If Joined already then try to delete the request in class_pd_req db's table  and Returns "Already Joined"...


    Then adds the user to the tables. First class_information and then joined_classes...
    If Student Entry is present in Joined Classes Then we can consider , That all process to add entry to dbs for student is successfull...
    That's Why we have used joined classes above to check wheter student is already joined the class or not...

    Then Deleting The Request From the class_pd_req db's Table...
    And adding a message to the db...
    At last return None...

    """

    try:
 
        class_name = get_class_name(classid)
        if class_name == None:
            fe.server_contact_error()
            return "Problem In Contacting"

        dbase1 = _mysql.connect(db="class_information",user = db_user , passwd = mysql_passwd)
        dbase2 =  _mysql.connect(db="classrooms",user = db_user , passwd = mysql_passwd)
        dbase3 =  _mysql.connect(db="class_pd_req",user = db_user , passwd = mysql_passwd)

        dbase3.query(f"""SELECT  `name`  FROM `{classid}_pd_req` WHERE email = '{user_email}' """)
        student = dbase3.store_result().fetch_row()
        if not student:
            fe.some_went_wrong()
            return "Request Not Found"
        st_name  = student[-1][0].decode()

        no_class = check_len_classes(user_email)
        if not(no_class):
            fe.no_more_join_ft()
            
            try:
                dbase3.query(f"""DELETE FROM `{classid}_pd_req` WHERE `{classid}_pd_req`.`email` = '{user_email}'""")
                dbase3.commit()
            except Exception:
                pass

            # Add decline request to user notification

            return "Max joined"

        if no_class == "Problem In Contacting":
            fe.server_contact_error()
            return no_class

        max_participants = check_max_participants(classid)
        if max_participants == "Problem In Contacting":
            fe.server_contact_error()
            return max_participants

        elif not(max_participants):
            fe.max_participants()

            try:
                dbase3.query(f"""DELETE FROM `{classid}_pd_req` WHERE `{classid}_pd_req`.`email` = '{user_email}'""")
                dbase3.commit()
            except Exception:
                pass

            # Add decline request to user notification
            
            return "Max Participants"

        dbase2.query(f"""SELECT  `sno` FROM joined_classes WHERE email = '{user_email}' and classid = '{classid}'""")
        entry_al_present = dbase2.store_result().fetch_row()
        if entry_al_present:
            try:
                dbase3.query(f"""DELETE FROM `{classid}_pd_req` WHERE `{classid}_pd_req`.`email` = '{user_email}'""")
                dbase3.commit()
            except Exception:
                pass
            fe.already_joined_ft()
            return "Already Joined"

        dbase1.query(f"""INSERT INTO `{classid}` (`email`, `name`, `role`, `statics`) VALUES ('{user_email}', '{st_name}', 'Student', '{"{}"}');""")
        dbase1.commit()

        dbase2.query(f"""INSERT INTO `joined_classes` (`role`, `classid`, `email`, `class_name`) VALUES  ('Student', '{classid}', '{user_email}', "{class_name}")""")
        dbase2.commit()

        dbase3.query(f"""DELETE FROM `{classid}_pd_req` WHERE `{classid}_pd_req`.`email` = '{user_email}'""")
        dbase3.commit()

        # Add approve request to user notification

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"


def decline_request(classid , user_email):

    try:

        dbase =  _mysql.connect(db="class_pd_req",user = db_user , passwd = mysql_passwd)

        dbase.query(f"""DELETE FROM `{classid}_pd_req` WHERE `{classid}_pd_req`.`email` = '{user_email}'""")

        # hm.add_decline_req_message(user_email , class_name)

        return None

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"


def remove_student(classid , user_email , remover):
    try:
 

        dbase1 = _mysql.connect(db="class_information",user = db_user , passwd = mysql_passwd)
        dbase2 =  _mysql.connect(db="classrooms",user = db_user , passwd = mysql_passwd)

        dbase1.query(f"""DELETE FROM `{classid}` WHERE `{classid}`.`email` = '{user_email}'""")
        dbase1.commit()

        dbase2.query(f"""DELETE FROM `joined_classes` WHERE `joined_classes`.`email` = '{user_email}' AND `joined_classes`.`classid` = '{classid}'""")
        dbase2.commit()

        # Add notification here using remover

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"



def delete_class(classid):

    try:

        dbase =  _mysql.connect(db="classrooms",user = db_user , passwd = mysql_passwd)

        dbase.query(f"""SELECT  `email` FROM joined_classes WHERE classid = '{classid}' """)
        em_tp =  dbase.store_result().fetch_row(maxrows = 0)
        em_li = [ email[-1].decode() for email in em_tp]

        dbase.query(f"""DELETE FROM `joined_classes` WHERE `joined_classes`.`classid` = '{classid}'""")


        del_tables = try_del_tables(classid)

        # hm.add_class_del_message(class_name , em_li)
        
    except Exception:
        return "Problem In Contacting"



if __name__ == "__main__":

    # print(add_joining_req("agrawalNaitik13@gmail.com" , "Naitik" , "m9onafx70xtigwc"))
    
    # print(create_new_class("agrawalNaitik13@gmail.com" , "Naitik's Maths Class" , "Naitik Agrawal" , "6 A"))

    # print(get_more_info_classes("agrawalNaitik13@gmail.com"))
    
    # print( add_joining_req("agrawalNaitik12gmail.com" , "Naitik" , "fdjxfc9n9w8uo6c" , "Plz Add!" , "10 B "))

    # print(get_class_cards("agrawalNaitik13@gmail.com"))

    # print(get_participants("03neblduab6u0fm"))
    # print(get_participants_email("03neblduab6u0fm"))


    # print(get_join_req("oodc5ij3ufw74sp"))
    # print(approve_request("agrawalNaitik132gmail.com" , "fdjxfc9n9w8uo6c"))
    # print(get_class_name("fdjxfc9n9w8uo6c"))
    # print(approve_request("agrawalNaitik13542@gmail.com","oodc5ij3ufw74sp"))

    # print(decline_request("fdjxfc9n9w8uo6c" , "agrawalNaitik12gmail.com" ))

    # print(delete_class("oodc5ij3ufw74sp"))
    pass