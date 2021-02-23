from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import json_util


app = Flask(__name__)

# mongo database URI
client = MongoClient(
    # "mongodb://admin:KOVrdi56562@node9145-advweb-07.app.ruk-com.cloud:11121/"  # public URI
    "mongodb://admin:KOVrdi56562@10.100.2.122:27017/"  # private URI
)
# database name
db = client["CloudDB"]

# root path
@app.route("/", methods=["GET"])
def get():
    return jsonify({"message": "Hello Cloud mongoDB"})


# Get All Staffs from staffs collection
@app.route("/staffs", methods=["GET"])
def get_staffs():
    # data = db.staffs.find()  # setlect * from staffs

    pipeline = [
        {
            "$lookup": {
                "from": "department",
                "localField": "dep_id",
                "foreignField": "dep_id",
                "as": "join_dep_id",
            }
        },
        {
            "$unwind": {
                "path": "$join_dep_id",
                "preserveNullAndEmptyArrays": True,
            }
        },
        {
            "$lookup": {
                "from": "location",
                "localField": "join_dep_id.location_id",
                "foreignField": "location_id",
                "as": "join_location",
            }
        },
        {
            "$unwind": {
                "path": "$join_location",
                "preserveNullAndEmptyArrays": True,
            }
        },
        {
            "$project": {
                "_id": 0,
                "staff_id": 1,
                "name": 1,
                "email": 1,
                "location": {
                    "street": "$join_location.street",
                    "postal_code": "$join_location.postal_code",
                    "zone": "$join_location.zone",
                    "dscr": "$join_location.dscr",
                },
            }
        },
    ]

    data = db.staffs.aggregate(pipeline)

    return json_util.dumps(data)


# Get single Staff
@app.route("/staff/<staff_id>", methods=["GET"])
def get_staff(staff_id):
    # data = db.staffs.find_one({"staff_id": staff_id})  # select <staff_id> from staffs
    pipeline = [
        {
            "$lookup": {
                "from": "department",
                "localField": "dep_id",
                "foreignField": "dep_id",
                "as": "join_dep_id",
            }
        },
        {
            "$unwind": {
                "path": "$join_dep_id",
                "preserveNullAndEmptyArrays": True,
            }
        },
        {
            "$lookup": {
                "from": "location",
                "localField": "join_dep_id.location_id",
                "foreignField": "location_id",
                "as": "join_location",
            }
        },
        {
            "$unwind": {
                "path": "$join_location",
                "preserveNullAndEmptyArrays": True,
            }
        },
        {
            "$match": {
                "staff_id": staff_id,
            }
        },
        {
            "$project": {
                "_id": 0,
                "staff_id": 1,
                "name": 1,
                "email": 1,
                "location": {
                    "street": "$join_location.street",
                    "postal_code": "$join_location.postal_code",
                    "zone": "$join_location.zone",
                    "dscr": "$join_location.dscr",
                },
            }
        },
    ]

    data = db.staffs.aggregate(pipeline)

    return json_util.dumps(data)


# Create a Staff
@app.route("/staff", methods=["POST"])
def add_staff():
    # get raw type json
    staff_id = request.json["staff_id"]
    name = request.json["name"]
    email = request.json["email"]
    phone = request.json["phone"]

    # prepare new staff data before insert
    new_staff = {"staff_id": staff_id, "name": name, "email": email, "phone": phone}
    # insert one document to staffs collection
    insertResult = db.staffs.insert_one(new_staff).inserted_id

    return json_util.dumps({"insert complete": insertResult})


# Update a Staff
@app.route("/staff/<staff_id>", methods=["PUT"])
def update_staff(staff_id):
    name = request.json["name"]
    email = request.json["email"]
    phone = request.json["phone"]

    # update filter
    filter = {"staff_id": staff_id}
    # update field
    update_staff = {"name": name, "email": email, "phone": phone}

    # update one document Where match filter
    updateResult = db.staffs.update_one(filter, {"$set": update_staff}).raw_result

    return json_util.dumps({"update complete": updateResult})


# Delete Staff
@app.route("/staff/<staff_id>", methods=["DELETE"])
def delete_staff(staff_id):
    # delete one document
    deleteResult = db.staffs.delete_one({"staff_id": staff_id}).raw_result

    return json_util.dumps({"delete complete": deleteResult})


@app.route("/timeAtten", methods=["GET"])
def get_time():
    data = db.timeAttendance.find()
    return json_util.dumps(data)


if __name__ == "__main__":
    app.run(port=80, host="0.0.0.0")
