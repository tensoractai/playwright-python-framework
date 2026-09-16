## Feature: Workflows Management

# TC_01_Edit_WF_Start_Annotate_Review_Complete.py

### Scenario: Create, edit, and update workflow Start -> Annotate -> Review -> Complete
```gherkin
Given I am logged in and on the "Workflows" page
When I create a workflow "AUT_WF_01_Edit" with nodes ["Start", "Annotate", "Review", "Complete"]
And I apply template "AUT_WF_Com_Temp_A" to Annotate node
And I connect Review 1 to Annotate 1 node
And I click "Save"
Then the workflow "AUT_WF_01_Edit" should be saved successfully
When I edit the workflow "AUT_WF_01_Edit" and change template to "AUT_WF_Com_Temp_B"
And I set required annotators to "3"
And I rename nodes to "New_Ann" and "New_Rev"
And I click "Save"
Then the workflow "AUT_WF_01_Edit" should be updated successfully in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_02_Delete_WF_Start_Annotate_Review_Complete.py

### Scenario: Prevent deletion of linked workflow Start -> Annotate -> Review -> Complete
```gherkin
Given I am logged in
When I create a project "AUT_WF_Project_02" linking dataset "AUT_WF_Com_Dataset" and workflow "AUT_WF_01_Edit"
And I navigate to the "Workflows" page
And I attempt to delete the linked workflow "AUT_WF_01_Edit"
Then I should see an error popup preventing deletion of the linked workflow
When I click "Cancel" on the delete confirmation popup
Then the workflow "AUT_WF_01_Edit" should remain in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_03_Edit_WF_Start_Ann1_Ann2_Rev_Complete_Same.py

### Scenario: Create, edit, and update workflow Start -> Annotate 1 -> Annotate 2 -> Review -> Complete (Same Template)
```gherkin
Given I am logged in and on the "Workflows" page
When I create a workflow "AUT_WF_03_Edit" with nodes ["Start", "Annotate", "Annotate", "Review", "Complete"]
And I apply template "AUT_WF_Com_Temp_A" to Annotate 1 and Annotate 2
And I connect Review 1 to Annotate 2 node
And I click "Save"
Then the workflow "AUT_WF_03_Edit" should be saved successfully
When I edit the workflow "AUT_WF_03_Edit" and change template to "AUT_WF_Com_Temp_B"
And I set required annotators to "3"
And I rename nodes to "New_Ann" and "New_Rev"
And I click "Save"
Then the workflow "AUT_WF_03_Edit" should be updated successfully in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_04_Delete_WF_Start_Ann1_Ann2_Rev_Complete_Same.py

### Scenario: Prevent deletion of linked workflow Start -> Annotate 1 -> Annotate 2 -> Review -> Complete (Same Template)
```gherkin
Given I am logged in
When I create a project "AUT_WF_Project_04" linking dataset "AUT_WF_Com_Dataset" and workflow "AUT_WF_03_Edit"
And I navigate to the "Workflows" page
And I attempt to delete the linked workflow "AUT_WF_03_Edit"
Then I should see an error popup preventing deletion of the linked workflow
When I click "Cancel" on the delete confirmation popup
Then the workflow "AUT_WF_03_Edit" should remain in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_05_Edit_WF_Start_Ann1_Ann2_Rev_Complete_Diff.py

### Scenario: Create, edit, and update workflow Start -> Annotate 1 -> Annotate 2 -> Review -> Complete (Different Templates)
```gherkin
Given I am logged in and on the "Workflows" page
When I create a workflow "AUT_WF_05_Edit" with nodes ["Start", "Annotate", "Annotate", "Review", "Complete"]
And I apply template "AUT_WF_Com_Temp_A" to Annotate 1 and template "AUT_WF_Com_Temp_B" to Annotate 2
And I connect Review 1 to Annotate 2 node
And I click "Save"
Then the workflow "AUT_WF_05_Edit" should be saved successfully
When I edit the workflow "AUT_WF_05_Edit" and change template to "AUT_WF_Com_Temp_B"
And I set required annotators to "3"
And I rename nodes to "New_Ann" and "New_Rev"
And I click "Save"
Then the workflow "AUT_WF_05_Edit" should be updated successfully in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_06_Delete_WF_Start_Ann1_Ann2_Rev_Complete_Diff.py

### Scenario: Prevent deletion of linked workflow Start -> Annotate 1 -> Annotate 2 -> Review -> Complete (Different Templates)
```gherkin
Given I am logged in
When I create a project "AUT_WF_Project_06" linking dataset "AUT_WF_Com_Dataset" and workflow "AUT_WF_05_Edit"
And I navigate to the "Workflows" page
And I attempt to delete the linked workflow "AUT_WF_05_Edit"
Then I should see an error popup preventing deletion of the linked workflow
When I click "Cancel" on the delete confirmation popup
Then the workflow "AUT_WF_05_Edit" should remain in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_07_Edit_WF_Start_Ann_Rev1_Rev2_Complete.py

