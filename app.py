from flask import Flask,jsonify,request
import json
from functions import TodosProducto,limiteProducto
app = Flask(__name__)
@app.route('/')
def Home():
    return 'hola'

@app.route('/mercado_libre', methods=["GET"])
def mercadoLibre():
    print(request.data,type(request.data))
    data = json.loads(request.data)
    if "limite" not in data:
        titulos,urls,precios = TodosProducto(data["producto"])
    else:
        titulos,urls,precios = limiteProducto(data["producto"],data["limite"])            
    return jsonify({"datos":{"titulos":titulos,"urls":urls,"precios":precios}})


if __name__ =="__main__":
    app.run("0.0.0.0",debug=True)