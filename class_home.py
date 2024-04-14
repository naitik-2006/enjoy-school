
"""
Module to manage the class home page ...

"""


from MySQLdb import _mysql
import media_files as mf
import time
import flash_errors as fe
import mysql.connector
import json


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
    '''
        Delete classworks if they exceed the maximum limit (12)
    '''
    
    try:
        mycur  = db.cursor()
        query = (f"""SELECT  `sno` FROM `{classid}_other` WHERE `{classid}_other`.`type` = "classwork" """)
        mycur.execute(query)
        snos = mycur.fetchall()

        if len(snos) >= 12:

            query = (f"""DELETE FROM `{classid}_other` WHERE `{classid}_other`.`sno` = '{snos[0][0]}'""")
            mycur.execute(query)
            db.commit()
    
    except Exception:
        pass

def del_clswrk(classid , sno):
    '''
        Delete classworks if they exceed the maximum limit (12)
    '''
    
    try:
        mysql_db = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_other")
        mycur = mysql_db.cursor()
        query = (f"""SELECT  `sno` FROM `{classid}_other` WHERE `{classid}_other`.`sno` = {int(sno)} """)
        mycur.execute(query)
        snos = mycur.fetchall()

        # if len(snos) >= 12:

        query = (f"""DELETE FROM `{classid}_other` WHERE `{classid}_other`.`sno` = '{snos[0][0]}'""")
        mycur.execute(query)
        mysql_db.commit()
    
    except Exception:
        pass

def insert_new_classwork(classid , class_work_name , pdf_file , start_date , end_date , db , dbase_tb_class):
    
    try:
        mysql_db = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_other")
        mycursor = mysql_db.cursor()
         
        del_older_clswrk(classid , mysql_db)

        pdf_upload_url = mf.upload_pdf_file(pdf_file , dbase_tb_class , db, 30)

        if pdf_upload_url in ("Problem In Contacting" , "fi"):
            return pdf_upload_url

        details_str = str({"pdf_file_url" : pdf_upload_url , "class_work_name" : class_work_name,"start_date" : start_date,"end_date" : end_date})

        

        query = (f"""INSERT INTO `{classid}_other` (`type`, `details` , `st_details`) VALUES ('classwork', "{details_str}" , '{"{}"}');""")
        mycursor.execute(query)
        mysql_db.commit()

    except Exception:
        return "Problem In Contacting"

def valid_clswrk_submission(start_date , end_date , user_email , st_details , flash_msg = True):
    '''
        check whether user able to submit classwork or not
    '''
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

    # try:
        mysql_db = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_other")
        mycursor = mysql_db.cursor()

        query = (f"""SELECT  `details` , `sno` , `st_details` FROM {classid}_other WHERE `type`  = 'classwork' """)
        mycursor.execute(query)
        classworks = []

        while True:

            row = mycursor.fetchone()
            print("printing row")
            if row:
                # eval to convert str to dict
                details_dict = eval(row[0] , dict())
                details_dict["classwork_id"] = row[1]
                st_details_dict = eval(row[2] , dict())


                if valid_clswrk_submission(details_dict["start_date"] , details_dict["end_date"] , user_email , st_details_dict , flash_msg = False) :
                    details_dict["status"] = 0

                else:
                    details_dict["status"] = 1

                classworks.append(details_dict)
            else:
                break

        return classworks

    # except Exception:
    #     return "Problem In Contacting"

def add_student_work(pdf_file , dbase_tb_class, db , classid , st_email , classwork_id ):

    try:

        mysql_db = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_other")
        mycursor = mysql_db.cursor()

        query = (f"""SELECT  `st_details` , `details` FROM {classid}_other WHERE `type`  = 'classwork'  AND `sno` = '{classwork_id}' """)
        mycursor.execute(query)

        result = mycursor.fetchall()
        if not result:
            fe.some_went_wrong()
            return "No Classwork Found"

        details_dict = eval(result[-1][1] , dict())
        st_details_dict = eval(result[-1][0] , dict())

        if valid_clswrk_submission(details_dict["start_date"] , details_dict["end_date"] , st_email , st_details_dict) :
            return "Problem"
        
        pdf_upload = mf.upload_pdf_file(pdf_file , dbase_tb_class , db , 30 )

        if pdf_upload == "Problem In Contacting":
            fe.server_contact_error()
            return pdf_upload


        date_li = list(time.localtime())[:3]
        date = str(date_li[0]) + "-" + str(date_li[1]) + "-" + str(date_li[2])

        st_details_dict[f"""{st_email}"""] = [pdf_upload, date]

        query = (f"""UPDATE `{classid}_other` SET `st_details` = "{st_details_dict}" WHERE `{classid}_other`.`sno` = '{classwork_id}';""")
        mycursor.execute(query)
        mysql_db.commit()
    
    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"
        
def get_all_st_submitted_wrk(classid , classwork_id):

    try:
        mysql_db = mysql.connector.connect(host="localhost",user=db_user,password="",database="class_other")
        mycursor = mysql_db.cursor()

        query = (f"""SELECT  `st_details`, `details`  FROM {classid}_other WHERE `type`  = 'classwork'  AND `sno` = '{classwork_id}' """)
        mycursor.execute(query)

        result = mycursor.fetchall()
        if not result:
            return "No Classwork Found"

        st_details_dict = eval(result[-1][0], dict())
        details_dict = eval(result[-1][1], dict())

        return ((st_details_dict.keys()) , st_details_dict, details_dict['class_work_name'])

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"

if __name__ == '__main__':
    pass
    