#Update Collection
import pymongo
import ssl
myclient = pymongo.MongoClient("mongodb+srv://ZhaissMongoPP2:mongo2001@cluster0-i1cp1.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["mydatabase"]
mycol = mydb["zhaiss"]

#You can update a record, or document as it is called in MongoDB, by using the update_one() method.
myquery = {"address": "valley 345"}
newvalues = {"$set": {"address": "Canyon 123"}}
mycol.update_one(myquery, newvalues)

for x in mycol.find():
    print(x)