## Feature: Dataset Management

# TC_01_Valid_Dataset_Creation.py

### Scenario: Create a valid dataset, upload CSV file and validate across pages
```gherkin
Given I am logged in and on the "Datasets" page
When I click the "Create Dataset" button
And I enter dataset name "AUT_Dataset_Valid"
And I select dataset type "CSV"
And I click "Create"
Then I should see dataset "AUT_Dataset_Valid" created successfully in dataset list
When I click on the dataset "AUT_Dataset_Valid"
And I upload valid files "CSV Test data.csv" and "converted_data.csv" using upload button
Then I should see a success message "2 files added"
And all uploaded files should appear inside the dataset
When I navigate to the "Files" tab
Then I should see all uploaded files listed in the files table
And the dataset name "AUT_Dataset_Valid" should be associated with the files
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_02_Invalid_Dataset_Creation.py

### Scenario: Attempt to upload invalid file types into a PDF dataset
```gherkin
Given I am logged in and on the "Datasets" page
When I click the "Create Dataset" button
And I enter dataset name "AUT_Dataset_Invalid"
And I select dataset type "PDF"
And I click "Create"
Then the dataset "AUT_Dataset_Invalid" should be created in the list
When I open dataset "AUT_Dataset_Invalid"
And I attempt to upload incompatible files "CSV Test data.csv" and "converted_data.csv"
Then I should see an error message "files skipped (incompatible)"
And the Upload button should remain disabled
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_03_Invalid_Naming_Convention.py

### Scenario: Create dataset with invalid special characters in name
```gherkin
Given I am logged in and on the "Datasets" page
When I click the "Create Dataset" button
And I enter an invalid dataset name "AUT_123_#$%^&_hello" with special characters
And I select dataset type "PDF"
And I click "Create"
Then I should see an error message "Only letters, numbers, spaces, _ and - are allowed"
When I click "Cancel" on the dataset creation modal
Then the dataset creation dialog should close

### Scenario: Attempt to create a dataset with an existing dataset name
Given I am on the "Datasets" page
When I click the "Create Dataset" button
And I enter an already existing dataset name "AUT_Dataset_Invalid"
And I select dataset type "PDF"
And I click "Create"
Then I should see an error message "A Dataset with this name already exists"
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_04_Pagination_Controls.py

### Scenario: Verify dataset table pagination limit set to 5
```gherkin
Given I am logged in and on the "Datasets" page
When I select dataset pagination limit to 5
Then the dataset names displayed should not exceed 5 items
When I create a new dataset "AUT_Pagination_Check" with type "PDF"
Then the dataset table should still display a maximum of 5 items
When I navigate to the "Files" tab and return to the "Datasets" tab
Then the pagination limit should persist as 5 items per page

### Scenario: Verify dataset table pagination limit set to 10
Given I am on the "Datasets" page
When I select dataset pagination limit to 10
Then the dataset names displayed should not exceed 10 items

### Scenario: Verify dataset table pagination limit set to 20
Given I am on the "Datasets" page
When I select dataset pagination limit to 20
Then the dataset names displayed should not exceed 20 items

### Scenario: Verify dataset table pagination limit set to 50
Given I am on the "Datasets" page
When I select dataset pagination limit to 50
Then the dataset names displayed should not exceed 50 items
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_05_Search_Dataset_Names.py

### Scenario: Search dataset by name
```gherkin
Given I am logged in and on the "Datasets" page
And I have created a dataset named "AUT_Search_Datset"
When I click on the search box
And I enter "AUT_Search_Datset" in the search field
Then I should see "AUT_Search_Datset" displayed properly in the dataset list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_06_Add_Files_Dataset.py

### Scenario: Add uploaded files to an existing dataset
```gherkin
Given I am logged in and on the "Files" page
When I upload text files "ascii-art.txt", "long-doc.txt", "sample-1.doc", "sample1.docx"
And I upload extra text file "config conftest.py.txt"
Then I should see success toast message "Files uploaded successfully"
When I navigate to the "Datasets" page
And I create a dataset "AUT_Dataset_Text" with type "TEXT"
And I open dataset "AUT_Dataset_Text"
And I add each uploaded text file to the dataset
Then I should see success message "1 file added" for each file
And all added text files should be displayed inside dataset "AUT_Dataset_Text"

