from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ganti dengan kunci rahasia Anda

# Konfigurasi koneksi ke database
db_config = {
    'user': 'root',  # ganti dengan user MySQL Anda
    'password': '',  # ganti dengan password MySQL Anda
    'host': 'localhost',
    'database': 'pelatihan'
}

# Fungsi untuk mendapatkan koneksi ke database
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pendaftaran')
def pendaftaran():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM peserta')
    peserta = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('pendaftaran.html', peserta=peserta)

@app.route('/pendaftar')
def list_pendaftar():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM peserta')
    peserta = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('pendaftar.html', peserta=peserta)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        nik = request.form['nik']
        no_whatsapp = request.form['no_whatsapp']
        email = request.form['email']
        program_pelatihan = request.form['program_pelatihan']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO peserta (name, nik, no_whatsapp, email, program_pelatihan) '
            'VALUES (%s, %s, %s, %s, %s)',
            (name, nik, no_whatsapp, email, program_pelatihan)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('list_pendaftar'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        nik = request.form['nik']
        no_whatsapp = request.form['no_whatsapp']
        email = request.form['email']
        program_pelatihan = request.form['program_pelatihan']

        cursor.execute(
            'UPDATE peserta SET name = %s, nik = %s, no_whatsapp = %s, email = %s, program_pelatihan = %s '
            'WHERE id = %s',
            (name, nik, no_whatsapp, email, program_pelatihan, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('list_pendaftar'))
    
    cursor.execute('SELECT * FROM peserta WHERE id = %s', (id,))
    peserta = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('pendaftaran.html', peserta=[peserta])

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM peserta WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('list_pendaftar'))

if __name__ == '__main__':
    app.run(debug=True)
