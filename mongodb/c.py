#INSERT
import pymongo
import ssl
myclient = pymongo.MongoClient("mongodb+srv://ZhaissMongoPP2:mongo2001@cluster0-i1cp1.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["mydatabase"]
mycol = mydb["zhaiss"]
mydict = {"name": "ZHAISAN", "UNIVERSITY": "KBTU"}
#To insert a record, or document as it is called in MongoDB, into a collection, we use the insert_one() method.
x = mycol.insert_one(mydict)
print(x.inserted_id)#this holds the id of the inserted