### Scenario: Add files to a dataset when some files already exist in dataset
Given I am inside dataset "AUT_Dataset_Text"
When I select a combination of new files and already added files
And I click "Add to Dataset"
Then I should see a toast message "1 file added"
And the duplicate file additions should be handled gracefully without errors
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_07_Delete_Single_Multiple_Dataset.py

### Scenario: Delete a single dataset
```gherkin
Given I am logged in and on the "Datasets" page
And I have created 4 datasets "AUT_Delete_Dataset_1", "AUT_Delete_Dataset_2", "AUT_Delete_Dataset_3", "AUT_Delete_Dataset_4"
When I select the checkbox for dataset "AUT_Delete_Dataset_1"
And I click the "Delete" button
And I enter "DELETE" in the deletion confirmation dialog
And I confirm deletion
Then I should see dataset "AUT_Delete_Dataset_1" removed from the dataset list

### Scenario: Delete multiple datasets simultaneously
Given I am on the "Datasets" page
And datasets "AUT_Delete_Dataset_2", "AUT_Delete_Dataset_3", and "AUT_Delete_Dataset_4" exist in the list
When I select checkboxes for "AUT_Delete_Dataset_2", "AUT_Delete_Dataset_3", and "AUT_Delete_Dataset_4"
And I click the "Delete" button
And I enter "DELETE" in the confirmation dialog
And I confirm deletion
Then all remaining 3 datasets should be removed from the dataset list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_08_Delete_Files_From_Dataset.py

### Scenario: Delete a file from a dataset and verify detachment across tabs
```gherkin
Given I am logged in and on the "Datasets" page
When I create a dataset "AUT_Delete_Files" with type "CSV"
And I open dataset "AUT_Delete_Files"
And I upload file "CSV Test data.csv" to the dataset
When I navigate to the "Files" tab
Then I should see dataset "AUT_Delete_Files" associated with "CSV Test data.csv"
When I navigate back to the dataset "AUT_Delete_Files"
And I select file "CSV Test data.csv" and click "Delete"
And I confirm the deletion in dialog
Then I should see toast message "Successfully Detached File"
And "CSV Test data.csv" should no longer be listed inside dataset "AUT_Delete_Files"
When I navigate to the "Files" tab
Then dataset name "AUT_Delete_Files" should no longer be associated with the file
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_09_Prevent_Delete_Dataset_In_Project.py

### Scenario: Prevent deletion of a dataset associated with an active project
```gherkin
Given I am logged in and on the "Datasets" page
When I create dataset "AUT_Prevent_Dataset" with type "Audio"
And I upload audio file "audio 2.flac" to the dataset
And I create a template "AUT_Prevent_Template"
And I create a workflow "AUT_Prevent_WorkFlow" with template applied
And I create a project "AUT_Prevent_Project" linking "AUT_Prevent_Dataset" and "AUT_Prevent_WorkFlow"
When I navigate to the "Datasets" page
And I attempt to delete dataset "AUT_Prevent_Dataset"
Then I should see a failure popup "Failed Deleted Dataset"
And dataset "AUT_Prevent_Dataset" should NOT be deleted from the dataset list
When I navigate to the "Projects" page
And I delete the project "AUT_Prevent_Project"
Then I should see success message "Successfully Deleted Project"
When I return to the "Datasets" page
And I delete dataset "AUT_Prevent_Dataset"
Then I should see success popup "Successfully Deleted Dataset"
And dataset "AUT_Prevent_Dataset" should be permanently removed from the list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_10_All_Dataset_Types_Lifecycle.py

### Scenario: Validate all available dataset types in creation modal
```gherkin
Given I am logged in and on the "Datasets" page
When I click the "Create Dataset" button
And I click the "Select Type" dropdown
Then I should see all expected dataset types ["Text", "Image", "Audio", "Video", "PDF", "Scanned (OCR)", "CSV"]
When I click "Cancel" on the creation popup
Then the modal should close without creating a dataset

### Scenario: Lifecycle of creating, uploading files, verifying, and deleting all dataset types
Given I am on the "Datasets" page
When I create datasets for each type:
  | Dataset Name         | Dataset Type  | File to Upload                  |
  | AUT_Dataset_Text_1   | TEXT          | text/ascii-art.txt              |
  | AUT_Dataset_Image    | Image         | image/web_optimized_1200x800.jpg |
  | AUT_Dataset_Video    | Video         | video/sample_960x540.mkv        |
  | AUT_Dataset_PDF      | PDF           | pdf/PDF Test data.pdf           |
  | AUT_Dataset_OCR      | Scanned (OCR) | pdf/Resume for Testing.pdf      |
  | AUT_Dataset_CSV      | CSV           | csv/CSV Test data.csv           |
