"""
    Module works using flask sqlalchemy and its classes are accepted as arguments in the respective functions...   """



import flash_errors as fe
import numpy
from flask import redirect
import string
from random import choice

class User():
    
    def __init__(self,user_name,user_email,role,sno):
        self.name = user_name
        self.email = user_email
        self.role = role
        self.user_id = sno

        
        self.user_id_wi_rl = f"{sno}_{role}" # For sending messages in clsass
        

    def is_active(self):
        return True

    def get_id(self):
        return {"user":self.user_id , "role":self.role}

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
        
    def __str__(self):
        return f'{self.name} , {self.email} , {self.role}'

def find_account(email,dbase1 , dbase2):

    try:
        
        st_account = dbase1.query.filter_by(user_email = email).first()
        if st_account == None:
            t_account = dbase2.query.filter_by(user_email = email).first()

            if t_account == None:
                fe.login_err()            
                return None , None

            return (t_account  , "Teacher")
        return (st_account , "Student")

    except Exception:

        fe.server_contact_error()
        return "Problem in contacting" , None


def get_user_details(dbase,dbase2,role,sno):

    try:
        if role == "Teacher":
            user_account = dbase2.query.filter_by(sno = sno).first()
            if user_account == None :
                return None , None
            return user_account.user_name , user_account.user_email
        elif role == "Student":
            user_account = dbase.query.filter_by(sno = sno).first()
            if user_account == None :
                return None , None
            return user_account.user_name , user_account.user_email
        return None , None
        
    except Exception:

        fe.server_contact_error()        
        return None , None


def send_forg_pass_otp_verify_mail(mail , email , params , session , session_var):
    
    try:
        otp = numpy.random.randint(11111,99999)
        mail.send_message(subject = "Otp Verification!",
        recipients= [email],
        sender= params["verify-email-id"],
        body = f"Your Verification Otp to Change Password is {otp} \nPlease don't share your passwords with anyone.")
        return otp

    except Exception:

        fe.flash_mail_err()
        session[session_var] = email
        return None

def resend_forg_pass_otp_verify_mail(mail , email , params , otp):

    try:
        mail.send_message(subject = "Otp Verification!",
        recipients= [email],
        sender= params["verify-email-id"],
        body = f"Your Verification Otp to Change Password is {otp} \nPlease don't share your passwords with anyone.")
        return otp

    except Exception:
        return None

def check_user_acc(dbase1,dbase2,email,session,session_var,path):

    try:

        account = dbase1.query.filter_by(user_email = email).first()
        if account == None:
            account2 =  dbase2.query.filter_by(user_email = email).first()
            if account2 == None:

                session[session_var] = email
                fe.email_nf_err()
                return redirect(path)

            return None
        return None

    except Exception:
        fe.server_contact_error()
        session[session_var] = email         
        return redirect(path)


def add_forg_pass_req(dbase , db , email , otp ,path,session,session_var):
    try:
        exist_req = dbase.query.filter_by(email = email).first()
        if exist_req != None:
            db.session.delete(exist_req)
            db.session.commit()

        values = dbase(email = email , otp = otp)
        db.session.add(values)
        db.session.commit()
        return None

    except Exception:

        fe.server_contact_error()
        session[session_var] = email
        return redirect(path)


def get_values(request , *args):

    return_values = []
    
    for item in args :
        return_values.append(request.form.get(item))
    
    return return_values

def find_forg_req(dbase,email):

    try:
        req = dbase.query.filter_by(email = email).first()
        if req== None:
            return None

        return req

    except Exception:

        fe.server_contact_error()
        return "Problem In contacting"

def add_url_to_dbs(db,dbase,dbase2,email):

    try:
        while True:

            url = ''.join(choice(string.ascii_letters + string.digits) for x in range(60))
            exist_url = dbase2.query.filter_by(url = url).first()
            if exist_url == None:
                break
            else:
                continue

        del_entry(db,dbase,email)
        enter_value = dbase(url = url , email = email)
        enter_value2 = dbase2(url = url)
        db.session.add(enter_value)
        db.session.add(enter_value2)
        db.session.commit()
        return url

    except Exception:
        return None
    



def del_entry(db,dbase,email):
    entry = dbase.query.filter_by(email = email).first()
    if entry == None:
        return 
    db.session.delete(entry)
    db.session.commit()
    return 


def find_forg_pass_ch_url(dbase,url):
    try:
        url_pressence = dbase.query.filter_by(url = url).first()
        if url_pressence == None :
            fe.some_went_wrong()
        return url_pressence
    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"

def delete_url_entry(db,dbase,url):
    try:
        entry = dbase.query.filter_by(url= url).first()
        if entry == None:
            return "Problem In Contacting"
        db.session.delete(entry)
        db.session.commit()
        return None

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"

def add_entry_to_post_db(dbase,email,url,db):

    # try:
            
        del_entry(db,dbase,email)
        entry = dbase(email = email , url = url)
        db.session.add(entry)
        db.session.commit()
        return None

    # except Exception:
    #     fe.server_contact_error()
    #     return "Problem In Contacting"

def find_post_url(dbase,url):
    try:
        entry = dbase.query.filter_by(url = url).first()
        if entry == None:
            fe.some_went_wrong()
            return entry
        return entry.email
    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"

def search_acc_in_dbs(dbase1,dbase2,email):
    
    try:

        account = dbase1.query.filter_by(user_email = email).first()
        if account == None:
            account2 =  dbase2.query.filter_by(user_email = email).first()
            if account2 == None:
                return None , None
            return account2 , "Teacher"
        return account , "Student"

    except Exception:

        fe.server_contact_error()  
        return None , None


def add_custom_url_to_db(db,dbase,url,email):
    try:
        del_entry(db,dbase,email)
        entry = dbase(url = url , email = email)
        db.session.add(entry)
        db.session.commit()
        return None
    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"

def change_password(db,dbase,dbase2,account,password,role):
    try:

        user_name = account.user_name
        phone_no = account.user_phone
        email = account.user_email

        if role == "Student":
            enter_values = dbase(user_name = user_name, user_phone = phone_no, user_email = email , user_password = password)

        elif role == "Teacher":
            enter_values = dbase2(user_name = user_name, user_phone = phone_no, user_email = email , user_password = password)

        db.session.add(enter_values)
        db.session.delete(account)
        db.session.commit()
        return None

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"