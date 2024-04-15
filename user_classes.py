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






import string
from random import choice
import flash_errors as fe
import home_messages as hm
import mysql.connector

mysql_passwd = ''
db_user = "root"

def get_user_classes(user_email):

    """This function will return user classes as a list of dictionaries..
    
    In those dictionaries there are two key-value pairs one is class name and other is class id of that class for making reqests to enter that class...

    Example - 
    
    [{'class_name': "Naitik's History Class", 'classid': 'gipn3bcspn5wphm'},
    {'class_name': "Naitik's Maths Class", 'classid': 'mngfdhr54hjuyd6'}]"""

    try:

        db = mysql.connector.connect(host="localhost",user=db_user,password="",database="classrooms")
        mycursor = db.cursor()
        query = f"""SELECT  `classid` ,  `class_name`FROM joined_classes WHERE email = '{user_email}' """
        mycursor.execute(query)
        cls_tp = mycursor.fetchall()
        class_li = [{"class_name" : class_name , "classid" : classid } for classid , class_name in cls_tp ]
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

        db = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_inf")
        mycursor = db.cursor()
        
        class_li = get_user_classes(user_email)
        print(class_li)

        if class_li in (None , "Problem In Contacting"):
            return class_li

        class_mr_li = []

        for user_class in class_li:

            classid = user_class["classid"]

            query = f"""SELECT  `class_standard` FROM basic_information WHERE class_id = '{classid}' """
            print("more info")
            # class_standard =  db.store_result().fetch_row()[-1][-1] 
            mycursor.execute(query)
            cls_tp = mycursor.fetchall()
            print(cls_tp)
            class_standard = cls_tp[-1] 
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
    print("class card function called")
    

    try:
        db2 = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_information")
        db = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_inf")

        mycursor2 = db2.cursor()
        mycursor = db.cursor()
        class_li = get_user_classes(user_email)

        if class_li in (None , "Problem In Contacting"):
            return class_li

        class_mr_li = []

        for user_class in class_li:

            classid = user_class["classid"]

            query = f"""SELECT  `class_name` , `class_standard` FROM basic_information WHERE `class_id` = '{classid}' """
            mycursor.execute(query)
            result = mycursor.fetchall()
            result = result[-1]

            query = f"""SELECT `name` FROM `{classid}` WHERE `role` = 'Teacher'"""
            mycursor2.execute(query)
            result2 = mycursor2.fetchall()
            result2 = result2[-1]

            class_name , te_name , class_standard =  result[0]  , result2[0] , result[1] 

            class_mr_li.append({"class_name" : user_class["class_name"] , "classid" : classid , "class_standard" : class_standard , "teacher" : te_name})
        print(class_mr_li)

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
        dbase = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_information")

        mycursor = dbase.cursor()

        query = (f"""SELECT  `name` , `email` FROM {classid} WHERE `role`  = 'Teacher' """)
        mycursor.execute(query)
        result = mycursor.fetchall()[-1]
        teacher_name , teacher_email =  result[0]  , result[1] 

        query = (f"""SELECT  `name` , `email` FROM {classid} WHERE `role`  = 'Student' """)
        students = []
        mycursor.execute(query)
        result = mycursor.fetchall()

        for row in result:
            if row:
                # print("printing")
                # print(row)
                students.append({ "name" : row[0]  , "email" :row[1]  })
            else:
                break
        
        students.sort(key = lambda x: x["name"])

        participants = {"teacher" : {"name" : teacher_name , "email" : teacher_email} , "students" : students} 
        # print(participants)
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
        mysql_db = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_information")
        mycursor = mysql_db.cursor()

        query = (f"""SELECT  `name` , `email` FROM {classid} """)
        mycursor.execute(query)

        participants_dict = {}

        
        while True:
            row = mycursor.fetchone()
            if row:
                participants_dict[f"{row[1] }"]  = row[0] 
            else:
                break


        return participants_dict

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"

