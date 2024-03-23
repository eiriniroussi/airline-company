import random, json, string, re, math, bcrypt, os
from pymongo import MongoClient
from flask import Flask, render_template, request, url_for, redirect, session, jsonify, flash
from bson import ObjectId
from datetime import datetime, timedelta, date
from flask_mail import Mail, Message

# Connect to MongoDB
# client = MongoClient('localhost:27017')
mongodb_hostname = os.environ.get("MONGO_HOSTNAME", "localhost")
client = MongoClient('mongodb://'+mongodb_hostname+':27017/')

# Choose database
db = client['DS_Airlines']
# Choose collections
collection = db['users']
collection1 = db['flights']
collection2 = db['reservations']
collection3 = db['refund']
collection4 = db['reviews']
collection5 = db['contact_us']
collection6 = db['newsletter']

# Flask App
app = Flask(__name__)
app.secret_key = "MLou_2024"


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'webprotectgr@gmail.com' 
app.config['MAIL_PASSWORD'] = 'kblcpuphodueqrzs' 
mail = Mail(app)

def generate_unique_code():
    while True:
        # Generate a random 6-digit code
        code = random.randint(100000, 999999)
        # Check if the code already exists in the database
        if collection5.find_one({'id_code': code}) is None:
            # If not, return the unique code
            return code

def generate_unique_username(base_username):
    while True:
        # Append 4 random digits to the base_username
        random_digits = random.randint(1000, 9999)
        username = f"{base_username}{random_digits}"
        
        # Check if the username exists in the database
        if not collection.find_one({"username": username}):
            # If it doesn't exist, break the loop and return the username
            return username
        # If the username does exist, the loop will continue and generate a new username

def generate_unique_flight_number():
    while True:
        # Generate a flight number (3 letters followed by 7 numbers)
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        numbers = ''.join(random.choices(string.digits, k=7))
        flightNumber = letters + numbers
        
        # Check if the flight number already exists
        if collection1.find_one({'flightNumber': flightNumber}) is None:
            return flightNumber  # Return if unique

def generate_booking_code():
    """Generates a unique booking code."""
    letters = string.ascii_uppercase
    while True:
        code = ''.join(random.choice(letters) for _ in range(2)) + ''.join(random.choice(string.digits) for _ in range(4))
        # Check if this code is already used
        if collection2.find_one({'booking_code': code}) is None:
            return code  # Code is unique, return it

def send_email(to, subject, html_body):
    msg = Message(subject, 
                  recipients=[to], 
                  html=html_body, 
                  sender=('DS Airlines', 'noreply@dsairlines.com')) 
    mail.send(msg)
########################################################################################
########################################################################################
        
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if request.form.get('submit') == 'ΕΙΣΟΔΟΣ':
            return redirect(url_for('register'))
        else:
            return render_template('home.html')
    return render_template('home.html')

########################################################################################
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        print(request.form.get('submit'))

        if request.form.get('submit') == 'Register':
            email = request.form.get("email")
            fullname = request.form.get("fullname")
            password = request.form.get("password")

            wrong_email = 0

            email_exist = collection.find_one({"email": email})
            if email_exist:
                wrong_email = 1

            base_username = email.split('@')[0]
            # Generate a unique username
            unique_username = generate_unique_username(base_username)
        
            # Validate password
            d = 0
            if len(password) >= 8:
                for i in password:
                    if i.isdigit():
                        d += 1
                if d < 1:
                    print("Invalid password, there is no digit")
                    return render_template('register.html', error2=1)
            else:
                print("Invalid password, length less than 8")
                return render_template('register.html', error3=1)

            # Check for duplicate email
            if wrong_email == 1:
                print("A user with the given email exists")
                return render_template('register.html', error=1)
            else:
                session['email'] = email
                password = request.form.get("password").encode('utf-8')
                # Hash password
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

                # Determine role based on email
                role = "admin" if email == "admin@admin.com" else "user"

                collection.insert_one({
                    "email": email, 
                    "fullname": fullname, 
                    "username": unique_username,
                    "password": hashed_password, 
                    "points": 300, 
                    "role": role
                })
                print("A user was added to the database")
                return render_template('login.html', succ=1)

    return render_template('register.html')


