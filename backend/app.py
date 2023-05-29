import datetime
from flask import Flask, jsonify,Flask, request ,render_template 
from backend.database_operations.mysql_credentials_reader import MysqlCredentials
from backend.database_operations.mysql_connection import DatabaseConnection
from backend.database_operations.user import UserDAO, UserLogin, UserRegistration

app = Flask(__name__)
db_name = 'ai_trainer'
credentials =  MysqlCredentials.get_mysql_credentials()
connection = DatabaseConnection.connect_to_mysql_server(credentials['DBN'],credentials['mysql_username'],credentials['mysql_pwd'],credentials['mysql_host'])
user_login = UserLogin(connection, db_name)



@app.route('/check_user', methods=['POST'])
def check_user():
    email = request.json['email']
    user_info = user_login.user_dao.retrieve_user_information(email)
    if user_info is not None:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})

@app.route('/signin', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    authenticated = UserLogin(connection,db_name ).authenticate_user(email, password)
    if authenticated:
        # login successful
        return jsonify({'status':True,'message': 'Login successful'})
    else:
        # login failed
        return jsonify({'status':False,'message': 'Login failed'})
    
user_registration = UserRegistration(connection,db_name )

@app.route('/register', methods=['POST'])
def register():
    email = request.json['email']
    username = request.json['username']
    password = request.json['password']

    registered = user_registration.register_user(email, username, password)

    if registered:
        return jsonify ({'status':True ,'message' :f"email {email} registered successfully"})
    else:
        return jsonify ({'status':False ,'message' :f"Email {email} is already taken"})
    
@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.json['email']
    new_password = request.json['new_password']

    reset_successful = user_login.reset_password(email, new_password)

    if reset_successful:
        return f"Password for email {email} has been reset successfully"
    else:
        return f"Password reset failed for email {email}"
    
@app.route('/add_user_info', methods=['POST'])
def add_user_info():
    email = request.json['email']
    height = request.json['height']
    weight = request.json['weight']
    age = request.json['age']

    user_dao = UserDAO(connection, db_name)
    user_info = user_dao.retrieve_user_information(email)

    if user_info is None:
        return f"Email {email} not found in database"

    user_dao.update_user_information(email, height, weight, age)

    return f"User information updated for email {email}"

@app.route('/fit_weight_bmi', methods=['POST'])
def calculate_fit_weight_bmi():
    # Get data 
    weight = float(request.json['weight'])
    height = float(request.json['height'])
    gender = request.json['gender']

    # Calculate BMI
    bmi = weight / (height ** 2)

    #  weight status based on BMI
    if bmi < 18.4:
        weight_status = 'underweight'
    elif 18.5 <= bmi < 24.9:
        weight_status = 'normal'
    elif 25.0 <= bmi < 39.9:
        weight_status = 'overweight'
    else:
        weight_status = 'obese'

    #  ideal BMI based on gender
    if gender == 'male':
        ideal_bmi = 23
    else:
        ideal_bmi = 22

    # Calculate fit weight based on ideal BMI and height
    fit_weight = ideal_bmi * (height ** 2)

    # Construct response message
    response = f"Your BMI is {bmi:.2f} , which is considered {weight_status}. "
    response += f"Your fit weight is {fit_weight:.2f} kg."
    return response
    

   

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)