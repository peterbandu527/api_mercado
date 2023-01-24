from flask import Flask,jsonify,request,render_template,Response
import json
from functions import TodosProducto,limiteProducto
import requests

app = Flask(__name__)
@app.route('/',methods=["GET","POST"])
def Home():
    if request.method=="POST":
        print("hola")
        producto = request.form["producto"]
        limite = request.form["limite"]
        r = requests.get('https://api-mercadolibre.onrender.com/mercado_libre',json={"producto":producto,"limite":int(limite)})
        print(r.status_code)
        if r.status_code==200:        
            data = json.loads(r.text)
            
            t = ""
            for i,j,z in zip(data["datos"]["titulos"],data["datos"]["precios"],data["datos"]["urls"]):
                print(i,j,z)
                t += f"{i}|{j}|{z}\n"
            return Response(
                t,
                mimetype="csv",
                headers={
                    "content-disposition":"attachment; filename=datos_mercado_libre.csv"
                }
            )
            
        return"Error"
        pass
    return render_template('index.html')

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
    app.run(port=5001,debug=True)