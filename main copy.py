from flask import Flask, render_template, request, redirect , url_for, flash, session, jsonify, json, Response
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_socketio import SocketIO, join_room, leave_room
from flask_login import LoginManager , login_required , login_user , logout_user  , current_user
from flask_ngrok import run_with_ngrok
import numpy
import string
import flash_errors as fe
import flash_success as fs
import user_classes2 as uc


# hp = Null
with open("config.json") as json_file:
    params = json.load(json_file)

pdf_details = ""
pdf_details_mimetype = ""

app=Flask(__name__)
app.secret_key = "super-secret-key"
app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = params["local_host"]
db = SQLAlchemy(app)

# Binding both the databses to the sqlalchemy uri...
SQLALCHEMY_BINDS = {
    'classes':        'mysql://root:@localhost/classrooms',
    'users':        'mysql://root:@localhost/users'
}
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
run_with_ngrok(app)
#socketio = SocketIO(app)
# For sending Verification mail...
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params["verify-email-id"],
    MAIL_PASSWORD = params["verify-email-password"]
)
mail = Mail(app)

class User():
    
    def __init__(self,user_name,user_email,role,sno):
        self.name = user_name
        self.email = user_email
        self.role = role
        self.user_id = sno
        

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


@login_manager.user_loader
def load_user(details):

    user_id = details["user"]
    user_role = details["role"]    

    user_name = "Naitik"
    email = "codeswithnaitik@gmail.com"

    if user_name == None:
        return

    return User(user_name , email , user_role, user_id)


def check_in_t_db(name , phone_no , email , path ,session_var):
    check_in_datbase = None
    check_in_datbase2 = None

    if check_in_datbase != None or check_in_datbase2 != None:
        flash(("error",params["email-al-regis"]))
        values = {"name":name,
        "phone": phone_no,
        "email" : email}
        session[session_var] = values        

        return redirect(path)

    else:
        return None

def add_pd_req(email,name,phone_no,password,otp,role):
    
    pd_db_search = "yes"  

def send_verify_mail(user_email):

    try:
        otp = numpy.random.randint(11111,99999)
        mail.send_message(subject = "Otp Verification!",
        recipients= [user_email],
        sender= params["verify-email-id"],
        body = f"Your Email Verification Otp is {otp}"
        )
        return otp

    except Exception:
        return 909090

@app.route("/")
def index():
    class_cards = [{'class_name': "Madhav Hindi Class", 'classid': '03neblduab6u0fm', 'class_standard': '12 B', 'teacher': 'Madhav Agrawal'}, {'class_name': "Madhav Hindi Class", 'classid': '5uzgiwo2uvbobk0', 'class_standard': '12 B', 'teacher': 'Madhav Agrawal'}, {'class_name': "Madhav Hindi Class", 'classid': '5upgiwo2uab6u0fm', 'class_standard': '12 B', 'teacher': 'Madhav Agrawal'}, {'class_name': "Madhav Hindi Class", 'classid': '52uab6u0fm', 'class_standard': '12 B', 'teacher': 'Madhav Agrawal'}, {'class_name': "Madhav Hindi Class", 'classid': '5upg2uab6u0fm', 'class_standard': '12 B', 'teacher': 'Madhav Agrawal'}, {'class_name': "Madhav Hindi Class", 'classid': '5upg2uab6u0fm', 'class_standard': '12 B', 'teacher': 'Madhav Agrawal'}, {'class_name': "Madhav Hindi Class", 'classid': '5upg2uab6u0fm', 'class_standard': '12 B', 'teacher': 'Madhav Agrawal'}, {'class_name': "Madhav Hindi Class", 'classid': '5upg2uab6u0fm', 'class_standard': '12 B', 'teacher': 'Madhav Agrawal'}]
    if current_user.is_authenticated:
        return render_template("home.html", get_class_cards = class_cards)
    return redirect("/login")

