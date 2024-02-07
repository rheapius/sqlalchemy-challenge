# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file

engine= create_engine("sqlite:///../rheapius/desktop/Starter_Code/Resources/hawaii.sqlite")
conn= engine.connect()

# Declare a Base using `automap_base()`
Base= automap_base()
Base.prepare(autoload_with=engine)

# Use the Base class to reflect the database tables
Base.classes.keys()

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement= Base.classes.measurement
Station=Base.classes.station

# Create a session
session= Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
#List all available api routes
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Enter start and end date for temperature data:<br>"
        f"/api/v1.0/ "
    )

#list of dates & precipitation
@app.route("/api/v1.0/precipitation")
def prcp():

    session= Session(engine)
    precipitation= session.query(Measurement.date,Measurement.prcp).all()
    session.close()
    dictionary= [dict(row) for row in precipitation]
    return jsonify(dictionary)

#list of stations
@app.route("/api/v1.0/stations")
def station():
    session= Session(engine)
    stations= session.query(Station.station).all()
    session.close()
    station_names= list(np.ravel(stations))
    return jsonify(station_names)

#list of dates and temperature observations of the most-active station for the previous year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    temp= session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > '2016-08-23')\
                            .filter(Measurement.station=='USC00519281').all()
    session.close()
    temperature= list(np.ravel(temp))
    return jsonify(temperature)

#Temperature stats from the entered start date
@app.route("/api/v1.0/<start>")
def info(start):
    canonicalised= start.replace("","")

    session=Session(engine)
    stats=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))\
                 .filter(Measurement.station=='USC00519281').filter(Measurement.date>=canonicalised).all()
    session.close()

    list_stats= list(np.ravel(stats))
    return jsonify(list_stats)

# Accepting start & end dates for temperature data
@app.route("/api/v1.0/<start>/<end>")
def function(start,end):
    start_date= start.replace("","")
    end_date= end.replace("","")
    
    session=Session(engine)
    stats=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))\
                 .filter(Measurement.station=='USC00519281').filter(Measurement.date>=start_date)\
                 .filter(Measurement.date<=end_date).all()
    session.close()

    list_stats= list(np.ravel(stats))
    return jsonify(list_stats)


#Running the flask code

if __name__ == "__main__":
    app.run(debug=True)


