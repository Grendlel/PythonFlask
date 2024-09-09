from flask import Flask, render_template, request, flash, redirect
app = Flask(__name__)
from database import db
from flask_migrate import Migrate
from models import Pedidos
app.config['SECRET_KEY'] = '9ebe6f92407c97b3f989420e0e6bebcf9d1976b2e230acf9faf4783f5adffe1b'

# --> drive://usuario:senha@servidor/banco_de_dados

conexao = "mysql+pymysql://alunos:cefetmg@127.0.0.1/FlaskGabriel"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aula')
@app.route('/aula/<nome>')
@app.route('/aula/<nome>/<curso>')
@app.route('/aula/<nome>/<curso>/<int:ano>')
def aula(nome = 'Gabriel', curso = 'Informática', ano = '1'):
    dados = {'nome':nome, 'curso':curso, 'ano':ano}
    return render_template('aula.html', dados_curso=dados)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/dados', methods=['POST'])
def dados():
    flash('Dados Enviados!!!')
    dados = request.form
    return render_template('dados.html', dados = dados)

@app.route("/pedidos")
def pedidos():
    p = Pedidos.query.all()
    return render_template("pedidos_lista.html", dados = p)

@app.route("/pedidos/add")
def pedidos_add():
    return render_template('pedidos_add.html')

@app.route("/pedidos/save", methods=['POST'])
def pedidos_save():
    data_pedido = request.form.get('data_pedido')
    valor_total = request.form.get('valor_total')
    status = request.form.get('status')
    if data_pedido and valor_total and status:
        pedidos = Pedidos(data_pedido, valor_total, status)
        db.session.add(pedidos)
        db.session.commit()
        flash('Pedido Cadastrado com sucesso!!!')
        return redirect('/pedidos')
    else:
        flash('Preencha todos os campos!!!')
        return redirect('/pedidos')

@app.route("/pedidos/remove/<int:id>")
def pedidos_remove(id_pedido):
    pedidos = Pedidos.query.get(id_pedido)
    if pedidos:
        db.session.delete(pedidos)
        db.session.commit()
        flash("Pedido removido com sucesso!!")
        return redirect("/pedidos")
    else:
        flash("Caminho Incorreto")
        return redirect("/pedidos")

@app.route("/pedidos/edita/<int:id>")
def pedidos_edita(id):
    pedidos = Pedidos.query.get(id)
    return render_template("pedidos_edita.html", dados=pedidos)

@app.route("/pedidos/editasave", methods=["POST"])
def pedidos_editasave():
    data_pedido = request.form.get('data_pedido')
    valor_total = request.form.get('valor_total')
    status = request.form.get('status')
    id_pedido = request.form.get('id_pedido')
    if id_pedido and data_pedido and valor_total and status:
        pedidos = Pedidos.query.get(id_pedido)
        pedidos.data_pedido = data_pedido
        pedidos.valor_total = valor_total
        pedidos.status = status
        db.session.commit()
        flash("Dados Atualizados com sucesso!")
        return redirect("/pedidos")
    else:
        flash("Faltando dados!!!")
        return redirect("/pedidos")


if __name__ == '__main__':
    app.run()