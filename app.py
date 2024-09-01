from flask import Flask, render_template, request, redirect, url_for
from pony.orm import Database, Required, db_session, select
from datetime import datetime  # Tambahkan ini untuk mengimpor modul datetime
import clr

app = app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import MessageBox

db = Database()
db.bind(provider='mysql', host='localhost', user='root', passwd='', db='db_hutang')

class Hutang(db.Entity):
    nama_penghutang = Required(str)
    jumlah_uang = Required(float)
    nama_pemberi_hutang = Required(str)
    status_hutang = Required(str)

db.generate_mapping(create_tables=True)

@app.route('/', methods=['GET', 'POST'])
@db_session
def tambah_hutang():
    MessageBox.Show("Selamat Datang kembali Rauf!")
    if request.method == 'POST':
        nama_penghutang = request.form['nama_penghutang']
        jumlah_uang = request.form['jumlah_uang']
        nama_pemberi_hutang = request.form['nama_pemberi_hutang']
        status_hutang = request.form['status_hutang']

        Hutang(
            nama_penghutang=nama_penghutang,
            jumlah_uang=float(jumlah_uang),
            nama_pemberi_hutang=nama_pemberi_hutang,
            status_hutang=status_hutang
        )
        
        return redirect(url_for('hutang_terkini'))

    return render_template('index.html')


@app.route('/hutang_terkini')
@db_session
def hutang_terkini():
    hutang_list = select(h for h in Hutang)
    return render_template('hutang_terkini.html', hutang_list=hutang_list)

@app.route('/edit_hutang/<int:hutang_id>', methods=['GET', 'POST'])
@db_session
def edit_hutang(hutang_id):
    hutang = Hutang.get(id=hutang_id)  # Mendapatkan objek hutang berdasarkan ID
    
    if not hutang:
        return "Data hutang tidak ditemukan.", 404  # Mengembalikan error 404 jika data tidak ditemukan
    
    if request.method == 'POST':
        hutang.nama_penghutang = request.form['nama_penghutang']
        hutang.jumlah_uang = float(request.form['jumlah_uang'])
        hutang.nama_pemberi_hutang = request.form['nama_pemberi_hutang']
        hutang.status_hutang = request.form['status_hutang']
        # Update created_at ke timestamp saat ini jika perlu
        hutang.created_at = datetime.now()
        
        return redirect(url_for('hutang_terkini'))

    return render_template('edit_hutang.html', hutang=hutang)

@app.route('/delete_hutang/<int:hutang_id>', methods=['GET'])
@db_session
def delete_hutang(hutang_id):
    hutang = Hutang.get(id=hutang_id)
    
    if not hutang:
        return "Data hutang tidak ditemukan.", 404
    
    hutang.delete()  # Menghapus data hutang dari database
    return redirect(url_for('hutang_terkini'))

if __name__ == '__main__':
    app.run(debug=True)
