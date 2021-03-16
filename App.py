from flask import Flask,render_template,request,redirect,url_for
from flask.helpers import flash
from flask_mysqldb import MySQL
app = Flask(__name__)

#Mysql connection
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_DB']   = "flask_app"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASS'] = ""
mysql = MySQL(app)

#settings
app.secret_key = "mysecretkey"

#---Home----
@app.route("/")
def index():
    command = mysql.connection.cursor()
    command.execute("SELECT * FROM contacto")
    data = command.fetchall()
    print(data)
    
    
    return render_template('index.html',contactos = data)


#---Agregar contactos
@app.route("/add_contact", methods =['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone    = request.form['phone']
        email    = request.form['email']
        command = mysql.connection.cursor()
        command.execute("INSERT INTO contacto(fullname,phone,email)VALUES(%s,%s,%s)",(fullname,phone,email))
        mysql.connection.commit()
        flash('Contact Added succesfully')
        return redirect(url_for('index'))

#---Editar contactos
@app.route("/edit/<id>")
def get_contact(id):
    command = mysql.connection.cursor()
    command.execute('SELECT * FROM contacto WHERE id = {}' .format(id))
    data = command.fetchall()
    return render_template('edit-contacto.html',contacto= data[0])

#Actualizar
@app.route("/update/<id>", methods =['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone    = request.form['phone']
        email    = request.form['email']
    command = mysql.connection.cursor()
    command.execute("""
        UPDATE  contacto SET  
            fullname = %s,
            phone = %s,
            email = %s
        WHERE id = %s     
     """, (fullname,phone,email,id))
    mysql.connection.commit()
    flash("Contact Update succesfully")
    return redirect(url_for('index'))

#---Eliminar contacto
@app.route("/delete/<string:id>")
def delete_contact(id):
    command = mysql.connection.cursor()
    command.execute('DELETE FROM contacto WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed succesfuly')
    return redirect(url_for('index'))
    
    



if __name__ == '__main__':
    app.run(debug=True) ##Recarga el proyecto cada ves que se le haga un cambio