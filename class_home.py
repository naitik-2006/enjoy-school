
"""
Module to manage the class home page ...

"""


from MySQLdb import _mysql
import media_files as mf
import time
import flash_errors as fe


mysql_passwd = ''
db_user = "root"


def no_of_days(date , nt_list_format = True):
    
    if nt_list_format:
        date = date.split("-")
    return int(date[0]) * 365 + int(date[1]) * 30 + int(date[2])

def no_of_mins(time , nt_list_format = True):
    
    if nt_list_format:
        time = time.split(":")
    return int(time[0]) * 60 + int(time[1])



# --------------------------- CLASSWORK FUNCTIONS -------------------------------------------

def del_older_clswrk(classid , db):
    
    try:

        db.query(f"""SELECT  `sno` FROM `{classid}_other` WHERE `{classid}_other`.`type` = "classwork" """)
        snos =  db.store_result().fetch_row(maxrows = 0)

        if len(snos) >= 12:

            db.query(f"""DELETE FROM `{classid}_other` WHERE `{classid}_other`.`sno` = '{snos[0][0].decode()}'""")
    
    except Exception:
        pass

def insert_new_classwork(classid , class_work_name , pdf_file , start_date , end_date , db , dbase_tb_class):
    
    try:

        mysql_db = _mysql.connect(db = "class_other" , user = db_user , passwd = mysql_passwd)
         
        del_older_clswrk(classid , mysql_db)

        pdf_upload = mf.upload_pdf_file(pdf_file , dbase_tb_class , db, 30)

        if pdf_upload in ("Problem In Contacting" , "fi"):
            return pdf_upload

        details_str = str({"pdf_file_url" : pdf_upload ,
                            "class_work_name" : class_work_name,
                            "start_date" : start_date,
                            "end_date" : end_date})

        

        mysql_db.query(f"""INSERT INTO `{classid}_other` (`type`, `details` , `st_details`) VALUES ('classwork', "{details_str}" , '{"{}"}');""")


    except Exception:
        return "Problem In Contacting"

def valid_clswrk_submission(start_date , end_date , user_email , st_details , flash_msg = True):

    current_date_li = list(time.localtime())[:3]

    if no_of_days(end_date) - no_of_days(current_date_li , nt_list_format=False) < 0  or no_of_days(current_date_li , nt_list_format=False)  - no_of_days(start_date) < 0 :
        if flash_msg:
            fe.cant_submit_now()
        return True

    elif user_email in st_details:
        if flash_msg:
            fe.already_submit()
        return True

    else:
        return False

def get_all_classworks(classid , user_email):

    try:

        mysql_db = _mysql.connect(db = "class_other" , user = db_user , passwd = mysql_passwd)

        mysql_db.query(f"""SELECT  `details` , `sno` , `st_details` FROM {classid}_other WHERE `type`  = 'classwork' """)

        result = mysql_db.store_result()
        classworks = []

        while True:

            row = result.fetch_row()
            if row:

                details_dict = eval(row[-1][0].decode() , dict())
                details_dict["classwork_id"] = row[-1][1].decode()
                st_details_dict = eval(row[-1][2].decode() , dict())


                if valid_clswrk_submission(details_dict["start_date"] , details_dict["end_date"] , user_email , st_details_dict , flash_msg = False) :
                    details_dict["status"] = 0

                else:
                    details_dict["status"] = 1

                classworks.append(details_dict)
            else:
                break

        return classworks

    except Exception:
        return "Problem In Contacting"

def add_student_work(pdf_file , dbase_tb_class, db , classid , st_email , classwork_id , req):

    try:

        mysql_db = _mysql.connect(db = "class_other" , user = db_user , passwd = mysql_passwd)

        mysql_db.query(f"""SELECT  `st_details` , `details` FROM {classid}_other WHERE `type`  = 'classwork'  AND `sno` = '{classwork_id}' """)
     

        result = mysql_db.store_result().fetch_row()
        if not result:
            fe.some_went_wrong()
            return "No Classwork Found"

        details_dict = eval(result[-1][1].decode() , dict())
        st_details_dict = eval(result[-1][0].decode() , dict())

        if valid_clswrk_submission(details_dict["start_date"] , details_dict["end_date"] , st_email , st_details_dict) :
            return "Problem"
        
        pdf_upload = mf.upload_pdf_file(pdf_file , dbase_tb_class , db , 30 , req)

        if pdf_upload == "Problem In Contacting":
            fe.server_contact_error()
            return pdf_upload


        date_li = list(time.localtime())[:3]
        date = str(date_li[0]) + "-" + str(date_li[1]) + "-" + str(date_li[2])

        st_details_dict[f"""{st_email}"""] = [pdf_upload, date]

        mysql_db.query(f"""UPDATE `{classid}_other` SET `st_details` = "{st_details_dict}" WHERE `{classid}_other`.`sno` = '{classwork_id}';""")

    
    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"
        
