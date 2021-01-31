#LIMIT
import pymongo
import ssl
myclient = pymongo.MongoClient("mongodb+srv://ZhaissMongoPP2:mongo2001@cluster0-i1cp1.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["mydatabase"]
mycol = mydb["zhaiss"]

#The limit() method takes one parameter, a number defining how many documents to return.
myresult = mycol.find().limit(3)

for x in myresult:
  print(x)