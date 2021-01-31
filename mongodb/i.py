#filter with Regular Expressions
import pymongo
import ssl
myclient = pymongo.MongoClient("mongodb+srv://ZhaissMongoPP2:mongo2001@cluster0-i1cp1.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["mydatabase"]
mycol = mydb["zhaiss"]

#Regular expressions can only be used to query strings.
#To find only the documents where the "address" field starts with the letter "S", use the regular expression {"$regex": "^V"}:
myquery = {"address": {"$regex": "^V"}}
mydoc = mycol.find(myquery)
for x in mydoc:
    print(x)