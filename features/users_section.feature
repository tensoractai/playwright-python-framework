## Feature: User Management

# TC_01_Create_Valid_User_And_Login.py

### Scenario: Create a valid user with multiple roles and verify login as Company Admin
```gherkin
Given I am logged in as a Company Admin and on the "Users" page
When I click the "Create User" button
And I enter full name "AutomationTesting1"
And I enter email "automationtesting1@test.com"
And I enter password "AUT_Testing@123" and confirm password "AUT_Testing@123"
And I enable alternate MFA email checkbox
And I select roles ["Company Admin", "Project Supervisor", "Project Viewer", "Annotator", "Reviewer", "Dataset Supervisor", "Dataset Viewer", "API User"]
And I click "Create User" button
Then "automationtesting1@test.com" should appear in the users list
When I open a new browser instance and log in with email "automationtesting1@test.com" and password "AUT_Testing@123"
Then I should see the home page welcome header
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_02_Create_User_Validation_Errors.py

### Scenario: Validate error messages for invalid email format, short password, and password mismatch
```gherkin
Given I am logged in as a Company Admin and on the "Users" page
When I click the "Create User" button
And I enter invalid email "hello123"
Then I should see an error message "Invalid email address"
When I enter short password "hello"
Then I should see an error message "Password must be at least 8"
When I enter password "hello" and confirm password "automation"
Then I should see an error message "Passwords must match"
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_03_Duplicate_User_And_Query_Keyword_Validation.py

### Scenario: Validate duplicate user email creation error and SQL query keyword input validation
```gherkin
Given I am logged in as a Company Admin and on the "Users" page
When I attempt to create a user with an already existing email "automationtesting1@test.com"
Then I should see an error message "User already exists in this"
When I attempt to create a user with SQL query keyword name "DROP", email "drop@drop.com", and password "Drop@123"
Then the input should be handled securely without database syntax execution
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_04_Validate_User_Roles_Dropdown_Options.py

### Scenario: Validate all expected user role options in the select roles dropdown
```gherkin
Given I am logged in as a Company Admin and on the "Users" page
When I click "Create User" button
And I click "Select roles" dropdown
Then I should see options ["Company Admin", "Project Supervisor", "Project Viewer", "Annotator", "Reviewer", "Dataset Supervisor", "Dataset Viewer", "API User"]
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_05_SuperUser_Company_Creation_And_Admin_User_Flow.py

### Scenario: Super User creates company, configures roles, creates Company Admin, and Company Admin creates Annotator and Reviewer users
```gherkin
Given I am logged in as a Super User
When I navigate to "Companies" page and click "Add Company"
And I create a company with name "AUT_Testing_1", legal name "AUT_Testing", domain "automation.com", and initial role "Project Supervisor"
And I configure allowed company roles ["Company Admin", "Project Viewer", "Annotator", "Reviewer", "Dataset Supervisor", "Dataset Viewer", "API User"]
Then "AUT_Testing_1" should appear in the companies list
When I navigate to "Users" page and create Company Admin user "Testing" with email "aaa@automation.com"
Then "aaa@automation.com" should appear in the users list
When I open a new browser instance and log in as "aaa@automation.com" under organization "AUT_Testing_1" as Company Admin
Then I should navigate to "Users" page and create Annotator user "annotator@automation.com" and Reviewer user "reviewer@automation.com"
And both "annotator@automation.com" and "reviewer@automation.com" should appear in the users list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_06_Delete_Company_And_Validate_User_Removal.py

### Scenario: Super User creates company and user, deletes company, and validates cascade removal of company and associated user
```gherkin
Given I am logged in as a Super User
When I create a company "AUT_testing" with domain "auttesting.com"
And I configure company roles and verify "AUT_testing" appears in the companies list
And I create a user "delete_user@auttesting.com" assigned to company "AUT_testing"
Then "delete_user@auttesting.com" should appear in the users list
When I navigate to "Companies" page, select company "AUT_testing", acknowledge deletion, type "delete a company", and click "Delete"
Then "AUT_testing" should no longer appear in the companies list
When I navigate to "Users" page
Then "delete_user@auttesting.com" should no longer appear in the users list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_07_Search_User_Validation.py

