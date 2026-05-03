By: 
* Nicolas Fiore
* Cullan Evans

# System Overview
The application is a serverless image processing platform that uses API Gateway as the public entry point. A static website is served from S3 via a Lambda function, while API requests are routed through dedicated Lambda handlers for inbox management, job submission, polling, and result retrieval.

Incoming files are stored in an S3 inbox bucket. A submit Lambda starts a Step Functions workflow, which coordinates three worker Lambdas: L1 fetches the image from S3, L2 calls Amazon Textract for OCR, and L3 saves the results into Aurora and DynamoDB. CloudWatch provides observability for the Step Functions workflow.

## Diagram
```mermaid
graph TD
    User[User brower] --> APIG[API Gateway\nPublic Entry Point]


    APIG -->|GET /| L0[Lambda\nFetch and Return index.html]

    APIG -->|GET POST DELETE /api/inbox| LInbox[Lambda\nManage S3 inbox files]

    APIG -->|POST /api/jobs| LSubmit[Lambda\nstartExecution]
    APIG -->|GET /api/jobs/jobId| LPoll[Lambda\nPoll job status]

    APIG -->|GET DELETE /api/records| LRecords[Lambda\nFetch and delete Results]



    L0 -.-> S3Web[S3 Bucket\nindex.html, JS, CSS]

    Linbox -.-> S3Store[S3 Bucket\nInbox images]
    LSubmit -->|startExecution| SF
    LPoll -.->DDB[DynamoDb\nJob State and metadata]
    LRecords -.-> Aurora[Aurora RDS\nResults]

   

    subgraph Serverless[Serverless Domain]
        SF[Step Functions State Machine]
       

         SF --> L1[Lambda\nFetch image from S3]
        SF --> L2[Lambda\nCall Textract]
        SF --> L3[Lambda\nSave Results]
        L2 -.-> Textract[Amazon Textract\nReplaces Bedrock]
    end

   
    L1 -.-> S3Store
    L3 -.-> Aurora
    L3 -.-> DDB

   
    CW[CloudWatch] -.-> SF
```
# DevOps 

![Devops](./pics/dev.png)

## Gherkin
Nicolas Fiore: 
@import "./image.feature"
Cullan Evans: 
@import "./poll.feature"
# Well Architected Questions
1. Operational Excellence
    Fiore: Monitor with CloudWatch and keep deployment repeatable with SAM.  
    Evans: Use DevOps user stories, linked GitHub commits, and Gherkin feature files to track work clearly from planning to implementation.
    
2. Security
    Fiore: Use least-privilege IAM and encrypt data at rest.  
    Evans: Restrict API Gateway routes, protect S3 buckets from public access, and require MFA on AWS root account
    
4. Reliability
    Fiore: Add retries, backups, and alarms for failures.  
    Evans: Use DynamoDB job status tracking so failed image processing steps can be identified and rerun.
   
6. Performance
    Fiore: Use serverless scaling and keep functions small.  
    Evans: Split the workflow into separate Lambda functions so tasks like fetching images and saving results run independently.
    
8. Cost Optimization
    Fiore: Use pay-per-request services and remove unused resources.  
    Evans: Use S3, Lambda, and DynamoDB only when processing jobs are needed. This keeps the monthly cost lower.

# Security, Access, and Recovery
- Apply least-privilege IAM so each Lambda only accesses the S3 bucket, DynamoDB table, or Step Functions execution it needs.
- Encrypt data at rest for S3 and DynamoDB using AWS-managed or customer-managed KMS keys.
- Restrict API Gateway to only allowed routes and methods, and avoid exposing any extra public endpoints.
- Limit Step Functions access so only the submit Lambda and trusted roles can start executions.
- For recovery, enable S3 versioning, use DynamoDB point-in-time recovery, and keep database snapshots for results storage.
- Monitor issues with CloudWatch alarms and use retries or dead-letter queues for Lambda and workflow failures.

# Trusted Advisor
![trusted](./pics/advisor.png)

# TCO 
* Estimated Cost: $2.00 A Month

# Template.yaml
@import "./template.yaml"

# Website Picture
![website](./pics/website.png)
