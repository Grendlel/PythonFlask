from database import db

class Pedidos(db.Model):
    __tablename__= "pedidos"
    id_pedido = db.Column(db.Integer, primary_key = True)
    data_pedido = db.Column(db.Date)
    valor_total = db.Column(db.Float(10, 2))
    status = db.Column(db.String(20))

    # construtor
    def __init__(self, data_pedido, valor_total, status):
        self.data_pedido = data_pedido
        self.valor_total = valor_total
        self.status = status

    # representação do objeto criado...
    def __repr__(self):
        return "<ID do Pedido: {}>".format(self.id_pedido)