# deploymentframework
This repo has a actual Python code developed and exposed as Lamda function.


# FAQ
**Q: What does this framework do?**

This framework intents to provide a feature that will expose a microservice on serverless or dedicated infrastructure with just a click of a button. 
This framework is exposed as REST API which can be triggered by any RESTful client with the minimum information required.

**Q: What are the use-cases framework is supporting currently?**

This is currently supporting migrating existing microservice to serverless infrastructure. 

**Q: Are you planning to enhance this framework?**

Yes.

**Q: What other use-cases are you planning to implement?**

We are planning to entend this framework for the following use-cases
1. Migrating existing microservices to dedicated infrastructure.
2. Add the capability to expose mock service as a lambda function from API specification e.g. swagger

**Q: What are the prerequisite before running this framework?**

1. Custom EC2 image 
2. SNS topics need to be configured and subscribed        
	1. DeploymentFrameworkNotify - microservice endpoint details 
	2. DeploymentFrameworkLog - lambda execution complete log   

**Q: How can we run this from scratch?**

1. Create a custom EC2 image that should have all the required software and configuration           
	1. Launch EC2 instance
	2. Install Git and Node
	3. Setup your AWS credentials using AWS configure 
	4. Create a private custom image 
	5. Add permissions 
	
2. Create a Lambda function           
	1. Go to AWS Lambda service and create Lambda function
	2. Select runtime as Python 3.8
	3. Add handler name as lambda_function.msDeployHandler 
	4. Copy content from msDeployHandler.py and paste it into your Lambda function 
	5. Create two environment variable `gitusername` and `gitpassword` for git configuration and set your git repo credentials 

2. Add API Gateway to expose Lambda as REST API           
	1. Go to AWS Lambda service
	2. Click onto you Lambda function
	3. Create API gateway trigger as REST - This will give API gateway endpooint that you can use to trigger your lambda function 

**Q: What all AWS services is this framework using?**

1. Lambda
2. API Gateway
3. EC2
4. IAM
5. SNS
