#FIND
import pymongo
import ssl
myclient = pymongo.MongoClient("mongodb+srv://ZhaissMongoPP2:mongo2001@cluster0-i1cp1.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["mydatabase"]
mycol = mydb["zhaiss"]
#The find_one() method returns the first occurrence in the selection.
#x = mycol.find_one()
#print(x)


#The find() method returns all occurrences in the selection.
#for x in mycol.find():
#    print(x)


#RETURN ONLY SOME FIELDS
#for x in mycol.find({},{"_id": 0, "name": 1, "address": 1}):#Return only the names and adresses,not the _ids
#    print(x)



#In this case will exclude "adresses" form the result:
for  x in mycol.find({},{"address": 0}):
    print(x)