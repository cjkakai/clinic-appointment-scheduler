from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random

from lib.db.models import Base, Doctor, Patient, Appointment

fake = Faker()

engine = create_engine("sqlite:///app.db") 
Session = sessionmaker(bind=engine)
session = Session()

def seed():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    doctors = [
        Doctor(
            name=fake.name(),
            specialization=fake.job()
        )
        for _ in range(5)
    ]
    session.add_all(doctors)

    patients = [
        Patient(
            name=fake.name(),
            age=random.randint(1, 90)
        )
        for _ in range(15)
    ]
    session.add_all(patients)
    session.commit()  

    appointments = []
    for _ in range(20):
        doctor = random.choice(doctors)
        patient = random.choice(patients)
        date = datetime.now() + timedelta(days=random.randint(0, 30))
        appointments.append(
            Appointment(date=date, doctor=doctor, patient=patient)
        )

    session.add_all(appointments)
    session.commit()

    print("🌱 Database seeded successfully!")

if __name__ == "__main__":
    seed()
