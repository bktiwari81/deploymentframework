import boto3
import json
import os
REGION = 'us-west-2' # region to launch instance.
AMI = 'ami-013552adb20de7566'
    # matching region/setup amazon linux ami, as per:
    # https://aws.amazon.com/amazon-linux-ami/
INSTANCE_TYPE = 't2.micro' # instance type to launch.

EC2 = boto3.client('ec2', region_name=REGION)

def msDeployHandler(event, context):
    """ Lambda handler taking [message] and creating a httpd instance with an echo. """
    # message = event['message']
    for key in event:
        print(key)
    print("body:::"+event['body'])
    body=event['body']
    json_object = json.loads(body)
    gitURL=""
    isNew=""
    isServerless=""
    gitusername = os.environ['gitusername']
    gitpassword = os.environ['gitpassword']
    #print("giturl"+json_object.gitURL)
    for (k, v) in json_object.items():
        print("Key: " + k)
        print("Value: " + str(v))
        if(k=='gitURL'):
            gitURL= str(v)
        elif (k=='isNew'):
            isNew= str(v)
        elif (k=='isServerless'):
            isServerless= str(v)
    startindex = gitURL.rindex("/")+1
    endindex = len(gitURL)-4
    projectname = gitURL [startindex:endindex]
    gitCheckinUrlprefix = "https://"+gitusername +":"+gitpassword+"@"
    gitCheckinUrl=gitURL
    gitCheckinUrl = gitCheckinUrl.replace("https://",gitCheckinUrlprefix)
    
    
    # bash script to run:
    #  - update and install httpd (a webserver)
    #  - start the webserver
    #  - create a webpage with the provided message.
    #  - set to shutdown the instance in 10 minutes.
    init_script = """#!/bin/bash
        exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
        echo BEGIN
        sudo yum update -y
        cd /home/ec2-user
        git clone """+gitURL+"""
        cd """+projectname+"""
        npm install claudia-api-builder --save
        npm install -g claudia
        if [ """+isNew+""" == true ]; then 
            exec > >(tee /var/log/serviceDetails.log|logger -t serviceDetails -s 2>/var/log/user-data.log) 2>&1
            echo BEGIN
            claudia create --timeout 10 --region us-west-2 --api-module src/app
            git add . 
            git commit -m "claudia file" 
            git push """+gitCheckinUrl+"""
            cd /var/log
            aws sns publish --topic-arn arn:aws:sns:us-west-2:207236964171:DeploymentFrameworkNotify --message file://serviceDetails.log --subject "service details logs"
        else 
            exec > >(tee /var/log/serviceDetails.log|logger -t serviceDetails -s 2>/var/log/user-data.log) 2>&1
            echo BEGIN
            claudia update --timeout 10
            cd /var/log
            aws sns publish --topic-arn arn:aws:sns:us-west-2:207236964171:DeploymentFrameworkNotify --message file://serviceDetails.log --subject "service details logs"
        fi
        echo END
        aws sns publish --topic-arn arn:aws:sns:us-west-2:207236964171:DeploymentFrameworkLog --message file://user-data.log --subject "user data log"
        shutdown -h +30"""

    print ("Running script:")
    print (init_script)
    
    #claudia create --timeout 10 --region us-west-2 --api-module src/app
    
    instance = EC2.run_instances(
        ImageId=AMI,
        InstanceType=INSTANCE_TYPE,
        MinCount=1, # required by boto, even though it's kinda obvious.
        MaxCount=1,
        KeyName='ECKyePair',
        InstanceInitiatedShutdownBehavior='terminate', # make shutdown in script terminate ec2
        UserData=init_script # file to run on instance init.
    )

    print ("New instance created.")
    instance_id = instance['Instances'][0]['InstanceId']
    print (instance_id) 
    return {
        "statusCode": 200,
        "body": json.dumps('your Api configuration is complete, please check your email for deploymeent status and information!!')
    }