### Scenario: Create, edit, and update workflow Start -> Annotate 1 -> Review 1 -> Review 2 -> Complete
```gherkin
Given I am logged in and on the "Workflows" page
When I create a workflow "AUT_WF_07_Edit" with nodes ["Start", "Annotate", "Review", "Review", "Complete"]
And I apply template "AUT_WF_Com_Temp_A" to Annotate node 1
And I connect Review 1 to Annotate 1 and Review 2 to Review 1
And I click "Save"
Then the workflow "AUT_WF_07_Edit" should be saved successfully
When I edit the workflow "AUT_WF_07_Edit" and change template to "AUT_WF_Com_Temp_B"
And I set required annotators to "3"
And I rename nodes to "New_Ann" and "New_Rev"
And I click "Save"
Then the workflow "AUT_WF_07_Edit" should be updated successfully in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_08_Delete_WF_Start_Ann_Rev1_Rev2_Complete.py

### Scenario: Prevent deletion of linked workflow Start -> Annotate 1 -> Review 1 -> Review 2 -> Complete
```gherkin
Given I am logged in
When I create a project "AUT_WF_Project_08" linking dataset "AUT_WF_Com_Dataset" and workflow "AUT_WF_07_Edit"
And I navigate to the "Workflows" page
And I attempt to delete the linked workflow "AUT_WF_07_Edit"
Then I should see an error popup preventing deletion of the linked workflow
When I click "Cancel" on the delete confirmation popup
Then the workflow "AUT_WF_07_Edit" should remain in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_09_Edit_WF_Start_Ann1_Ann2_Complete_Same.py

### Scenario: Create, edit, and update workflow Start -> Annotate 1 -> Annotate 2 -> Complete (Same Template)
```gherkin
Given I am logged in and on the "Workflows" page
When I create a workflow "AUT_WF_09_Edit" with nodes ["Start", "Annotate", "Annotate", "Complete"]
And I apply template "AUT_WF_Com_Temp_A" to Annotate 1 and Annotate 2
And I click "Save"
Then the workflow "AUT_WF_09_Edit" should be saved successfully
When I edit the workflow "AUT_WF_09_Edit" and change template to "AUT_WF_Com_Temp_B"
And I set required annotators to "3"
And I rename nodes to "New_Ann" and "New_Rev"
And I click "Save"
Then the workflow "AUT_WF_09_Edit" should be updated successfully in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_10_Delete_WF_Start_Ann1_Ann2_Complete_Same.py

### Scenario: Prevent deletion of linked workflow Start -> Annotate 1 -> Annotate 2 -> Complete (Same Template)
```gherkin
Given I am logged in
When I create a project "AUT_WF_Project_10" linking dataset "AUT_WF_Com_Dataset" and workflow "AUT_WF_09_Edit"
And I navigate to the "Workflows" page
And I attempt to delete the linked workflow "AUT_WF_09_Edit"
Then I should see an error popup preventing deletion of the linked workflow
When I click "Cancel" on the delete confirmation popup
Then the workflow "AUT_WF_09_Edit" should remain in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_11_Edit_WF_Start_Ann1_Ann2_Complete_Diff.py

### Scenario: Create, edit, and update workflow Start -> Annotate 1 -> Annotate 2 -> Complete (Different Templates)
```gherkin
Given I am logged in and on the "Workflows" page
When I create a workflow "AUT_WF_11_Edit" with nodes ["Start", "Annotate", "Annotate", "Complete"]
And I apply template "AUT_WF_Com_Temp_A" to Annotate 1 and template "AUT_WF_Com_Temp_B" to Annotate 2
And I click "Save"
Then the workflow "AUT_WF_11_Edit" should be saved successfully
When I edit the workflow "AUT_WF_11_Edit" and change template to "AUT_WF_Com_Temp_B"
And I set required annotators to "3"
And I rename nodes to "New_Ann" and "New_Rev"
And I click "Save"
Then the workflow "AUT_WF_11_Edit" should be updated successfully in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_12_Delete_WF_Start_Ann1_Ann2_Complete_Diff.py

### Scenario: Prevent deletion of linked workflow Start -> Annotate 1 -> Annotate 2 -> Complete (Different Templates)
```gherkin
Given I am logged in
When I create a project "AUT_WF_Project_12" linking dataset "AUT_WF_Com_Dataset" and workflow "AUT_WF_11_Edit"
And I navigate to the "Workflows" page
And I attempt to delete the linked workflow "AUT_WF_11_Edit"
Then I should see an error popup preventing deletion of the linked workflow
When I click "Cancel" on the delete confirmation popup
Then the workflow "AUT_WF_11_Edit" should remain in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_13_Edit_WF_Start_Ann1_Rev1_Ann2_Rev2_Complete_Same.py