########################################################################################
# ΣΥΝΔΕΣΗ ΧΡΗΣΤΗ
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email_given = request.form.get("email")
        password_given = request.form.get("password").encode('utf-8')

        user_in_db = collection.find_one({"email": email_given})

        if user_in_db:
            # Verify hashed password
            if bcrypt.checkpw(password_given, user_in_db['password']):
                # Passwords match
                if user_in_db['role'] == "user":
                    session['user_email'] = email_given
                    print("User logged in successfully")
                    return redirect(url_for('user_logged_in'))
                elif user_in_db['role'] == "admin":
                    session['admin_email'] = email_given
                    print("Admin logged in successfully")
                    return redirect(url_for('admin_logged_in'))
            else:
                # Passwords don't match
                print("Invalid username or password")
                return render_template('login.html', error=1)
        else:
            print("Invalid username or password")
            return render_template('login.html', error=1)

    return render_template('login.html')


########################################################################################
# ΑΠΟΣΥΝΔΕΣΗ ΧΡΗΣΤΗ
@app.route('/logout')
def logout():
    # Remove the email address from session
    session.pop('user_email', None)
    session.pop('admin_email', None) 
    # Redirect to the home page
    return redirect(url_for('home'))

########################################################################################
# ΔΙΑΓΡΑΦΗ ΛΟΓΑΡΙΑΣΜΟΥ ΧΡΗΣΤΗ
@app.route('/delete_account')
def delete_account():
    # Ensure the user is logged in
    user_email = session.get('user_email')
    if user_email:
        # Delete the user account from the database
        result = collection.delete_one({"email": user_email})
        if result.deleted_count > 0:
            print("Account deleted successfully.")
        else:
            print("No account found to delete.")
        # Clear the user session
        session.clear()
        # Redirect to homepage or a specific page after deletion
        return redirect(url_for('home'))
    else:
        # If the user is not logged in, redirect to login page
        return redirect(url_for('login'))

########################################################################################
# ΑΡΧΙΚΗ ΣΕΛΙΔΑ ΣΥΝΔΕΔΕΜΕΝΟΥ ΧΡΗΣΤΗ
@app.route('/user_logged_in', methods=['POST', 'GET'])
def user_logged_in():
    # Check if 'user_email' is in session
    if 'user_email' not in session:
        # If not, redirect to the login page
        return redirect(url_for('login'))
    
    # Retrieve email from session
    user_email = session.get('user_email')
    # Query the database for the user by email
    user_info = collection.find_one({"email": user_email})
    if user_info:
        # Pass username and full_name to the template if the user is found
        return render_template('user_logged_in.html', username=user_info['username'], full_name=user_info['fullname'], points=user_info['points'])
    else:
        return render_template('login.html')


########################################################################################
# ΑΡΧΙΚΗ ΣΕΛΙΔΑ ΔΙΑΧΕΙΡΙΣΤΗ
@app.route('/admin_logged_in', methods=['POST', 'GET'])
def admin_logged_in():
   
    # Check if 'user_email' is in session
    if 'admin_email' not in session:
        # If not, redirect to the login page
        return redirect(url_for('login'))
    
    # Retrieve email from session
    admin_email = session.get('admin_email')
    # Query the database for the user by email
    user_info = collection.find_one({"email": admin_email})
    if user_info:
        # Pass username and full_name to the template if the user is found
        return render_template('admin_logged_in.html', username=user_info['username'], full_name=user_info['fullname'])
    else:
        return render_template('login.html')


