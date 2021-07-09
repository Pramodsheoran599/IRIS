# Importing Libraries
from datetime import datetime
import smtplib
from email.message import EmailMessage

import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

firebase_config = {                                                                 # Firebase Configuration
        "apiKey": "AIzaSyAyrz-irseUwS5NLnVFUdDG7DrQx6A8zq8",
        "authDomain": "iris-pramod.firebaseapp.com",
        "databaseURL": "https://iris-pramod-default-rtdb.firebaseio.com",
        "projectId": "iris-pramod",
        "storageBucket": "iris-pramod.appspot.com",
        "messagingSenderId": "68729237436",
        "appId": "1:68729237436:web:2a00ca05afd23497cc45b9",
        "measurementId": "G-MMZWLBXMSK"
    }

firebase = pyrebase.initialize_app(firebase_config)                                 # Firebase App
storage = firebase.storage()                                                        # Firebase Storage

cred = credentials.Certificate(r"..\Service_Account_Key.json")                      # Credentials of the Cloud Database
firebase_admin.initialize_app(cred)                                                 # Firebase Admin App
db = firestore.client()                                                             # Firestore Database


def user_exists(username):
    """Checks if a Username exists in the Database"""

    if db.collection("Users").document(username).get().exists:
        return True

    else:
        return False


def push_user_to_database(new_user):
    """Add User to The Database. The input Parameter is a Dictionary"""

    document_id = new_user["Username"]                                              # Each Document Id is set to respective Username

    if user_exists(document_id):                                                    # If User Already Registered
        return 0                                                                         #  return 0 to notify User Already Exists

    else:
        db.collection("Users").document(document_id).set(new_user)                  # Add user to the Database
        return 1                                                                        # Return 1 to notify User Registration Done


def get_user_data(document_id, field):
    """Get a Specifit User data from the Users Collection"""

    user = db.collection("Users").document(document_id).get().to_dict()
    return user[field]


def generate_log(username, action):
    """Generate a Log in Database for a User Action"""

    document_id = datetime.now().strftime("%d-%m-%Y %H:%M:%S")                     # Time Stamp used as Doc-ID

    log = {                                                                        # Log Dictionary
        "Username": username,
        "Action": action,
        "Time Stamp": firestore.SERVER_TIMESTAMP                                   # Server Timestamp
    }

    db.collection("Logs").document(document_id).set(log)                           # Push Log to the Database


def generate_alert(username, detection_type, comment):
    """Generate an Alert and Store its Details in Database"""

    document_id = datetime.now().strftime("%d-%m-%Y %H:%M:%S")                     # Time Stamp used as Doc-ID

    # Storing Evidence based on the Detection_type and then getting its url
    storage.child(detection_type).child(document_id).put("../Recordings/Image Evidence/screenshot.jpg")
    url = storage.child(detection_type).child(document_id).get_url(None)

    send_notification(url)

    alert = {                                                                      # Alert Details
        "Username": username,
        "Detection Type": detection_type,
        "Evidence_Url": url,
        "Comment": comment if comment else None,
        "Time Stamp": firestore.SERVER_TIMESTAMP                                   # Server Timestamp
    }

    db.collection("Alerts").document(document_id).set(alert)


def send_notification(url):

    msg = EmailMessage()
    msg.set_content(f"""Suspicious Activity Detected By the System \n link: {url}""")

    msg['Subject'] = '!!!---IRIS SYSTEM ALERT---!!!'
    msg['From'] = "pramodsheoran599@gmail.com"
    msg['To'] = "pramodsheoran599@gmail.com"

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("pramodsheoran599@gmail.com", "Pramod@7726")
    server.send_message(msg)
    server.quit()
