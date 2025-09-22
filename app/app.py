from flask import Flask,render_template,request,url_for,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema,fields,ValidationError

app = Flask(__name__)

#Conexion con Base de Datos SQLAlquemy

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:26729325@localhost/webTest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db= SQLAlchemy(app)   #Le pasamos la app a la conexion con SQL

#definicion de un modelo(tabla db)
class Usuario(db.Model):
    __tablename__='usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False )
    email = db.Column(db.String(50), unique=True, nullable=False)

#SCHEMA PARA LA SERIALIZACION DE MARSHMALLOW
class UsuarioSchema(Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String(required=True)
    email = fields.String(required=True)

#instanioas del eschema
usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    try:
        #deserializa el json a solicitud
        data = usuario_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    #crear objeto y guardar en bd
    nuevo_usuario = Usuario(nombre=data['nombre'], email=data['email'])
    db.session.add(nuevo_usuario)
    db.session.commit()

    #serializar objeto para respuesta
    return jsonify(usuario_schema.dump(nuevo_usuario)), 201

#endpoint Listar usuarios
@app.route('/usuarios', methods=['GET'])
def listas_usuarios():
    #consulta usando ORM
    usuarios = Usuario.query.all()
    #serializar para respuesta json(marshmallow)
    return jsonify(usuarios_schema.dump(usuarios))


"""@app.before_request
def before_request():
    print('antes de la consulta')

@app.after_request
def after_request(response):
    print('despues de la consulta')
    return response"""

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



    """funcion para redirigir a pagina por defecto de error en este caso es '404.html' o redirijir a index"""
"""def pagina_no_encontrada(error):

    return redirect(url_for('index'))

    #return render_template('404.html'),404"""

if __name__ == '__main__':
    """app.register_error_handler(404)
    app.add_url_rule('/query_string', view_func=query_string)"""
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    
