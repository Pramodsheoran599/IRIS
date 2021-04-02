# Importing Dependencies
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("Service_Account_Key.json")                          # Credentials of the Cloud Database
firebase_admin.initialize_app(cred)                                                 # Initializing the Connection

db = firestore.client()                                                             # Database Object


def user_exists(collection_name, document_id):
    """Checks if a Document is present in the Database"""
    if db.collection(collection_name).document(document_id).get().exists:
        return 1

    else:
        return 0


def push_user_to_database(new_user):
    """Add User to The Database The input Parameter is a Dictionary"""
    document_id = new_user["Username"]                                              # Each Document Id is set to respective Username

    if user_exists("Users", document_id):                                            # If User Already Registered return -1
        return 0

    else:
        db.collection("Users").document(document_id).set(new_user)                  # Document Reference
        return 1


def get_data(document_id, field):
    user = db.collection("Users").document(document_id).get().to_dict()
    print(user)
    print(user[field])
    return user[field]



