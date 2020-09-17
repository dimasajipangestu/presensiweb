from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy  # add
from datetime import datetime  # add
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # add
db = SQLAlchemy(app)  # add

indonesia = pytz.timezone('Asia/Jakarta')


# add
class Presensi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(80), nullable=False)
    nim = db.Column(db.Integer, primary_key=False)
    waktu = db.Column(db.DateTime, nullable=False,
                           default=datetime.now(indonesia))

    def __repr__(self):
        return '<Presensi %r>' % self.name


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']
        waktu = datetime.now(indonesia)
        new_presensi = Presensi(nama=nama, nim=nim, waktu=waktu)

        try:
            db.session.add(new_presensi)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"

    else:
        presensi = Presensi.query.order_by(Presensi.waktu.desc(), Presensi.nim).all()
        return render_template('index.html', presensi=presensi)

@app.route('/delete/<int:id>')
def delete(id):
    presensi = Presensi.query.get_or_404(id)

    try:
        db.session.delete(presensi)
        db.session.commit()
        return redirect('/')
    except:
        return "Error"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
