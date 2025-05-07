# MongoDB AppSync App

This repository contains a way to interact with the data residing in your MongoDB cluster with a managed GraphQL API backed by AWS AppSync

### Overview

This project leverages the Serverless Application Model (SAM) to deploy a serverless application in your AWS account. It utilizes AWS Lambda as a serverless function that contains the logic to interact with your MongoDB cluster. In addition to the lambda function, you will have to setup an AppSync API from the AWS Console that you will use on top of the lambda function to query your data in MongoDB.

The deployed lambda function will offer you the following operations to interact with your data residing in MongoDB:
1. findOne
2. find
3. insertOne
4. insertMany
5. updateOne
6. updateMany
7. deleteOne
8. deleteMany
9. aggregate

### Steps for deployment 

#### 1) Deploy the SAM App

1) In your AWS account, go the [Lambda](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions) console. Click on the **Applications** section present on the right

![alt text](<images/Lambda_Applications.png>)

2) Click on **Create Application** present on the top right.

![alt text](<images/Create_Application.png>)

3) Select **Serverless application**

![alt text](<images/Serverless_Applications.png>)

4) Search for **MongoDB-AppSync-App** in the search bar and check the box that says *Show apps that create custom IAM roles or resource policies*. Select the application highlighted.

![alt text](<images/AppSync_App.png>)

5) Enter the name of the application, your MongoDB Atlas Cluster Connection Endpoint then check the acknowledgement box and click on **Deploy**.

![alt text](<images/App_Deployment_1.png>)

After you click on **Deploy**, AWS will initiate a cloudformation stack which will create a lambda function in your AWS account.

6) Check the **Outputs** section in your cloudformation stack, you will find the following artifacts:

![alt text](/images/CF_Outputs.png)

### Test the deployed API

There are 2 ways in which you can test the deployed AppSync API with Lambda resolver as a data source:
#### 1) Test the API directly from the "Queries" section present in the AWS AppSync console.

The API request and response payloads maintain the structure previously used by [DataAPI](https://www.mongodb.com/docs/atlas/app-services/data-api/openapi)
If you plan to test your queries from the AppSync console then refer the following sample queries [here](/QUERIES.md).

#### 2) Import the [Postman](/postman.json) collection in your Postman app and perform the testing in Postman.