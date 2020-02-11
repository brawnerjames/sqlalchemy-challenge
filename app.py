from flask import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
from flask import Flask, jsonify



engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station




app = Flask(__name__)

@app.route("/")
def index():
    
    return"Endpoints: " "http://127.0.0.1:5000/api/v1.0/precipitation" ' ' "http://127.0.0.1:5000/api/v1.0/stations" ' ' "http://127.0.0.1:5000/api/v1.0/tobs" '' "http://127.0.0.1:5000/api/v1.0/start" ' ' "http://127.0.0.1:5000/api/v1.0/startend"
    
        
    
    


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    session.close()

    all_precip = list(np.ravel(results))
    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()

    session.close()

    all_stations = list(np.ravel(results))
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station == 'USC00519281').all()

    session.close()

    all_tobs = list(np.ravel(results))
    return jsonify(all_tobs)

@app.route("/api/v1.0/start")
def start():
    session = Session(engine)
    start_date = '2016-08-23'

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    session.close()

    start_list = list(np.ravel(results))
    return jsonify(start_list)


@app.route("/api/v1.0/startend")
def startend():
    session = Session(engine)

    start_date = '2015-08-23'
    end_date = '2016-08-23'

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    start_end_list = list(np.ravel(results))
    return jsonify(start_end_list)




if __name__ == "__main__":
    app.run(debug=True)