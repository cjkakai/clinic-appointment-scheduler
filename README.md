# Clinic Appointment Scheduler CLI

## Overview
A simple command-line application to manage a clinic's appointments. Users can:
- View doctors and their specializations
- View patients and their ages
- List all scheduled appointments
- Schedule new appointments interactively
- Update appointment date


The project uses **Python**, **SQLAlchemy**, and **SQLite**, with fake data generated via **Faker**.

---

## Project Structure
lib/
  ├─ cli.py # Main interactive CLI
  ├─ helpers.py # Helper functions
  ├─ debug.py # Debugging/testing
  └─ db/
     ├─ models.py # Database models
     ├─ seed.py # Seed script for test data
     └─ migrations/ # Alembic migration files
app.db # SQLite database
Pipfile # Pipenv dependencies
README.md # This file
LICENSE.md # MIT License


---

## Setup & Installation

1. Clone the repository:
```bash
git clone git@github.com:cjkakai/clinic-appointment-scheduler.git
cd clinic-appointment-scheduler

2. Install dependencies:
pipenv install
pipenv shell

3. Seed the database:
pipenv run python -m lib.db.seed


## Usage
Run the CLI from the project root:

```bash
pipenv run python -m lib.cli
