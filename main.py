#=====================IMPORTS==========================================

from flask import Flask, render_template, request, redirect , url_for, session, jsonify , Response , send_file
from flask_login import LoginManager , login_required , login_user , logout_user  , current_user
from flask_socketio import SocketIO, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from io import BytesIO
import numpy,  json , re
import signup_functions as si
import login_system as ls
import flash_errors as fe
import flash_success as fs
import home_messages as hm
import user_classes as uc
import class_chats as cc
import media_files as mf
import class_home as ch

with open("config.json") as json_file:
    params = json.load(json_file)

#=====================IMPORTS==========================================



#====================DECLARATIONS========================================

app=Flask(__name__)
app.secret_key = "super-secret-key"
app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = params["local_host"]
socketio = SocketIO(app)

# Binding both the databses to the sqlalchemy uri...
SQLALCHEMY_BINDS = {
    'media_files':        'mysql://root:@localhost/media_Files',
    'users':        'mysql://root:@localhost/users'
}
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS
db = SQLAlchemy(app)

# For sending Verification mail...
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params["verify-email-id"],
    MAIL_PASSWORD = params["verify-email-password"]
)
mail = Mail(app)


# For Login ------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




#====================DECLARATIONS========================================



#=======================Database Classes==================================

# Main databse tables for accounts---

class Students(db.Model):
    
    # Students information table class...
    __bind_key__ = 'users'
    __tablename__ = 'students'

    """
    Data base (users) rows structure - Table students
    sno , user_name  , user_phone , user_email , user_password"""

    sno = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    user_phone = db.Column(db.String(120), nullable=False)
    user_email = db.Column(db.String(200), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)

class Teachers(db.Model):
    
    # Teachers information table class..
    __bind_key__ = 'users'
    __tablename__ = 'teachers'

    """
    Data base (users) rows structure - Table teachers
    sno , user_name  , user_phone , user_email , user_password"""

    sno = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    user_phone = db.Column(db.String(120), nullable=False)
    user_email = db.Column(db.String(200), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)

