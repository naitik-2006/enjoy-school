"""
    Module works using flask sqlalchemy and its classes are accepted as arguments in the respective functions...   """



from flask import flash , redirect 
import flash_errors as fe
import flash_success as fs
import numpy

def add_pd_req(email,name,phone_no,password,otp,role,dbase,db,path,session,session_var):
    
    try:

    
        pd_db_search = dbase.query.filter_by(email = email).first()

        if pd_db_search != None:
            db.session.delete(pd_db_search)
            db.session.commit()

        enter_pd_values = dbase(email = email, user_name = name, user_phone = phone_no , user_role= role, user_password = password , user_otp = otp)

        db.session.add(enter_pd_values)
        db.session.commit()  

    except Exception:
        
        fe.server_contact_error()
        values = {"name":name,
            "phone": phone_no,
            "email" : email}
        session[session_var] = values  

        return redirect(path)

def check_in_t_db(name , phone_no , email , path ,session_var , dbase , dbase2 , db , params,session):
    try:
        check_in_datbase = dbase.query.filter_by(user_email = email).first()
        check_in_datbase2 = dbase2.query.filter_by(user_email = email).first()

        if check_in_datbase != None or check_in_datbase2 != None:
            fe.email_al_regis_error()
            values = {"name":name,
            "phone": phone_no,
            "email" : email}
            session[session_var] = values        

            return redirect(path)

        else:
            return None

    except Exception:
        print('error')
        fe.server_contact_error()
        values = {"name":name,
            "phone": phone_no,
            "email" : email}
        session[session_var] = values  

        return redirect(path)   

def acc_presence( path ,email , dbase , dbase2 , db , session , session_var):
    try:
        check_in_datbase = dbase.query.filter_by(user_email = email).first()
        check_in_datbase2 = dbase2.query.filter_by(user_email = email).first()

        if check_in_datbase != None or check_in_datbase2 != None:
            return redirect(path)

        else:
            return None

    except Exception:
        fe.server_contact_error()    
        session[session_var] = email
        return redirect(path)   

def send_verify_mail(name,phone_no,email,mail,params,session_var,session):
    
    try:
        otp = numpy.random.randint(11111,99999)
        mail.send_message(subject = "Otp Verification!",
        recipients= [email],
        sender= params["verify-email-id"],
        body = f"Your Email Verification Otp is {otp}"
        )
        return otp

    except Exception:
        fe.flash_mail_err()

        values = {"name":name,
        "phone": phone_no,
        "email" : email}

        session[session_var] = values 
        return None


def get_values(request , *args):

    return_values = []
    
    for item in args :
        return_values.append(request.form.get(item))
    
    return return_values

    
def get_signup_info(dbase , slug):

    try:
        db_row = dbase.query.filter_by(email = slug).first()

        if db_row == None:
            return None        
        return db_row

    except Exception:
        fe.server_contact_error()

        return  "Problem In contacting!"


def add_account(db, dbase , name , phone_no , email , password , url_for , db_row , session , path , slug):
    """If there is  no problem in creating a account..."""
    try:
        enter_values = dbase(user_name = name , 
            user_phone = phone_no,
            user_email = email ,
            user_password = password)

        db.session.add(enter_values)
        db.session.delete(db_row)
        db.session.commit() 

        fs.acc_created()           
        
        return None

    except Exception:

        fe.server_contact_error()

        return redirect(url_for(path))

def resend_otp(mail , email , otp , params ):
    try:
        mail.send_message(subject = "Otp Verification!",
        recipients= [email],
        sender= params["verify-email-id"],
        body = f"Your Email Verification Otp is {otp}"
        )
        return otp

    except Exception:
        return None