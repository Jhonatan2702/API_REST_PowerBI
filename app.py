from flask import Flask, jsonify
import pyodbc
import pandas as pd
import requests

app = Flask(__name__)

# Configuração do SQL Server
SQL_SERVER = "servidor"
DATABASE = "nome do banco de dados"
USERNAME = "usuario"
PASSWORD = "senha"
DRIVER = "ODBC Driver 17 for SQL Server"

# String de conexão
conn_str = f"DRIVER={{{DRIVER}}};SERVER={SQL_SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};TrustServerCertificate=yes"

# Power BI API
POWER_BI_URL = "https://api.powerbi.com/beta/{workspace_id}/datasets/{dataset_id}/rows?key={api_key}"

@app.route('/update_powerbi', methods=['GET'])
def update_powerbi():
    try:
        # Conectar ao SQL Server
        conn = pyodbc.connect(conn_str)
        query = "SELECT id, nome, valor FROM produtos"  # Ajuste conforme necessário
        df = pd.read_sql(query, conn)
        conn.close()

        # Converter para JSON no formato esperado pelo Power BI
        data = df.to_dict(orient='records')

        # Enviar os dados para o Power BI
        headers = {"Content-Type": "application/json"}
        response = requests.post(POWER_BI_URL, json=data, headers=headers)

        return jsonify({"status": response.status_code, "message": response.text})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