### Scenario: Create, edit, and update workflow Start -> Annotate 1 -> Review 1 -> Annotate 2 -> Review 2 -> Complete (Same Template)
```gherkin
Given I am logged in and on the "Workflows" page
When I create a workflow "AUT_WF_13_Edit" with nodes ["Start", "Annotate", "Review", "Annotate", "Review", "Complete"]
And I apply template "AUT_WF_Com_Temp_A" to Annotate 1 and Annotate 2
And I connect Review 1 to Annotate 1 and Review 2 to Annotate 2
And I click "Save"
Then the workflow "AUT_WF_13_Edit" should be saved successfully
When I edit the workflow "AUT_WF_13_Edit" and change template to "AUT_WF_Com_Temp_B"
And I set required annotators to "3"
And I rename nodes to "New_Ann" and "New_Rev"
And I click "Save"
Then the workflow "AUT_WF_13_Edit" should be updated successfully in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_14_Delete_WF_Start_Ann1_Rev1_Ann2_Rev2_Complete_Same.py

### Scenario: Prevent deletion of linked workflow Start -> Annotate 1 -> Review 1 -> Annotate 2 -> Review 2 -> Complete (Same Template)
```gherkin
Given I am logged in
When I create a project "AUT_WF_Project_14" linking dataset "AUT_WF_Com_Dataset" and workflow "AUT_WF_13_Edit"
And I navigate to the "Workflows" page
And I attempt to delete the linked workflow "AUT_WF_13_Edit"
Then I should see an error popup preventing deletion of the linked workflow
When I click "Cancel" on the delete confirmation popup
Then the workflow "AUT_WF_13_Edit" should remain in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_15_Edit_WF_Start_Ann1_Rev1_Ann2_Rev2_Complete_Diff.py

### Scenario: Create, edit, and update workflow Start -> Annotate 1 -> Review 1 -> Annotate 2 -> Review 2 -> Complete (Different Templates)
```gherkin
Given I am logged in and on the "Workflows" page
When I create a workflow "AUT_WF_15_Edit" with nodes ["Start", "Annotate", "Review", "Annotate", "Review", "Complete"]
And I apply template "AUT_WF_Com_Temp_A" to Annotate 1 and template "AUT_WF_Com_Temp_B" to Annotate 2
And I connect Review 1 to Annotate 1 and Review 2 to Annotate 2
And I click "Save"
Then the workflow "AUT_WF_15_Edit" should be saved successfully
When I edit the workflow "AUT_WF_15_Edit" and change template to "AUT_WF_Com_Temp_B"
And I set required annotators to "3"
And I rename nodes to "New_Ann" and "New_Rev"
And I click "Save"
Then the workflow "AUT_WF_15_Edit" should be updated successfully in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_16_Delete_WF_Start_Ann1_Rev1_Ann2_Rev2_Complete_Diff.py

### Scenario: Prevent deletion of linked workflow Start -> Annotate 1 -> Review 1 -> Annotate 2 -> Review 2 -> Complete (Different Templates)
```gherkin
Given I am logged in
When I create a project "AUT_WF_Project_16" linking dataset "AUT_WF_Com_Dataset" and workflow "AUT_WF_15_Edit"
And I navigate to the "Workflows" page
And I attempt to delete the linked workflow "AUT_WF_15_Edit"
Then I should see an error popup preventing deletion of the linked workflow
When I click "Cancel" on the delete confirmation popup
Then the workflow "AUT_WF_15_Edit" should remain in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_17_Edit_WF_Start_Ann_Consensus_Rev_Complete.py