def get_participants_email(classid):
    try:
        db = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_information")
        mycursor = db.cursor()
        query = f"""SELECT  `email` FROM {classid}"""
        mycursor.execute(query)
        result = mycursor.fetchall()
        print(result)
        email_li = [ email[-1] for email in result ]

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
        db = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_inf")
        classid =  ''.join(choice(string.ascii_lowercase  + string.digits) for x in range(15))

        while True:
            query = (f"""SELECT  `class_name` FROM basic_information WHERE class_id = '{classid}' """)
            mycursor = db.cursor()
            mycursor.execute(query)
            myresult = mycursor.fetchall()

            if not (myresult):
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
        dbase = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_chats")
        dbase2 = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_information")
        dbase3 = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_other")
        dbase4 = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_pd_req")
        dbase5 = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_inf")

        mycursor = dbase.cursor()
        mycursor5 = dbase5.cursor()
        mycursor2 = dbase2.cursor()
        mycursor3 = dbase3.cursor()
        mycursor4 = dbase4.cursor()
         
        try: 
            query = (f"""DROP TABLE `{classid}_chats`""")
            mycursor.execute(query)
        except Exception:
            pass

        try: 
            query = (f"""DROP TABLE `{classid}`""")
            mycursor2.execute(query)
        except Exception:
            pass

        try: 
            query = (f"""DROP TABLE `{classid}_other`""")
            mycursor3.execute(query)
        except Exception:
            pass

        try: 
            query = (f"""DROP TABLE `{classid}_pd_req`""")
            mycursor4.execute(query)
        except Exception:
            pass

        try: 
            query = (f"""DELETE FROM `basic_information` WHERE `class_id` = '{classid}'""")
            mycursor5.execute(query)
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
        mycur = dbase.cursor()
        query = (f"""CREATE TABLE `class_chats`.`{classid}_chats` ( `sno` INT(5) NOT NULL AUTO_INCREMENT ,  `user_email` VARCHAR(200) NOT NULL , `user_name` VARCHAR(200) NOT NULL , `send_msg` TEXT NOT NULL,  `msg` TEXT NOT NULL , `date-time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ,    PRIMARY KEY  (`sno`)) ENGINE = InnoDB;""")
        mycur.execute(query)


        query = (f"""INSERT INTO `{classid}_chats` (`sno`, `user_email`, `send_msg`, `msg` , `date-time`) VALUES (1 , 'None', 'None' '[]', 'None' , current_timestamp());""")
        mycur.execute(query)
        dbase.commit()

        mycur = dbase2.cursor()
        query = (f"""CREATE TABLE `class_information`.`{classid}` ( `email` VARCHAR(400) NOT NULL ,  `name` TEXT NOT NULL ,  `role` TEXT NOT NULL , `statics` TEXT NOT NULL ,    PRIMARY KEY  (`email`)) ENGINE = InnoDB;""")
        mycur.execute(query)

        query = (f"""INSERT INTO `{classid}` (`email`, `name`, `role`, `statics`) VALUES ('{email}', '{name}', 'Teacher', '{"{}"}');""")
        mycur.execute(query)
        dbase2.commit()

        
        mycur = dbase3.cursor()
        query = (f"""CREATE TABLE `class_other`.`{classid}_other` ( `sno` INT(5) NOT NULL AUTO_INCREMENT , `type` VARCHAR(30) NOT NULL , `details` TEXT NOT NULL , `st_details` TEXT NOT NULL,  PRIMARY KEY (`sno`)) ENGINE = InnoDB;""")
        mycur.execute(query)

        query = (f"""INSERT INTO `{classid}_other` (`sno`, `type`, `details`, `st_details`) VALUES (1 , 'None', 'None' , 'None');""")
        mycur.execute(query)
        dbase3.commit()

        mycur = dbase4.cursor()
        query = (f"""CREATE TABLE `class_pd_req`.`{classid}_pd_req` ( `email` VARCHAR(400) NOT NULL ,  `name` TEXT NOT NULL, PRIMARY KEY  (`email`)) ENGINE = InnoDB;""")
        mycur.execute(query)

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

    # print("all previous classes delted successfully")

    if del_tables == "Problem In Contacting":
        fe.server_contact_error()
        return None

    try:

        dbase = mysql.connector.connect(host="localhost",user=db_user,password="",database="classrooms")
        db = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_chats")
        db2 = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_information")
        db3 = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_other")
        db4 = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_pd_req")
        db5 = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_inf")

        cr_tab = create_tables(db , db2, db3 , db4 , classid , name , user_email , class_standard)

        if cr_tab == "Problem In Contacting":
            # print("returning none")
            return None

        
        query = (f"""INSERT INTO `joined_classes` (`role`, `classid`, `email`, `class_name`) VALUES  ('Teacher', '{classid}', '{user_email}', "{class_name}")""")
        mycursor = dbase.cursor()
        mycursor.execute(query)
        dbase.commit()
        query = (f"""INSERT INTO `basic_information` (`class_id`, `class_name`, `teacher`, `class_standard` , `description`) VALUES ('{classid}', "{class_name}", '{user_email}', '{class_standard}' , '{description}');""")
        mycursor = db5.cursor()
        mycursor.execute(query)
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
        dbase = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_pd_req")
        mycursor = dbase.cursor()

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"
    
    try:
        
        query = (f"""SELECT  `name` FROM `{classid}_pd_req` WHERE `email` = '{email}' """)
        print("not")
        mycursor.execute(query)
        result = mycursor.fetchall()
        print(len(result))
        if(len(result) != 0):
            fe.already_req()
            return "Already Joined"
    except Exception:
        fe.some_went_wrong()
        return "Problem In Contacting"

        
    try:
        query = (f"""INSERT INTO `{classid}_pd_req` (`email`, `name`) VALUES ('{email}', '{name}');""")
        mycursor.execute(query)
        dbase.commit()

    except Exception:
        fe.some_went_wrong()
        return "Problem In Contacting"
        
    return None

