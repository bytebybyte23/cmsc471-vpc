Feature: Image Upload to Inbox
  As a user
  I want to upload images to the inbox
  So that they can be processed by the transcription workflow

  Scenario: Upload an image successfully
    Given the API is running at the Prod stage
    When I POST an image to /api/inbox with key 'test.jpg'
    Then the response status code must be 201
    And the response body must contain 'uploaded successfully'
    And the image must exist in the InboxBucket S3 bucket

  Scenario: List inbox files
    Given the API is running at the Prod stage
    And at least one image has been uploaded
    When I GET /api/inbox
    Then the response status code must be 200
    And the response body must contain an 'items' array

  Scenario: Delete an inbox file
    Given the API is running at the Prod stage
    And a file 'test.jpg' exists in the inbox
    When I DELETE /api/inbox/test.jpg
    Then the response status code must be 200
    And 'test.jpg' must no longer exist in the InboxBucket
