graph TD
    %% Edge & Network
    User[User] --> R53[Route 53 DNS]
    R53 --> CF[CloudFront]
    CF --> S3Web[S3 Static Site]
    CF --> ALB[Application Load Balancer]

    %% Compute (Tier 2)
    subgraph VPC [VPC - Public & Private Subnets]
        ALB --> ASG[EC2 Auto Scaling Group / Docker]
        ASG --> APIG[API Gateway]
    end

    %% Orchestration & Serverless (Tier 3)
    APIG --> SF[Step Functions State Machine]
    subgraph Serverless [Serverless Domain]
        SF --> L1[Lambda: Fetch Image S3]
        SF --> L2[Lambda: Invoke Bedrock]
        SF --> L3[Lambda: Save Results]
        L2 -.-> Bedrock[Amazon Bedrock AI]
    end

    %% Persistence (Tier 4)
    L1 -.-> S3Store[S3 Bucket: Images]
    S3Store -.-> Glacier[S3 Glacier: Archival Compliance]
    L3 -.-> Aurora[Aurora RDS: Relational Data]
    L3 -.-> DDB[DynamoDB: Job State/Metadata]
    
    %% Analytics & Storage concepts
    Aurora -.-> Redshift[(Redshift: Analytics Mention)]
    ASG -.-> EFS[EFS: Shared EC2 Storage]

    %% Monitoring
    CW[CloudWatch / Trusted Advisor] -.-> VPC
    CW -.-> Serverless