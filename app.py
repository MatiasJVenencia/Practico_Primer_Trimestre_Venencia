from flask import(
    Flask,
    render_template,
    request,
    redirect,
    url_for
)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

from datetime import date


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://BD2021:BD2021itec@143.198.156.171/bd_practicoPrimerTrimestre_Venencia"

db = SQLAlchemy(app=app)
migrate = Migrate(app, db)

class Usuario(db.Model):
    __teblename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.username

class Entrada(db.Model):
    __teblename__ = 'entrada'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'),nullable=False)
    categoria_id = db.Column(db.Integer, ForeignKey('categoria.id'),nullable=False)
    
class Comentario(db.Model):
    __teblename__ = 'coentario'

    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'),nullable=False)
    post_id = db.Column(db.Integer, ForeignKey('entrada.id'),nullable=False)

    def __str__(self):
        return self.titulo
    
class Categoria(db.Model):
    __teblename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class UsuarioActual(db.Model):
    __teblename__ = 'usuario_actual'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario_actual = db.Column(db.Integer, nullable=False)
    





@app.context_processor
def inject_mensaje():
    entradas = Entrada.query.all()
    usuarios = Usuario.query.all()
    usuarioActual = UsuarioActual.query.all()
    comentarios = Comentario.query.all()
    categorias = Categoria.query.all()
    return dict(
        usuarios = usuarios,
        entradas = entradas,
        usuarioActual = usuarioActual,
        comentarios = comentarios,
        categorias = categorias
        
    )

@app.route("/")
def index():
    return render_template(
        'index.html'
    )

@app.route("/registrarse")
def registrarse():
    return render_template(
        'registrarse.html'
    )
@app.route("/blog")
def blog():
   
    return render_template(
        'blog.html',
        
    )


@app.route('/crear_nuevo_usuario', methods=['POST'])
def agregar_usuario():
    usuarios = Usuario.query.all()
    if request.method == 'POST':
        nombre_usuario = request.form['username']
        password_usuario = request.form['password']
        email_usuario = request.form['email']
        nuevo_usuario = Usuario(username=nombre_usuario, email=email_usuario,password=password_usuario)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        usuarioActual = UsuarioActual(id_usuario_actual = nuevo_usuario.id)
        db.session.add(usuarioActual)
        db.session.commit()

        return redirect(url_for('blog'))

@app.route('/crear_nuevo_post', methods=['POST'])
def agregar_post():
    usuarioActual = UsuarioActual.query.all()
    categorias = Categoria.query.all()
    fecha = date.today()
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['entrada']        
        usuario_id = usuarioActual[-1].id_usuario_actual
        for categoria in categorias: 
            if categoria.nombre == request.form['categoria']:
                categoria_id = categoria.id
        nueva_entrada = Entrada(titulo=titulo, contenido=contenido,fecha=fecha,usuario_id=usuario_id,categoria_id = categoria_id)
        
        db.session.add(nueva_entrada)
        db.session.commit()
        

        return redirect(url_for('blog'))

@app.route('/crear_nuevo_comentario', methods=['POST'])
def agregar_comentario():
    usuarioActual = UsuarioActual.query.all()
    entradas = Entrada.query.all()
    fecha = date.today()
    if request.method == 'POST':
        contenido = request.form['comentario']        
        usuario_id = usuarioActual[-1].id_usuario_actual
        post_id = 0
        for entrada in entradas:
            if entrada.titulo.strip() == request.form['entrada'].strip():
                post_id = entrada.id
                print('si')
                
        nuevo_comentario = Comentario(contenido=contenido,fecha=fecha,usuario_id=usuario_id, post_id = post_id)
        
        
        db.session.add(nuevo_comentario)
        db.session.commit()
        

        return redirect(url_for('blog'))

@app.route('/entrar', methods=['POST'])
def entrar():
    if request.method == 'POST':
        usuarios = Usuario.query.all()
        for usuario in usuarios:
            if usuario.username == request.form['username'] and usuario.password == request.form['password']:
              usuarioActual = UsuarioActual(id_usuario_actual = usuario.id)
              db.session.add(usuarioActual)
              db.session.commit()
              return redirect(url_for('blog'))