### Scenario: Create, edit, and update workflow Start -> Annotate (Consensus Mode 2 Annotators) -> Review -> Complete
```gherkin
Given I am logged in and on the "Workflows" page
When I create a workflow "AUT_WF_17_Edit" with nodes ["Start", "Annotate", "Review", "Complete"]
And I apply template "AUT_WF_Com_Temp_A" to Annotate node 1
And I set required annotators to "2" (Consensus Mode)
And I connect Review 1 to Annotate 1
And I click "Save"
Then the workflow "AUT_WF_17_Edit" should be saved successfully
When I edit the workflow "AUT_WF_17_Edit" and change template to "AUT_WF_Com_Temp_B"
And I set required annotators to "3"
And I rename nodes to "New_Ann" and "New_Rev"
And I click "Save"
Then the workflow "AUT_WF_17_Edit" should be updated successfully in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_18_Delete_WF_Start_Ann_Consensus_Rev_Complete.py

### Scenario: Prevent deletion of linked workflow Start -> Annotate (Consensus Mode 2 Annotators) -> Review -> Complete
```gherkin
Given I am logged in
When I create a project "AUT_WF_Project_18" linking dataset "AUT_WF_Com_Dataset" and workflow "AUT_WF_17_Edit"
And I navigate to the "Workflows" page
And I attempt to delete the linked workflow "AUT_WF_17_Edit"
Then I should see an error popup preventing deletion of the linked workflow
When I click "Cancel" on the delete confirmation popup
Then the workflow "AUT_WF_17_Edit" should remain in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_19_Edit_WF_Start_Ann1_Ann2_Consensus_Rev_Complete.py

### Scenario: Create, edit, and update workflow Start -> Annotate 1 -> Annotate 2 (Consensus Mode 2 Annotators) -> Review -> Complete
```gherkin
Given I am logged in and on the "Workflows" page
When I create a workflow "AUT_WF_19_Edit" with nodes ["Start", "Annotate", "Annotate", "Review", "Complete"]
And I apply template "AUT_WF_Com_Temp_A" to Annotate 1 and Annotate 2
And I set required annotators to "2" for Annotate 2 (Consensus Mode)
And I connect Review 1 to Annotate 2
And I click "Save"
Then the workflow "AUT_WF_19_Edit" should be saved successfully
When I edit the workflow "AUT_WF_19_Edit" and change template to "AUT_WF_Com_Temp_B"
And I set required annotators to "3"
And I rename nodes to "New_Ann" and "New_Rev"
And I click "Save"
Then the workflow "AUT_WF_19_Edit" should be updated successfully in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_20_Delete_WF_Start_Ann1_Ann2_Consensus_Rev_Complete.py

### Scenario: Prevent deletion of linked workflow Start -> Annotate 1 -> Annotate 2 (Consensus Mode 2 Annotators) -> Review -> Complete
```gherkin
Given I am logged in
When I create a project "AUT_WF_Project_20" linking dataset "AUT_WF_Com_Dataset" and workflow "AUT_WF_19_Edit"
And I navigate to the "Workflows" page
And I attempt to delete the linked workflow "AUT_WF_19_Edit"
Then I should see an error popup preventing deletion of the linked workflow
When I click "Cancel" on the delete confirmation popup
Then the workflow "AUT_WF_19_Edit" should remain in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_21_Workflow_Save_Disabled_Without_Template.py

### Scenario: Save button disabled when template is not configured on annotate node
```gherkin
Given I am logged in and on the "Workflows" page
When I click "Create workflow" and enter name "AUT_WF_21_Unconfigured_Template_Save_Disabled"
And I add nodes ["Start", "Annotate", "Review", "Complete"]
And I connect the nodes without configuring any template on the Annotate node
Then the "Save" button should be in disabled mode
When I cancel or navigate away from the workflow editor
Then the workflow "AUT_WF_21_Unconfigured_Template_Save_Disabled" should NOT be created in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_22_Duplicate_Invalid_Workflow_Naming.py

### Scenario: Duplicate workflow name error validation
```gherkin
Given I am logged in and on the "Workflows" page
When I have an existing workflow "AUT_Workflow_Duplicate"
And I attempt to click "Create workflow" and enter the duplicate name "AUT_Workflow_Duplicate"
Then I should see an error message "A workflow with this name already exists"
When I click "Cancel" on the workflow creation modal
Then the creation modal should close without creating a duplicate workflow
```

### Scenario: Special character workflow name error validation
```gherkin
Given I am on the "Workflows" page
When I click "Create workflow" and enter a name with special characters "AUT_@$%%$_Workflow"
Then I should see an error message "Only letters, numbers, spaces, _ and - are allowed"
When I click "Cancel" on the workflow creation modal
Then the creation modal should close without creating the invalid workflow
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_23_Search_Workflow_Names.py