def get_all_st_submitted_wrk(classid , classwork_id):

    try:

        mysql_db = _mysql.connect(db = "class_other" , user = db_user , passwd = mysql_passwd)

        mysql_db.query(f"""SELECT  `st_details`  FROM {classid}_other WHERE `type`  = 'classwork'  AND `sno` = '{classwork_id}' """)

        result = mysql_db.store_result().fetch_row()
        if not result:
            return "No Classwork Found"

        st_details_dict = eval(result[-1][0].decode())

        return ((st_details_dict.keys()) , st_details_dict)

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"

def valid_file_download(classid , clswrk_id):

    mysql_db = _mysql.connect(db = "class_other" , user = db_user , passwd = mysql_passwd)

    mysql_db.query(f"""SELECT  `details` FROM {classid}_other WHERE `type`  = 'classwork'  AND `sno` = '{clswrk_id}' """)

    result = mysql_db.store_result().fetch_row()
    if not result:
        fe.some_went_wrong()
        return False

    details_dict = eval(result[-1][1].decode() , dict())

    current_date_li = list(time.localtime())[:3]

    if no_of_days(details_dict["end_date"]) - no_of_days(current_date_li , nt_list_format=False) < 0  or no_of_days(current_date_li , nt_list_format=False)  - no_of_days(details_dict["start_date"]) < 0 :
        fe.cant_downlod_now()
        return False

    return True



# --------------------------- MEETING FUNCTIONS -------------------------------------------



def del_older_meeting(classid , db):
    
    try:

        db.query(f"""SELECT  `sno` FROM `{classid}_other` WHERE `{classid}_other`.`type` = "meeting" """)
        snos =  db.store_result().fetch_row(maxrows = 0)

        if len(snos) >= 12:

            db.query(f"""DELETE FROM `{classid}_other` WHERE `{classid}_other`.`sno` = '{snos[0][0].decode()}'""")
    
    except Exception:
        pass



def schedule_meeting(subject , meet_date_time , classid , duration):

    try:

        mysql_db = _mysql.connect(db = "class_other" , user = db_user , passwd = mysql_passwd)

        del_older_meeting(classid , mysql_db)

        meet_date , meet_time = meet_date_time.split("T")

        details_str = str({"meet_date" : meet_date ,
                        "meet_time" : meet_time ,
                        "duration" : duration , 
                        "subject": subject , 
                        "te_attend" : 0})

        mysql_db.query(f"""INSERT INTO `{classid}_other` (`type`, `details` , `st_details`) VALUES ('meeting', "{details_str}" , '{"{}"}');""")


    except Exception:
        return "Problem In Contacting"




def check_valid_attendance(meet_time , meet_date , duration , flash = False , min_limit = 15):

    current_date_time = list(time.localtime())
    current_date_li = current_date_time[:3]
    current_time_li = current_date_time[4:5]

    if no_of_days(meet_date) - no_of_days(current_date_li , nt_list_format=False) != 0 :
        if flash :
            fe.cant_attend_meet_now()
        return True

    elif no_of_mins(meet_time) - no_of_mins(current_time_li , nt_list_format=False) > min_limit or no_of_mins(current_time_li , nt_list_format=False) - no_of_mins(meet_time) > no_of_mins(duration) :
        if flash :
            fe.cant_attend_meet_now()
        return True

    return False



