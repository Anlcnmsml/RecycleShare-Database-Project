RecycleShare - Waste Sharing & Recycling Platform ♻️

RecycleShare is a PostgreSQL-based database management system designed to connect waste owners with authorized collectors. The platform facilitates the registration, categorization, and reservation of recyclable materials, incentivizing the process through a custom scoring system.

📂 Project Structure

As shown on the desktop organization, the repository is divided into four main sections:

SQL codes: Contains schema.sql (table structures, triggers, functions) and data.sql (initial records).

interface code: Contains recycleDB.py, the Python Tkinter source code for the graphical user interface.

screenshots: Visual evidence of the database tables and the functional UI.

docs: Project reports and documentation.

🛠️ Database Features & Constraints

The system is built on a robust relational architecture with 6 primary tables: users, categories, waste_items, bookings, messages, and reviews.

Integrity Enforcement: Comprehensive use of Primary Keys (PK) and Foreign Keys (FK) to maintain relational consistency.

Business Logic Triggers:

trg_booking_made: Automatically updates waste status to 'Reserved' upon booking.

trg_check_waste_weight: Prevents entry of zero or negative weights.

trg_prevent_waste_deletion: Protects reserved or recycled items from accidental deletion.

Advanced SQL Objects: Includes Views for impact reporting, Stored Functions utilizing Cursors and Records for regional analysis, and Indexes for optimized location-based searches.

🖥️ Application Interface

The Python interface provides tailored experiences based on user roles:

Admin: Full management of items, categories, and system reports.

User: Can post waste advertisements and track their environmental impact score.

Collector: Can browse available waste by location and manage pickup reservations.

🚀 Getting Started

Prerequisites

Python 3.x

PostgreSQL

Python libraries: psycopg2, tkinter

Installation

Database Setup: Create a database named RecycleShareDB in PostgreSQL. Run the schema.sql followed by data.sql found in the SQL codes folder.

Configuration: Open recycleDB.py and update the DB_PASS and DB_USER variables with your local PostgreSQL credentials.

Run: Execute the application:

Bash
python recycleDB.py

👥 Roles for Testing

Admin: admin / 1234 


User: ahmet / 1234 


Collector: mehmet_coll / 1234 

👤 Developer

Anılcan MUŞMUL

This project was developed for the Database Management Systems (BLM3041) course at Yıldız Technical University.
