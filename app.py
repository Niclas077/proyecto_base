from flask import Flask
from responses import Responses
from flask import render_template, redirect, request, Response, session, flash
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__,static_folder='static',template_folder='Template')

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='2304'
app.config['MYSQL_DB']='proyecto_base'
app.config['MYSQL_CURSORCLASS']='DictCursor'
Mysql=MySQL(app)


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/mostrarU', methods = ["GET", "POST"])
def mostrar_usuarios():
    cur=Mysql.connection.cursor();
    cur.execute('SELECT * FROM USUARIOS')
    usuarios=cur.fetchall();
    cur.close();
    return render_template('musuarios.html', usuarios=usuarios)

@app.route('/rect')
def rect():
    return render_template('rect.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

#Funcion Login
@app.route('/access_login', methods = ["GET", "POST"])
def login():
    if request.method == 'POST' and 'txtcorreo' in request.form and 'txtpassword': #trae la data almacenada en el metodo post en los campos de correo y contraseña
        correo=request.form['txtcorreo'] #alamcena la informacion en esas variables 
        contraseña=request.form['txtpassword']
        
        cur=Mysql.connection.cursor() #establece la conexion con la base de datos 
        cur.execute('SELECT * FROM USUARIOS WHERE correo = %s AND password = %s', (correo,contraseña)) 
        #la linea 39 crea la consulta a la tabla y realiza una comparacion para verificar que los datos conincidan "correo y contraseña"
        account = cur.fetchone() #ejecuta la consulta, account es la variable que viene de la base de datos
        
        if account:
            session['Logeado'] = True #session es la "sesion" que se creara para darle rol al usuario
            session['id'] = account['id']
            session['id_rol'] = account['id_rol']
            usuario = account['correo']
            
            if session['id_rol'] == 1:
             return render_template("admin.html", usuario=usuario) 
            elif session['id_rol'] == 2:
                return render_template("usuario.html", usuario=usuario) 
        else: 
           return render_template('index.html') 
   
   
#funcion registro
@app.route('/registro')
def registro():
    return render_template("registro.html")

@app.route('/registroU', methods = ["GET", "POST"])
def registroU():
    if request.method =='POST' and 'txtusuario' in request.form and 'txtcontraseña':
        correo=request.form['txtusuario']
        password=request.form['txtcontraseña']

        cur=Mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (correo,password,id_rol) VALUES (%s, %s,'2')",(correo,password))#usar comillas dobles en insersion de datos 
        Mysql.connection.commit()
        
        return render_template('index.html')

   
@app.route('/restaurarP', methods = ["GET", "POST"])
def restaurarP():
    if request.method == 'POST' and 'txtusuario' in request.form and 'txtcontraseña':
        correo=request.form['txtusuario']
        newpass=request.form['txtcontraseña']
        
        cur=Mysql.connection.cursor();
        cur.execute("UPDATE usuarios set password =%s where correo=%s",(newpass,correo))
        Mysql.connection.commit()
        
        return render_template('index.html')
   
    
@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__": #arranque de la app
    app.secret_key="nicolaspc2304"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    

    