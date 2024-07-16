# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt
from datetime import date
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

last_year = '2016-08-22'


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date > last_year).order_by(measurement.date).all()
    

    percepitation = []
    for date, prcp in results:
        percepitation_dict = {}
        percepitation_dict["date"]
        percepitation_dict["prcp"]
        percepitation.append(percepitation_dict)


    return jsonify(percepitation)

@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(station.station).all()

    station_names = list(np.ravel(results))

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    stations_activity = session.query(measurement.station, func.count(measurement.tobs).label('count')).group_by(measurement.station).order_by(func.count(measurement.tobs).desc()).first()[0]
    results = session.query(measurement.date, measurement.tobs).filter(measurement.station == stations_activity).filter(measurement.date > last_year).order_by(measurement.date).all()
    
    temp_list = []
    
    for date, tobs in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict['tobs'] = tobs
        temp_list.append(temp_dict)
    

    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def start():

    start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()    
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_date).all()
    
    temp_start = list(np.ravel(results))
    return jsonify(temp_start)

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    temp_start_end = list(np.ravel(results))

    return jsonify(temp_start_end)

if __name__ == '__main__':
    app.run(debug=True)