class Pending_Requests(db.Model):

    __bind_key__ = 'users'
    __tablename__ = 'pending_requests'

    email = db.Column(db.String(200), nullable=False , primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    user_phone = db.Column(db.String(15), nullable=False)
    user_role = db.Column(db.String(20), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_otp = db.Column(db.Integer, nullable=False )

class Forgot_password_otp(db.Model):
    
    __bind_key__ = 'users'
    __tablename__ = 'forgot_password'

    email = db.Column(db.String(200), nullable=False , primary_key=True)
    otp = db.Column(db.Integer, nullable=False)

class Forgot_password_urls(db.Model):
    
    __bind_key__ = 'users'
    __tablename__ = 'forgot_pass_urls'

    url = db.Column(db.String(100), nullable=False , primary_key=True)
    email = db.Column(db.String(200), nullable=False)

class Change_password_post(db.Model):
    
    __bind_key__ = 'users'
    __tablename__ = 'change_password_post'

    url = db.Column(db.String(100), nullable=False , primary_key=True)
    email = db.Column(db.String(200), nullable=False)

class Change_password_urls(db.Model):

    __bind_key__ = 'users'
    __tablename__ = 'change_pass_urls'

    url = db.Column(db.String(100), nullable=False , primary_key=True)



# For Media Files -----

class Media_Files_Images(db.Model):
    
    __bind_key__ = 'media_files'
    __tablename__ = 'images'


    url = db.Column(db.String(8), nullable=False , primary_key=True)
    file = db.Column(db.String, nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    mimetype = db.Column(db.String, nullable=False)
    date = db.Column(db.String(10), nullable=False)

class Media_Files_Pdfs(db.Model):
    
    __bind_key__ = 'media_files'
    __tablename__ = 'pdfs'


    url = db.Column(db.String(8), nullable=False , primary_key=True)
    file = db.Column(db.String, nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    mimetype = db.Column(db.String, nullable=False)
    date = db.Column(db.String(10), nullable=False)

class Media_Files_Audios(db.Model):
    
    __bind_key__ = 'media_files'
    __tablename__ = 'audios'


    url = db.Column(db.String(8), nullable=False , primary_key=True)
    file = db.Column(db.String, nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    mimetype = db.Column(db.String, nullable=False)
    date = db.Column(db.String(10), nullable=False)

class Media_Files_Videos(db.Model):
    
    __bind_key__ = 'media_files'
    __tablename__ = 'videos'


    url = db.Column(db.String(8), nullable=False , primary_key=True)
    file = db.Column(db.String, nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    mimetype = db.Column(db.String, nullable=False)
    date = db.Column(db.String(10), nullable=False)

class Media_Files_Docs(db.Model):
    
    __bind_key__ = 'media_files'
    __tablename__ = 'docs'


    url = db.Column(db.String(8), nullable=False , primary_key=True)
    file = db.Column(db.String, nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    mimetype = db.Column(db.String, nullable=False)
    date = db.Column(db.String(10), nullable=False)


#=======================Database Classes==================================



#=========================================================================

# Main Helper functions -----

@login_manager.user_loader
def load_user(details):
    
    user_id = details["user"]
    user_role = details["role"]    

    user_name , email = ls.get_user_details(Students , Teachers , user_role , user_id)

    if user_name == None:
        return

    return ls.User(user_name , email , user_role, user_id)


@app.errorhandler(404) 
def not_found(e): 
    return render_template("404.html")


# To display classes in nav bar ----
def get_nav_classes(user):
    
    if user.role == "Teacher":
        classes = uc.get_more_info_classes(user.email)
        if classes == "Problem In Contacting":
            fe.server_contact_error()
            return "Problem"

    else:

        classes = uc.get_user_classes(user.email)
        if classes == "Problem In Contacting":
            fe.server_contact_error()
            return "Problem"    

# For chats

@app.route("/upload" , methods = ["POST"])
def upload():


    file = request.files.get("image")
    # print(request.form.get("date"))

    upload_image = mf.upload_image_file(file , Media_Files_Images , db , 15 , request)

    return jsonify(upload_image)

@app.route("/images/<string:slug>" , methods=["GET","POST"])
def get_img(slug):

    img_details = mf.reterive_img_file(slug , Media_Files_Images)
    if img_details:
    #    return Response(*img_details[:2] , mimetype=img_details[2])
        return send_file(BytesIO(img_details[0]) , attachment_filename=img_details[1] , as_attachment=True)

@app.route("/get-images/<string:slug>")
def get_image_back(slug):
    return render_template("test2.html" , slug = slug)





#=========================================================================

# For login and signup pages --------

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect("/")
    if(request.method=='POST'):
        name = request.form.get('name')

        if name == None or name == "":
            fe.some_went_wrong()
            return redirect("/signup")        

        if name=="option1":
            value="/signup-student"
            value1="true"

        elif name=="option2":

            value="/signup-teacher"
            value1="true"
    else:
        value1="false"
        value="/signup"
    
    return render_template("signup.html", params=value , params2=value1)

@app.route("/signup-student" , methods = ['GET','POST'])
def signup_student():
    if current_user.is_authenticated:
        return redirect("/")
    
    if request.method == 'POST':

        name,phone_no,email,password = si.get_values(request , 'name' , 'phone' , 'email' , 'password')

        if None in (name,phone_no,email,password) or "" in (name,phone_no,email,password) :
            fe.some_went_wrong()
            return redirect("/signup-student")

        if not (bool(re.match(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" , password))):
            fe.some_went_wrong()
            return redirect("/signup-student")


        account_presence = si.check_in_t_db(name , phone_no , email , request.path , "St_wi_pass", Students , Teachers , db , params , session)

        if  account_presence != None:
            return account_presence   

        mail_otp = si.send_verify_mail(name,phone_no,email,mail,params,"St_wi_pass",session)

        if mail_otp == None:
            return redirect(request.path)

        si.add_pd_req(email,name,phone_no,password,mail_otp,"Student",Pending_Requests,db,request.path,session,"St_wi_pass")

        session["student-otp-verification"] = email
        return redirect(request.path)

    if "St_wi_pass" in session:
        values = session["St_wi_pass"]
        session.pop('St_wi_pass', None)

    else:
        values = {"name":"",
            "phone": "",
            "email" : ""}

    if 'student-otp-verification' in session:
        to_return =   render_template("otp-verification.html" , email = session["student-otp-verification"] , role = "student")
        session.pop('student-otp-verification')

        return to_return

    return render_template("signup-student.html" , values = values )

@app.route("/signup-teacher" , methods = ['GET',"POST"])
def signup_teacher():
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
    
        name,phone_no,email,password = si.get_values(request , 'name' , 'phone' , 'email' , 'password')

        if None in (name,phone_no,email,password) or "" in (name,phone_no,email,password) :
            fe.some_went_wrong()
            return redirect("/signup-student")

        if not (bool(re.match(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" , password))):
            fe.some_went_wrong()
            return redirect("/signup-student")
        
        account_presence = si.check_in_t_db(name , phone_no , email , request.path , "t_wi_pass" , Students , Teachers , db , params , session)

        if  account_presence != None:
            return account_presence        
            
        mail_otp = si.send_verify_mail(name,phone_no,email,mail,params,"t_wi_pass",session)

        if mail_otp == None:
            return redirect(request.path)

        
        si.add_pd_req(email,name,phone_no,password,mail_otp,"Teacher",Pending_Requests,db,request.path , session , "t_wi_pass")
        session["teacher-otp-verification"] = email

        return redirect(request.path)

    if "t_wi_pass" in session:
        values = session["t_wi_pass"]
        session.pop('t_wi_pass', None)

    else:
        values = {"name":"",
            "phone": "",
            "email" : ""}

    if 'teacher-otp-verification' in session:
        to_return =   render_template("otp-verification.html" , email = session["teacher-otp-verification"] , role = "teacher")
        session.pop('teacher-otp-verification')

        return to_return

    return render_template("signup-teacher.html" , values = values )

@app.route("/signup-student/otp-verification/<string:slug>" , methods = ['POST'])
def signup_student_verification(slug):
    if current_user.is_authenticated:
        return redirect("/")
    main_path = "signup_student"
    db_row = si.get_signup_info(Pending_Requests , slug)

    if db_row == None:
    
        fe.some_went_wrong()
        return redirect(url_for(main_path))

    if db_row == "Problem In contacting!":
        session["student-otp-verification"] = slug
        return redirect(url_for(main_path))

    user_role = db_row.user_role
    if user_role != "Student":
        fe.some_went_wrong()
        return redirect(url_for(main_path))

    name , email , password , phone_no = db_row.user_name , db_row.email , db_row.user_password , db_row.user_phone 

    account_presence = si.acc_presence(main_path , email , Students  , Teachers , db , session , "student-otp-verification")
            
    if  account_presence != None:
        return account_presence   

    if request.method == "POST":
    
        otp = db_row.user_otp 

        value = request.form.get("otp_value")

        if str(otp) == value:
    

            add_details = si.add_account(db , Students , name , phone_no , email , password , url_for , db_row , session , main_path , slug)

            if add_details != None:    
                session["student-otp-verification"] = slug
                return add_details

            else:
                return redirect(url_for("login"))

        else:
            fe.incorrect_otp()
            session["student-otp-verification"] = slug
    
    return  redirect(url_for(main_path))

@app.route("/signup-teacher/otp-verification/<string:slug>" , methods = ['POST'])
def signup_teacher_verification(slug):
    if current_user.is_authenticated:
        return redirect("/")
    main_path = "signup_teacher"
    db_row = si.get_signup_info(Pending_Requests , slug)

    if db_row == None:
        fe.some_went_wrong()
        return redirect(url_for(main_path))

    if db_row == "Problem In contacting!":
        session["teacher-otp-verification"] = slug
        return redirect(url_for(main_path))

    user_role = db_row.user_role
    if user_role != "Teacher":
        fe.some_went_wrong()
        return redirect(url_for(main_path))

    name , email , password , phone_no = db_row.user_name , db_row.email , db_row.user_password , db_row.user_phone 

    account_presence = si.acc_presence(main_path , email , Students  , Teachers , db , session , "teacher-otp-verification")
            
    if  account_presence != None:
        return account_presence   

    if request.method == "POST":
    
        otp = db_row.user_otp   

        value= request.form.get("otp_value")

        if str(otp) == value:

            add_details = si.add_account(db , Teachers , name , phone_no , email , password , url_for , db_row , session , main_path , slug)

            if add_details != None:    
                session["teacher-otp-verification"] = slug
                return add_details

            else:
                return redirect(url_for("login"))

        else:
            fe.incorrect_otp()
            session["teacher-otp-verification"] = slug
    
    return  redirect(url_for(main_path))

@app.route("/otp-verification/resend/<string:slug>" , methods = ["POST"])
def resend_user_verification_otp(slug):
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "GET":
        return redirect(url_for("signup"))
    
    db_row = si.get_signup_info(Pending_Requests , slug)

    if db_row == None:
        return "Problem"

    if db_row == "Problem In contacting!":
        return "Problem"

    otp = db_row.user_otp
    mail_send = si.resend_otp(mail , slug , otp , params)

    if mail_send == None:
        return "Problem"

    return "Successfull"

@app.route("/login" , methods = ["POST", "GET"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user_account , role = ls.find_account(email , Students
         , Teachers)

        if user_account == None or user_account == "Problem in contacting":
            session["log-details"] = email
            return redirect(request.path)

        user_acc_pass = user_account.user_password
        if user_acc_pass != password:
            fe.login_err()
            session["log-details"] = email
            return redirect(request.path)

        user_name = user_account.user_name
        user_email = user_account.user_email
        user_id = user_account.sno
        user_to_log = ls.User(user_name , user_email , role, user_id)

        login_user(user_to_log)
        fs.login_success()

        return redirect(url_for("index"))

    if "log-details" in session:
        return_email = session["log-details"]
        session.pop("log-details")
    else:
        return_email = ""
    return render_template("login.html" , email = return_email)

@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


# Forget Password -------

@app.route("/login/forget-password"  , methods = ["POST" , "GET"])
def forget_password():
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        email = request.form.get("email")

        if email == None or email == "":
            fe.some_went_wrong()
            return redirect("/login/forget-password")

        check_acc = ls.check_user_acc(Students , Teachers , email , session , "fg-details" , request.path)

        if check_acc != None:
            return check_acc

        mail_otp = ls.send_forg_pass_otp_verify_mail(mail , email , params , session , "fg-details")

        if mail_otp == None:
            return redirect(request.path)

        add_req = ls.add_forg_pass_req(Forgot_password_otp , db , email, mail_otp , request.path , session , "fg-details")

        if add_req != None:
            return add_req

        session["forget-password-email"] = email
        return redirect(request.path)

    if "forget-password-email" in session:
        to_return = render_template("forget-password-verify-otp.html" , email = session["forget-password-email"])
        session.pop("forget-password-email")
        return to_return

    if "fg-details" in session:
        return_email = session["fg-details"]
        session.pop("fg-details")
    else:
        return_email = ""

    return render_template("forget-password-email.html" , email = return_email)

@app.route("/login/forget-password/check-otp/<string:slug>" ,methods = ["POST"])
def forget_pass_check_otp(slug):
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "GET":
        return redirect(url_for("forget_password"))
    email = slug
    account = ls.find_forg_req(Forgot_password_otp, email)

    if account == None:
        fe.some_went_wrong()
        return redirect(url_for("forget_password"))

    if account == "Problem In contacting":
        session["forget-password-email"] = email
        return redirect(url_for('forget_password'))

    user_otp = request.form.get("otp_value")

    otp = str(account.otp)

    if user_otp != otp:

        fe.incorrect_otp()
        session["forget-password-email"] = email
        return redirect(url_for('forget_password'))

    url = ls.add_url_to_dbs(db,Forgot_password_urls,Change_password_urls,email)
    ls.del_entry(db,Forgot_password_otp,email)


    if url == None:
        fe.server_contact_error()
        session["forget-password-email"] = email
        return redirect(url_for('forget_password'))

    session["forget-password-change-email"] = email
    return redirect("/login/forget-password/" + str(url))


@app.route("/login/forget-password/<string:slug>" , methods = ["GET" , "POST"])
def forgot_change_password(slug):
    if current_user.is_authenticated:
        return redirect("/")

    url = slug
    if request.method == "POST":

        email = ls.find_post_url(Change_password_post,url)

        if email in (None , "Problem In Contacting"):
            return redirect(url_for('forget_password'))

        password = request.form.get("password")
        
        if not (bool(re.match(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" , password))):
            url_entry = ls.add_custom_url_to_db(db , Forgot_password_urls , url,email )
            if url_entry != None:
                return redirect(url_for('forget_password'))
            fe.some_went_wrong()
            session["forget-password-change-email"] = email
            return redirect(request.path)

        account , role = ls.search_acc_in_dbs(Students,Teachers,email) 
        if account == None:
            fe.some_went_wrong()
            return redirect(url_for('forget_password'))

        if password == account.user_password:

            url_entry = ls.add_custom_url_to_db(db , Forgot_password_urls , url,email )
            if url_entry != None:
                return redirect(url_for('forget_password'))
            fe.same_pass_err()
            session["forget-password-change-email"] = email
            return redirect(request.path)
        
        ch_pass = ls.change_password(db,Students,Teachers,account,password,role)

        if ch_pass != None:
            return redirect(url_for('forget_password'))

        ls.del_entry(db,Change_password_post,email)

        fs.ch_pass_success()
        return redirect(url_for("login"))

        
    url_pressence = ls.find_forg_pass_ch_url(Forgot_password_urls , url)

    if url_pressence in ("Problem In Contacting" , None) :
        return redirect(url_for('forget_password'))

    if "forget-password-change-email" in session:
        session_email = session["forget-password-change-email"]
        session.pop("forget-password-change-email")
    else:
        return redirect(url_for('forget_password'))
    
    if session_email != url_pressence.email:
        return redirect(url_for('forget_password'))

    del_entry = ls.delete_url_entry(db ,Forgot_password_urls , url)
    if del_entry != None:
        return redirect(url_for('forget_password'))

    post_entry = ls.add_entry_to_post_db(Change_password_post,session_email,url,db)

    if post_entry != None:
        return redirect(url_for('forget_password'))    

    return render_template("change-password.html", slug = url)

@app.route("/login/forget-password/otp-resend/<string:slug>",methods = ["POST"])
def resend_foget_pass_verify_otp(slug):
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "GET":
        return  redirect(url_for("forgot_password"))
    
    email = slug
    acc  = ls.find_forg_req(Forgot_password_otp, email)

    if acc in (None, "Problem In contacting"):
        return "Problem"
    otp = acc.otp
    send_otp = ls.resend_forg_pass_otp_verify_mail(mail,email,params,otp)

    if send_otp == None:
        return "Problem"

    return "Successfull"

#=========================================================================





#=========================================================================

# For Managing classes pages (Creating , Requesting etc. ) --------

@login_required
@app.route("/create-class" , methods = ["POST", "GET"] )
def create_class():
    # print("request")
    if current_user.role == 'Teacher':

        if request.method == 'POST':

            cls_name = request.form.get('name')
            std = request.form.get("Standard")
            desp = request.form.get("description")

            if None in (cls_name , std) or "" in (cls_name , std) :
                fe.some_went_wrong()
                return redirect("/create-class")
            
            create_class_request = uc.create_new_class(current_user.email, cls_name, current_user.name, std, desp)

            
            if create_class_request == None :
                return redirect(url_for(f"/create-class"))
            
            else:
                fs.create_class()
                return redirect((f"/class/{create_class_request}"))
        
        return render_template("create_class.html"  )
    
    else:
        return render_template("404.html")

@login_required
@app.route("/join-class" , methods = ["POST" , "GET"] )
def req_join_class():
    if current_user.role == 'Student':
        
        if request.method == 'POST':
            cls_id = request.form.get("id")

            # print(cls_id)
            if cls_id == None or cls_id == "":
                fe.some_went_wrong()
                return redirect("/join-class")
            # print(cls_id)
            join_class_request = uc.add_joining_req(current_user.email, current_user.name, cls_id)

            if join_class_request in ("Problem In Contacting" , "No class found" , "Already Joined" , "Already Requested", "Max Joined" ):
                return render_template("join_class.html"  )
            
            fs.join_req_class()
            return redirect(url_for('index'))
        
        return render_template("join_class.html" )
    else:
        return render_template("404.html")


#=========================================================================





#=========================================================================

# For index page ------

@app.route("/")
def index():
    if current_user.is_authenticated:

        # Class Cards to display in main element ---
        class_cards = uc.get_class_cards(current_user.email)

        if class_cards == "Problem In Contacting":
            fe.server_contact_error()
            return render_template("home.html" , get_class_cards = ([]) )

        return render_template("home.html" , get_class_cards = class_cards  )

    return redirect("/login")

#=========================================================================




#=========================================================================

# For each individual class --------

@app.route("/get-class-name/" ,  methods = ["POST"])
@login_required
def class_name():
    return jsonify(uc.get_class_name(request.form.get("class_id")))


"""---------------------------------------------------------------------"""


# Home Page -----

@login_required
@app.route("/class/<string:slug>")
def class_home_page(slug):

    cls_name = uc.get_class_name(slug)

    if uc.get_class_name(slug) == None or current_user.email not in uc.get_participants_email(slug):
        return render_template("404.html")

    clswrks = ch.get_all_classworks(slug , current_user.email)
    # print(clswrks)
    meetings = ""

    return render_template("class_template/class_work.html", href_window = slug , tittle = cls_name , classworks = clswrks , meetings = meetings)



# Classwork functions ---------------------------------------------------------------------

@login_required
@app.route("/class/<string:classid>/add-new-classwork" , methods = ["POST"])
def add_new_classwork(classid):



    if current_user.role != 'Teacher':
        fe.some_went_wrong()
        return jsonify("index")

    if uc.get_class_name(classid) == None or current_user.email not in uc.get_participants_email(classid):
        fe.some_went_wrong()
        return redirect(f"/class/{classid}")

    pdf_file = request.files.get("pdf_file")
    class_work_name = request.form.get("class_work_name")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")

    if None in (pdf_file.filename , class_work_name , start_time , end_time) or "" in (pdf_file.filename , class_work_name , start_time , end_time , request):
        fe.some_went_wrong()
        return redirect(f"/class/{classid}")

    classwork_upload_status = ch.insert_new_classwork(classid , class_work_name, pdf_file , start_time , end_time , db , Media_Files_Pdfs)

    if classwork_upload_status == "Problem In Contacting":
        fe.server_contact_error()
        return redirect(f"/class/{classid}")

    if classwork_upload_status == "fi":
        return redirect(f"/class/{classid}")

    fs.clswrk_uploaded()
    return redirect(f"/class/{classid}")

@login_required
@app.route("/class/<string:data>/delete" , methods = ["POST"])
def delete_classwork(data):

    if current_user.role != "Teacher":
        return render_template("404.html")

    try:
        classid , clswrk_id = data.split("&")
    except Exception:
        return render_template("404.html")

    if uc.get_class_name(classid) == None or current_user.email not in uc.get_participants_email(classid):
        fe.some_went_wrong()
        return redirect(f"/class/{classid}")
    
    ch.del_clswrk(classid, clswrk_id)

    

    fs.clswrk_deleted()
    return redirect(f"/class/{classid}")



@login_required
@app.route("/class/<string:classid>/submit-classwork" , methods = ["POST"])
def add_st_wrk(classid):

    if current_user.role != "Student":
        fe.some_went_wrong()
        return redirect(f"/class/{classid}")

    if uc.get_class_name(classid) == None or current_user.email not in uc.get_participants_email(classid):
        fe.some_went_wrong()
        return redirect(f"/class/{classid}")
    
    pdf_file = request.files.get("pdf_file")
    classwork_id = request.form.get("pdf_file_url")

    if None in (pdf_file.filename , classwork_id) or "" in (pdf_file.filename , classwork_id) :
        fe.some_went_wrong()
        return redirect(f"/class/{classid}")

    add_wrk = ch.add_student_work(pdf_file , Media_Files_Pdfs , db , classid , current_user.email , classwork_id)

    if add_wrk != None  :
        return redirect(f"/class/{classid}")
    fs.student_wrk_upload()
    return redirect(f"/class/{classid}")

    

# Function to view the work submitted by the students...

@login_required
@app.route("/class/classwork-submitted/<string:data>")
def get_classwork_submission_details(data):

    if current_user.role != "Teacher":
        return render_template("404.html")

    try:
        classid , clswrk_id = data.split("&")
    except Exception:
        return render_template("404.html")
    title = uc.get_class_name(classid)

    if uc.get_class_name(classid) == None or current_user.email not in uc.get_participants_email(classid):
        return render_template("404.html")

    submission_details = ch.get_all_st_submitted_wrk(classid , clswrk_id)

    if submission_details == "No Classwork Found":
        return render_template("404.html")

    if submission_details == "Problem In Contacting":
        redirect(f"/class/{classid}")

    participants = uc.get_participants_dict(classid)

    if participants == "Problem In Contacting":
        redirect(f"/class/{classid}")

    return render_template("class_template/classwork_submission_details.html" , href_window = data, st_email_li = list(submission_details[0]) , st_pdf = submission_details[1] , participants = participants, class_name = submission_details[2], title = title, cls_id = clswrk_id, id = classid)



@login_required
@app.route("/class/classwork/pdf/<string:url>", methods = ['POST'])
def get_wrk_pdf(url):

    classid = request.form.get("classid")
    classsno = request.form.get("class_sno")
    if uc.get_class_name(classid) == None or current_user.email not in uc.get_participants_email(classid):
        fe.some_went_wrong()
        return "error"
    
    pdf_details = mf.reterive_pdf_file(url , Media_Files_Pdfs)

    if pdf_details:
        print(pdf_details)
        return send_file(BytesIO(pdf_details[0].encode()) , download_name=pdf_details[1] , as_attachment=True , mimetype=pdf_details[2])

    else:
        fe.no_file_fnd()
        return jsonify("fnf")



# For Teacher (Using AJAX) ---------------------------------------------


@login_required
@app.route("/class/delete-class" , methods = ["POST"])
def delete_class():
    # Only for ajax --

    if current_user.role == 'Teacher':

        classid = request.form.get('id')

        if uc.get_class_name(classid) == None or current_user.email not in uc.get_participants_email(classid):
            fe.some_went_wrong()
            return "swr"

        del_class = uc.delete_class(classid)
        if del_class == "Problem In Contacting":
            fe.server_contact_error()
            return "Problem"
        fs.delete_class()
        return jsonify(None)
    else:
        fe.dnt_have_access()
        return jsonify(None)


"""---------------------------------------------------------------------"""


# Discussion Page ----

@app.route("/class/<string:slug>/discuss")
@login_required
def class_discuss_page(slug):

    cls_name = uc.get_class_name(slug)

    if cls_name == None or current_user.email not in uc.get_participants_email(slug) :
        return render_template("404.html")

    return render_template("class_template/chat.html" , href_window = slug, old_chats = cc.get_class_chats(slug)   , tittle = cls_name , participants = uc.get_participants(slug))


@socketio.on('join_room')
def handle_join_room_event(data):

    room_url = data["room"]
    classid = room_url[:15]
    # print("printing")
    # print(room_url)
    # print(classid)

    if uc.get_class_name(classid) == None or current_user.email not in uc.get_participants_email(classid):
        fe.some_went_wrong()
        return "swr"
    print("room joined")
    join_room(classid)


@socketio.on('send_message')
def handle_send_msg_event(data):

    room_url = data["room"]
    classid = room_url[:15]
    msg_type = data["type"]


    if uc.get_class_name(classid) == None or current_user.email not in uc.get_participants_email(classid):
        fe.some_went_wrong()
        return "swr"


    add_msg = cc.add_message(classid, current_user.email, current_user.name , data , msg_type, db , Media_Files_Images , Media_Files_Pdfs , Media_Files_Videos , Media_Files_Audios , Media_Files_Docs)
    if add_msg in ("Problem In Contacting" , "fi" , "swr"):
        return "swr"
    
    socketio.emit('recieve_krle', (add_msg) , room = classid)

@app.route("/chat/image/<string:url>" , methods = ["POST"])
def get_image_response(url):

    # Used to reterive the image in chats

    img_file_details = mf.reterive_chat_media_file("image" , url , img_class = Media_Files_Images)
    

    if img_file_details:
       return Response(*img_file_details[:2] , mimetype = img_file_details[2])

    else:
        return jsonify(None)


@app.route("/chat/media-file/<string:data>" , methods = ["POST"])
def download_media_file(data):

    # Used to reterive the image in chats

    try:
        media_type , url = data.split("&")
    except Exception:
        return jsonify(None)

    
    file_details = mf.reterive_chat_media_file(media_type , url , pdf_class= Media_Files_Pdfs , img_class = Media_Files_Images , audio_class= Media_Files_Audios , video_class= Media_Files_Videos ,doc_class = Media_Files_Docs)

    if file_details:
        return send_file(BytesIO(file_details[0]) , attachment_filename = file_details[1] , as_attachment = True , mimetype = file_details[2])

    else:
        return jsonify(None)



"""---------------------------------------------------------------------"""


# Participant Page ------

@app.route("/class/<string:slug>/participants")
@login_required
def class_participant_page(slug):

    cls_name = uc.get_class_name(slug)

    if cls_name == None or current_user.email not in uc.get_participants_email(slug):
        return render_template("404.html")

    participants = uc.get_participants(slug)

    if current_user.role == "Teacher":

        pending_requests = uc.get_join_req(slug)
        return render_template("class_template/participants.html", pending_student = pending_requests , href_window = slug , participants = participants  , title = cls_name)

    else:
        return render_template("class_template/participants.html" , href_window = slug , participants = participants   , tittle = cls_name)



# For Teacher only (Using Ajax) ----------------------------------------- 

@login_required
@app.route("/class/pending-request/approve" , methods = ["POST"])
def approve_class_join_req():
    if current_user.role == 'Teacher':

        classid = request.form.get('id')
        # print(classid)

        if uc.get_class_name(classid) == None or current_user.email not in uc.get_participants_email(classid):
            fe.some_went_wrong()
            return "swr"

        app_req = uc.approve_request(request.form.get('student_email'), classid)
        # print("add_req")

        if app_req in ("Problem In Contacting" , "Request Not Found" , "Max joined" , "Max Participants" , "Already Joined"):
            return "redirect"

        fs.approve_request()
        return "redirect"
    else:
        fe.dnt_have_access()


@login_required
@app.route("/class/pending-request/decline" , methods = ["POST"])
def decline_class_join_req():
    if current_user.role == 'Teacher':

        classid = request.form.get('id')

        if uc.get_class_name(classid) == None or current_user.email not in uc.get_participants_email(classid):
            fe.some_went_wrong()
            return "swr"
        
        dec_req = uc.decline_request(classid, request.form.get('student_email'))
        if dec_req == "Problem In Contacting":
            return "Problem"

        fs.decline_request()
        return jsonify(None)
    else:
        fe.dnt_have_access()


@login_required
@app.route("/class/remove-student/" , methods = ["POST"])
def remove_student():
    if current_user.role == 'Teacher':

        classid = request.form.get('url')

        if uc.get_class_name(classid) == None or current_user.email not in uc.get_participants_email(classid):
            fe.some_went_wrong()
            return "swr"


        rmv_st = uc.remove_student(classid, request.form['email'] , "HOST")
        if rmv_st == "Problem In Contacting":
            return jsonify(rmv_st)
        fs.remove_student()
        return jsonify(None)

    else:
        fe.dnt_have_access()



# For Student (Using Ajax) ----------

@login_required
@app.route("/class/leave-class/" , methods = ["POST"])
def leave_class():
    if current_user.role == 'Student':

        classid = request.form.get('url')

        if uc.get_class_name(classid) == None or current_user.email not in uc.get_participants_email(classid):
            fe.some_went_wrong()
            return "swr"

        rmv_st = uc.remove_student(classid, current_user.email , "SELF")
        if rmv_st == "Problem In Contacting":
            return jsonify(rmv_st)
        fs.leave_class()
        return jsonify(None)

    else:
        fe.dnt_have_access()


#--------------------------------------------------------------------------        

"""---------------------------------------------------------------------"""


#=========================================================================




#--------------------------------------------------------------------------

@login_required
@app.route("/get-class-cards" , methods = ['POST'])
def get_class_cards():
    class_cards = uc.get_class_cards(current_user.email)
    if class_cards == "Problem In Contacting":
        fe.server_contact_error()
        return "Problem"

    return jsonify(class_cards)


# For Nav bars ------

@login_required
@app.route("/get-teacher-classes" , methods = ["POST"])
def get_teacher_classes():
    classes = uc.get_more_info_classes(current_user.email)
    if classes == 'Problem In Contacting':
        classes = "Problem"
    return jsonify(classes)

@login_required
@app.route("/get-student-classes" , methods = ["POST"])
def get_student_classes():
    classes = uc.get_user_classes(current_user.email)
    if classes == 'Problem in contacting':
        classes = "Problem"
    return jsonify(classes)


@app.route("/get-class-chats/" , methods = ['POST'])
@login_required
def get_old_chats():
    classid = request.form.get('id')
    if uc.get_class_name(classid) == None or current_user.email not in uc.get_participants_email(classid):
        fe.some_went_wrong()
        return "swr"
    
    messages = cc.get_class_chats(classid)
    return jsonify(messages)


@app.route("/get-participants", methods = ["POST"])
@login_required
def get_participants():
    classid = request.form.get('id')
    if uc.get_class_name(classid) == None or current_user.email not in uc.get_participants_email(classid):
        fe.some_went_wrong()
        return "swr"

    participants = uc.get_participants(classid)

    return jsonify(participants)

@app.route("/test", methods = ['GET'])
def test():
    data = "string"
    data = jsonify(data)
    # print(data)
    return data

#************************************************************************

if __name__ == "__main__":


        
        socketio.run(app, debug=True)