def get_join_req(classid):

    """ This function will help us to get all the pending requests for joining the class...
    
    Returns a list of dicts...
    
    Example - 
    
    [{'email': 'agrawalNaitik13@gmail.com', 'name': 'Naitik Agrawal'} ,{'email': 'Naitik1789@gmail.com', 'name': 'Naitik'}]
    
    """

    try:
        dbase = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_pd_req")

        mycursor = dbase.cursor()

        query = (f"""SELECT * FROM `{classid}_pd_req`""")
        mycursor.execute(query)

        req_tp  =  mycursor.fetchall()

        req_li = [{"email" : email  , "name" : name } for email, name in req_tp ]

        return req_li

    except Exception:
        return "Problem In Contacting"

def get_class_name(classid):

    """This function helps us to know the name of the The Class using classid...
    
    Returns None if Classid Is Wrong or connection to db is not successfull....
    """


    try:
        db = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_inf")
        mycursor = db.cursor()

        query = (f"""SELECT  `class_name` FROM basic_information WHERE `class_id` = '{classid}' """)
        mycursor.execute(query)
        cls_tp = mycursor.fetchall()
        return cls_tp[-1][-1]
        
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
        dbase1 = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_information")
        dbase2 = mysql.connector.connect(host="localhost",user=db_user,password="",database="classrooms")
        dbase3 = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_pd_req")
        mycursor1 = dbase1.cursor()
        mycursor2 = dbase2.cursor()
        mycursor3 = dbase3.cursor()

        print("all connection success")

        query = (f"""SELECT  `name`  FROM `{classid}_pd_req` WHERE email = '{user_email}' """)
        mycursor3.execute(query)
        student = mycursor3.fetchall()
        if not student:
            fe.some_went_wrong()
            return "Request Not Found"
        st_name  = student[-1][0] 

        no_class = check_len_classes(user_email)
        if not(no_class):
            fe.no_more_join_ft()
            
            try:
                query = (f"""DELETE FROM `{classid}_pd_req` WHERE `{classid}_pd_req`.`email` = '{user_email}'""")
                mycursor3.execute(query)
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
                query = (f"""DELETE FROM `{classid}_pd_req` WHERE `{classid}_pd_req`.`email` = '{user_email}'""")
                mycursor3.execute(query)
                dbase3.commit()
            except Exception:
                pass

            # Add decline request to user notification
            
            return "Max Participants"
        # print("max participant")
        query = (f"""SELECT  `sno` FROM joined_classes WHERE email = '{user_email}' and classid = '{classid}'""")
        mycursor2.execute(query)
        entry_al_present = mycursor2.fetchall()
        # print("entry checked")
        if entry_al_present:
            try:
                query = (f"""DELETE FROM `{classid}_pd_req` WHERE `{classid}_pd_req`.`email` = '{user_email}'""")
                mycursor3.execute(query)
                dbase3.commit()
            except Exception:
                pass
            fe.already_joined_ft()
            return "Already Joined"

        query = (f"""INSERT INTO `{classid}` (`email`, `name`, `role`, `statics`) VALUES ('{user_email}', '{st_name}', 'Student', '{"{}"}');""")
        mycursor1.execute(query)
        dbase1.commit()

        query = (f"""INSERT INTO `joined_classes` (`role`, `classid`, `email`, `class_name`) VALUES  ('Student', '{classid}', '{user_email}', "{class_name}")""")
        mycursor2.execute(query)
        dbase2.commit()

        query = (f"""DELETE FROM `{classid}_pd_req` WHERE `{classid}_pd_req`.`email` = '{user_email}'""")
        mycursor3.execute(query)
        dbase3.commit()
        # print("finally added")

        # Add approve request to user notification

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"

def decline_request(classid , user_email):

    try:
        dbase = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_pd_req")
        mycursor = dbase.cursor()

        query = (f"""DELETE FROM `{classid}_pd_req` WHERE `{classid}_pd_req`.`email` = '{user_email}'""")
        mycursor.execute(query)
        dbase.commit()

        # hm.add_decline_req_message(user_email , class_name)

        return None

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"

def remove_student(classid , user_email , remover):
    try:
 
        dbase1 = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_information")
        dbase2 = mysql.connector.connect(host="localhost",user=db_user,password="",database="classrooms")
        mycursor = dbase1.cursor()
        mycursor2 = dbase2.cursor()

        query = (f"""DELETE FROM `{classid}` WHERE `{classid}`.`email` = '{user_email}'""")
        mycursor.execute(query)
        dbase1.commit()

        query = (f"""DELETE FROM `joined_classes` WHERE `joined_classes`.`email` = '{user_email}' AND `joined_classes`.`classid` = '{classid}'""")
        mycursor2.execute(query)
        dbase2.commit()

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"

def delete_class(classid):

    try:
        dbase = mysql.connector.connect(host="localhost",user=db_user,password="",database="classrooms")

        mycursor = dbase.cursor()
        

        query = (f"""DELETE FROM `joined_classes` WHERE `joined_classes`.`classid` = '{classid}'""")
        mycursor.execute(query)
        dbase.commit()


        try_del_tables(classid)
        
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