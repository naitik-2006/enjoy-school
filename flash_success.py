from flask import flash

def ch_pass_success():
    return flash(("good" , "Your password is changed successfully!"))

def acc_created():
    return flash (("good","Your account is successfully created! Kindly log in to your account.")) 

def login_success():
    return flash(("good" , "You are logged in successfully!")) 

def join_req_class():
    return flash(("good" , "Class Joining request has been submitted successfully!"))

def create_class():
    return flash(("good" , "Your class has been created succesfully")) 

def decline_request():
    return flash(("good" , "Requset has been declined successfully")) 

def approve_request():
    return flash(("good" , "Request has been approved successfully")) 

def delete_class():
    return flash(("good" , "Class has been deleted successfully")) 

def clswrk_uploaded():
    return flash(("good" , "Classwork has been assigned to the class successfully.")) 

def remove_student():
    return flash(("good" , "Student has been removed successfully.")) 

def leave_class():
    return flash(("good" , "You have left the class successfully.")) 

def student_wrk_upload():
    return flash(("good" , "Classwork has been submitted successfully.")) 
def clswrk_deleted():
    return flash(("good" , "Classwork has been deleted successfully.")) 




    