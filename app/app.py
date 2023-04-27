from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'penjualan'
app.config['MYSQL_PORT'] = 3306
mysql = MySQL(app)

#root
@app.route('/')
def root():
    return 'Selamat Datang Ini adalah root end point Restfull API Penjualan'

# Menambahkan produk baru
@app.route('/produk', methods=['POST'])
def tambah_produk():
    cur = mysql.connection.cursor()
    nama = request.json['nama']
    harga = request.json['harga']
    stok = request.json['stok']
    cur.execute("INSERT INTO produk (nama, harga, stok) VALUES (%s, %s, %s)", (nama, harga, stok))
    mysql.connection.commit()
    cur.close()
    return jsonify({'status': 'sukses'})

# Mendapatkan semua produk
@app.route('/all-produk', methods=['GET'])
def semua_produk():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM produk')
    col_names = [i[0] for i in cur.description]
    result = []
    for row in cur.fetchall():
        result.append(dict(zip(col_names, row)))
    cur.close()
    return jsonify(result)

# Mendapatkan semua produk berdasarkan nama produk yang mirip
@app.route('/produk', methods=['GET'])
def search_produk():
    cur = mysql.connection.cursor()
    name = request.args.get('name')
    cur.execute("SELECT * FROM produk WHERE nama LIKE %s", ("%" + name + "%",))
    col_names = [i[0] for i in cur.description]
    result = []
    for row in cur.fetchall():
        result.append(dict(zip(col_names, row)))
    cur.close()
    return jsonify(result)

# Mengupdate produk
@app.route('/produk/<int:produk_id>', methods=['PUT'])
def update_produk(produk_id):
    cur = mysql.connection.cursor()
    nama = request.json['nama']
    harga = request.json['harga']
    stok = request.json['stok']
    cur.execute("UPDATE produk SET nama=%s, harga=%s, stok=%s WHERE id=%s", (nama, harga, stok, produk_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'status': 'sukses'})

# Menghapus produk
@app.route('/produk/<int:produk_id>', methods=['DELETE'])
def hapus_produk(produk_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM produk WHERE id=%s", (produk_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'status': 'sukses'})

# Menambahkan pesanan baru
@app.route('/pesanan', methods=['POST'])
def tambah_pesanan():
    cur = mysql.connection.cursor()
    id_produk = request.json['id_produk']
    jumlah = request.json['jumlah']
    cur.execute("INSERT INTO pesanan(id_produk, jumlah, tanggal) VALUES (%s, %s, CURDATE())", (id_produk, jumlah))
    cur.execute("UPDATE produk SET stok=(stok-%s) WHERE id=%s", (jumlah, id_produk))
    mysql.connection.commit()
    cur.close()
    return jsonify({'status': 'sukses'})

# Mendapatkan pesanan berdasarkan produk
@app.route('/pesanan', methods=['GET'])
def pesanan():
    cur = mysql.connection.cursor()
    id_produk = request.args.get('id_produk')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sql = 'SELECT * FROM pesanan WHERE id_produk = %s'
    val = (id_produk,)
    if start_date:
        sql += ' AND tanggal >= %s'
        val += (start_date,)
    
    if end_date:
        sql += ' AND tanggal <= %s'
        val += (end_date,)

    cur.execute(sql, val)

    col_names = [i[0] for i in cur.description]
    result = []
    for row in cur.fetchall():
        result.append(dict(zip(col_names, row)))
    cur.close()
    return jsonify(result)

# Mendapatkan detail pesanan berdasarkan id
@app.route('/pesanan/<int:id>', methods=['GET'])
def detail_pesanan(id):
    cur = mysql.connection.cursor()

    cur.execute('SELECT a.id, a.jumlah, b.nama, (a.jumlah * b.harga) as total_harga, a.tanggal FROM pesanan a INNER JOIN produk b ON a.id_produk = b.id WHERE a.id = %s', (id,))

    col_names = [i[0] for i in cur.description]
    result = []
    for row in cur.fetchall():
        result.append(dict(zip(col_names, row)))
    cur.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
