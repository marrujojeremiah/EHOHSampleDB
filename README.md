## Live Demo

You can view the live demo of this project [Here]https://ehohsampledb-5c75a0ccdabf.herokuapp.com/

Login has been turned off for this live demo. 

Server Setup and Installation:

I installed the Flask application on a dedicated server machine within the facility. The server runs a Linux-based operating system, providing a stable and secure environment for the application.
I configured the server to host the application using a production-grade web server, such as Gunicorn, and set up a reverse proxy with Nginx to handle incoming requests efficiently.
Database Configuration:

The database is set up using PostgreSQL, a robust and secure relational database management system, hosted on the same server. I configured PostgreSQL with role-based access control to ensure that only authorized users can access the database.
The database connection is secured using SSL/TLS encryption to protect data in transit.
Local Network Access:

I configured the application to be accessible only within the local network using private IP addresses. This ensures that the application is not exposed to the public internet, reducing the risk of unauthorized access.
The five computers within the facility are connected to the local network via a secure router with a firewall, providing an additional layer of protection against external threats.
User Authentication and Access Control:

I implemented a user authentication system within the application, requiring staff to log in with unique usernames and strong passwords before accessing the database. Passwords are hashed and stored securely in the database.
Role-based access control is applied within the application, ensuring that different levels of staff have appropriate access rights to various sections of the database. For example, only authorized medical staff can update medication records.
Data Encryption and Backup:

Sensitive data within the database, such as social security numbers and medical information, is encrypted using industry-standard encryption algorithms to protect against unauthorized access, even if the database is compromised.
Regular automated backups of the database are scheduled, with backups stored securely both on-site and in an encrypted off-site location. This ensures data integrity and availability in the event of a hardware failure or other disaster.
Security Audits and Monitoring:

I set up continuous monitoring of the server and application logs to detect and respond to any suspicious activity. Intrusion detection systems (IDS) are employed to alert administrators of potential security breaches.
Regular security audits and vulnerability assessments are conducted to ensure that the application and server environment remain secure and up-to-date with the latest security patches.
