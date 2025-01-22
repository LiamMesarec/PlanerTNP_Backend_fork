from bson import ObjectId
from datetime import datetime
from db import db

def set_task(user_id, task_data):
    collection = db.users
    task_data["_id"] = ObjectId()  # Assign a unique ID to each task

    result = collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"tasks": task_data}}
    )

    if result.matched_count == 0:
        return {"error": "User not found"}, 404

    task_data["_id"] = str(task_data["_id"])  # Convert task ID to string for JSON response
    return {"message": "Task added successfully", "task": task_data}, 200


def get_all_tasks(user_id):
    collection = db.users
    user = collection.find_one(
        {"_id": ObjectId(user_id)}
    )
    if user is None:
        return {"error": "User not found"}, 404

    tasks = user.get("tasks", [])
    # Convert task IDs to strings for JSON serialization

    tasks = [task for task in user["tasks"] if task.get("deleted") != True]

    for task in tasks:
        task["_id"] = str(task["_id"])

    return {"tasks": tasks}, 200


def delete_task(user_id, task_id):
    collection = db.users

    # Mark the task as deleted by adding a 'deleted' flag or a 'deletedAt' timestamp
    result = collection.update_one(
        {"_id": ObjectId(user_id), "tasks._id": ObjectId(task_id)},
        {"$set": {"tasks.$.deleted": True, "tasks.$.deletedAt": datetime.utcnow()}}
    )

    if result.matched_count == 0:
        return {"error": "User or task not found"}, 404

    return {"message": "Task marked as deleted successfully"}, 200


# Method to get all tasks including soft-deleted ones (if needed)
def get_all_tasks_with_deleted(user_id):
    collection = db.users
    user = collection.find_one({"_id": ObjectId(user_id)}, {"tasks": 1})

    if user is None:
        return {"error": "User not found"}, 404

    tasks = user.get("tasks", [])
    # Convert task IDs to strings for JSON serialization
    for task in tasks:
        task["_id"] = str(task["_id"])

    return {"tasks": tasks}, 200

# Method to retrieve only active tasks (excluding soft-deleted ones)
def get_active_tasks(user_id):
    collection = db.users
    user = collection.find_one(
        {"_id": ObjectId(user_id)},
        {"tasks": {"$elemMatch": {"deleted": {"$ne": True}}}}  # Exclude soft-deleted tasks
    )

    if user is None:
        return {"error": "User not found"}, 404

    tasks = user.get("tasks", [])
    # Convert task IDs to strings for JSON serialization
    for task in tasks:
        task["_id"] = str(task["_id"])

    return {"tasks": tasks}, 200

def update_task(user_id, task_id):
    collection = db.users
    data = request.json

    # Ensure the payload contains fields to update
    if not data:
        return {"error": "No data provided for update"}, 400

    # Update the specific task in the user's task list
    result = collection.update_one(
        {"_id": ObjectId(user_id), "tasks._id": ObjectId(task_id)},
        {"$set": {f"tasks.$.{key}": value for key, value in data.items()}}
    )

    if result.matched_count == 0:
        return {"error": "User or task not found"}, 404

    return {"message": "Task updated successfully"}, 200
