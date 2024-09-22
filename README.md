DS Airlines
Mandatory assignment for the course "Information Systems"
Department of Digital Systems, University of Piraeus

Application Execution
To run the web service on someone's computer, Docker and Docker Compose must be installed.

Installation on WINDOWS systems
(Docker Compose is already included in Docker for Windows)
You can download the executable file to install Docker from here: Install Docker Desktop on Windows

Installation on LINUX systems
Simply run the following commands in the terminal:

bash
Αντιγραφή κώδικα
sudo apt-get update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository -y "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt install docker-ce
sudo curl -L https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
Application Requirements
The web service will run on port 5000 via Flask, and MongoDB will run on port 27017. If there are other services running on these ports, they need to be stopped.

A database named DS_Airlines has been created in MongoDB.

Running the Application
Download the .zip file from this repository.
Unzip it on your computer.
Rename the folder and remove the -main suffix from the folder name.
Open the terminal at the path: YpoxreotikiErgasiaFebr24
Run the following command to create the container:
bash
Αντιγραφή κώδικα
(sudo) docker-compose up -d
To stop the application, run:
bash
Αντιγραφή κώδικα
(sudo) docker-compose down
Open your preferred browser and access the web service via the following link:
http://localhost:5000/
MongoDB
Navigate to the path: YpoxreotikiErgasiaSept22_E19226_Loulaki_Marina

To use the Mongo Shell, run the following command in PowerShell/Terminal:

bash
Αντιγραφή κώδικα
(sudo) docker exec -it mongodb mongo
To use the database that has been created, execute the command:

bash
Αντιγραφή κώδικα
use DS_Airlines
To display the collections, use the command:

bash
Αντιγραφή κώδικα
show collections
To display all user records, execute:

bash
Αντιγραφή κώδικα
db.users.find({})
To display all flights created by the admin, execute:

bash
Αντιγραφή κώδικα
db.flights.find({})
To display all reservations made by users, execute:

bash
Αντιγραφή κώδικα
db.reservations.find({})
To display all cancellations made by users with pending refunds, execute:

bash
Αντιγραφή κώδικα
db.refund.find({})
You can do the same with all collections.

If you want the output to be more readable, add .pretty() at the end of each find command, like this:

bash
Αντιγραφή κώδικα
db.users.find({}).pretty()
The database already contains data related to users, flights, reviews, reservations, communication messages, registered newsletter users, and canceled reservations.

Flask
To execute Flask, run the following command from PowerShell/Terminal (from the project directory):
bash
Αντιγραφή κώδικα
docker exec -it flask /bin/bash
Containerize Web Service
To create the image, execute the following command:
bash
Αντιγραφή κώδικα
docker build -t ds_airlines .
To see the available images, run:
bash
Αντιγραφή κώδικα
docker images
If you want to delete an image, run:
bash
Αντιγραφή κώδικα
docker rmi (imageid)
Data
All application data, in addition to being stored in the container, are also saved in a local folder named data. This folder is created automatically when the command docker-compose up -d is executed, ensuring that data is not lost in case something happens to the database container.

---------------------------------------------------------------------------------------------------------------------------------------------------------------

# Ergasia_Febrouariou
# DS Airlines

Υποχρεωτική εργασία στο μάθημα "Πληροφοριακά Συστήματα"  
Τμήμα Ψηφιακών Συστημάτων, Πανεπιστήμιο Πειραιώς

## Εκτέλεση εφαρμογής
Για να εκτελεστεί το web service απο τον υπολογιστή κάποιου, θα πρέπει να υπάρχει εγκατεστημένο το Docker - Docker Compose.     

### Για να εγκατασταθεί σε συστήματα WINDOWS
###### (Tο docker-compose υπάρχει ήδη στο Docker των Windows)