And I upload respective files to each dataset
When I navigate to the "Files" tab
Then all created datasets and uploaded files should be listed in the Files tab
When I navigate back to the "Datasets" page
And I delete each dataset one by one
Then all datasets should be successfully deleted from the Datasets list
When I navigate to the "Files" tab
Then none of the deleted datasets should be present in the Files tab
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_11_Search_Dataset_In_Add_To_Dataset_Popup.py

### Scenario: Search dataset name in Add to Dataset popup from Files section
```gherkin
Given I am logged in and on the "Datasets" page
When I create a dataset "AUT_Popup_Search_Dataset" with type "Text"
And I navigate to the "Files" page
And I upload a text file "text/ascii-art.txt"
And I select the file "text/ascii-art.txt" and click "Add to Dataset"
When I enter dataset name "AUT_Popup_Search_Dataset" in the "Search datasets..." search bar inside the popup
Then dataset "AUT_Popup_Search_Dataset" should be displayed in the filtered dataset list
When I select dataset "AUT_Popup_Search_Dataset" and click "Add"
Then I should see a success toast message "1 items added"
And the file "text/ascii-art.txt" should be associated with "AUT_Popup_Search_Dataset"
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_12_Prevent_Add_Incompatible_Dataset_To_Project.py

### Scenario: Prevent adding an incompatible dataset type to a project workflow
```gherkin
Given I am logged in and on the "Datasets" page
When I create an Image dataset "AUT_Incompatible_Dataset" with type "Image"
And I upload image file "image/web_optimized_1200x800.jpg" to the dataset
And I create a Template "AUT_Incompatible_Template"
And I create a Workflow "AUT_Incompatible_Workflow" with template applied
When I navigate to the "Projects" page and click "Create Project"
And I enter project name "AUT_Incompatible_Project"
And I select workflow "AUT_Incompatible_Workflow"
And I attempt to select incompatible dataset "AUT_Incompatible_Dataset"
Then I should see an error message "dataset not compatible with workflow"
And the incompatible dataset addition to project should be blocked
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_13_Prevent_Delete_File_Linked_To_Project.py

### Scenario: Prevent deleting a file in a dataset linked to an active project and allow deletion after unlinking
```gherkin
Given I am logged in and on the "Datasets" page
When I create dataset "AUT_Prevent_Delete_File_Dataset" with type "Audio"
And I upload audio file "audio 2.flac" to the dataset
And I create template "AUT_Prevent_Delete_File_Template"
And I create workflow "AUT_Prevent_Delete_File_Workflow" with template applied
And I create project "AUT_Prevent_Delete_File_Project" linking dataset "AUT_Prevent_Delete_File_Dataset" and workflow "AUT_Prevent_Delete_File_Workflow"
When I open dataset "AUT_Prevent_Delete_File_Dataset"
And I select file "audio 2.flac" and click "Delete"
And I type "DELETE" in confirmation box and confirm
Then I should see an error message "Failed Detached File"
And the file "audio 2.flac" should NOT be deleted from the dataset
When I navigate to "Projects", open project "AUT_Prevent_Delete_File_Project", and remove dataset from project
And I return to dataset "AUT_Prevent_Delete_File_Dataset"
And I select file "audio 2.flac" and confirm deletion with "DELETE"
Then the file "audio 2.flac" should be successfully deleted from the dataset
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_14_Switch_Role_Validate_Company_Name.py

### Scenario: Switch role to Super User and validate dataset company name matches environment configuration
```gherkin
Given I am logged in and on the "Datasets" page
When I create dataset "AUT_Switch_Role_Dataset" with type "Text"
And I upload text file "text/ascii-art.txt" to the dataset
When I click the Admin profile button
And I click "Switch Role"
And I select "Super User" role
And I close the profile menu
When I navigate to the "Datasets" menu
Then I grab the company name associated with dataset "AUT_Switch_Role_Dataset"
And the grabbed company name should match the "company_Name" configured in environment file
```
