from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

# Database configuration
db_config = {
    'user': 'root',      
    'password': '',  
    'host': 'localhost',
    'database': 'bike_rental'   
}

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# --- CRUD Operations for Bikes ---

# Read Bikes
@app.route('/bikes')
def bikes():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bikes")
    bikes = cursor.fetchall()
    conn.close()
    return render_template('bikes/bikes.html', bikes=bikes)

# Create Bike
@app.route('/add_bike', methods=['GET', 'POST'])
def add_bike():
    if request.method == 'POST':
        model_name = request.form['ModelName']
        bike_type = request.form['Type']
        hourly_rate = request.form['HourlyRate']
        daily_rate = request.form['DailyRate']
        purchase_date = request.form['PurchaseDate']
        last_maintenance_date = request.form.get('LastMaintenanceDate', None)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO Bikes (ModelName, Type, HourlyRate, DailyRate, PurchaseDate, LastMaintenanceDate)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(insert_query, (model_name, bike_type, hourly_rate, daily_rate, purchase_date, last_maintenance_date))
            conn.commit()
            flash('Bike added successfully!', 'success')
        except Error as e:
            flash(f'Error adding bike: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('bikes'))
    return render_template('bikes/add_bike.html')

# Update Bike
@app.route('/edit_bike/<int:bike_id>', methods=['GET', 'POST'])
def edit_bike(bike_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    if request.method == 'POST':
        model_name = request.form['ModelName']
        bike_type = request.form['Type']
        hourly_rate = request.form['HourlyRate']
        daily_rate = request.form['DailyRate']
        purchase_date = request.form['PurchaseDate']
        last_maintenance_date = request.form.get('LastMaintenanceDate', None)

        update_query = """
        UPDATE Bikes
        SET ModelName = %s, Type = %s, HourlyRate = %s, DailyRate = %s, PurchaseDate = %s, LastMaintenanceDate = %s
        WHERE BikeID = %s
        """
        try:
            cursor.execute(update_query, (model_name, bike_type, hourly_rate, daily_rate, purchase_date, last_maintenance_date, bike_id))
            conn.commit()
            flash('Bike updated successfully!', 'success')
        except Error as e:
            flash(f'Error updating bike: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('bikes'))
    else:
        cursor.execute("SELECT * FROM Bikes WHERE BikeID = %s", (bike_id,))
        bike = cursor.fetchone()
        conn.close()
        return render_template('bikes/edit_bike.html', bike=bike)

# Delete Bike
@app.route('/delete_bike/<int:bike_id>', methods=['POST'])
def delete_bike(bike_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    delete_query = "DELETE FROM Bikes WHERE BikeID = %s"
    try:
        cursor.execute(delete_query, (bike_id,))
        conn.commit()
        flash('Bike deleted successfully!', 'success')
    except Error as e:
        flash(f'Error deleting bike: {e}', 'danger')
    finally:
        conn.close()
    return redirect(url_for('bikes'))

# --- CRUD Operations for Customers ---

# Read Customers
@app.route('/customers')
def customers():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()
    conn.close()
    return render_template('customers/customers.html', customers=customers)

# Create Customer
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        email = request.form['Email']
        phone = request.form['Phone']
        license_number = request.form['LicenseNumber']
        membership_status = request.form['MembershipStatus']
        registration_date = request.form['RegistrationDate']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO Customers (FirstName, LastName, Email, Phone, LicenseNumber, MembershipStatus, RegistrationDate)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(insert_query, (first_name, last_name, email, phone, license_number, membership_status, registration_date))
            conn.commit()
            flash('Customer added successfully!', 'success')
        except Error as e:
            flash(f'Error adding customer: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('customers'))
    return render_template('customers/add_customer.html')

# Update Customer
@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    if request.method == 'POST':
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        email = request.form['Email']
        phone = request.form['Phone']
        license_number = request.form['LicenseNumber']
        membership_status = request.form['MembershipStatus']
        registration_date = request.form['RegistrationDate']

        update_query = """
        UPDATE Customers
        SET FirstName = %s, LastName = %s, Email = %s, Phone = %s, LicenseNumber = %s, MembershipStatus = %s, RegistrationDate = %s
        WHERE CustomerID = %s
        """
        try:
            cursor.execute(update_query, (first_name, last_name, email, phone, license_number, membership_status, registration_date, customer_id))
            conn.commit()
            flash('Customer updated successfully!', 'success')
        except Error as e:
            flash(f'Error updating customer: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('customers'))
    else:
        cursor.execute("SELECT * FROM Customers WHERE CustomerID = %s", (customer_id,))
        customer = cursor.fetchone()
        conn.close()
        return render_template('customers/edit_customer.html', customer=customer)

# Delete Customer
@app.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    delete_query = "DELETE FROM Customers WHERE CustomerID = %s"
    try:
        cursor.execute(delete_query, (customer_id,))
        conn.commit()
        flash('Customer deleted successfully!', 'success')
    except Error as e:
        flash(f'Error deleting customer: {e}', 'danger')
    finally:
        conn.close()
    return redirect(url_for('customers'))

# --- CRUD Operations for Rentals ---

# Read Rentals
@app.route('/rentals')
def rentals():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = """
    SELECT Rentals.*, Customers.FirstName, Customers.LastName, Bikes.ModelName, Bikes.Type
    FROM Rentals
    JOIN Customers ON Rentals.CustomerID = Customers.CustomerID
    JOIN Bikes ON Rentals.BikeID = Bikes.BikeID
    """
    cursor.execute(query)
    rentals = cursor.fetchall()
    conn.close()
    return render_template('rentals/rentals.html', rentals=rentals)

# Create Rental
@app.route('/add_rental', methods=['GET', 'POST'])
def add_rental():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    if request.method == 'POST':
        customer_id = request.form['CustomerID']
        bike_id = request.form['BikeID']
        start_time = request.form['StartTime']
        end_time = request.form.get('EndTime', None)
        total_cost = request.form.get('TotalCost', None)
        deposit_amount = request.form['DepositAmount']
        return_status = request.form['ReturnStatus']

        insert_query = """
        INSERT INTO Rentals (CustomerID, BikeID, StartTime, EndTime, TotalCost, DepositAmount, ReturnStatus)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(insert_query, (customer_id, bike_id, start_time, end_time, total_cost, deposit_amount, return_status))
            conn.commit()
            flash('Rental added successfully!', 'success')
        except Error as e:
            flash(f'Error adding rental: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('rentals'))
    else:
        cursor.execute("SELECT CustomerID, FirstName, LastName FROM Customers")
        customers = cursor.fetchall()
        cursor.execute("SELECT BikeID, ModelName, Type FROM Bikes WHERE Status = 'Available'")
        bikes = cursor.fetchall()
        conn.close()
        return render_template('rentals/add_rental.html', customers=customers, bikes=bikes)

# Update Rental
@app.route('/edit_rental/<int:rental_id>', methods=['GET', 'POST'])
def edit_rental(rental_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    if request.method == 'POST':
        customer_id = request.form['CustomerID']
        bike_id = request.form['BikeID']
        start_time = request.form['StartTime']
        end_time = request.form.get('EndTime', None)
        total_cost = request.form.get('TotalCost', None)
        deposit_amount = request.form['DepositAmount']
        return_status = request.form['ReturnStatus']

        update_query = """
        UPDATE Rentals
        SET CustomerID = %s, BikeID = %s, StartTime = %s, EndTime = %s, TotalCost = %s, DepositAmount = %s, ReturnStatus = %s
        WHERE RentalID = %s
        """
        try:
            cursor.execute(update_query, (customer_id, bike_id, start_time, end_time, total_cost, deposit_amount, return_status, rental_id))
            conn.commit()
            flash('Rental updated successfully!', 'success')
        except Error as e:
            flash(f'Error updating rental: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('rentals'))
    else:
        # Fetch rental details
        cursor.execute("SELECT * FROM Rentals WHERE RentalID = %s", (rental_id,))
        rental = cursor.fetchone()
        # Fetch customers and bikes for dropdowns
        cursor.execute("SELECT CustomerID, FirstName, LastName FROM Customers")
        customers = cursor.fetchall()
        cursor.execute("SELECT BikeID, ModelName, Type FROM Bikes")
        bikes = cursor.fetchall()
        conn.close()
        return render_template('rentals/edit_rental.html', rental=rental, customers=customers, bikes=bikes)

# Delete Rental
@app.route('/delete_rental/<int:rental_id>', methods=['POST'])
def delete_rental(rental_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    delete_query = "DELETE FROM Rentals WHERE RentalID = %s"
    try:
        cursor.execute(delete_query, (rental_id,))
        conn.commit()
        flash('Rental deleted successfully!', 'success')
    except Error as e:
        flash(f'Error deleting rental: {e}', 'danger')
    finally:
        conn.close()
    return redirect(url_for('rentals'))

# --- CRUD Operations for Maintenance ---

# Read Maintenance Records
@app.route('/maintenance')
def maintenance():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = """
    SELECT Maintenance.*, Bikes.ModelName, Bikes.Type
    FROM Maintenance
    JOIN Bikes ON Maintenance.BikeID = Bikes.BikeID
    """
    cursor.execute(query)
    maintenance_records = cursor.fetchall()
    conn.close()
    return render_template('maintenance/maintenance.html', maintenance_records=maintenance_records)

# Create Maintenance Record
@app.route('/add_maintenance', methods=['GET', 'POST'])
def add_maintenance():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    if request.method == 'POST':
        bike_id = request.form['BikeID']
        maintenance_type = request.form['MaintenanceType']
        maintenance_date = request.form['MaintenanceDate']
        description = request.form.get('Description', None)
        cost = request.form['Cost']
        technician_name = request.form['TechnicianName']

        insert_query = """
        INSERT INTO Maintenance (BikeID, MaintenanceType, MaintenanceDate, Description, Cost, TechnicianName)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(insert_query, (bike_id, maintenance_type, maintenance_date, description, cost, technician_name))
            conn.commit()
            flash('Maintenance record added successfully!', 'success')
        except Error as e:
            flash(f'Error adding maintenance record: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('maintenance'))
    else:
        cursor.execute("SELECT BikeID, ModelName, Type FROM Bikes")
        bikes = cursor.fetchall()
        conn.close()
        return render_template('maintenance/add_maintenance.html', bikes=bikes)

# Update Maintenance Record
@app.route('/edit_maintenance/<int:maintenance_id>', methods=['GET', 'POST'])
def edit_maintenance(maintenance_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    if request.method == 'POST':
        bike_id = request.form['BikeID']
        maintenance_type = request.form['MaintenanceType']
        maintenance_date = request.form['MaintenanceDate']
        description = request.form.get('Description', None)
        cost = request.form['Cost']
        technician_name = request.form['TechnicianName']

        update_query = """
        UPDATE Maintenance
        SET BikeID = %s, MaintenanceType = %s, MaintenanceDate = %s, Description = %s, Cost = %s, TechnicianName = %s
        WHERE MaintenanceID = %s
        """
        try:
            cursor.execute(update_query, (bike_id, maintenance_type, maintenance_date, description, cost, technician_name, maintenance_id))
            conn.commit()
            flash('Maintenance record updated successfully!', 'success')
        except Error as e:
            flash(f'Error updating maintenance record: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('maintenance'))
    else:
        # Fetch maintenance record details
        cursor.execute("SELECT * FROM Maintenance WHERE MaintenanceID = %s", (maintenance_id,))
        maintenance = cursor.fetchone()
        # Fetch bikes for dropdown
        cursor.execute("SELECT BikeID, ModelName, Type FROM Bikes")
        bikes = cursor.fetchall()
        conn.close()
        return render_template('maintenance/edit_maintenance.html', maintenance=maintenance, bikes=bikes)

# Delete Maintenance Record
@app.route('/delete_maintenance/<int:maintenance_id>', methods=['POST'])
def delete_maintenance(maintenance_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    delete_query = "DELETE FROM Maintenance WHERE MaintenanceID = %s"
    try:
        cursor.execute(delete_query, (maintenance_id,))
        conn.commit()
        flash('Maintenance record deleted successfully!', 'success')
    except Error as e:
        flash(f'Error deleting maintenance record: {e}', 'danger')
    finally:
        conn.close()
    return redirect(url_for('maintenance'))

# --- Predefined Queries ---

# Query 1: View Pending Rentals with Customer and Bike Details
@app.route('/query1')
def query1():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = """
    SELECT Rentals.RentalID, Customers.FirstName, Customers.LastName, Bikes.ModelName, Rentals.StartTime, Rentals.EndTime
    FROM Rentals
    JOIN Customers ON Rentals.CustomerID = Customers.CustomerID
    JOIN Bikes ON Rentals.BikeID = Bikes.BikeID
    WHERE Rentals.ReturnStatus = 'Pending'
    """
    cursor.execute(query)
    results = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    conn.close()
    return render_template('query_results.html', results=results, headers=headers, title="Pending Rentals")

# Query 2: Customers with More Than 5 Rentals
@app.route('/query2')
def query2():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = """
    SELECT Customers.FirstName, Customers.LastName, COUNT(Rentals.RentalID) AS RentalCount
    FROM Customers
    JOIN Rentals ON Customers.CustomerID = Rentals.CustomerID
    GROUP BY Customers.CustomerID
    HAVING RentalCount > 5
    """
    cursor.execute(query)
    results = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    conn.close()
    return render_template('query_results.html', results=results, headers=headers, title="Frequent Renters")

# Query 3: Bikes That Haven't Been Maintained in Over 6 Months
@app.route('/query3')
def query3():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = """
    SELECT BikeID, ModelName, LastMaintenanceDate
    FROM Bikes
    WHERE LastMaintenanceDate < DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
    """
    cursor.execute(query)
    results = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    conn.close()
    return render_template('query_results.html', results=results, headers=headers, title="Bikes Needing Maintenance")

if __name__ == '__main__':
    app.run(debug=True)
