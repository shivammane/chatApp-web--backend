import json
from flask_socketio import SocketIO, emit
from flask import Flask, request
import mysql.connector
from flask_cors import CORS

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shivam",
    database='chatapp'
)
mycursor = mydb.cursor(dictionary=True)

# get connection id


def connectionId(id):
    mycursor.execute(
        f'''select connection_id from users
            where userid={id}''')
    result = mycursor.fetchall()
    return result[0]['connection_id']


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


# login validation done
@app.route('/login', methods=['GET', 'POST'])
def login():
    data = json.loads(request.data)
    mycursor.execute(
        f'''select count(*) from users
            where email="{data["email"]}" and password="{data["password"]}"''')
    for i in mycursor:
        count = i["count(*)"]
        if (int(count) != 0):
            mycursor.execute(
                f'''select concat(firstname,' ',lastname) as name,email,userid from users
                    where email="{data["email"]}"''')
            j = mycursor.fetchall()
            return json.dumps(j)
        else:
            return json.dumps([{"email": "false"}])


# create new account done
@app.route('/createNew', methods=['GET', 'POST'])
def createNew():
    try:
        data = json.loads(request.data)
        sql = "INSERT INTO users (firstname,lastname,email,password) VALUES (%s,%s,%s,%s)"
        val = (data['firstname'], data['lastname'],
               data['email'], data['password'])
        mycursor.execute(sql, val)
        mydb.commit()
        return 'true'
    except:
        return 'false'


# display users done
@app.route('/users', methods=['GET', 'POST'])
def users():
    data = json.loads(request.data)
    mycursor.execute(
        f'''select concat(firstname,' ',lastname) as name,email,userid from users
         where userid not in({data})''')
    result = mycursor.fetchall()
    return json.dumps(result)

# display messeges done


@app.route('/messeges', methods=['GET', 'POST'])
def messeges():
    data = json.loads(request.data)
    mycursor.execute(
        f'''select * from messeges
            where (sender={data["sender"]} or sender={data["receiver"]}) and (receiver={data["sender"]} or receiver={data["receiver"]})
            ORDER BY messegeid''')
    result = mycursor.fetchall()
    return json.dumps(result)


# onconnect socket add id to database


@socketio.on('socketid')
def handle_message(data):
    mycursor.execute(
        f'''UPDATE users SET connection_id = "{data["socketid"]}"
            where userid={data["userid"]}''')
    mydb.commit()


@socketio.on('messege')
def handle_message(data):
    if (data["receiverid"] != '' and data["messege"] != '\n'):
        sql = '''INSERT INTO messeges (sender,messege,receiver) VALUES (%s,%s,%s)'''
        val = (data["userid"], data["messege"], data["receiverid"])
        mycursor.execute(sql, val)
        mydb.commit()
        emit("receivemsg", json.dumps(data),
             to=connectionId(data['receiverid']))


if __name__ == '__main__':
    socketio.run(app, debug=True)
