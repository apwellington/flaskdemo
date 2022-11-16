from flask import Flask, jsonify,request
from config import  config
from flask_mysqldb import MySQL

from src.Curso import Curso

app = Flask(__name__)
conexion = MySQL(app)
response = {'cursos':[], 'message':''}


@app.route("/cursos", methods=['GET'])
def listarCursos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM tuto"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursos = []
        for fila in result:
            curso = {'nombre':fila[0]}
            cursos.append(curso)
        return jsonify({'cursos': cursos, 'message':'success'})
    except Exception as es:
        print(es)
        return jsonify({'message':'succes'})


@app.route("/cursos/<name>", methods=['GET'])
def find_by_name(name):
    try:
        cursor = conexion.connection.cursor()
        sql = f"SELECT * FROM tuto WHERE nombre = %(nombre)s"
        params = {'nombre': name}
        cursor.execute(sql, params)
        datos = cursor.fetchone()
        if datos != None:
            curso = {'nombre': datos[0]}
            return jsonify({'curso': curso, 'message': 'success'})
        else:
            return jsonify({'curso': None, 'message': f'{name} does not exist'})
    except Exception as ex:

        response['message']=f"{ex}"
        return jsonify(response)


def map_from_json_to_curso(request):
    return Curso(request.json['nombre'])


@app.route("/cursos", methods=['POST'])
def save_tuto():
    try:
        cursor = conexion.connection.cursor()
        curso = map_from_json_to_curso(request)
        sql = f"INSERT INTO tuto (NOMBRE) VALUES (%)"
        params = {'nombre': curso.nombre}
        cursor.execute(sql, params)
        conexion.connection.commit()
        return jsonify({'message': 'success'})
    except Exception as ex:
        response['message']=f"{ex}"
        return jsonify(response)


@app.route("/cursos/<name>", methods=['DELETE'])
def delete_tuto(name):
    try:
        cursor = conexion.connection.cursor()
        sql = f"DELETE FROM TUTO  WHERE nombre = %(nombre)s"
        params = {'nombre': name}
        cursor.execute(sql, params)
        conexion.connection.commit()
        return jsonify({'message': 'success'})
    except Exception as ex:
        response['message']=f"{ex}"
        return jsonify(response)



@app.route("/cursos/<name>", methods=['PUT'])
def update_tuto(name):
    try:
        cursor = conexion.connection.cursor()
        curso = map_from_json_to_curso(request)
        sql = "UPDATE TUTO SET NOMBRE = %(nombreI)s WHERE nombre = %(nombreI)s"
        params = {'nombreI': curso.nombre, 'nombreN': curso.nombre}
        cursor.execute(sql, params)
        conexion.connection.commit()
        return jsonify({'message': 'success'})
    except Exception as ex:
        response['message']=f"{ex}"
        return jsonify(response)

def no_encontrada(error):
    return "Not Found"

if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, no_encontrada)
    app.run()



