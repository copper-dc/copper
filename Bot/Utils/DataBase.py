import asyncio
from datetime import date
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv('MONGODB_CONNECTION_STRING')

client = AsyncIOMotorClient(connection_string)
if client:
    print("connected DB")

db = client.Discord

#CRUD operations XD

async def create_db(user_id,user_name):

    document = {"uid": user_id, 
                "name": user_name,
                "points": 0,
                "last_active_date":"2024-06-07"}

    result = await db.User_info.insert_one(document)

    print("result %s" % repr(result.inserted_id))


async def find(user_id, flag = None):

    cursor = db.User_info.find()
    data = await cursor.to_list(length=100)
    
    for item in data:
        if item["uid"] == user_id and flag is not None:
            return item["points"]
        elif item["uid"] == user_id and flag is None:
            return True
    if flag is None:
        return False
    else:
        return "No User Found!"
    
async def findlastactive(user_id, flag = None):

    cursor = db.User_info.find()
    data = await cursor.to_list(length=100)
    
    for item in data:
        if item["uid"] == user_id and flag is not None:
            return item["last_active_date"]
        elif item["uid"] == user_id and flag is None:
            return True
    if flag is None:
        return False
    else:
        return "No User Found!"
    
    

async def update_db(user_id, points= None, name = None, flag = None):
    coll = db.User_info
    current_date = str(date.today())
    if points is not None:
        result = await coll.update_one({"uid": user_id}, {"$set": {"points": await find(user_id, flag = 1) + points, "last_active_date": current_date}})

        print(f"updated {result.modified_count} document" )

        doc = await coll.find_one({"uid": user_id})
        uname = doc["name"]
        upoint = doc["points"]

        print(f"point of {uname} is now {upoint}")

    if name is not None:
        result = await coll.update_one({"uid": user_id}, {"$set": {"name": name}})

        print(f"updated {result.modified_count} document" )

        doc = await coll.find_one({"uid": user_id})
        uid = doc["uid"]
        uname = doc["name"]
        upoint = doc["points"]
        
        print(f"New name of {uid} is {uname}")

    if points is not None and flag is not None:

        result = await coll.update_one({"uid": user_id}, {"$set": {"points": points, "last_active_date": current_date}})

        print(f"updated {result.modified_count} document" )

        doc = await coll.find_one({"uid": user_id})
        uname = doc["name"]
        upoint = doc["points"]

        print(f"point of {uname} is now {upoint}")

    
    

async def delete(user_id):
    coll = db.User_info

    n = await coll.count_documents({})

    print("%s documents before calling delete_one()" % n)

    result = await db.User_info.delete_one({"uid":user_id})

    print("%s documents after" % (await coll.count_documents({})))