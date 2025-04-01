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

#### Steps for deployment 

##### 1) Deploy the SAM App

1) In your AWS account, go the [Lambda](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions) console. Click on the **Applications** section present on the right

![alt text](<images/Lambda_Applications.png>)

2) Click on **Create Application** present on the top right.

![alt text](<images/Create_Application.png>)

3) Select **Serverless application**

![alt text](<images/Serverless_Applications.png>)

4) Search for **MongoDB-AppSync-App** in the search bar and check the box that says *Show apps that create custom IAM roles or resource policies*. Select the application highlighted.

![alt text](<images/AppSync_App.png>)

5) Enter the name of the application, your MongoDB Atlas Cluster Connection Endpoint, Database name and Collection name then check the acknowledgement box and click on **Deploy**.

![alt text](<images/App_Deployment.png>)

After you click on **Deploy**, AWS will initiate a cloudformation stack which will create a lambda function in your AWS account.

##### 2) Create AppSync API

- [Create](https://docs.aws.amazon.com/appsync/latest/devguide/quickstart.html) an AppSync GraphQL API from the AppSync console.
- Select **“GraphQL APIs”** in the API type section and **“Design from scratch”** in the GraphQL API Data Source section then click on Next.
![alt text](/images/Create_AppSync_API.png)
- Enter the API name as per your preference and click on Next.
![alt text](/images/AppSync_API_Name.png)
- Select **“Create GraphQL resources later”** in the Create a GraphQL type section and click on Next.
![alt text](/images/Creat_GraphQL_resources_later.png)
- Review the selections made and click on **Create API**.
![alt text](/images/Review_Create_AppSync_API.png)
- Once the AppSync API gets created, click on the **“Schema”** section present on the left side and paste the following schema inside the code block and click on **“Save Schema”** present on top right:
    ```
    type Mutation {
        insertOne(input: AWSJSON!): AWSJSON
        insertMany(input: AWSJSON!): AWSJSON
        updateOne(input: AWSJSON!): AWSJSON
        updateMany(input: AWSJSON!): AWSJSON
        deleteOne(input: AWSJSON!): AWSJSON
        deleteMany(input: AWSJSON!): AWSJSON
    }

    type Query {
        findOne(input: AWSJSON!): AWSJSON
        find(input: AWSJSON!): AWSJSON
        aggregate(input: AWSJSON!): AWSJSON
    }
    ```
- Click on the **“Data Sources”** section present on the left side.
- Click on **“Create data source”**. Here, we will add the lambda function that we created earlier as a data source for this AppSync API.
- Enter the data source name as per your preference. Select **“AWS Lambda function”** in the Data source type dropdown. Select the **“Region”** where you have created your lambda function and then select the function searching by its name under the Function section. Click on Create
![alt text](/images/Create_Data_Source.png)
- Go back to the **“Schema”** section and under the Resolvers section you will see Mutation and Query. Click **“Attach”** button against any one of the Field(s).
![alt text](/images/Attach_Data_source.png)
- Select **“Velocity Template Language (VTL)”** under the Resolver Runtime in Additional Settings and choose the **data source name** from the dropdown in the Data Source section. Click on Create.
![alt text](/images/Attach_Resolver.png)
- After you attach the resolver, paste the following piece of code in Request and Response mapping templates and click on Save
    - Request Mapping Template - 
    ```
    #**
    The value of 'payload' after the template has been evaluated
    will be passed as the event to AWS Lambda.
    *#
    {
        "version" : "2017-02-28",
        "operation": "Invoke",
        "payload": {
            "method": "POST",
            "rawPath": "/insertOne",
            "body": $util.toJson($context.args.input)
        }
    }
    ```
    Note: You need to update the `rawPath` for the field to which you have attached the resolver. For example, since I attached the resolver to the `insertOne` field in my schema, my rawPath is set to `/insertOne`.

    - Response Mapping Template - 
    ```
    ## Parse the body JSON into an array
    #set($responseBody = $utils.parseJson($context.result.body))

    ## Return the user object
    #set($finalresponse = $util.toJson($responseBody))

    ## Return final response
    $finalresponse
    ```
- The provided Request and Response Mapping Templates can be applied to all AppSync Schema operations.

#### Test the deployed API

There are 2 ways in which you can test the deployed AppSync API with Lambda resolver as a data source:
1. Test the API directly from the "Queries" section present in the AWS AppSync console.
2. Import the [Postman](/postman.json) collection in your Postman app and perform the testing in Postman.