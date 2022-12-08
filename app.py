import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Access hawaii.sqlite database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect database tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Reference tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)

# create flask app
app = Flask(__name__)

#######################
# Welcome
#######################
@app.route('/')
def welcome():
    return (
        f'Welcome to the Climate Analysis API!'
        f'Available Routes:'
        f'/api/v1.0/precipitation'
        f'/api/v1.0/stations'
        f'/api/v1.0/tobs'
        f'/api/v1.0/temp/start/end'
    )

#######################
# Precipitation
#######################
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#######################
# Stations
#######################
@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#######################
# tobs
#######################
@app.route('/api/v1.0/tobs')
def temp_monthly():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()

    temps = list(np.ravel(results))
    return jsonify(temps = temps)

#######################
# Starting and ending date
#######################
@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')
def stats(start=None,end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Had to add the following for the app to work with 'Hello world' example
#if __name__ == '__main__':
#    app.run(debug=True)