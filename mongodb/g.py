#QUERY
#The first argument of the find() method is a query object, and is used to limit the search.
import pymongo
import ssl
myclient = pymongo.MongoClient("mongodb+srv://ZhaissMongoPP2:mongo2001@cluster0-i1cp1.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["mydatabase"]
mycol = mydb["zhaiss"]

myquery = {"address": "Park Lane 38"}

mydoc = mycol.find(myquery)
for x in mydoc:
    print(x)