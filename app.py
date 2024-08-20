from flask import Flask, render_template, request, redirect, url_for
from pony.orm import Database, Required, db_session

app = Flask(__name__)

# Konfigurasi Database
db = Database()
db.bind(provider='mysql', host='localhost', user='root', passwd='', db='db_hutang')

class Hutang(db.Entity):
    nama_penghutang = Required(str)
    jumlah_uang = Required(float)
    nama_pemberi_hutang = Required(str)
    status_hutang = Required(str)

db.generate_mapping(create_tables=True)

@app.route('/tambah_hutang', methods=['GET', 'POST'])
@db_session
def tambah_hutang():
    if request.method == 'POST':
        nama_penghutang = request.form['nama_penghutang']
        jumlah_uang = request.form['jumlah_uang']
        nama_pemberi_hutang = request.form['nama_pemberi_hutang']
        status_hutang = request.form['status_hutang']

        # Simpan data ke database
        Hutang(
            nama_penghutang=nama_penghutang,
            jumlah_uang=float(jumlah_uang),
            nama_pemberi_hutang=nama_pemberi_hutang,
            status_hutang=status_hutang
        )
        
        return redirect(url_for('hutang_terkini'))

    return render_template('tambah_hutang.html')

@app.route('/hutang_terkini')
@db_session
def hutang_terkini():
    hutang_list = Hutang.select()
    return render_template('hutang_terkini.html', hutang_list=hutang_list)

if __name__ == '__main__':
    app.run(debug=True)
