import click
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.db.models import Base, Doctor, Patient, Appointment

# -------------------------------
# Database setup
# -------------------------------
DB_URL = "sqlite:///app.db"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

def list_doctors():
    click.secho("\n--- Doctors ---", fg="cyan", bold=True)
    for doc in session.query(Doctor).all():
        click.echo(f"{doc.id}: {doc.name} ({doc.specialization})")

def list_patients():
    click.secho("\n--- Patients ---", fg="cyan", bold=True)
    for pat in session.query(Patient).all():
        click.echo(f"{pat.id}: {pat.name}, Age: {pat.age}")

def list_appointments():
    click.secho("\n--- Appointments ---", fg="cyan", bold=True)
    appointments = session.query(Appointment).all()
    if not appointments:
        click.secho("No appointments found.", fg="yellow", bold=True)
        return
    for appt in appointments:
        click.echo(
            f"{appt.id}: {appt.date.strftime('%Y-%m-%d %H:%M')} "
            f"| Doctor: {appt.doctor.name} "
            f"| Patient: {appt.patient.name}"
        )

def schedule_appointment():
    list_doctors()
    doc_id = click.prompt("Enter doctor ID", type=int)
    list_patients()
    pat_id = click.prompt("Enter patient ID", type=int)
    date_str = click.prompt("Enter appointment date & time (YYYY-MM-DD HH:MM)", type=str)

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    except ValueError:
        click.secho("❌ Invalid date format. Use YYYY-MM-DD HH:MM", fg="red", bold=True)
        return

    doctor = session.query(Doctor).get(doc_id)
    patient = session.query(Patient).get(pat_id)

    if not doctor:
        click.secho("❌ Doctor not found.", fg="red", bold=True)
        return
    if not patient:
        click.secho("❌ Patient not found.", fg="red", bold=True)
        return

    if not click.confirm(
        f"Do you want to schedule an appointment for {patient.name} with {doctor.name} on {date}?"
    ):
        click.secho("❌ Appointment cancelled.", fg="yellow", bold=True)
        return

    new_appt = Appointment(doctor=doctor, patient=patient, date=date)
    session.add(new_appt)
    session.commit()
    click.secho(
        f"✅ Appointment scheduled for {patient.name} with {doctor.name} on {date}",
        fg="green",
        bold=True,
    )

def update_appointment():
    list_appointments()
    appt_id = click.prompt("Enter appointment ID to update", fg="yellow", type=int)
    appt = session.query(Appointment).get(appt_id)

    if not appt:
        click.secho("❌ Appointment not found.", fg="red", bold=True)
        return

    new_date_str = click.prompt("Enter new date & time (YYYY-MM-DD HH:MM)", type=str)
    try:
        new_date = datetime.strptime(new_date_str, "%Y-%m-%d %H:%M")
    except ValueError:
        click.secho("❌ Invalid date format. Use YYYY-MM-DD HH:MM", fg="red", bold=True)
        return

    if not click.confirm(f"Change appointment {appt.id} to {new_date}?"):
        click.secho("❌ Update cancelled.", fg="yellow", bold=True)
        return

    appt.date = new_date
    session.commit()
    click.secho(
        f"✅ Appointment {appt.id} updated to {new_date}", fg="green", bold=True
    )

def delete_appointment():
    list_appointments()
    appt_id = click.prompt("Enter appointment ID to delete", type=int)
    appt = session.query(Appointment).get(appt_id)

    if not appt:
        click.secho("❌ Appointment not found.", fg="red", bold=True)
        return

    if not click.confirm(f"Are you sure you want to delete appointment {appt.id}?"):
        click.secho("❌ Deletion cancelled.", fg="yellow", bold=True)
        return

    session.delete(appt)
    session.commit()
    click.secho(f"🗑️ Appointment {appt.id} deleted successfully", fg="green", bold=True)

def main_menu():
    while True:
        click.secho("\n--- Clinic Appointment CLI ---", fg="blue", bold=True)
        click.secho("1. List Doctors", fg="cyan", bold=True)
        click.secho("2. List Patients", fg="cyan", bold=True)
        click.secho("3. List Appointments", fg="cyan", bold=True)
        click.secho("4. Schedule Appointment", fg="green", bold=True)
        click.secho("5. Update Appointment", fg="yellow", bold=True)
        click.secho("6. Delete Appointment", fg="red", bold=True)
        click.secho("7. Exit", fg="magenta", bold=True)


        choice = click.prompt("Enter choice", type=str)
        if choice == "1":
            list_doctors()
        elif choice == "2":
            list_patients()
        elif choice == "3":
            list_appointments()
        elif choice == "4":
            schedule_appointment()
        elif choice == "5":
            update_appointment()
        elif choice == "6":
            delete_appointment()
        elif choice == "7":
            click.secho("👋 Thanks for using the CLI!", fg="green", bold=True)
            break
        else:
            click.secho("❌ Invalid choice, try again.", fg="red")

if __name__ == "__main__":
    main_menu()
