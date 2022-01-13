import pymongo

#Function to connect with Mongo
def connect_db(collection='dados_rastreamento'):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["denox"]
    mycol = mydb[collection]
    # process log
    print(f'Database successfully connected to collection {collection}')

    return mycol


#Database query, parameters: serial, datahora_inicio, datahora_fim
def db_consult(serial, datahora_inicio, datahora_fim):
    
    db = connect_db()

    query = {"serial": serial, 
              "datahora": { "$gt": datahora_inicio,"$lt": datahora_fim }}

    list_doc = []

    for x in db.find(query, {'_id': 0}):
        list_doc.append(x)
    
    #process log
    print('Querying Database')
    return list_doc
