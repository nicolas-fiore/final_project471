Feature: Poll job status and manage processed records
  Background:
    Given an image processing application
    And a DynamoDB jobs table
    And an API Gateway connected to Lambda functions

  Scenario: Successfully poll a job status
    Given a jobID exists in the request path
    When L_POLL is invoked through GET /api/jobs/{jobID}
    Then it reads the job from the DynamoDB jobs table
    And it returns the jobID, status, and message
    And it includes CORS headers in the response

  Scenario: Successfully load processed records
    Given processed records exist for completed image jobs
    When the records page calls GET /api/records
    Then the records are returned as JSON
    And index.html displays the records in the records table

  Scenario: Successfully delete a processed record
    Given a processed record exists in the records table
    When the user clicks the delete button for that record
    Then DELETE /api/records/{id} is called
    And the records table reloads without the deleted record

  Scenario: Replace Aurora with DynamoDB storage
    Given the learner lab does not allow Aurora DB cluster creation
    When the database dependency is updated
    Then the application uses DynamoDB as the storage solution