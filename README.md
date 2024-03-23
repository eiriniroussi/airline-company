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


