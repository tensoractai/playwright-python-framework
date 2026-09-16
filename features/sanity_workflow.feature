Feature: Workflow Sanity Validation

Scenario: TC_A - Start Annotate Review Complete workflow

    Given I login as Company Admin
    When I create a dataset
    Then the dataset should be displayed

    When I upload 2 files to the dataset
    Then the uploaded files should be displayed

    When I create and upload a template
    Then the template should be displayed

    When I create a workflow
      | Node      |
      | Start     |
      | Annotate  |
      | Review    |
      | Complete  |
    And I connect the workflow nodes
    And I save the workflow
    Then the workflow should be displayed

    When I create a project using the dataset, template and workflow
    Then the project should be displayed

    When I assign the Annotator and Reviewer to the project
    Then their email IDs should be displayed

    When I login as Annotator
    And I open the project from Tasks
    Then the uploaded files should be displayed

    When I claim File 1
    And I enter the Annotator transcription
    Then the transcription should be displayed
    And I submit the task

    When I login as Reviewer
    And I open the project from Tasks
    And I open File 1
    Then the Annotator transcription should be displayed

    When I enter the Reviewer annotation
    And I approve the task

    When I login as Company Admin
    And I open the project
    Then File 1 should have Complete status


Scenario: TC_B - Start Annotate Review Annotate Review Complete workflow

    Given I login as Company Admin
    When I create a dataset
    Then the dataset should be displayed

    When I upload 2 files to the dataset
    Then the uploaded files should be displayed

    When I create and upload a template
    Then the template should be displayed

    When I create a workflow
      | Node      |
      | Start     |
      | Annotate  |
      | Review    |
      | Annotate  |
      | Review    |
      | Complete  |
    And I connect the workflow nodes
    And I save the workflow
    Then the workflow should be displayed

    When I create a project using the dataset, template and workflow
    Then the project should be displayed

    When I assign Annotator 1, Annotator 2 and Reviewer to the project
    Then their email IDs should be displayed

    When I login as Annotator 1
    And I open the project from Tasks
    Then the uploaded files should be displayed

    When I process File 1 with Annotator 1
    And I process File 2 with Annotator 1
    Then both files should contain Annotator 1 transcription

    When I login as Reviewer
    And I open the project from Tasks
    And I review File 1
    And I approve File 1
    And I review File 2
    And I approve File 2

    When I login as Annotator 2
    And I open the project from Tasks
    And I claim File 1
    Then the previous annotation should not be displayed
    When I enter Annotator 2 transcription
    Then the transcription should be displayed
    And I submit the task

    When I claim File 2
    Then the previous annotation should not be displayed
    When I enter Annotator 2 transcription
    Then the transcription should be displayed
    And I submit the task

    When I login as Reviewer
    And I review File 1
    And I approve File 1
    And I review File 2
    And I reject File 2
    And I submit the task

    When I login as Company Admin
    And I open the project
    Then File 1 should have Complete status
    And File 2 should have Rejected status


Scenario: TC_C - Two Annotators Consensus workflow

    Given I login as Company Admin
    When I create a dataset
    Then the dataset should be displayed

    When I upload 2 files to the dataset
    Then the uploaded files should be displayed

    When I create and upload a template
    Then the template should be displayed

    When I create a workflow
      | Node                |
      | Start               |
      | Annotate            |
      | Consensus = 2       |
      | Review              |
      | Complete            |
    And I configure the Annotate node with consensus 2
    And I connect the workflow nodes
    And I save the workflow
    Then the workflow should be displayed

    When I create a project using the dataset, template and workflow
    Then the project should be displayed

    When I assign Annotator 1, Annotator 2 and Reviewer to the project
    Then their email IDs should be displayed

    When I login as Annotator 1
    And I open the project from Tasks
    Then the uploaded files should be displayed
    When I annotate File 1 and File 2
    Then the Annotator 1 transcription should be displayed
    And I submit the task

    When I login as Annotator 2
    And I open the project from Tasks
    Then the uploaded files should be displayed
    When I annotate File 1 and File 2
    Then the Annotator 2 transcription should be displayed
    And I submit the task

    When I login as Reviewer
    And I open the project from Tasks
    And I open File 1
    Then Annotator 1 transcription should be displayed
    And Annotator 2 transcription should be displayed

    When I enter the Reviewer annotation
    And I approve the task

    When I login as Company Admin
    And I open the project
    Then File 1 should have Complete status