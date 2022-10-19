import sqlite3
from flask import Flask,request,jsonify
import sqlite3
app = Flask(__name__)

def db_connection():
    conn =None
    try:
        conn=sqlite3.connect('users.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn

#to get list of users and post data
@app.route("/users",methods=["GET","POST"])
def users():

    conn= db_connection()  #create connection cursor
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute(("SELECT * FROM user ")) 
    
        users = [
            dict(id= row[0],user_name = row[1])
            for row in cursor.fetchall()
        ]
        if users is not None:
            return jsonify(users)
        
    if request.method == "POST":
        new_user_name = request.form["user_name"]
        sql = """ INSERT INTO book (user_name) VALUES (?) """
        cursor = cursor.execute(sql, (new_user_name))
        conn.commit()    #Saving the Actions performed 
        return f"User with the id: 0 created successfully", 201
#to get data from user based on user id and to update and delete data from user table
@app.route("/user/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_user(id):
    conn = db_connection()
    cursor = conn.cursor()
    user = None
    if request.method == "GET":
        cursor.execute(" SELECT * FROM user WHERE id='{}' ".format(id))
        rows = cursor.fetchall()
        for r in rows:
            user = r
        if user is not None:
            return jsonify(user), 200
        else:
            return "Something wrong", 404

    if request.method == "PUT":
        sql = """ UPDATE user
                SET user_name=?
                WHERE id=? """ 

        user_name = request.form["user_name"]
        updated_user = {
            "id": id,
            "user_name": user_name,
        }
        conn.execute(sql, (user_name, id))
        conn.commit()
        return jsonify(updated_user)

    if request.method == "DELETE":
        sql = """ DELETE FROM user WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return "The user with id: {} has been deleted.".format(id), 200
        



if __name__ == "__main__":
    app.run(debug=True, port=5000)
	
