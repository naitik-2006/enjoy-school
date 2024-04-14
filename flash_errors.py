from flask import flash

def login_err():
    return flash(("error","Incorrect Email Or Password !"))

def email_al_regis_error():
    return flash(("error","Email alreday Registered! Please log in into the existing account."))

def server_contact_error():
    return flash(("error","There is some problem in contacting to the server! Try again after some time."))

def flash_mail_err():
    return flash(("error","There was some problem in sending the otp to your Email!"))

def email_nf_err():
    return flash(("error","No Account Found! "))

def incorrect_otp():
    return flash(("error","Otp is not correct! Please check it!"))

def same_pass_err():
    return flash(("error","This is your existing password! Please enter another one."))

def dnt_have_access():
    return flash(("error","You are not authenticated to do such type of work"))

def not_create_moreclass():
    return flash(("error" , "Can Not Create More Classes ! You Have Already Created Maximum No. Of Classes."))

def no_class_found():
    return flash(("error","No class found! Please check your class ID."))

def already_joined():
    return flash(("error","You are already in this class!"))

def already_joined_ft():
    return flash(("error","The student is already in the class!"))

def request_found():
    return flash(("error","No request found of this student!"))

def some_went_wrong():
    return flash(("error","Something Went Wrong!"))

def already_req():
    return flash(("error","You have already requested to join this class!"))

def no_more_join():
    return flash(("error","Can Not Join More Classes ! You Have Already Joined Maximum No. Of Classes."))

def no_more_join_ft():
    return flash(("error","Can Not Join In The Class! Student Had Already Joined Maximum No. Of Classes."))

def max_participants():
    return flash(("error","Can Not Join More Students! Maximum No. Of Students Have Already Joined the Class."))

def filename_nt_crr():
    return flash(("error","File name is not in the correct way!"))

def select_file_nt_support():
    return flash(("error","Selected file extension is not supported!"))

def file_over_size(mx_mb_size):
    return flash(("error",f"The size of the file should be less than {mx_mb_size} MB!"))

def pdf_over_size():
    return flash(("error","The size of the pdf should be less than or equal to 25 MB!"))

def no_file_fnd():
    return flash(("error","File not found!"))

def already_submit():
    return flash(("error","You have already submitted the classwork!"))

def cant_submit_now():
    return flash(("error","Cannot submit the classwork now!"))

def cant_download_now():
    return flash(("error","Cannot download the classwork pdf now!"))

def cant_downlod_now():
    return flash(("error", "File can not download now"))
