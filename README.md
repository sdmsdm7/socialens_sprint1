# SociaLens alpha version 1.0
## GOAL: Get to SociaLens aplha version 2.0

---
### SETUP to run the initial commit
- install Flask, Pandas
- to run the application:
-   cd into the application root folder where app.py is.
-   run the application with:
``` python3 app.py ```

---
### USING SociaLens version 1.0
- You start off in index.html
- Click on data upload -> upload a xlsx file ("Student_Survey_-_Jan.xlsx")
- upload a pdf file -> observe the failure message
- after uploading a file -> click on datasets to see the uploaded file
- after uploading a file -> check the uploads folder in VSCode to see the uploaded file in the back-end
- click on descriptive statistics -> click on the uploaded dataset -> see the descriptive statistics

---
### TROUBLESHOOTING
- if you get an error connecting to the Flask application in chrome, flush the socket pool
- arc://net-internals/#sockets
- click on Flush Socket Pools
- reload the application
