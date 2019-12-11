# deploymentframework
This repo has a actual Python code developed and exposed as Lamda function.


# FAQ
Q: What does this framework do?

This framework intents to provide a feature that will expose a microservice on serverless or dedicated infrastructure with just a click of a button. 
This framework is exposed as REST API which can be triggered by any RESTful client with the minimum information required.

Q: What are the use-cases framework is supporting currently?

This is currently supporting migrating existing microservice to serverless infrastructure. 

Q: Are you planning to enhance this framework?

Yes.

Q: What other use-cases are you planning to implement?

We are planning to entend this framework for the following use-cases
1. Migrating existing microservices to dedicated infrastructure.
2. Add the capability to expose mock service as a lambda function from API specification e.g. swagger

Q: What are the prerequisite before running this framework?

1. Custom EC2 image 
2. SNS topics need to be configured and subscribed           
	a. DeploymentFrameworkNotify - microservice endpoint details 
	b. DeploymentFrameworkLog - lambda execution complete log   

Q: How can we run this from scratch?

1. Create a custom EC2 image that should have all the required software and configuration           
	a. Launch EC2 instance
	b. Install Git and Node
	c. Setup your AWS credentials using AWS configure 
	d. Create a private custom image 
	e. Add permissions 
	
2. Create a Lambda function
    a. Go to AWS Lambda service and create Lambda function
	b. Select runtime as Python 3.8
	c. Add handler name as lambda_function.msDeployHandler
	d. Copy content from msDeployHandler.py and paste it into your Lambda function
	e. Create two environment variable for git configuration and set your git repo credentials
		 gitusername
		 gitpassword

3. Add API Gateway as trigger 
    a. Go to AWS Lambda service
	b. Click onto you Lambda function
	c. Create API gateway trigger as REST - This will give API gateway endpooint that you can use to trigger your lambda function

Q: What all AWS services is this framework using?

1. Lambda
2. API Gateway
3. EC2
4. IAM
5. SNS



