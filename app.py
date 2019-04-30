import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
 
app = Flask(__name__)

@app.route('/')
def home():
    return(
        f'List of available routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
    )

@app.route('/api/v1.0/precipitation/<date>')
def prcp(date):
    result = list(np.ravel(session.query(Measurement.date, func.sum(Measurement.prcp)).filter(Measurement.date==date).all()))
    dict_result={result[0]:result[1]}
    
    return jsonify(dict_result)
    
    
@app.route('/api/v1.0/stations')
def stations():
    stations = session.query(Station.station).all()
    return jsonify(stations)


@app.route('/api/v1.0/tobs')
def tobs():
    date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date = list(date)
    date = dt.datetime.strptime(date[0], '%Y-%m-%d')
    year_date = date - dt.timedelta(days=365)
    year_date = year_date.strftime('%Y-%m-%d')
    result = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date==year_date).order_by(Measurement.date.desc()).all()
    #result = list(np.ravel(result))
    return jsonify(result)

@app.route('/api/v1.0/<start>')
def temps1(start):
    start_date = start
    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >=start_date).all()
    return jsonify(temps)

@app.route('/api/v1.0/<start>/<end>')
def temps2(start, end):
    start_date = start
    end_date = end
    temps2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(temps2)
    
if __name__ == "__main__":
    app.run(debug=True)