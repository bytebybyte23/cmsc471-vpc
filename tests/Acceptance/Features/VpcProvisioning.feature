Feature: VPC Infrastructure
  As a cloud architect
  I want a VPC with private subnets
  So that resources are isolated and secure

  Scenario: Verify VPC CIDR Block
    Given the SAM template is deployed
    When I describe the VPC resource
    Then the AWS::EC2::VPC must have CidrBlock '10.0.0.0/16'
    And DNS support must be enabled
    And DNS hostnames must be enabled

  Scenario: Verify Private Subnets exist
    Given the SAM template is deployed
    When I describe the subnet resources
    Then PrivateSubnet1 must have CidrBlock '10.0.1.0/24'
    And PrivateSubnet2 must have CidrBlock '10.0.2.0/24'
    And both subnets must be in different availability zones
