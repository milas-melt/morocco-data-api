# Documentation

Documentation is still work in progress ...

## Security

Our security considerations are listed below. Please feel free to point any constructive advice on how to improve the API security. Feel free to create a github issue for that.

### API Keys

We setup an API Key system for devs controlled with a DevUsagePlan to control traffic.

### Cognito User Pools

#### Overview

Amazon Cognito provides user identity and data synchronization services, allowing secure user sign-up, sign-in, and access control.

#### Usage

Best for APIs accessed by registered users where you need to handle user management and authentication.

#### How It Works

API Gateway can verify access tokens from a Cognito User Pool directly without needing a Lambda function.

### IAM Authorizers

#### Overview

IAM authorizers use AWS IAM permissions to control access to your API.

#### Usage

Suitable when both API consumers and the API itself are within the AWS ecosystem.

#### How It Works

Requests to your API must be signed using AWS Signature Version 4, and API Gateway verifies these signatures based on IAM policies.
