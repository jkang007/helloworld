# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Family Room"
__date__ = "$Dec 17, 2015 10:34:25 AM$"

# if __name__ == "__main__":
#    print "Hello World"

from flask import Flask, render_template, json, request
app = Flask(__name__)

from flask.ext.mysql import MySQL
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mysql'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def main():
    return render_template('index.html')
#    return "Welcome!"

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

from werkzeug import generate_password_hash, check_password_hash

@app.route('/signUp',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
 
    # validate the received values
    if _name and _email and _password:
	conn = mysql.connect()
	cursor = conn.cursor()
	_hashed_password = generate_password_hash(_password)
	cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
	data = cursor.fetchall()
 
	if len(data) is 0:
    		conn.commit()
    		return json.dumps({'message':'User created successfully !'})
	else:
    		return json.dumps({'error':str(data[0])})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


if __name__ == "__main__":
    app.run()
    
