這是一隻自動爬取所有熱門看板的爬蟲  
爬取後自動存入MongoDB內  
想更改連接的Mongo Server，請更改下面的連接設定  
myclient = pymongo.MongoClient('http://localhost')  
db = myclient.db_name  
col = db.collection_name  
