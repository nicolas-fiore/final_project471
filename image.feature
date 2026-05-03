Feature: Image processing pipeline
  Background:
    Given an S3 bucket with an image file
    And a DynamoDB job table

  Scenario: Successfully process an image through the pipeline
    Given a job_id, filename, and bucket in the event
    When L1Fetch is invoked
    Then it returns a job_id and filename
    And L2Call receives the output
    When L2Call invokes Textract
    Then it returns extracted items
    And L3Save receives the items
    When L3Save stores results
    Then the job status is updated to COMPLETED