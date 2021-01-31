#ADVANCED QUERY
import pymongo
import ssl
myclient = pymongo.MongoClient("mongodb+srv://ZhaissMongoPP2:mongo2001@cluster0-i1cp1.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["mydatabase"]
mycol = mydb["zhaiss"]

#to find the documents where the "address" field starts with the letter "S" or higher (alphabetically), use the greater than modifier: {"$gt": "S"}:
myquery = {"address": {"$gt": "S"}}
mydoc = mycol.find(myquery)
for x in mydoc:
    print(x)