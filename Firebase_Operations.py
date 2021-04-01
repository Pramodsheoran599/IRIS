import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("Service_Account_Key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def push_user(new_user):       #username,password, first_name, last_name, email_id, contact):
    # new_user = {
    #     "Username" : username,
    #     "Password" : password,
    #     "First Name" : first_name,
    #     "Last Name" : last_name,
    #     "Email ID" : email_id,
    #     "Contact" : contact
    # }
    db.collection("Users").add(new_user)
