#Delete Many Documents
import pymongo
import ssl
myclient = pymongo.MongoClient("mongodb+srv://ZhaissMongoPP2:mongo2001@cluster0-i1cp1.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["mydatabase"]
mycol = mydb["zhaiss"]

#\To delete more than one document, use the delete_many() method.
#Delete all documents were the address starts with the letter V:
myquery = {"address": {"$regex": "^V"}}
x = mycol.delete_many(myquery)
print(x.deleted_count, "documents deleted")

#To delete all documents in collection:
#x = mycol.delete_many({})