Μπορείτε να κατεβάσετε το εκτελέσιμο αρχείο για την εγκατάσταση
του Docker από εδώ: [Install Docker Desktop on Windows](https://docs.docker.com/desktop/install/windows-install/)  


### Για να εγκατασταθεί σε συστήματα LINUX
Αρκεί να εκτελέσετε τις παρακάτω εντολές στο terminal:
1. `sudo apt-get update`
2. `sudo apt install -y apt-transport-https ca-certificates curl
software-properties-common`
3. `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key
add - `
4. `sudo add-apt-repository -y "deb [arch=amd64]
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"`
5. `sudo apt-get update`
6. `sudo apt install docker-ce`
7. ``` sudo curl -L https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-`uname-s`-`uname -m` -o /usr/local/bin/docker-compose ```
8. ` sudo chmod +x /usr/local/bin/docker-compose`


## Απαιτήσεις εφαρμογής
Το web service θα εκτελείται στην πόρτα 5000 μέσω του Flask και η Mongodb θα εκτελείται στην πόρτα 27017. Αν υπάρχει κάποια άλλη υπηρεσία η οποία τρέχει σε αυτές τις πόρτες, θα πρέπει να σταματήσει η λειτουργία της.

Στην Mongodb έχει δημιουργηθεί μια βάση δεδομένων με όνομα **DS_Airlines** 

## Εκτέλεση εφαρμογής
* Κατεβάζουμε απο αυτό το repository το .zip αρχείο.
* Το κάνουμε unzip στον υπολογιστή μας.
* Κάνουμε μετονομασία και διαγράφουμε το -main απο τον τίτλο του φακέλου.
* Ανοίγουμε το terminal στο path: **YpoxreotikiErgasiaFebr24**
* Εκτελούμε την εντολή και δημιουργούμε το container : ` (sudo) docker-compose up -d `
* Για να σταματήσουμε την εκτέλεση : ` (sudo) docker-compose down `
* Ανοίγουμε απο τον browser της επιλογής μας το link και μπορούμε να χρησιμοποιήσουμε το web service: http://localhost:5000/

* ## MongoDB

Θα πρέπει να είμαστε στο path: **YpoxreotikiErgasiaSept22_E19226_Loulaki_Marina**  

* Για να χρησιμοποιηθεί το Mongo Shell, θα πρέπει να εκτελεστεί στο PowerShell / Terminal η εντολή : `(sudo) docker exec -it mongodb mongo`
* Για να χρησιμοποιηθεί η βάση δεδομένων που έχει δημιουργηθεί, θα πρέπει να εκτελεστεί η εντολή  : ` use DS_Airlines `
* Για να εμφανιστούν τα collections, θα πρέπει να εκτελεστεί η εντολή  : ` show collections `
* Για να εμφανιστούν όλες οι εγγραφές των χρηστών, θα πρέπει να εκτελεστεί η εντολή  : ` db.users.find({}) `
* Για να εμφανιστούν όλες οι πτήσεις που έχουν δημιουργηθεί απο τον διαχειριστή, θα πρέπει να εκτελεστεί η εντολή  : ` db.flights.find({}) `
* Για να εμφανιστούν όλες οι κρατήσεις που έχουν δημιουργηθεί απο τους χρήστες, θα πρέπει να εκτελεστεί η εντολή  : ` db.reservations.find({}) `
* Για να εμφανιστούν όλες οι ακυρώσεις που έχουν γίνει απο τους χρήστες και εκκρεμούν οι επιστροφές χρημάτων, θα πρέπει να εκτελεστεί η εντολή  : ` db.refund.find({}) `
* Το ίδιο μπορούμε να κάνουμε με όλα τα collection.
* Αν θέλουμε να εμφανιστούν σε έναν πιο όμορφο τρόπο, μετά το τέλος της κάθε μιας εντολής find, προσθέτουμε το : `.pretty() `

#### Στην βάση υπάρχουν ήδη αποθηκευμένα τα δεδομένα απο χρήστες, πτήσεις, αξιολογήσεις, κρατήσεις, μηνύματα επικοινωνίας, εγγεγραμένους χρήστες στο newsletter, ακυρωμένες κρατήσεις ####

## Flask

* Για να εκτελέσουμε το Flask θα πρέπει να εκτελέσουμε την εντολή απο το PowerShell / Terminal (απο τον φάκελλο του directory) :  ` docker exec -it flask /bin/bash `


## Containerize Web Service

* Για να δημιουργήσω τo image, εκτέλεσα την εντολή  : ` docker build -t ds_airlines .`
* Για να δούμε τα images που υπάρχουν, εκτελούμε την εντολή  : ` docker images `
* Αν θέλουμε να διαγράψουμε ένα image, εκτελούμε την εντολή  : ` docker rmi (imageid) `

## Data

Όλα τα δεδομένα της εφαρμογής, εκτός απο το container αποθηκεύονται και σε έναν τοπικό φάκελο **data**, ο οποίος δημιουργείται αυτόματα όταν εκτελούμε την εντολή : `docker-compose up -d ` , για να μην διαγραφούν τα δεδομένα σε περίπτωση που γίνει κάτι στο container της βάσης δεδομένων. 


