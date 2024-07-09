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

### Stage 4: Minimal application
Objective: Implement search for projects.

Requirements:
- Non-registered user can see all uploaded projects.
- Users can search for projects.
- Registered users can search for uploaded projects in dashboard.
- Create header.
- Create footer.
- Create basic styling for all pages.
- Map basic plotly style to fit default bootstrap style.
- If user is logged in show his username in header.
- Create Privacy Policy and Terms of Service routes.

### Stage 5: Flask admin
Objective: Implement admin dashboard.

Requirements:
- When registering user must enter a complex password.
- Logged in user can delete his account.
- Logged in user can change his password.
- Create admin page.
- Admin user can create another admin user.
- Admin user can delete any account.
- Registration of new user should be confirmed by admin user.
- When new user registers an email is sent to admin emails.
- Implement page not found template.