## Project 1: National progress plans data extraction project 

### Stage 1: Basic data extraction
Objective: Create a basic application to extract data from standartized excel spreadsheets, which are used for preparing national progress plans.

Requirements:
- Enable file upload in flask application. 
- Extract information from file and save it to a database.

### Stage 2: Basic user authentication
Objective: Create basic user authentication with Flask-Login.

Requirements:
- User can register.
- User can login and choose to stay logged in.
- User can logout.
- User can upload projects.
- User can read and delete projects.
- User can see menu items based on log in fact.
- User can access upload, dashboard and auth/logout routes only if he is logged in.


### Stage 3: Basic visualization for data
Objectives: 
- Enforce uploading only valid files.
- Create project specific and aggregate data visualization.

Requirements:
- Validate eligble to upload excel files.
- Create visuals of aggregate data.
- Create visuals for viewing specific project data.