def get_all_meetings(classid):

    try:

        mysql_db = _mysql.connect(db = "class_other" , user = db_user , passwd = mysql_passwd)

        mysql_db.query(f"""SELECT  `details` , `sno` , `st_details` FROM {classid}_other WHERE `type`  = 'meeting' """)


        result = mysql_db.store_result()
        meetings = []

        while True:

            row = result.fetch_row()
            if row:

                details_dict = eval(row[-1][0].decode() , dict())
                details_dict["meeting_id"] = row[-1][1].decode()


                if check_valid_attendance(details_dict["meet_time"] , details_dict["meet_date"] , details_dict["duration"]) :
                    details_dict["status"] = 0

                else:
                    details_dict["status"] = 1

                meetings.append(details_dict)
            else:
                break

        return meetings

    except Exception:
        return "Problem In Contacting"


def te_attend_meeting(classid , meet_id):

        mysql_db = _mysql.connect(db = "class_other" , user = db_user , passwd = mysql_passwd)
        
        mysql_db.query(f"""SELECT  `details` FROM {classid}_other WHERE `type`  = 'meeting' AND `sno` = '{meet_id}' """)


        result = mysql_db.store_result().fetch_row()

        if result:

            details_dict = eval(result[-1][0].decode() , dict())
            details_dict["te_attend"] = 1

        else :
            fe.some_went_wrong()
            return ("No Meeting Found")

        if check_valid_attendance(details_dict["meet_time"] , details_dict["meet_date"] , details_dict["duration"] , min_limit = 0) :
            fe.some_went_wrong()
            return ("Cannot Attend Now")

        mysql_db.query(f"""UPDATE `{classid}_other` SET `details` = "{details_dict}" WHERE `{classid}_other`.`sno` = '{meet_id}';""")


def st_attend_meeting(user , classid , meet_id):

        # st_details_dict dict() - contains keys  as user_email_dur
        # user_email_dur value is a list - format - [join-time , duration]
        
        mysql_db = _mysql.connect(db = "class_other" , user = db_user , passwd = mysql_passwd)
        
        mysql_db.query(f"""SELECT  `details` , `st-details` FROM {classid}_other WHERE `type`  = 'meeting' AND `sno` = '{meet_id}' """)


        result = mysql_db.store_result().fetch_row()

        if  not (result):
            fe.some_went_wrong()
            return ("No Meeting Found")


        details_dict = eval(result[-1][0].decode() , dict())
        st_details_dict = eval(result[-1][1].decode() , dict())

        if check_valid_attendance(details_dict["meet_time"] , details_dict["meet_date"] , details_dict["duration"] , min_limit = 0) :
            fe.some_went_wrong()
            return ("Cannot Attend Now")

        if details_dict["te_attend"] != 1:
            return "tntj"

        user_duration_key = user.email + "_dur"

        if not(st_details_dict[user_duration_key]):
            st_detail = []
            st_detail.append(time.time())
            st_detail.append(0)
        else:
            st_detail = st_details_dict[user_duration_key]
            st_detail[0] = time.time()      

        st_details_dict[user_duration_key]  = st_detail

        mysql_db.query(f"""UPDATE `{classid}_other` SET `st_details` = "{st_details_dict}" WHERE `{classid}_other`.`sno` = '{meet_id}';""")




def st_left_meeting(user , classid , meet_id):

        mysql_db = _mysql.connect(db = "class_other" , user = db_user , passwd = mysql_passwd)
        
        mysql_db.query(f"""SELECT `st-details` FROM {classid}_other WHERE `type`  = 'meeting' AND `sno` = '{meet_id}' """)


        result = mysql_db.store_result().fetch_row()

        if  not (result):
            fe.some_went_wrong()
            return ("No Meeting Found")

        st_details_dict = eval(result[-1][0].decode() , dict())

        user_duration_key = user.email + "_dur"

        if not(st_details_dict[user_duration_key]):
            return
        else:
            st_detail = st_details_dict[user_duration_key]

        if len(st_detail) != 2:
            return

        st_detail[1] += time.time() - st_detail[0]
        st_detail[0] = 0

        st_details_dict[user_duration_key]  = st_detail

        mysql_db.query(f"""UPDATE `{classid}_other` SET `st_details` = "{st_details_dict}" WHERE `{classid}_other`.`sno` = '{meet_id}';""")
















if __name__ == '__main__':
    pass
    