## Project 1: National progress plans data extraction project 

### Stage 1: Basic data extraction
Objective: Create a basic application to extract data from standardized excel spreadsheets, which are used for preparing national progress plans.

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
- Logged-in user can delete their account.
- Logged-in user can change their password.
- Create an admin page.
- Admin user can make another registered user an admin user.
- Admin user can delete any user and any project.
- Admin user can't create new user.
- Admin user can't create new project.
- All new users must be verified by an admin user.

### Stage 6: Improved UX
Objective: Implement features that improves user experience.

Requirements:
- When user registers an email is sent to user email.
- When new user registers an email is sent to all admin users emails.
- Include GDPR pop-up for cookie managment.
- Merge Plotly and bootstrap colors.
- Add comments in tables for invalid ratios values.
- Map database cashflows categories with user friendly category names.
- Restyle index page upper part.

### Stage 7: Testing
Objective: Create tests and clean up code.

Requirements:
- Create tests for testing application functionality.
- Clean up code from unused code.
- Add docstrings to at least all functions that are used in routes files.
- Add requirements.txt

### Stage 8: Deployment
Objective: Deploy an application.

Requirements:
- Deploy an app.