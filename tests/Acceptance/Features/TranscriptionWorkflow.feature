Feature: Transcription Workflow
  As a user
  I want to submit an image for transcription
  So that text is extracted and stored

  Scenario: Submit a transcription job
    Given the API is running at the Prod stage
    And an image 'test.jpg' exists in the inbox
    When I POST to /api/jobs with body '{"key": "test.jpg"}'
    Then the response status code must be 201
    And the response body must contain a 'jobId'
    And the job status must be 'PENDING'
    And a Step Functions execution must be started

  Scenario: Poll job status
    Given a job has been submitted with jobId 'abc-123'
    When I GET /api/jobs/abc-123
    Then the response status code must be 200
    And the response body must contain 'jobId' and 'status'

  Scenario: Job completes successfully
    Given an image with readable text has been submitted
    When the Step Functions state machine completes
    Then the job status in DynamoDB must be 'COMPLETED'
    And the results must contain extracted text lines
    And the updatedAt timestamp must be set

  Scenario: View transcription records
    Given at least one job has completed
    When I GET /api/records
    Then the response status code must be 200
    And the response body must contain a 'records' array
    And each record must have 'jobId', 'status', and 'results'
