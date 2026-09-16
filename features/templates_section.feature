## Feature: Template Management

# TC_01_Upload_Valid_Template.py

### Scenario: Upload a valid template zip file
```gherkin
Given I am logged in and on the "Templates" page
When I click the "Upload New Template" button
And I enter template name "AUT_Valid_Template"
And I enter description "Automation test template description"
And I upload a valid zip file "Updated Audio template.zip"
And I click "Upload"
Then I should see a success toast message "Successfully created Templates"
And "AUT_Valid_Template" should appear in the templates list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_02_Upload_Invalid_Template.py

### Scenario: Attempt to upload an invalid non-zip template file
```gherkin
Given I am on the "Templates" page
When I click the "Upload New Template" button
And I enter template name "AUT_Invalid_Template"
And I enter description "Automation test template description"
And I attempt to upload a non-zip file "Sample-BAT-File-calculator.bat"
Then I should see an error message "Only ZIP files are allowed"
And the "Upload" button should be in disabled mode
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_03_Duplicate_Invalid_Template_Naming.py

### Scenario: Validate template duplicate name, case-insensitive duplicate, and special character validation
```gherkin
Given I am on the "Templates" page
When I attempt to create a template with an existing name "AUT_Template_Duplicate"
Then I should see an error message "A template with this name already exists"
When I attempt to create a template with case-variant name "AUT_TEMPLATE_DUPLICATE"
Then I should see an error message "A template with this name already exists"
When I attempt to enter template name with special characters "AUT_@$%%$_Hello"
Then I should see an error message "Only letters, numbers, spaces, _ and - are allowed"
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_04_Search_Template_Names.py

### Scenario: Search template names and handle non-existing search
```gherkin
Given I am on the "Templates" page
When I enter an existing template name "AUT_Search_Temp" into the search bar
Then "AUT_Search_Temp" should be displayed in the search results
When I enter a non-existing template name "Checking_Template_Not_There" into the search bar
Then I should see a message "No templates found"
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_05_Delete_Single_Multiple_Template.py

### Scenario: Delete single and multiple templates
```gherkin
Given I am on the "Templates" page
When I select a single template "AUT_Delete_Template_1"
And I click "Delete"
And I type "DELETE" in the confirmation popup and click "Delete"
Then I should see a success toast message "Successfully Deleted Template"
And "AUT_Delete_Template_1" should be removed from the templates list
When I select multiple templates "AUT_Delete_Template_2", "AUT_Delete_Template_3", "AUT_Delete_Template_4"
And I click "Delete" and confirm deletion
Then I should see "Successfully Deleted Template" message
And all selected templates should be removed from the templates list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_06_Prevent_Delete_Template_In_Project.py

### Scenario: Prevent deleting a template that is configured in a project workflow
```gherkin
Given I have a template "AUT_Delete_Template" configured inside a workflow and linked to a project
When I navigate to the "Templates" page
And I select the template "AUT_Delete_Template" and click "Delete"
And I confirm deletion by typing "DELETE"
Then I should see an error message "Failed Deleted Template"
And the template "AUT_Delete_Template" should not be deleted from the templates list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_07_Bulk_Delete_Templates_Blocked_In_Workflow.py

### Scenario: Bulk delete templates blocked when configured in workflow annotate nodes
```gherkin
Given I have templates "AUT_Bulk_Template_1" and "AUT_Bulk_Template_2" configured in workflow annotate nodes
When I navigate to the "Templates" page
And I select both templates "AUT_Bulk_Template_1" and "AUT_Bulk_Template_2" for bulk deletion
And I click "Delete" and confirm deletion
Then I should see an error message "Failed Deleted Template"
When I click "Cancel" on the deletion popup
Then both templates "AUT_Bulk_Template_1" and "AUT_Bulk_Template_2" should remain visible in the templates list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_08_Upload_Invalid_Zip_Template.py

### Scenario: Upload an invalid mixed-files zip file as template
```gherkin
Given I am on the "Templates" page
When I click the "Upload New Template" button
And I enter template name "AUT_Invalid_Zip_Template"
And I upload a mixed files zip file "Mixed Files.zip"
Then I should see an error message "invalid Zip File"
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_09_Template_Boundary_Input_Validation.py

### Scenario: Boundary input validation for 50-character template name and 2000-character description
```gherkin
Given I am on the "Templates" page
When I click "Upload New Template"
And I enter a 50-character template name "AUT_Boundary_Template_Name_50_Characters_Length_Ex"
And I enter a 2000-character description
And I upload a valid zip file and click "Upload"
Then the template should be created successfully
And the 50-character template name should be accepted and visible in the templates list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_10_Update_Template_Functionality.py

### Scenario: Update an existing template with a new zip file
```gherkin
Given I am on the "Templates" page and have created a template "AUT_Update_Template"
When I click the "Update" button towards template "AUT_Update_Template"
And I upload a new zip file "Updated text template.zip" and click "Upload"
Then I should see a success toast message "Template updated successfully"
And the template should be updated with the new zip file
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_11_Templates_Pagination.py

### Scenario: Templates pagination controls (5, 10, 20, 50) and persistence across creation and navigation
```gherkin
Given I am on the "Templates" page
When I select pagination option "5"
Then the displayed templates count should not exceed 5
When I create a new template while pagination is set to 5
Then the displayed templates count should remain <= 5
When I navigate to the "Datasets" tab and return to "Templates" page
Then the pagination limit 5 should be preserved and count should remain <= 5
When I select pagination options "10", "20", and "50"
Then the displayed templates count should not exceed 10, 20, and 50 respectively
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_12_Bulk_Delete_Linked_Unlinked_Templates.py

### Scenario: Bulk delete containing both linked and unlinked templates
```gherkin
Given I have a linked template "AUT_Bulk_Linked_Template" in a project workflow
And an unlinked template "AUT_Bulk_Unlinked_Template"
When I navigate to the "Templates" page
And I select both "AUT_Bulk_Linked_Template" and "AUT_Bulk_Unlinked_Template" and click "Delete"
Then I should see an error message "Failed Deleted Template" for the linked template
When I cancel the deletion popup
Then the unlinked template "AUT_Bulk_Unlinked_Template" should be deleted from the list
And the linked template "AUT_Bulk_Linked_Template" should remain retained in the templates list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_13_Workflow_With_50_Chars_Template_Name.py

### Scenario: Create workflow with a 50-character template name
```gherkin
Given I am logged in and on the "Templates" page
When I create a template with a 50-character name "AUT_Boundary_Template_Name_50_Characters_Length_Ex"
And I navigate to the "Workflows" page
And I click "Create workflow" and enter name "AUT_Workflow_50_Chars_Template"
And I add nodes ["Start", "Annotate", "Review", "Complete"]
And I apply the 50-character template "AUT_Boundary_Template_Name_50_Characters_Length_Ex" to the Annotate node
And I connect the nodes flow and click "Save"
Then the workflow using the 50-character template name should be saved and created successfully
```