### Scenario: Create user, search for valid user email, and search non-existing user displaying empty state message
```gherkin
Given I am logged in as a Company Admin and on the "Users" page
When I create a new user with email "search_user_test@test.com"
And I enter "search_user_test@test.com" into the search field
Then "search_user_test@test.com" should appear in the search results
When I enter a non-existing user "non_existing_user_9999" into the search field
Then I should see the cell message "No users found"
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_08_Users_Pagination.py

### Scenario: Users pagination controls (5, 10, 20, 50) and persistence across user creation and tab navigation
```gherkin
Given I am logged in as a Company Admin and on the "Users" page
When I select pagination option "5"
Then the displayed users count should not exceed 5
When I create a new user while pagination is set to 5
Then the displayed users count should remain <= 5
When I navigate to "Datasets" tab and return to "Users" page
Then the pagination limit 5 should be preserved and count should remain <= 5
When I select pagination options "10", "20", and "50"
Then the displayed users count should not exceed 10, 20, and 50 respectively
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_09_Deactivate_User.py

### Scenario: Create user, deactivate user, verify inactive status, and validate inactive account error on login
```gherkin
Given I am logged in as a Company Admin and on the "Users" page
When I create a new user with email "deactivate_user@test.com"
Then "deactivate_user@test.com" should be present in the users list
When I select the checkbox for "deactivate_user@test.com" and click "Change Status" then "Deactivate"
Then the status badge for "deactivate_user@test.com" should display "inactive"
When I open a new browser instance and attempt to log in with email "deactivate_user@test.com" and password "DeactivateUser@123"
Then I should see the error message "Your account is not active."
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_10_Edit_User_Roles.py

### Scenario: Create user, edit user roles, and validate user presence after role update
```gherkin
Given I am logged in as a Company Admin and on the "Users" page
When I create a new user "Edit Roles" with email "edit_roles_user@test.com" and role "Company Admin"
Then "edit_roles_user@test.com" should appear in the users list
When I click the edit button for "Edit Roles"
And I expand the roles dropdown, select "Project Supervisor", uncheck "Company Admin", and click "Save Roles"
Then "edit_roles_user@test.com" should remain present in the users list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_11_Bulk_Deactivate_Users.py

### Scenario: Create two users with different roles, select checkboxes, perform bulk deactivation, and validate inactive status
```gherkin
Given I am logged in as a Company Admin and on the "Users" page
When I create user 1 "bulk_user1@test.com" with role "Company Admin"
And I create user 2 "bulk_user2@test.com" with role "Project Supervisor"
Then both "bulk_user1@test.com" and "bulk_user2@test.com" should be present in the users list
When I select the checkboxes for both "bulk_user1@test.com" and "bulk_user2@test.com"
And I click "Change Status" and select "Deactivate"
Then the status badges for both "bulk_user1@test.com" and "bulk_user2@test.com" should display "inactive"
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_12_Single_And_Bulk_Delete_Users.py

### Scenario: Create 3 users, single delete 1 user, and bulk delete remaining 2 users
```gherkin
Given I am logged in as a Company Admin and on the "Users" page
When I create user 1 "delete_user1@test.com", user 2 "delete_user2@test.com", and user 3 "delete_user3@test.com"
Then all 3 users should appear in the users list
When I select the checkbox for "delete_user1@test.com"
And I click "Delete", type "DELETE", and confirm deletion
Then "delete_user1@test.com" should be removed from the users list
When I select the checkboxes for both "delete_user2@test.com" and "delete_user3@test.com"
And I click "Delete", type "DELETE", and confirm deletion
Then both "delete_user2@test.com" and "delete_user3@test.com" should be removed from the users list
```
