# Ergasia_Febrouariou
# DS Airlines

Mandatory assignment for the course "Information Systems"
Department of Digital Systems, University of Piraeus

## Application Execution
To run the web service on someone's computer, Docker and Docker Compose must be installed.     

### Installation on WINDOWS systems
###### (Docker Compose is already included in Docker for Windows)

You can download the executable file to install Docker from here: [Install Docker Desktop on Windows](https://docs.docker.com/desktop/install/windows-install/)  

### Installation on LINUX systems
Simply run the following commands in the terminal:
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

## Application Requirements
The web service will run on port 5000 via Flask, and MongoDB will run on port 27017. If another service is running on these ports, it must be stopped.

A database named DS_Airlines has been created in MongoDB.** 

## Running the Application
* Download the .zip file from this repository.
* Unzip it on your computer.
* Rename the folder and remove the -main suffix from the folder name.
* Open the terminal at the path: **YpoxreotikiErgasiaFebr24**
* Run the following command to create the container: ` (sudo) docker-compose up -d `
* To stop the application, run: ` (sudo) docker-compose down `
* Open your preferred browser and access the web service via: http://localhost:5000/

* ## MongoDB

You must be in the path: YpoxreotikiErgasiaSept22_E19226_Loulaki_Marina 

* To use the Mongo Shell, execute the following command in PowerShell/Terminal: `(sudo) docker exec -it mongodb mongo`
* To use the database that has been created, run: ` use DS_Airlines `
* To display the collections, run: ` show collections `
* To display all user records, run: ` db.users.find({}) `
* To display all flights created by the admin, run: ` db.flights.find({}) `
* To display all reservations made by users, run: ` db.reservations.find({}) `
* To display all cancellations made by users with pending refunds, run: ` db.refund.find({}) `
* You can do the same for all collections.
* To display the output in a more readable format, append .pretty() at the end of each find command, like this: `.pretty() `

#### The database already contains stored data for users, flights, reviews, reservations, communication messages, registered newsletter users, and canceled reservations. ####


## Flask

* To run Flask, execute the following command from PowerShell/Terminal (from the directory folder):  ` docker exec -it flask /bin/bash `

## Containerize Web Service

* To create the image, run the following command: ` docker build -t ds_airlines .`
* To see the available images, run: ` docker images `
* To delete an image, run: ` docker rmi (imageid) `


# Data

All application data, in addition to being stored in the container, is also saved in a local folder called data, which is automatically created when you run the command:

 `docker-compose up -d `

This ensures that the data is not deleted if something happens to the database container.

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


