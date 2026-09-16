## Feature: File Management

# TC_01_Upload_Single_Multiple_Invalid_Files.py

### Scenario: Upload a single file 
```gherkin
Given I am logged in and on the "Files" page
When I click the "Upload File" button
And I select a file "document.pdf" from my computer
And I click "Upload"
Then I should see "Files uploaded successfully" message
And "document.pdf" should appear in the files list
```

### Scenario: Upload multiple files
```gherkin
Given I am on the "Files" page
When I click the "Upload Files" button
And I select multiple files "image1.jpg", "image2.jpg", "data.csv"
And I click "Upload"
Then I should see "Files uploaded Successfully" message
And all three files should appear in the files list
```

### Scenario: Upload invalid file type
```gherkin
Given I am on the "Files" page
When I attempt to upload a file "malware.exe"
Then I should see an error message "files skipped (incompatible)"
And the file should not be uploaded
And Upload button should be in disabled mode
```
/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_02_Files_Pagination.py

### Scenario: View list of files with 5 files per page
```gherkin
Given I am on the "Files" page
And the limit per page is set to 5
And there are more than 5 files in the system
Then I should see 5 files per page
And I should see pagination controls
When I click "Next Page"
Then I should see the next 5 files
When I upload a single file
Then I should see 5 files on the current page
When I switch to another tab
And I navigate back to the "Files" tab
Then the file pagination limit should remain set to 5
And I should see 5 files on the page

### Scenario: View list of files with 10 files per page
```gherkin
Given I am on the "Files" page
And the limit per page is set to 10
And there are more than 10 files in the system
Then I should see 10 files per page

### Scenario: View list of files with 20 files per page
```gherkin
Given I am on the "Files" page
And the limit per page is set to 20
And there are more than 20 files in the system
Then I should see 20 files per page

Scenario: View list of files with 50 files per page
```gherkin
Given I am on the "Files" page
And the limit per page is set to 50
And there are more than 50 files in the system
Then I should see 50 files per page

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_03_Search_Files_Name.py

### Scenario: Search for files by name
```gherkin
Given I am on the "Files" page
And I upload a file "sample_document.pdf"
And I click on the "Search" box
When I enter "sample_document" in the search field
Then I should see only files with "sample_document" in the filename

### Scenario: Search for a file uploaded from a Dataset
```gherkin
Given I am on the "Dataset" tab
When I create a new dataset
And I upload a file "dataset_file.pdf" to the dataset
And I navigate to the "Files" tab
And I click on the "Search" box
When I enter "dataset_file" in the search field
Then I should see "dataset_file.pdf" in the search results
And I should see the associated dataset name for the file

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_04_Delete_Multiple_files.py

### Scenario: Delete multiple files
```gherkin
Given I am on the "Files" page
When I select checkboxes for files "1", "2", and "3"
And I click the "Delete" button
And I confirm the deletion in the dialog
Then I should see a success message "Successfully Deleted Files"
And the selected files should be removed from the list

### Scenario: Delete a single file
```gherkin
Given I am on the "Files" page
When I select the checkbox for file "1"
And I click the "Delete" button
And I confirm the deletion in the dialog
Then I should see a success message "Successfully Deleted Files"
And the selected file should be removed from the list

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_05_Dataset_Add_Functionality.py

### Scenario: Add a single file to a dataset
```gherkin
Given I am on the "Dataset" tab
And I have created 2 datasets
And I navigate to the "Files" page
And I upload a file "document.pdf"
When I select the checkbox for file "document.pdf"
And I click the "Add to Dataset" button
Then I should see a success message "Files added successfully"

### Scenario: Add multiple files to a single dataset
```gherkin
Given I am on the "Files" page
And I have files "report1.pdf", "report2.pdf", and "report3.pdf" in the list
When I select checkboxes for files "report1.pdf", "report2.pdf", and "report3.pdf"
And I click "Add to Dataset"
Then I should see a success message "Files added successfully"

### Scenario: Add files to a dataset when some files already exist
```gherkin
Given I am on the "Files" page
And I upload a new file "new_file.pdf"
And I have a file "existing_file.pdf" that is already associated with "Training Dataset 2024"
When I select checkboxes for files "new_file.pdf" and "existing_file.pdf"
And I click the "Add to Dataset" button
And I select "Training Dataset 2024" from the dataset list
And I click "Add to Dataset"
Then I should see a message indicating that 1 file was added successfully
And I should see a message indicating that 1 file was skipped
And "new_file.pdf" should be associated with "Training Dataset 2024"
And "existing_file.pdf" should remain associated with "Training Dataset 2024"

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_06_Dataset_Delete_Functionality.py

### Scenario: Attempt to delete file attached to dataset
```gherkin
Given I am on the "Dataset" tab
And I have created one dataset
And I navigate to the "Files" page
And I upload one file
And I select the uploaded file
And I click "Add to Dataset"
And I select the created dataset
Then the file should be successfully added to the dataset
When I select the same file
And I click the "Delete" button
Then I should see an error message "Failed to Delete File"
And the file should not be deleted

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_07_Cancel_Dataset_Addition.py

### Scenario: Cancel file to dataset addition
```gherkin
Given I am on the "Files" page
And I have selected files to add to a dataset
When I click "Add to Dataset"
And the dataset selection modal opens
And I click "Cancel"
Then the modal should close
And no files should be added to any dataset
And my file selection should be preserved

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_08_Create_New_Dataset.py

### Scenario: Create a new dataset from the Files page
```gherkin
Given I am on the "Files" page
When I upload one file
And I select the uploaded file
And I click the "Add to Dataset" button
And I click "Create New Dataset" in the popup
And I enter a dataset name
And I click "Create"
Then the new dataset should be created successfully
And I should be able to navigate to the "Dataset" tab
And the newly created dataset should be displayed in the dataset list
And I should be able to open the newly created dataset
And the uploaded file should be present inside the dataset

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_09_Upload_Mixed_Files_Valid_Invalid.py

### Scenario: Group of Files Upload with Valid and Invalid Files
```gherkin
Given I am on the "Files" page
When I select mixed files containing both valid and invalid files
Then I should see an error message "files skipped (incompatible)" for invalid files
And I click "Upload" to upload valid files
Then I should see "Files uploaded successfully" message
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_10_Validate_Upload_Files_Tabs.py

### Scenario: Validate Upload Files modal tabs options
```gherkin
Given I am on the "Files" page
When I click the "Upload Files" button
Then I should see the upload modal tabs options ["Upload", "Import from S3"]
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_11_Cancel_File_Upload.py

### Scenario: Cancel file upload operation during active file upload
```gherkin
Given I am on the "Files" page
When I select multiple files to upload and click "Upload"
And I click the "% Uploading" progress button
And I click "Cancel" on the upload modal
And I confirm "OK" on the confirmation prompt "Are you sure you want to cancel the active upload?"
Then the upload operation should be cancelled
And the upload modal should be closed
And the "Upload Files" button should be visible again
```
