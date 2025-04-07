import os
import json
from pymongo import MongoClient
from bson import ObjectId
import traceback
from datetime import datetime

# Environment variables
ATLAS_CONNECTION_STRING = os.environ['ATLAS_CONNECTION_STRING']
DATABASE = os.environ['DATABASE']
COLLECTION = os.environ['COLLECTION']

def connect_to_mongodb():
    try:
        client = MongoClient(ATLAS_CONNECTION_STRING)
        return client
    except Exception as e: 
        print(e)
        return error_response("Not able to connect with Atlas Cluster")


def success_response(body):
    return {
        "statusCode": 200,
        "body": json.dumps(body, cls=DateTimeEncoder),
        "headers": {
            "Content-Type": "application/json"
        }
    }

def error_response(err):
    error_message = str(err)
    return {
        'statusCode': 400,
        'body': error_message,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

# Used to convert datetime object(s) to string
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

def lambda_handler(event, context):
    client = None
    try:
        payload = event['body']
        client = connect_to_mongodb()
        op = event['rawPath']
        db, coll = DATABASE, COLLECTION
        if op == "/findOne":
            filter_op = payload['filter'] if 'filter' in payload else {}
            projection = payload['projection'] if 'projection' in payload else {}
            result = {"document": client[db][coll].find_one(filter_op, projection)}
            if result['document'] is not None:
                if "_id" in result['document']:
                    if isinstance(result['document']['_id'], ObjectId):
                        result['document']['_id'] = str(result['document']['_id'])

        elif op == "/find":
            agg_query = []
        
            if 'filter' in payload and payload['filter'] != {}:
                agg_query.append({"$match": payload['filter']})

            if "sort" in payload and payload['sort'] != {}:
                agg_query.append({"$sort": payload['sort']})
            
            if "skip" in payload:
                agg_query.append({"$skip": payload['skip']})
                
            if 'limit' in payload:
                agg_query.append({"$limit": payload['limit']})
                
            if "projection" in payload and payload['projection'] != {}:
                agg_query.append({"$project": payload['projection']})
                
            result = {"documents": list(client[db][coll].aggregate(agg_query))}
            for obj in result['documents']:
                if '_id' in obj:
                    if isinstance(obj['_id'], ObjectId):
                        obj['_id'] = str(obj['_id'])
                
        elif op == "/insertOne":
            if "document" not in payload or payload['document'] == {}:
                return error_response("Send a document to insert")
            insert_op = client[db][coll].insert_one(payload['document'])
            result = {"insertedId": str(insert_op.inserted_id)}
        
        elif op == "/insertMany": 
            if "documents" not in payload or payload['documents'] == {}:
                return error_response("Send a document to insert")
            insert_op = client[db][coll].insert_many(payload['documents'])
            result = {"insertedIds": [str(_id) for _id in insert_op.inserted_ids]}
        
        elif op in ["/updateOne", "/updateMany"]:
            payload['upsert'] = payload['upsert'] if 'upsert' in payload else False
            if "_id" in payload['filter']:
                payload['filter']['_id'] = ObjectId(payload['filter']['_id'])
            if op == "/updateOne":
                update_op = client[db][coll].update_one(payload['filter'], payload['update'], upsert=payload['upsert'])
            else:
                update_op = client[db][coll].update_many(payload['filter'], payload['update'], upsert=payload['upsert'])
            result = {"matchedCount": update_op.matched_count, "modifiedCount": update_op.modified_count}
        
        elif op in ["/deleteOne", "/deleteMany"]:
            payload['filter'] = payload['filter'] if 'filter' in payload else {}
            if "_id" in payload['filter']:
                payload['filter']['_id'] = ObjectId(payload['filter']['_id'])
            if op == "/deleteOne":
                result = {"deletedCount": client[db][coll].delete_one(payload['filter']).deleted_count}
            else:
                result = {"deletedCount": client[db][coll].delete_many(payload['filter']).deleted_count}
        
        elif op == "/aggregate": 
            if "pipeline" not in payload or payload['pipeline'] == []:
                return error_response("Send a pipeline")
            docs = list(client[db][coll].aggregate(payload['pipeline']))
            for obj in docs:
                if '_id' in obj:
                    if isinstance(obj['_id'], ObjectId):
                        obj['_id'] = str(obj['_id'])
            result = {"documents": docs}
        
        else:
            return error_response("Not a valid operation")
        
        return success_response(result)

    except Exception as e:
        print(traceback.format_exc())
        return error_response(e)

    finally:
        if client:
            client.close()
