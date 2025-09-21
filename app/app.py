from flask import Flask,render_template,request,url_for,redirect,jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

#Conexion con Base de Datos MySQL

app.config['MYSQL_HOST']='localhost'    #servidor por defecto
app.config['MYSQL_USER']='root'         #usuario
app.config['MYSQL_PASSWORD']='123456'   #clave
app.config['MYSQL_DB']='NombreDB'       #nombre de la base de datos

conexion= MySQL(app)   #Le pasamos la app a la conexion con SQL

@app.before_request
def before_request():
    print('antes de la consulta')

@app.after_request
def after_request(response):
    print('despues de la consulta')
    return response

@app.route('/')
def index():
    
    cursos=['PHP', 'Java', 'JavaScript', 'Python', 'Kotlin', 'Dart']

    data={
        'titulo' : 'index123',
        'bienvenida': 'saludos', 
        'cursos': cursos,
        'numero_cursos': len(cursos)
    }

    return render_template('index.html',data=data)

@app.route('/contacto/<nombre>/<int:edad>')
def contacto_nombre(nombre,edad):
    """Funcion que contiene en un diccionario los valores a ingresar en la ruta del navegador"""
    data={
        'titulo': 'contacto',
        'nombre': nombre,
        'edad': edad

    }
    return render_template('contacto.html', data=data)

def query_string():
    """Funcion que devuelve los valores de la request[GET][PUT],etc por la termminal, y los parametro ingresados en la ruta del navegador"""
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "ok"

@app.route('/cursos')
def listar_cursos():
    data={}
    try:
        cursor=conexion.connection.cursor()
        sql= "SELECT codigo, nombre, creditos, FROM curso ORDER BY nombre ASC"
        cursor.execute(sql)
        cursos=cursos.fetchall()
        data['cursos']= cursos
        print(cursos)
        data['mensaje'] = 'Exito'
    except Exception as ex:
        data['mensaje'] = 'Error'
    return jsonify(data)


def pagina_no_encontrada(error):
    """funcion para redirigir a pagina por defecto de error en este caso es '404.html' o redirijir a index"""

    return redirect(url_for('index'))

    #return render_template('404.html'),404

if __name__ == '__main__':
    app.register_error_handler(404,pagina_no_encontrada)
    app.add_url_rule('/query_string', view_func=query_string)
    app.run(debug=True,port=5000)

    