########################################################################################
# ABOUT US
@app.route('/aboutus', methods=['POST', 'GET'])
def aboutus():
    return render_template('aboutus.html')


########################################################################################
# ΦΟΡΜΑ ΕΠΙΚΟΙΝΩΝΙΑΣ
@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        # Extract data from form submission
        name = request.form.get('name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        # Generate a unique 6-digit code
        id_code = generate_unique_code()

        # Save the data into MongoDB with the unique id_code
        collection5.insert_one({
            'id_code': id_code,
            'name': name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'message': message
        })

         # Redirect or return a response after saving
        return render_template('contact.html', succ=1)
    else:
        # Render the contact form template on GET request
        return render_template('contact.html')

########################################################################################
# ΠΡΟΒΟΛΗ ΜΗΝΥΜΑΤΩΝ ΑΠΟ ΤΗΝ ΦΟΡΜΑ ΕΠΙΚΟΙΝΩΝΙΑΣ
@app.route('/view_contact_us', methods=['POST', 'GET'])
def view_contact_us():
    messages = list(collection5.find())
    return render_template('view_contact_us.html', messages=messages)


########################################################################################
# ΔΙΑΓΡΑΦΗ ΜΗΝΥΜΑΤΩΝ ΑΠΟ ΤΗΝ ΦΟΡΜΑ ΕΠΙΚΟΙΝΩΝΙΑΣ
@app.route('/delete_message/<message_id>', methods=['POST'])
def delete_message(message_id):
    # Assuming `message_id` is the string representation of MongoDB's ObjectId
    result = collection5.delete_one({'_id': ObjectId(message_id)})
    if result.deleted_count > 0:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Message not found'}), 404
    
########################################################################################
# ΔΗΜΙΟΥΡΓΙΑ ΠΤΗΣΗΣ
@app.route('/flightcreation', methods=['POST', 'GET'])
def flightcreation():
    if request.method == 'POST':
        print("2. Invalid username or password")
        if request.form.get('submit') == 'Create':

            # Extract data from form
            departure = request.form.get('departure')
            destination = request.form.get('destination')
            dateOfFlight = request.form.get('dateOfFlight')
            hourOfDeparture = request.form.get('hourOfDeparture')
            costEconomy = request.form.get('costEconomy')
            costPremium = request.form.get('costPremium')
            costBusiness = request.form.get('costBusiness')
            flightDuration = request.form.get('flightDuration')

            # Generate a unique flight number
            flightNumber = generate_unique_flight_number()

            # Create flight document with 60 seats available
            flight_document = {
                'flightNumber': flightNumber,
                'departure': departure,
                'destination': destination,
                'dateOfFlight': dateOfFlight,
                'hourOfDeparture': hourOfDeparture,
                'costEconomy': float(costEconomy),
                'costPremium': float(costPremium),
                'costBusiness': float(costBusiness),
                'flightDuration': int(flightDuration),
                'seatsAvailable': 54
            }

            # Save the document in the database
            collection1.insert_one(flight_document)

            return render_template('admin_logged_in.html', create_flight=1)
    else:
        # Render the form for GET requests
        return render_template('flightcreation.html')


########################################################################################
# ΠΡΟΣΘΗΚΗ ΔΙΑΧΕΙΡΙΣΤΗ
@app.route('/add_admins', methods=['POST', 'GET'])
def add_admins():
    if request.method == 'POST':
        # Extract data from form submission
        fullname = request.form.get('fullName')
        email = request.form.get('adminEmail')
        password = request.form.get('adminPassword').encode('utf-8')  # Encode the password

        # Check if the email already exists
        existing_admin = collection.find_one({"email": email})
        if existing_admin is None:
            # Email does not exist, proceed to add new admin
            base_username = email.split('@')[0]
            # Generate a unique username
            unique_username = generate_unique_username(base_username)

            # Hash password
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            # Insert new admin into the database with hashed password
            collection.insert_one({
                "email": email,
                "fullname": fullname,
                "username": unique_username,
                "password": hashed_password,
                "role": "admin"
            })

            return render_template('admin_logged_in.html', admin_added=1)
        else:
            # Email already exists
            return render_template('add_admins.html', admin_not_created=1)

    else:
        # Render the form for GET requests
        return render_template('add_admins.html')
########################################################################################
# ΑΞΙΟΛΟΓΗΣΗ
@app.route('/reviews', methods=['POST', 'GET'])
def reviews():
    user_email = session.get('user_email')
    if not user_email:
        # Redirect to login if no user is in session
        return redirect(url_for('login'))

    # Retrieve user info based on session email
    user_info = collection.find_one({"email": user_email})
    if not user_info:
        return redirect(url_for('login'))

    if request.method == 'POST':
        print("hello")
        rating = request.form.get('inlineRadioOptions')
        review_text = request.form.get('Message')

        # Check if the user has already submitted a review
        existing_review = collection4.find_one({'email': user_email})
        if existing_review:
            # Update existing review
            collection4.update_one({'email': user_email}, {'$set': {'rating': rating, 'review': review_text}})
        else:
            # Insert new review
            collection4.insert_one({'email': user_email, 'username': user_info['username'], 'rating': rating, 'review': review_text})
        
        return redirect(url_for('reviews'))

    # For GET request, check if there's an existing review and pass it to the template
    existing_review = collection4.find_one({'email': user_email})
    return render_template('reviews.html', username=user_info['username'], email=user_email, full_name=user_info.get('fullname'),review=existing_review)

########################################################################################
# ΠΡΟΒΟΛΗ ΑΞΙΟΛΟΓΗΣΕΩΝ
@app.route('/view_reviews', methods=['GET'])
def view_reviews():

    # Retrieve all reviews or based on a filter
    reviews = list(collection4.find())

    # Pass the reviews to the template
    return render_template('view_reviews.html', reviews=reviews)


########################################################################################
# ΔΙΑΧΕΙΡΙΣΗ ΑΞΙΟΛΟΓΗΣΕΩΝ
@app.route('/reviews_management', methods=['GET'])
def reviews_management():
    # Check if user is logged in and is an admin
    if 'admin_email' not in session :
        return redirect(url_for('login'))

    # Retrieve all reviews or based on a filter
    reviews = list(collection4.find())

    # Pass the reviews to the template
    return render_template('ReviewsManagement.html', reviews=reviews)

########################################################################################
# ΔΙΑΓΡΑΦΗ ΑΞΙΟΛΟΓΗΣΗΣ

@app.route('/delete_review/<review_id>', methods=['POST'])
def delete_review(review_id):
    print("Deleting review with ID:", review_id)  # Confirm this prints the expected ID
    result = collection4.delete_one({'_id': ObjectId(review_id)})
    if result.deleted_count > 0:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Review not found'}), 404

########################################################################################
# ΑΝΑΖΗΤΗΣΗ ΠΤΗΣΕΩΝ
@app.route('/search_flights', methods=['GET', 'POST'])
def search_flights():
    if request.method == 'POST':
        session.pop('flights', None)

        departure = request.form.get('departure').lower()  # Convert to lowercase
        destination = request.form.get('destination').lower()  # Convert to lowercase
        departureDate = request.form.get('dateOfFlight')

        departureDate_dt = datetime.strptime(departureDate, '%Y-%m-%d')
        endDate_dt = departureDate_dt + timedelta(days=7)

        formatted_departureDate = departureDate_dt.strftime('%Y-%m-%d')
        formatted_endDate = endDate_dt.strftime('%Y-%m-%d')

        # Use regular expressions for case-insensitive search
        flights = list(collection1.find({
            'departure': {'$regex': f'^{re.escape(departure)}$', '$options': 'i'},
            'destination': {'$regex': f'^{re.escape(destination)}$', '$options': 'i'},
            'dateOfFlight': {
                '$gte': formatted_departureDate,
                '$lte': formatted_endDate
            }
        }))

        # Store search results in session for retrieval in the ViewFlights route
        session['flights'] = json.dumps(flights, default=str)  # Convert list to JSON string
        return redirect(url_for('ViewFlights'))
    else:
        return render_template('search_flights.html')  
     
########################################################################################
# ΠΡΟΒΟΛΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ
@app.route('/ViewFlights', methods=['GET'])
def ViewFlights():
    flights_data = session.get('flights')
    if flights_data:
        flights = json.loads(flights_data)
    else:
        flights = None

    if flights:
        return render_template('ViewFlights.html', flights=flights)
    else:
        return render_template('ViewFlights.html', message="No flights found or search not performed.")
########################################################################################
# ΔΗΜΙΟΥΡΓΙΑ ΚΡΑΤΗΣΗΣ
@app.route('/flightsBooking', methods=['POST', 'GET'])
def flightsBooking():
    if request.method == 'POST':
        # Retrieve the flight number from the submitted form data
        flightNumber = request.form.get('flightNumber')
        
        # Fetch the flight information from the database
        flight_info = collection1.find_one({"flightNumber": flightNumber})
        
        # Also fetch the booked seats for this flight
        reservations = collection2.find({"flightNumber": flightNumber})
        booked_seats = [passenger['seatNumber'] for reservation in reservations for passenger in reservation.get('passengers', [])]
        booked_seats_json = json.dumps(booked_seats)

        # Fetch user's points if logged in
        user_email = session.get('user_email')
        if user_email:
            user_info = db.users.find_one({"email": user_email})
            user_points = user_info.get('points', 0)
        else:
            user_points = 0
            
        if flight_info:
            flight_info = json.loads(json.dumps(flight_info, default=str))
            return render_template('flightsBooking.html', flight=flight_info, booked_seats=booked_seats_json, user_points=user_points)

        else:
            return "Flight not found.", 404
    else:
        # Handle the GET request or other cases
        return "This page requires a flight selection.", 400


########################################################################################
# ΑΠΟΣΤΟΛΗ ΚΡΑΤΗΣΗΣ
@app.route('/reserve', methods=['POST'])
def reserve():
    data = {
        'flightNumber': request.form.get('flightNumber'),
        'passengers': [],
        'cardNumber': request.form.get('cardnumber'),
        'cardType': request.form.get('cardType'),
        'expirationDate': request.form.get('expDate'),
        'totalCost': request.form.get('totalCost'),
        'tel': request.form.get('tel1'),
        'email': request.form.get('email1'),
    }
    # Generate a unique booking code
    booking_code = generate_booking_code()
    data['booking_code'] = booking_code  

    # Always add the first passenger with email and telephone
    data['passengers'].append({
        'name': request.form.get('fname1'),
        'lastName': request.form.get('lname1'),
        'passportNumber': request.form.get('pass1'),
        'seatNumber': request.form.get('seat1'),
        'ticketType': request.form.get('type1')
    })

    # Add additional passengers without email and telephone
    for i in range(2, 5):
        fname = request.form.get(f'fname{i}')
        if fname:  # Check if the passenger's first name is provided
            passenger_data = {
                'name': fname,
                'lastName': request.form.get(f'lname{i}'),
                'passportNumber': request.form.get(f'pass{i}'),
                'seatNumber': request.form.get(f'seat{i}'),
                'ticketType': request.form.get(f'type{i}')
            }
            data['passengers'].append(passenger_data)

    # Check if the user opted to use points for a discount
    use_points_for_discount = request.form.get('use_points') == 'on'

    # Fetch user details
    user_email = session.get('user_email')
    points_used = 0  # Initialize points used variable

    if user_email and use_points_for_discount:
        user_info = db.users.find_one({"email": user_email})
        user_points = user_info.get('points', 0)

        # If the user has enough points for a discount
        if user_points >= 1000:
            # Apply a €10 discount to the total cost
            total_cost = max(0, float(data['totalCost']) - 10)  # Ensure total cost doesn't go negative
            data['totalCost'] = str(total_cost)  # Update the total cost in the booking data
            
            # Deduct 1000 points from the user's account
            db.users.update_one({'email': user_email}, {'$inc': {'points': -1000}})
            flash('€10 discount applied successfully! 1000 points have been deducted from your account.', 'success')
            
            # Record the points used
            points_used = 1000
        else:
            flash('Not enough points for a discount.', 'error')

    # Add points used to the reservation data if any points were used
    if points_used > 0:
        data['points'] = points_used
            
    # Insert the booking data into MongoDB
    collection2.insert_one(data)

    flight_details = {
        'from': request.form.get('from'),
        'to': request.form.get('to'),
        'flightDate': request.form.get('flightDate'),
        'flightTime': request.form.get('flightTime')
    }

    data['flight_details'] = flight_details

    # Prepare email content
    email_html = render_template('email_template.html', booking=data)
    # Generate PDF from HTML content
    
    email_html = render_template('email_template.html', booking=data)
    send_email(data['email'], "DS Airlines | Your Booking Confirmation", email_html)


    user_email = session.get('user_email')

    # Convert totalCost to points (rounding up)
    total_cost = float(request.form.get('totalCost'))
    points_to_add = math.ceil(total_cost)
    if user_email:
            # Update the user's points in the database
            db.users.update_one({'email': user_email}, {'$inc': {'points': points_to_add}})
    

    # Update the number of available seats for the flight
    num_tickets_sold = len(data['passengers'])  # Corrected to use data dictionary
    collection1.update_one({'flightNumber': data['flightNumber']}, {'$inc': {'seatsAvailable': -num_tickets_sold}})
    flash('You have successfully booked your flight! We cant wait to see you onboard!', 'success')

    # Redirect or return a response
    return redirect(url_for('user_logged_in'))

########################################################################################
# ΑΚΥΡΩΣΗ ΚΡΑΤΗΣΗΣ
@app.route('/cancel_reservation', methods=['POST', 'GET'])
def cancel_reservation():
    if request.method == 'POST':
        booking_id = request.form['booking_id']
        email = request.form['email']

        # Find the reservation to be cancelled
        reservation = collection2.find_one({"email": email, "booking_code": booking_id})

        num_seats_to_add_back = len(reservation['passengers'])
        collection1.update_one({"flightNumber": reservation["flightNumber"]}, {"$inc": {"seatsAvailable": num_seats_to_add_back}})

        if reservation:
            # Refund points if applicable
            if "points" in reservation:
                points_refund = reservation["points"]
                collection.update_one({"email": email}, {"$inc": {"points": points_refund}})

            # Record the refund details in collection3 before deleting the reservation
            refund_details = {
                "flightNumber": reservation["flightNumber"],
                "cardType": reservation["cardType"],
                "cardNumber": reservation["cardNumber"],
                "expirationDate": reservation["expirationDate"],
                "email": reservation["email"],
                "bookingCode": reservation["booking_code"],
                "totalCost": reservation["totalCost"]
            }
            collection3.insert_one(refund_details)

            # Delete the reservation
            collection2.delete_one({"booking_code": booking_id, "email": email})

            return render_template('cancel_reservation.html', succ=1)
        else:
            return render_template('cancel_reservation.html', error=1)

    else:
        return render_template('cancel_reservation.html')
########################################################################################
# ΠΡΟΒΟΛΗ ΟΛΩΝ ΤΩΝ ΚΡΑΤΗΣΕΩΝ
@app.route('/view_reservations_users', methods=['GET'])
def view_reservations_users():
    user_email = session.get('user_email')
    if user_email:
        # Fetch bookings for the logged-in user
        bookings = collection2.find({"email": user_email})
        bookings_list = []

        for booking in bookings:
            # Fetch flight details for each booking
            flight_details = collection1.find_one({"flightNumber": booking["flightNumber"]})
            if flight_details:
                booking["flight_details"] = flight_details
            bookings_list.append(booking)

        return render_template('view_reservations_users.html', bookings=bookings_list)
    else:
        return redirect(url_for('login'))


########################################################################################
# ΠΡΟΒΟΛΗ ΟΛΩΝ ΤΩΝ ΠΤΗΣΕΩΝ ΑΠΟ ΔΙΑΧΕΙΡΙΣΤΗ
@app.route('/view_all_flights_admin', methods=['GET'])
def view_all_flights_admin():
    # Fetch all flights and sort them by date
    flights = list(collection1.find().sort("dateOfFlight", 1))  # 1 for ascending order
    return render_template('view_all_flights_admin.html', flights=flights, current_date=date.today().strftime('%Y-%m-%d'))


########################################################################################
# ΕΠΕΞΕΡΓΑΣΙΑ ΠΤΗΣΗΣ
@app.route('/edit_flight/<flightNumber>', methods=['GET', 'POST'])
def edit_flight(flightNumber):
    if request.method == 'GET':
        flight = collection1.find_one({'flightNumber': flightNumber})
        if flight:
            return render_template('edit_flight.html', flight=flight)
        else:
            return 'Flight not found', 404
    elif request.method == 'POST':
        action = request.form.get('action')

        if action == 'edit':
            # Extract the updated fields from the form
            updated_fields = {
                'hourOfDeparture': request.form.get('hourOfDeparture'),
                'costEconomy': float(request.form.get('costEconomy')),
                'costPremium': float(request.form.get('costPremium')),
                'costBusiness': float(request.form.get('costBusiness')),
                'flightDuration': int(request.form.get('flightDuration'))
            }
            # Update the flight document in the database
            collection1.update_one({'flightNumber': flightNumber}, {'$set': updated_fields})
            return redirect(url_for('view_all_flights_admin'))

        elif action == 'delete':
            # Delete the flight from the database
            collection1.delete_one({'flightNumber': flightNumber})
            return redirect(url_for('view_all_flights_admin'))

        else:
            return 'Invalid action', 400

########################################################################################
# ΔΙΑΧΕΙΡΙΣΗ ΧΡΗΣΤΩΝ
@app.route('/view_users', methods=['POST', 'GET'])
def view_users():
    if request.method == 'POST':
        user_email_to_delete = request.form.get('delete_email')
        if user_email_to_delete:
            collection.delete_one({'email': user_email_to_delete})
            flash('User deleted successfully', 'success')  # Flash a success message
        return redirect(url_for('view_users'))
    
    users = list(collection.find({"role": "user"}))
    return render_template('view_users.html', users=users)

########################################################################################
# ΔΙΑΧΕΙΡΙΣΗ ΔΙΑΧΕΙΡΙΣΤΩΝ
@app.route('/view_admins', methods=['POST', 'GET'])
def view_admins():
    if request.method == 'POST':
        admin_email_to_delete = request.form.get('delete_email')
        if admin_email_to_delete:
            collection.delete_one({'email': admin_email_to_delete})
            flash('Admin deleted successfully', 'success')  # Flash a success message
        return redirect(url_for('view_admins'))
    
    users = list(collection.find({"role": "admin"}))    
    return render_template('view_admins.html', users=users)


########################################################################################
# email template 1
@app.route('/email_template', methods=['POST', 'GET'])
def email_template():
    return render_template('email_template.html')

########################################################################################
# email template 2
@app.route('/email_template2', methods=['POST', 'GET'])
def email_template2():
    return render_template('email_template2.html')


########################################################################################
# ΕΠΑΝΥΠΟΣΤΟΛΗ EMAIL
@app.route('/resend_confirmation', methods=['POST'])
def resend_confirmation():
    booking_id = request.form.get('booking_id')
    # Fetch the booking details from the database
    booking = collection2.find_one({'booking_code': booking_id})
    
    if booking:
        # Fetch flight details using the flightNumber from the booking
        flight = collection1.find_one({'flightNumber': booking['flightNumber']})
        print(booking['flightNumber'])
        print(flight['departure'])
        if flight:
            email = booking['email']
            # Merge flight details into the booking object for easier template access
            booking['flight_details'] = {
                'departure': flight['departure'],
                'destination': flight['destination'],
                'dateOfFlight': flight['dateOfFlight'],
                'hourOfDeparture': flight['hourOfDeparture']
            }
            # Prepare email content
            email_html = render_template('email_template2.html', booking=booking)
            # Resend the email
            try:
                send_email(email, "Resend | Your Booking Confirmation | DS Airlines", email_html)
            except Exception as e:
                flash('Failed to resend booking confirmation.', 'danger')
                print(e)  # Log the error for debugging
        else:
            flash('Flight details not found for this booking.', 'danger')
    else:
        flash('Booking not found.', 'danger')
        
    return redirect(url_for('view_reservations_users'))


########################################################################################
# ΠΡΟΒΟΛΗ ΟΛΩΝ ΤΩΝ ΚΡΑΤΗΣΕΩΝ ΑΠΟ ΤΟΝ ΔΙΑΧΕΙΡΙΣΤΗ
@app.route('/view_reservations_admin', methods=['POST', 'GET'])
def view_reservations_admin():
    bookings = list(collection2.find())
    for booking in bookings:
        # Fetch flight details for each booking
        flight_details = collection1.find_one({'flightNumber': booking['flightNumber']})
        if flight_details:
            # Merge the flight details into the booking object
            booking['flight_details'] = flight_details
    return render_template('view_reservations_admin.html', bookings=bookings)

########################################################################################
# ΑΠΟΣΤΟΛΗ NEWSLETTER
@app.route('/newsletter', methods=['POST', 'GET'])
def newsletter():
    if request.method == 'POST':
        subject = request.form.get('name')  # Ensure your form has an input with name='subject'
        message_content = request.form.get('message')  # Ensure your form has a textarea with name='message'

        # Fetch all subscribed emails
        subscribers = collection6.find({}, {"email": 1, "_id": 0})
        subscriber_emails = [subscriber['email'] for subscriber in subscribers]

        if subscriber_emails:
            # Compose and send the newsletter to all subscribers
            try:
                with mail.connect() as conn:
                    for email in subscriber_emails:
                        msg = Message(subject=subject,
                                      sender=('DS Airlines | Newsletter', 'noreply@dsairlines.com'),
                                      recipients=[email],
                                      body=message_content)
                        conn.send(msg)
                return render_template('newsletter.html', succ=1)
            except Exception as e:
                return render_template('newsletter.html', error2=1)

        else:
            return render_template('newsletter.html', error3=1) #no subscribed users


    # GET request or initial page load
    return render_template('newsletter.html')

########################################################################################
# ΕΓΓΡΑΦΗ NEWSLETTER
@app.route('/subscribe_newsletter', methods=['GET', 'POST'])
def subscribe_newsletter():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        email_exist = collection6.find_one({"email": email})
        if email_exist:
            return render_template('home.html', error=1)
            
        collection6.insert_one({"email": email, "name": name})
        
        return render_template('home.html', error2=1)
        
    return render_template('aboutus.html')

########################################################################################
# ΟΝΟΜΑ ΔΙΕΡΓΑΣΙΑΣ
@app.route('/test', methods=['POST', 'GET'])
def test():
    return render_template('test.html')


########################################################################################
########################################################################################

# Εκτέλεση flask service
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

#MARINA LOULAKI