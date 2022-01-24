import csv

def read_files_from_AMA():
    #Read textfile with long descriptors
    longult = []
    with open('LONGULT.txt') as f:
        longult = f.readlines()

    #Read textfile with medium descriptors
    medu = []
    with open('MEDU.txt') as f:
        medu = f.readlines()

    #Read textfile with consumer descriptors
    consumers = []
    with open('ConsumerDescriptor.txt') as f:
    	consumers = f.readlines() 
    # returns a list of all descriptions from each file
    return [longult,medu,consumers]

### function created to meet Algolia's free storage size
def delete_cpts_from_firestore(self):
    countDocs = 0
    docs = doc_ref.where(u'rvu', u'==', 0.0).stream()
    for doc in docs:
        countDocs += 1
        if countDocs < 2:
            doc_ref.document(doc.id).delete()
            # print(f'{doc.id} => {doc.to_dict()}')

def process_cpts(longult, medu, consumers, doc_ref):
    count = 0
    for line in longult:  
        count += 1
        ## first cpt was found on line 33
        # start reading at first CPT code
        if count > 33:
            #Store CPT Code
            code = ""
            code = line[0:5]
            longDescription = ""
            #Store CPT Description
            longDescription = line[6:]
            mediumDescription = ""
            #Find code in MEDU.txt
            for med in medu:
            	if med[0:5] == code:
            		mediumDescription = med[6:]
            consumerDescription = ""
            for consumer in consumers:
            	if consumer[8:13] == code:
            		consumerDescription = consumer[14:]
            rvu = 0.0
            #Read csv file with RVUs
            with open("PPRRVU21_JAN - PPRRVU21_JAN.csv", "r") as f:
                rvus = csv.reader(f)
                for row in rvus:
                #Find code in RVU.csv
                    if row[0] == code:
                    	rvu = float(row[5])
            cpt_dict = {
                u'code':code,
                u'longDescription':longDescription,
                u'mediumDescription':mediumDescription,
                u'rvu':float(rvu),
                u'consumerDescription':consumerDescription,
                u'year': "2022",
                u'version': "Q1"
            }
            print(cpt_dict)
            # doc_ref.document().set(cpt_dict)

def upload_cpts(doc_ref):
    cptData = read_files_from_AMA()
    process_cpts(cptData[0],cptData[1], cptData[2],doc_ref)
