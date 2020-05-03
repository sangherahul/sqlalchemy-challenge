from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
app=Flask(__name__)


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base=automap_base()


Base.prepare(engine, reflect=True)

measurement=Base.classes.measurement
station=Base.classes.station


@app.route("/")
def home():
       return( f"<h1>Welcome to the home page!</h1> <br/>" 
              f"<h3>Here are the available routes: </h3><br/> 1: /api/v1.0/precipitation <br/> 2: /api/v1.0/stations <br/> 3: /api/v1.0/tobs <br/> 4:/api/v1.0/start_date <br/> 5: /api/v1.0/start_date/end_date")
    

@app.route("/api/v1.0/precipitation")
def prcp():
        session=Session(engine)
        
        date=dt.date(2017,8,23)-dt.timedelta(days=365)
        data=session.query(measurement.date,measurement.prcp).filter(measurement.date>=date).all()
        
        
        dict={date:prcp for date,prcp in data}
        
        session.close()
        
        return jsonify(dict)

@app.route("/api/v1.0/stations")
def station_list():
        session=Session(engine)
        data=session.query(station.name,station.id,station.station).all()
        
        dict={s_name:[id,stn] for s_name,id,stn in data}
        
        session.close()
        
        return jsonify(dict)


@app.route("/api/v1.0/tobs")

def active_stn():
    
    session=Session(engine)
    date=dt.date(2017,8,23)-dt.timedelta(days=365)
    most_temp=session.query(station.name,measurement.station,func.count(measurement.tobs)).filter(station.station==measurement.station).group_by(measurement.station).order_by(func.count(measurement.tobs).desc()).first()

    data1=session.query(measurement.date,measurement.tobs).filter(measurement.date>=date).filter(measurement.station==most_temp[1]).all()
    
    dict={date:tobs for date,tobs in data1}
    session.close()
    
    return jsonify(dict)
    
    
#/api/v1.0/<start> and /api/v1.0/<start>/<end>

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

@app.route("/api/v1.0/<start>")

def date_s(start):
    session=Session(engine)
    date = dt.datetime.strptime(start, '%Y%m%d').date()

    data=session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs).filter(measurement.date>date)).all()
                       
    result=f"Temperature analysis of the days after {date} are as follows: <br/><br/> Minimum temeperature: {data[0][0]} <br/> Maximum Temeprature : {data[0][1]} <br/>Avarage Temperature: {round(data[0][2],2)}"
    session.close()
    
    return (result)

@app.route("/api/v1.0/<start>/<end>")

def date_2(start,end):
    session=Session(engine)
    
    s_date=dt.datetime.strptime(start, '%Y%m%d').date()
    e_date=dt.datetime.strptime(end, '%Y%m%d').date()
    
    data=session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs).filter(measurement.date>s_date).filter(measurement.date <e_date)).all()
    
    results=f"Temperature analysis of the days in between {s_date} and {e_date} are as follows: <br/><br/> Minimum temeperature: {data[0][0]} <br/> Maximum Temeprature : {data[0][1]} <br/>Avarage Temperature: {round(data[0][2],2)}"
    session.close()
    
    return (results)

#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
if __name__=='__main__':
    app.run(debug=True)
              