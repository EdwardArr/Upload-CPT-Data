import firebase_admin
from firebase_admin import credentials, firestore
from upload_cpts_to_firestore import *
from upload_modifiers_to_firestore import *
import sys

globalPath = sys.argv[1]

def main():
	global globalPath
	
	cred = credentials.Certificate(globalPath)

	firebaseApp = firebase_admin.initialize_app(cred)

	db = firestore.client()
	cptDocRef = db.collection(u'cpts')
	modDocRef = db.collection(u'modifiers')
	
	upload_cpts(cptDocRef)
	upload_modifiers(modDocRef)

if __name__ == '__main__':
	main()