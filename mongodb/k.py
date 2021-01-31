#Delete
import pymongo
import ssl
myclient = pymongo.MongoClient("mongodb+srv://ZhaissMongoPP2:mongo2001@cluster0-i1cp1.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["mydatabase"]
mycol = mydb["zhaiss"]

#To delete one document, we use the delete_one() method.
#If the query finds more than one document, only the first occurrence is deleted.
myquery = {"address": "Mountain 21"}

mycol.delete_one(myquery)