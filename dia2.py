# ejemplo en un mismo archivo (no recomendado)
# mezcla de UI, lógica de negocio y acceso a datos
from flask import Flask, request, jsonify
import sqlite3
import os
 
app = Flask(__name__)
DB_FILE = "app.db"
 
# --- Setup "rápido y sucio": crear DB y tabla  ---
def init_db():
    create = not os.path.exists(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    if create:
        conn.execute("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.commit()
    conn.close()
 
init_db()
 
# --- "Helper" super simple (sin repositorios, sin capas) ---
def get_conn():
    return sqlite3.connect(DB_FILE)
 
# --- ENDPOINTS: TODO EN EL MISMO LUGAR (UI + LÓGICA + SQL) ---
 
@app.get("/products")
def list_products():
    # Lógica de consulta y mapeo mezclada con la capa web
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, price, stock FROM products")
    rows = cur.fetchall()
    conn.close()
    items = [{"id": r[0], "name": r[1], "price": r[2], "stock": r[3]} for r in rows]
    return jsonify(items)
 
@app.post("/products")
def create_product():
    data = request.get_json() or {}
    # Validaciones ad-hoc aquí mismo (deberían vivir en dominio/casos de uso)
    name = (data.get("name") or "").strip()
    price = data.get("price")
    stock = data.get("stock", 0)
 
    if not name:
        return jsonify({"error": "name is required"}), 400
    try:
        price = float(price)
        stock = int(stock)
        if price < 0 or stock < 0:
            return jsonify({"error": "price/stock must be >= 0"}), 400
    except Exception:
        return jsonify({"error": "invalid price/stock"}), 400
 
    # Acceso a datos inline (sin puerto/repositorio)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
                (name, price, stock))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({"id": new_id, "name": name, "price": price, "stock": stock}), 201
 
@app.put("/products/<int:pid>")
def update_product(pid):
    data = request.get_json() or {}
    # Validaciones/lógica de negocio aquí (mezcladas)
    fields = []
    params = []
 
    if "name" in data:
        name = (data.get("name") or "").strip()
        if not name:
            return jsonify({"error": "name cannot be empty"}), 400
        fields.append("name = ?")
        params.append(name)
 
    if "price" in data:
        try:
            price = float(data["price"])
            if price < 0:
                return jsonify({"error": "price must be >= 0"}), 400
            fields.append("price = ?")
            params.append(price)
        except Exception:
            return jsonify({"error": "invalid price"}), 400
 
    if "stock" in data:
        try:
            stock = int(data["stock"])
            if stock < 0:
                return jsonify({"error": "stock must be >= 0"}), 400
            fields.append("stock = ?")
            params.append(stock)
        except Exception:
            return jsonify({"error": "invalid stock"}), 400
 
    if not fields:
        return jsonify({"error": "no fields to update"}), 400
 
    conn = get_conn()
    cur = conn.cursor()
    params.append(pid)
    cur.execute(f"UPDATE products SET {', '.join(fields)} WHERE id = ?", params)
    if cur.rowcount == 0:
        conn.close()
        return jsonify({"error": "product not found"}), 404
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})
 
@app.delete("/products/<int:pid>")
def delete_product(pid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = ?", (pid,))
    if cur.rowcount == 0:
        conn.close()
        return jsonify({"error": "product not found"}), 404
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"})
 
if __name__ == "__main__":
    # ejecución directa (sin configuración por entorno)
    app.run(debug=True, host="127.0.0.1", port=5000)
