from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///text_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class TextEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    judgement = db.Column(db.String(50), nullable=True)
    judged_at = db.Column(db.DateTime, nullable=True)

# Create Database Tables
with app.app_context():
    db.create_all()

# Route to display and add text
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_text = request.form['text']
        entry = TextEntry(text=new_text)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('index'))
    
    entries = TextEntry.query.order_by(TextEntry.created_at.desc()).all()
    return render_template('index.html', entries=entries)

# Route to add judgement
@app.route('/judge/<int:id>', methods=['POST'])
def judge(id):
    entry = TextEntry.query.get(id)
    if entry:
        entry.judgement = request.form['judgement']
        entry.judged_at = datetime.utcnow()
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