@app.route("/signup", methods = ['GET', 'POST'])
def signup():

    if(request.method=='POST'):
        name = request.form.get('name')

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
    
    if request.method == 'POST':
        
        """ Gets all the values from the form of the HTML..."""
        name = request.form.get('name')
        phone_no = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')

        account_presence = check_in_t_db(name , phone_no , email , request.path , "St_wi_pass")
        if  account_presence != None:
            return account_presence      
                   

        mail_otp = send_verify_mail(email)
        if mail_otp == None:

            flash(("error","There was some problem in sending the otp to your Email!"))

            redirected = redirect(request.path)

            values = {"name":name,
            "phone": phone_no,
            "email" : email}

            session["st_wi_pass"] = values 
            return redirected
        
        add_pd_req(email,name,phone_no,password,mail_otp,"Student")


        return render_template("otp-verification.html",email = email , role = "student")

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
    if request.method == 'POST':
    
        """ Gets all the values from the form of the HTML..."""
        name = request.form.get('name')
        phone_no = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        
        account_presence = check_in_t_db(name , phone_no , email , request.path , "t_wi_pass")
        if  account_presence != None:
            return account_presence        
            
        mail_otp = send_verify_mail(email)
       
        add_pd_req(email,name,phone_no,password,mail_otp,"Teacher")
        
        return render_template("otp-verification.html",email = email , role = "teacher")

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

@app.route("/signup-student/otp-verification/<string:slug>" , methods = ['GET', 'POST'])
def signup_student_verification(slug):

    presence = "true"
    if presence == None:
        return redirect(url_for("signup_teacher"))

    if request.method == "POST":
    
        otp = 55555

        num1 = request.form.get('num1')
        num2 = request.form.get('num2')
        num3 = request.form.get('num3')
        num4 = request.form.get('num4')
        num5 = request.form.get('num5')

        value= str(num1) + str(num2)  + str(num3) + str(num4) + str(num5)

        if str(otp) == value:

            name = "Naitik"
            email = "pawanagrawal1217@gmail.com"
            password = "Papamummy143@"
            phone_no = 9412550789
            user_role = "Teacher"
            user_role = user_role.lower()

            account_presence = check_in_t_db(name , phone_no , email , request.path ,"St_wi_pass")
            if  account_presence != None:
                return account_presence   

            if user_role != "student":
                return redirect(url_for("signup_student"))

            """If there is  no problem in creating a account...""" 

            flash (("good","Your account is successfully created! Kindly log in to your account."))            
            return redirect(url_for('login'))

        else:
            flash(("error","Otp is not correct! Please check it!"))
            session["teacher-otp-verification"] = slug
    
    return  redirect(url_for('signup_teacher'))

@app.route("/signup-teacher/otp-verification/<string:slug>" , methods = ['GET', 'POST'])
def signup_teacher_verification(slug):
    
    presence = "Yes"
    if presence == None:
        return redirect(url_for("signup_teacher"))


    if request.method == "POST":

        otp = 55555
        value= request.form.get("otp_value")

        if str(otp) == value:

            name = "Naitik"
            email = "pawanagrawal1217@gmail.com"
            password = "Papamummy143@"
            phone_no = 9412550789
            user_role = "Teacher"
            user_role = user_role.lower()

            account_presence = check_in_t_db(name , phone_no , email , request.path , "t_wi_pass")
            if  account_presence != None:
                return account_presence   

            if user_role != "teacher":
                return redirect(url_for("signup_student"))

            flash (("good","Your account is successfully created! Kindly log in to your account."))            
            return redirect(url_for('login'))

        else:
            flash(("error","Otp is not correct! Please check it!"))
            session["teacher-otp-verification"] = slug
    
    return  redirect(url_for('signup_teacher'))

