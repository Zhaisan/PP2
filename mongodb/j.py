#SORT
import pymongo
import ssl
myclient = pymongo.MongoClient("mongodb+srv://ZhaissMongoPP2:mongo2001@cluster0-i1cp1.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["mydatabase"]
mycol = mydb["zhaiss"]

#The sort() method to sort the result in ascending or descending order.

mydoc = mycol.find().sort("name")
for x in mydoc:
    print(x)

#if we want to sort descending:
#We just use the value -1 like:
# sort("name", -1)