### Scenario: Search workflow names and handle non-existing search
```gherkin
Given I am logged in and on the "Workflows" page
When I enter an existing workflow name "AUT_WF_Search_Workflow" into the search bar
Then "AUT_WF_Search_Workflow" should be displayed in the search results
When I enter a non-existing workflow name "Checking_Workflow_Not_There" into the search bar
Then I should see a message "No workflows found"
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_24_Edit_Workflow_Functionality.py

### Scenario: Edit an existing workflow and save updates
```gherkin
Given I am logged in and on the "Workflows" page
When I have created a valid workflow "AUT_WF_24_Edit_Workflow"
And I click on the workflow "AUT_WF_24_Edit_Workflow"
Then the "Edit" button should be visible on the workflow details page
When I click the "Edit" button
And I modify the workflow by adding a node
And I click "Save"
Then I should see the workflow "AUT_WF_24_Edit_Workflow" updated successfully
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_25_Delete_Single_And_Bulk_Unlinked_Workflows.py

### Scenario: Single unlinked workflow deletion
```gherkin
Given I am logged in and on the "Workflows" page
When I create a single unlinked workflow "AUT_WF_Single_Delete"
And I select the checkbox for "AUT_WF_Single_Delete" and click "Delete"
Then the workflow "AUT_WF_Single_Delete" should be removed from the workflows list
```

### Scenario: Bulk unlinked workflow deletion
```gherkin
Given I am logged in and on the "Workflows" page
When I create 3 unlinked workflows ["AUT_WF_Bulk_Delete_01", "AUT_WF_Bulk_Delete_02", "AUT_WF_Bulk_Delete_03"]
And I select checkboxes for all 3 workflows and click "Delete"
Then all 3 workflows should be removed from the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_26_Prevent_Delete_Workflow_Linked_To_Project.py

### Scenario: Prevent deletion of a workflow linked to an active project
```gherkin
Given I am logged in
When I create a dataset "AUT_WF_Linked_Dataset_26" and template "AUT_WF_Linked_Temp_26"
And I create a workflow "AUT_WF_Linked_Workflow_26"
And I create a project "AUT_WF_Linked_Project_26" linking the dataset and workflow
And I navigate back to the "Workflows" page
And I attempt to delete the workflow "AUT_WF_Linked_Workflow_26"
Then I should see an error message "Cannot delete workflow linked to project"
And the workflow "AUT_WF_Linked_Workflow_26" should remain in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_27_Workflows_Pagination.py

### Scenario: Workflows pagination limits (5, 10, 20, 50) and persistence
```gherkin
Given I am logged in and on the "Workflows" page
When I select pagination option "5"
Then the displayed workflows count should be <= 5
When I create a new template and a new workflow "AUT_WF_Pagination_Workflow"
Then the displayed workflows count should remain <= 5
When I navigate to the "Datasets" page and return to the "Workflows" page
Then the pagination limit should persist as "5" and displayed workflows count should remain <= 5
When I select pagination option "10"
Then the displayed workflows count should be <= 10
When I select pagination option "20"
Then the displayed workflows count should be <= 20
When I select pagination option "50"
Then the displayed workflows count should be <= 50
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_28_Annotation_Review_QueryName.py

### Scenario: Incomplete workflow save with Annotation & Review selection does not persist workflow
```gherkin
Given I am logged in and on the "Workflows" page
When I click "Create workflow" and enter name "DROP"
And I select the "Annotation & Review" radio button option
And I apply template "AUT_WF_Linked_Temp_26" to Annotate node without connecting nodes
And I click "Save"
Then navigating to the "Workflows" page should confirm the workflow "DROP" is NOT created in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_29_Valid_Annotation_Review_Option.py

### Scenario: Create workflow with Annotation & Review radio selection option
```gherkin
Given I am logged in and on the "Workflows" page
When I click "Create workflow" and enter name "AUT_WF_Ann_Rev_Radio"
And I select the "Annotation & Review" radio button option
And I apply template "AUT_WF_Com_Temp_A" to Annotate node
And I click "Save"
Then the workflow "AUT_WF_Ann_Rev_Radio" should be saved and created successfully in the workflows list
```

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TC_30_Linked_Workflow_Edit_Disabled.py

### Scenario: Verify Edit button is not visible for a workflow linked to an active project
```gherkin
Given I am logged in
When I create a workflow "AUT_WF_30_Linked_Workflow" and save it
And I create a project "AUT_WF_Project_30" linking dataset "AUT_WF_Com_Dataset" and workflow "AUT_WF_30_Linked_Workflow"
And I navigate to the "Workflows" page
And I click on the workflow name "AUT_WF_30_Linked_Workflow"
Then the "Edit" button should NOT be visible on the workflow details page
```