@app.route("/get_user_value")
@login_required
def get_user_vale():
    return render_template("hello.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@login_required
def get_chats():
    messages = [{'id' : 1, 'msg_type':'msg_text', 'msg_details' :{'urls':['']}, 'participant_email' : "pawan1212@gmail.com" ,'message' : "Hello I am Fine", 'date-time' : "24-10-2020 12:12", 'send-to' : ['codeswithnaitik@gmail.com', 'pawan1212@gmail.com'], "participant_name":'Madhav'},{'id' : 2, "participant_name":'Madhav', 'participant_email' : "pawan1212@gmail.com" ,'msg_type':'msg_text', 'msg_details':{'urls':['']}, 'message' : "Hello I am Fine", 'date-time' : "24-10-2020 12:12", 'send-to' : ['codeswithnaitik@gmail.com', 'pawan1212@gmail.com'], "participant_name":'Madhav'}, {'id' : 2.5, 'participant_email' : "codeswithnaitik@gmail.com" ,'message' : "Hello am Fine", 'msg_type':'msg_text', 'msg_details':{'urls':['']}, 'date-time' : "14-4-2021 12:12", 'send-to' : ['codeswithnaitik@gmail.com', 'codeswithnaitik1234.com'], "participant_name":'Madhav'}, {'id' : 3, 'participant_email' : "codeswithnaitik1234" ,'message' : "Hello I am Fine", 'msg_type':'msg_text', 'msg_details':{'urls':['']}, 'date-time' : "27-10-2020 12:12", 'send-to' : ['rahul@gmail.com', 'madhav@gmail.com'], "participant_name":'Madhav'}, {"participant_email" : 'rahul@gmail.com' , "user_name" : 'rahul@gmail.com' , "msg_type" : 'msg_text', 'msg_details':{'urls':['https://auth.geeksforgeeks.org/user/ChinmoyLenka/articles']} , "message" : "My Profile: https://auth.geeksforgeeks.org/user/ChinmoyLenka/articles in the portal of http://www.geeksforgeeks.org/" , "participant_name":'Madhav','send-to' : ['codeswithnaitik@gmail.com', 'pawan1212@gmail.com'], 'date-time' : "24-10-2020 12:12"}]
    return messages

@app.route("/class/<string:slug>/discuss")
@login_required
def class_slug(slug):
    chat = get_chats()
    participants = get_participats()
    return render_template("class_template/chat.html",  tittle="Madhav's Math Class", href_window=slug, old_chats = chat, participants=participants)
@app.route("/class/<string:slug>/participants")
@login_required
def class_slug_chat(slug):
    hello = [{'email': "agrawalmadhav13@gmail.com", 'name': 'Madhav Agrawal', 'class_standard': '10 B', 'msg': 'Hello I am Madhav'} ,{'email': 'Naitik1789@gmail.com', 'name': 'Naitik', 'class_standard': '10 C', 'msg': 'Please Add Me !'} ,{'email': 'Naitik189@gmail.com', 'name': 'Naitik Agrawal', 'class_standard': '10 C', 'msg': 'Please Add Me !'}]

    participants = get_participats()
    return render_template("class_template/participants.html", pending_student=hello, tittle="Madhav's Math Class", href_window = slug, participants=participants)

@app.route("/class/<string:slug>")
@login_required
def class_slug_classwork(slug):
    classwork  = [{'pdf_file_url': 'tyuerecv', 'class_work_name': 'Classwork', 'start_date': '2021-04-26', 'end_date': '2021-04-16', 'classwork_id': '2', 'status': 1}, {'pdf_file_url': '1lkljhui', 'class_work_name': 'New Classwork1', 'start_date': '2021-04-26', 'end_date': '2022-05-06', 'classwork_id': '3', 'status': 0}, {'pdf_file_url': '1lkiutyv', 'class_work_name': 'Old', 'start_date': '2021-04-26', 'end_date': '2022-05-26', 'classwork_id': '3', 'status': 0}]
    return render_template("class_template/class_work.html", tittle="Madhav's Math Class", href_window=slug, classworks = classwork)

#@socketio.on('send_message')
#def send_mmm(data):
 #   app.logger.info(f"{data['username']} has  to the room {data['room']}")
  #  print('hello')
   # data['msg'] = data['message']
    #data.pop('message')
    #data['user_name'] = data['username']
    #data.pop('username')
    #data['user_email'] = data['useremail']
    #data.pop('useremail')
    #socketio.emit('recieve_krle', data, room=data['room'])


@login_required
def get_participats():
    party = {'teacher': {"name":'Naitik Agrawal', "email":'pawan1212@gmail.com'}, 'students': [{'name':"Lalit", "email":'codeswithnaitik1234@gmail.com'}, {'name':"Lalit", "email":'codeswithnaitik@gmail.com'}]}
    return party

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_name = "Name"
        user_email = "codeswithnaitik@gmail.com"
        user_id = "21"
        role = "Teacher"
        user_to_log = User(user_name , user_email , role, user_id)
        login_user(user_to_log)
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/get-class-name/" ,  methods = ["POST"])
@login_required
def class_name():
    return jsonify("Class Name")

@app.route("/login/otp-verification", methods = ['GET', 'POST'])
def login_verification():
    if request.method == "POST":
        return redirect(url_for('login_password'))

    return render_template("otp-login.html")

@app.route("/login/forget-password", methods = ['GET', 'POST'])
def login_password():
    if request.method == "POST":
        return render_template("change-password.html")
    return render_template("forget-password-email.html", email="pawan@gmail.com")

@app.route("/hello_o/", methods = ['GET', 'POST'])
def hello_o():
    mail_otp = send_verify_mail("pawanagrawal1217@gmail.com")
    if mail_otp == None:
        mail_otp = 'None'
    else:
        mail_otp = 'sucess'
    return jsonify({'data': mail_otp, 'email':"pawanagrawal1217"})


@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html")

@app.route("/get-messages" , methods = ["POST"])
def get_messages():
    hello = uc.get_user_classes('current_user')
    return jsonify(hello)

@login_required
@app.route("/join-class" , methods = ["GET", "POST"] )
def join_class():
    if current_user.role == 'Student':
        if request.method == 'POST':
            if current_user.role == 'Student':
                join_class_request = "Problem IN Contacting"
                if join_class_request == "Problem In Contacting":
                    fe.server_contact_error()
                    return render_template("join_class.html")
                elif join_class_request == "No class found":
                    fe.no_class_found()
                    return render_template("join_class.html")
                elif join_class_request == "Already Joined":
                    fe.already_joined()
                    return render_template("join_class.html")
                else:
                    fs.joined_class()
                    return redirect(url_for('join_class'))
        return render_template("join_class.html")
    else:
        return redirect(url_for('create_class'))
def create_class_table(email, name, name2, standard):
    # fe.server_contact_error()
    print(email)
    print(name)
    print(name2)
    print(standard)
    return "hwllo"

@login_required
@app.route("/create-class" , methods = ["GET", "POST"] )
def create_class():
    if current_user.role == 'Teacher':
        if request.method == 'POST':
            if current_user.role == 'Teacher':
                create_class_request = create_class_table(current_user.email, request.form.get('name'), current_user.name, request.form.get("Standard"))
                if create_class_request == "Problem In Contacting":
                    fe.server_contact_error()
                    return render_template("create_class.html")
                elif create_class_request == "No class found":
                    fe.no_class_found()
                    return render_template("create_class.html")
                elif create_class_request == "Already Joined":
                    fe.already_joined()
                    return render_template("create_class.html")
                elif create_class_request == None :
                    return render_template("create_class.html")
                else:
                    fs.create_class()
                    return redirect(url_for('index'))
        return render_template("create_class.html")
    else:
        return redirect(url_for('index'))

@app.route("/get-teacher-classes" , methods = ["POST"])
def get_teacher_classes():
    hello = [{'class_name': "Madhav History", 'classid': 'gipn3bcspn5wphm', 'class_standard':'10 B'},
    {'class_name': "Madhav's Maths Class", 'classid': 'mngfdhr54hjuyd6', 'class_standard':'10 B'}]
    return jsonify(hello)

@app.route("/get-student-classes" , methods = ["POST"])
def get_student_classes():
    hello = [{'class_name': "Madhav's History Class", 'classid': 'gipn3bcspn5wphm'},
    {'class_name': "Madhav's Maths Class", 'classid': 'mngfdhr54hjuyd6'}]
    return jsonify(hello)


@app.route("/get-class-cards" , methods = ['GET', 'POST'])
def get_class_cards():
    hp = [{'class_name': "Madhav's Hindi Class", 'classid': '03neblduab6u0fm', 'class_standard': '12 B', 'teacher': 'Madhav Agrawal'}, {'class_name': "Madhav's Hindi Class", 'classid': '5uzgiwo2uvbobk0', 'class_standard': '12 B', 'teacher': 'Madhav Agrawal'}, {'class_name': "Madhav's Hindi Class", 'classid': '5upgiwo2uab6u0fm', 'class_standard': '12 B', 'teacher': 'Madhav Agrawal'}, {'class_name': "Madhav's Hindi Class", 'classid': '52uab6u0fm', 'class_standard': '12 B', 'teacher': 'Madhav Agrawal'}, {'class_name': "Madhav's Hindi Class", 'classid': '5upg2uab6u0fm', 'class_standard': '12 B', 'teacher': 'Madhav Agrawal'}]
    to_return = ""
    if hp in (None , "Problem In Contacting"):
        to_return = None
    else:
        to_return = hp  
    return jsonify(to_return)

#@socketio.on('join_room')
#def handle_join_room_event(data):
#    app.logger.info(f"{data['username']} has joined the room {data['room']}")
#    join_room(data['room'])

@app.route("/pending/class/decline/", methods = ["POST"])
def pending_class():
    print(request.form['student_email'])
    if current_user.role == 'Teacher':
        hello = "hello I Ms "
        if hello in (None , "Problem In Contacting"):
            fe.server_contact_error()
            return jsonify("redirect")
        fs.decline_request()
        return jsonify("redirect")
    else:
        fe.have_acccess()

@app.route("/pending/class/approve/", methods = ["POST"])
def approve_class():
    if current_user.role == 'Teacher':
        hello = "hello I Ms "
        if hello in (None , "Problem In Contacting"):
            fe.server_contact_error()
        elif hello == "Already Joined":
            fe.already_joined()
        elif hello == "Request Not Found":
            fe.request_found()
        fs.accept_request()
        return jsonify('redirect')
    else:
        fe.have_acccess()

@app.route("/remove-student/", methods = ["POST"])
def remove_student():
    print(request.form['email'])
    if current_user.role == 'Teacher':
        hello = "hello I Ms "
        if hello in (None , "Problem In Contacting"):
            fe.server_contact_error()
            return jsonify('redirect nhi hn')
        return jsonify('redirect')
    else:
        hello = "hello I Ms "
        if hello in (None , "Problem In Contacting"):
            fe.server_contact_error()
        return jsonify('redirect2')
        
@app.route("/dismiss-class/" , methods = ["POST"])
def dismiss_class():
    if current_user.role == 'Teacher':
        hello = "hello I Ms "
        return jsonify('redirect')
    else:
        fe.have_acccess()
        return jsonify('redirect nhi krna hai')

@login_required
@app.route("/class/<string:classid>/add-new-classwork" , methods = ["POST"])
def add_new_classwork(classid):

    global pdf_details, pdf_details_mimetype
    pdf_file = request.files["pdf_file"]
    print(request.files.get("pdf_file"))
    class_work_name = request.form.get("class_work_name")
    start_time = request.form.get("start_time")
    pdf_details = pdf_file.read(), pdf_file.filename
    pdf_details_mimetype = pdf_file.mimetype
    print(pdf_file.mimetype)

    return redirect("/class/classwork/pdf/url")


@login_required
@app.route("/class/classwork/pdf/<string:url>" , methods = ["Get", "POST"])
def get_wrk_pdf(url):

    # Used to reterive the image in chats
    

    if pdf_details:
        print(Response(pdf_details[:2] , mimetype=pdf_details_mimetype))
        return Response(pdf_details[:2] , mimetype=pdf_details_mimetype)

    else:
        return jsonify(None)

@login_required
@app.route("/class/<string:classid>/submit-classwork" , methods = ["GET", "POST"])
def add_st_wrk(classid):
    # Using Ajax --
    print(classid)
    pdf_file = request.files['pdf_file']
    print(pdf_file.filename)
    print(request.form.get("pdf_file_url"))

    add_wrk = True

    if add_wrk != None  :
        return "swr"
    return jsonify(None)


if __name__ == "__main__":
    Flask.run(app, debug = True)
