Feature: Health Check
  As a developer
  I want a health check endpoint
  So that I can verify the API is running

  Scenario: Health check returns status and timestamp
    Given the API is running at the Prod stage
    When I GET /api/health
    Then the response status code must be 200
    And the response body must contain 'status' equal to 'healthy'
    And the response body must contain a 'date' field
    And the response body must contain a 'time' field
