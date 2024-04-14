"""
Module to handle media files storage in th database...

"""

from MySQLdb import _mysql
import time
import string
from random import choice
from werkzeug.utils import secure_filename
import flash_errors as fe
import mysql.connector


mysql_passwd = ''
db_user = "root"



def reterive_chat_media_file(media_type , url , pdf_class=None , img_class=None , audio_class=None , video_class=None , doc_class=None):

    """
    Used to get the media file from the database..."""

    if media_type == "image":
        dbase_class = img_class
        
    elif media_type == "pdf":
        dbase_class = pdf_class

    elif media_type == "audio":
        dbase_class = audio_class

    elif media_type == "video":
        dbase_class = video_class

    elif media_type == "doc":
        dbase_class = doc_class

    else:
        return None


    file_row = dbase_class.query.filter_by(url = url).first()

    if file_row == None:
        return None

    return file_row.file , file_row.filename , file_row.mimetype

def reterive_pdf_file(url , dbase_class):

    # For classwork only....
    
    """
    Used to get the pdf file from the databse..."""

    file_row = dbase_class.query.filter_by(url = url).first()

    if file_row == None:
        return None

    return file_row.file , file_row.filename , file_row.mimetype

def get_counted_days():
    """
    Gives the no. of days...
    
    Used to delete the old files frrom the databases..."""


    un_cal_date = time.localtime()[:3]
    return un_cal_date[0]*365 + un_cal_date[1]*30 + un_cal_date[2]

def get_uni_url(db , table_name):

    """
    Used to get a unique url to store the file in the database and reterive it... """
    

    try:

        url =  ''.join(choice(string.ascii_lowercase  + string.digits) for x in range(8))
        mycursor = db.cursor()
        while True:
            query = (f"""SELECT  `filename` FROM {table_name} WHERE url = '{url}' """)
            mycursor.execute(query)
            if not (mycursor.fetchall()):
                return url
            url =  ''.join(choice(string.ascii_lowercase + string.digits) for x in range(8))
    except Exception:
        return "Problem In Contacting"

def upload_chat_file(file_content , filename  , mimetype , filesize , db , pdf_class , img_class , audio_class , video_class , doc_class):

    try:

        if not "." in filename :
            fe.filename_nt_crr()
            return "fi" , None

        ext = filename.rsplit(".", 1)[1]

        if (ext.upper() in ["JPEG" , "JPG" , "GIF" , "PNG"]):
            dbase_class = img_class
            mx_mb_size = 5
            table_name = "images"

        elif (ext.upper() in ["PDF" , "TXT" , "DOC" , "DOCX" , "PPT" , "PPTX"]):
            dbase_class = pdf_class
            mx_mb_size = 20
            table_name = "pdfs"

        elif (ext.upper() in ["MP3" , "WAV" , "AIFF" , "AU" , "FLAC"]):
            dbase_class = audio_class
            mx_mb_size = 10
            table_name = "audios"

        elif (ext.upper() in ["MP4" ,"MKV"]):
            dbase_class = audio_class
            mx_mb_size = 15
            table_name = "videos"

        else:
            dbase_class = doc_class
            mx_mb_size = 20
            table_name = "docs"


        mysql_db = _mysql.connect(db = "media_files" , user = db_user , passwd = mysql_passwd)
        
        current_days = get_counted_days()

        if filesize > mx_mb_size:
            fe.file_over_size(mx_mb_size)
            return "fi" , None

        url = get_uni_url(mysql_db , table_name)

        if url == "Problem In Contacting":
            fe.server_contact_error()
            return url , None

        add_file = dbase_class(
            url = url,
            file= file_content,
            filename= secure_filename(filename),
            mimetype = mimetype,
            date = current_days
        )

        db.session.add(add_file)
        db.session.commit() 

        old_days_del_msg = current_days - 15


        try:
            mysql_db.query(f"""DELETE from `{table_name}` WHERE `{table_name}`.`date` <= {old_days_del_msg}""")

        except Exception:
            pass


        return url , table_name

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting" , None

def upload_pdf_file(pdf_file ,dbase_tb_class , db , no_days):

    try:

        filename = pdf_file.filename

        if not "." in filename :
            fe.filename_nt_crr()
            return "fi"

        ext = filename.rsplit(".", 1)[1]

        if not(ext.upper() in ["PDF" , "TXT" , "DOC" , "DOCX" , "PPT" , "PPTX"]):
            fe.select_file_nt_support()
            return "fi"
        mysql_db = mysql.connector.connect(host="localhost",user=db_user,password="",database="media_files")
        mycursor = mysql_db.cursor()

        current_days = get_counted_days()
        pdf_content = pdf_file.read().decode('utf-8')

        if len(pdf_content) > 1024 * 1024 * 25:
            fe.pdf_over_size()
            return "fi"

        url = get_uni_url(mysql_db , "pdfs")

        if url == "Problem In Contacting":
            return url
        
        add_pdf = dbase_tb_class( url = url, file= pdf_content, filename= secure_filename(filename), mimetype = pdf_file.mimetype, date = current_days)

        db.session.add(add_pdf)
        db.session.commit() 

        old_days_del_pdf = current_days - no_days

        try:
            query = (f"""DELETE from `pdfs` WHERE `pdfs`.`date` <= {old_days_del_pdf}""")
            mycursor.execute(query)
            mysql_db.commit()

        except Exception:
            pass

        return url

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"

