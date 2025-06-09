from fastapi import FastAPI, HTTPException,Depends,status
from sqlalchemy import Column,Integer,Date,create_engine,String
from datetime import date
from sqlalchemy.orm import declarative_base,sessionmaker,Session
from pydantic import BaseModel
from typing import Optional

engine = create_engine("sqlite:///./booking.db",echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

app = FastAPI()

class ServiceBooking(Base):
    __tablename__="service_bookings_table"
    id = Column(Integer,primary_key=True,index=True)
    customer_name = Column(String,nullable=False)
    vehicle_number = Column(String,nullable=False)
    service_type = Column(String,nullable=False)
    booking_date = Column(Date,nullable=False)

Base.metadata.create_all(engine)

#pydantic
class ServiceBookingCreate(BaseModel):
    customer_name : str 
    vehicle_number : str
    service_type :str
    booking_date :date

class ServiceBookingUpdate(BaseModel):
    customer_name : Optional[str] = None
    vehicle_number : Optional[str]=None
    service_type :Optional[str]=None
    booking_date :Optional[date]=None


#dependency
def get_dp():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"hello":"welcome to our vehicle service centre"}


@app.post("/bookings/")
def create_booking(booking : ServiceBookingCreate , db : Session = Depends(get_dp)):
    
    if booking.booking_date< date.today():
        raise HTTPException(status_code=status.WS_1003_UNSUPPORTED_DATA, detail="INVALID DATE...!")

    new_booking = ServiceBooking(customer_name=booking.customer_name,
                                 vehicle_number=booking.vehicle_number,
                                 service_type=booking.service_type,
                                 booking_date= booking.booking_date
                                 )
    
    try:
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
    except Exception as e:
        db.rollback()
        print(f'Error occured -> {e}')
    
    return new_booking
    

@app.get("/bookings/get-all")
def get_all_bookings(db : Session = Depends(get_dp)):
    bookings = db.query(ServiceBooking).all()
    return bookings


@app.get("/bookings/{booking_id}")
def get_booking_byID(booking_id : int ,db : Session = Depends(get_dp)):
   
    try:
        booking = db.query(ServiceBooking).filter(ServiceBooking.id==booking_id).first()

        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Booking Not found...!")
    
    except Exception as e:
        print(f'Error occured->{e}')

    return booking

@app.put("/bookings/update/{booking_id}")
def update_booking(booking_id :int ,update_booking : ServiceBookingUpdate , db : Session = Depends(get_dp)):
    
    try:
        booking = db.query(ServiceBooking).filter(ServiceBooking.id == booking_id).first()

        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Booking Not found...!")
        if update_booking.booking_date is not None and update_booking.booking_date < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking date cannot be in the past."
            )

        if update_booking.customer_name is not None:
            booking.customer_name=update_booking.customer_name
        if update_booking.vehicle_number is not None:
            booking.vehicle_number = update_booking.vehicle_number
        if update_booking.booking_date is not None:
            booking.booking_date = update_booking.booking_date
        if update_booking.service_type is not None:
            booking.service_type = update_booking.service_type

        try:
            db.commit()
            db.refresh(booking)
        except Exception as e:
            db.rollback()
            print(f'error occured->{e}')

    except Exception as e:
        print(f'error occured->{e}')

    return booking


@app.delete("/bookings/delete/{booking_id}")
def delete_booking_byID(booking_id : int ,db : Session = Depends(get_dp)):

    try:
        booking = db.query(ServiceBooking).filter(ServiceBooking.id == booking_id).first()

        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Booking Not found...!")
        
        try:
            db.delete(booking)
            db.commit()
            db.refresh()

        except Exception as e:
            db.rollback()
            print(f'Error Occurred : {e}')
    except:
        print(f'error occured->{e}')

    return {"detail": "Booking deleted successfully."}
