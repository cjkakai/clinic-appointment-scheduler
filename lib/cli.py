from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.db.models import Base, Doctor, Patient, Appointment

DB_URL = "sqlite:///app.db"  # make sure it matches your seeder
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

def list_doctors():
    print("\n--- Doctors ---")
    for doc in session.query(Doctor).all():
        print(f"{doc.id}: {doc.name} ({doc.specialization})")

def list_patients():
    print("\n--- Patients ---")
    for pat in session.query(Patient).all():
        print(f"{pat.id}: {pat.name}, Age: {pat.age}")

def list_appointments():
    print("\n--- Appointments ---")
    for appt in session.query(Appointment).all():
        print(f"{appt.id}: {appt.date.strftime('%Y-%m-%d %H:%M')} | Doctor: {appt.doctor.name} | Patient: {appt.patient.name}")

def schedule_appointment():
    list_doctors()
    doc_id = int(input("Enter doctor ID: "))
    list_patients()
    pat_id = int(input("Enter patient ID: "))
    date_str = input("Enter appointment date & time (YYYY-MM-DD HH:MM): ")
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")

    doctor = session.query(Doctor).get(doc_id)
    patient = session.query(Patient).get(pat_id)

    new_appt = Appointment(doctor=doctor, patient=patient, date=date)
    session.add(new_appt)
    session.commit()
    print(f"✅ Appointment scheduled for {patient.name} with {doctor.name} on {date}")

def main_menu():
    while True:
        print("\n--- Clinic Appointment CLI ---")
        print("1. List Doctors")
        print("2. List Patients")
        print("3. List Appointments")
        print("4. Schedule Appointment")
        print("5. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            list_doctors()
        elif choice == "2":
            list_patients()
        elif choice == "3":
            list_appointments()
        elif choice == "4":
            schedule_appointment()
        elif choice == "5":
            print("Thanks for using the CLI!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main_menu()
