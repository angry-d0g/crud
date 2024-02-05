from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgre@localhost/personnel_department'  # Замените значения подключения к вашей базе данных PostgreSQL
db = SQLAlchemy(app)


class Members(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #, autoincrement=True
    dob = db.Column(db.Date, nullable=False)

    fk_department = db.Column(db.Integer, db.ForeignKey("department.id"),  nullable=False)#!!!!!!!!!!!!!!!!

    fio = db.Column(db.String(128))

    relH = db.relationship('History', backref='history', cascade="all, delete-orphan")
    relMT = db.relationship('MemTrips', backref='mem_trips', cascade="all, delete-orphan")


    
    def __repr__(self):
        return f"<Member {self.fio}>"




class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    members = db.Column(db.Integer, nullable=False)



    def __repr__(self):
        return f"<Department {self.name}>"


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.BigInteger, primary_key=True)
    dat = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(128))
    pos = db.Column(db.String(256), nullable=False)

    fk_member = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)#!!!!!!!!!!!!

    tel_number = db.Column(db.String(128))

    def __repr__(self):
        return f"<History {self.id}>"


class MemTrips(db.Model):
    __tablename__ = 'mem_trips'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #, autoincrement=True

    mem_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False)


    def __repr__(self):
        return f"<MemTrips {self.id}>"


class Trips(db.Model):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128), nullable=False)
    costs = db.Column(db.Integer)

    rel_mt = db.relationship('MemTrips', backref='history', cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Trips {self.city}>"



## отображение и добавление данных 

@app.route('/', methods =['POST', 'GET'])
def index():

    if request.method == "POST":
        dob = request.form['dob']
        fk_department = request.form['fk_department']
        fio = request.form['fio']

        members = Members(dob=dob, fk_department=fk_department, fio=fio)

        try:
            db.session.add(members)
            db.session.commit()
            return redirect('/')
        except:
            return "Такого department.id не существует!"
    else:
        members = Members.query.order_by(Members.id.desc()).all()
        return render_template('members.html', rows=members)

@app.route('/history', methods=['POST', 'GET'])
def history():
    if request.method == "POST":
        dat = request.form['dat']
        email = request.form['email']
        pos = request.form['position']
        fk_member = request.form['fk_member']
        tel_number = request.form['tel_number']

        members = History(dat=dat, email=email, pos=pos, fk_member=fk_member, tel_number=tel_number)


        try:
            db.session.add(members)
            db.session.commit()
            return redirect('/history')
        except: 
            return "При добавлении строки произошла ошибка"
    else:
        members = History.query.order_by(History.id.desc()).all()
        return render_template('history.html', rows=members)
    

@app.route('/department', methods =['POST', 'GET'])
def department():
    if request.method == "POST":
        name = request.form['name']
        members = request.form['members']

        members = Department( name=name, members=members)#!!!!!!!

        try:
            db.session.add(members)
            db.session.commit()
            return redirect('/department')
        except: 
            return "При добавлении строки произошла ошибка"
    else:
        
        members = Department.query.order_by(Department.id.desc()).all()

        return render_template('department.html', rows=members)

@app.route('/trips', methods =['POST', 'GET'])
def trips():
    if request.method == "POST":
        city = request.form['city']
        costs = request.form['costs']
        
        members = Trips(city=city, costs=costs)

        try:
            db.session.add(members)
            db.session.commit()
            return redirect('/trips')
        except: 
            return "При добавлении строки произошла ошибка"
    else:
        members = Trips.query.order_by(Trips.id.desc()).all()
        return render_template('trips.html', rows=members)
    

@app.route('/mem_trips', methods =['POST', 'GET'])
def mem_trips():
    if request.method == "POST":
        mem_id = request.form['mem_id']
        trip_id = request.form['trip_id']
        
        members = MemTrips(mem_id=mem_id, trip_id=trip_id)

        try:
            db.session.add(members)
            db.session.commit()
            return redirect('/mem_trips')
        except: 
            return "При добавлении строки произошла ошибка! Проверьте существуют ли member.id и trip.id, которые вы хотите добавить."
    else:
        members = MemTrips.query.order_by(MemTrips.id.desc()).all()
        return render_template('mem_trips.html', rows=members)





## удаление строк !!!!!!!!!!!!!!!!!!!!!

@app.route('/trips/<int:id>/del')
def trips_del(id):
    # print(id)
    
    members = Trips.query.get_or_404(id)
    # print(members)



    # try:
    db.session.delete(members)
    db.session.commit()
    return redirect ('/trips')
    # except:
    #     return "При удалении строки произошла ошибка"


@app.route('/department/<int:id>/del')
def department_del(id):
    
    members = Department.query.get_or_404(id)



    try:
        db.session.delete(members)
        db.session.commit()
        return redirect ('/department')
    except:
        return "Измините id отдела у сотрудников"

@app.route('/mem_trips/<int:id>/del')
def mem_trips_del(id):

    # members = MemTrips.query.filter_by(mem_id=m).all()
    members = MemTrips.query.get_or_404(id)
    # try:
    db.session.delete(members)
    db.session.commit()
    return redirect ('/mem_trips')
    # except:
    #     return "При удалении строки произошла ошибка"


@app.route('/members/<int:id>/del')
def members_del(id):
    members = Members.query.get_or_404(id)
    # try:
    db.session.delete(members)
    db.session.commit()
    return redirect ('/')
    # except:
    #     return "При удалении строки произошла ошибка"


@app.route('/hystory/<int:id>/del')
def history_del(id):
    members = History.query.get_or_404(id)
    # try:
    db.session.delete(members)
    db.session.commit()
    return redirect ('/history')
    # except:
    #     return "При удалении строки произошла ошибка"






#изменение строк

@app.route('/update_member', methods=['POST'])
def update_member():
    member_id = request.form.get('id')
    new_dep = request.form.get('dep')

    member = Members.query.get(member_id)
    member.fk_department = new_dep

    db.session.commit()

    return jsonify({'status': 'success'})


@app.route('/update_department', methods=['POST'])
def update_department():
    member_id = request.form.get('id')
    new_members = request.form.get('members')

    member = Department.query.get(member_id)
    member.members = new_members

    db.session.commit()

    return jsonify({'status': 'success'})

@app.route('/update_trips', methods=['POST'])
def update_trips():
    member_id = request.form.get('id')
    new_costs = request.form.get('costs')

    member = Trips.query.get(member_id)
    member.costs = new_costs

    db.session.commit()

    return jsonify({'status': 'success'})

#добавление строк
# @app.route('/add_record', methods=['POST'])
# def add_member():
#     dob = request.form['dob']
#     fk_department = request.form['fk_department']
#     fio = request.form['fio']


#     new_member = Members(fio=fio, dob=dob, fk_department=fk_department)
#     db.session.add(new_member)
#     db.session.commit()

#     return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)