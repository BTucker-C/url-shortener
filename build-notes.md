# Day 1 — Cloud Resume Project Setup

## Initialize Project Structure
    Local Development
        Created project folder: Cloud-Resume-Project
            \Serves as the root directory for all project files.

        Initialized Git repository
            \Enables version control and tracking of changes.

        Connected local repo to GitHub
            \Allows remote storage and collaboration.

        Created initial file structure
            \Includes index.html, style.css, and script.js.

---

## Create Basic Resume Page
    Frontend
        Built initial HTML resume page
            \Provides the base structure for displaying resume content.

        Added basic CSS styling
            \Improves readability and layout.

        Structured content sections
            \Includes header, experience, and projects.

---

## Setup S3 Hosting
    S3 Hosting
        Created an S3 Bucket: brandon-tucker-resume in us-east-2
            \Bucket used to host static website objects.

        Enabled static website hosting
            \Configured index.html as the root document.

        Configured bucket policy
            \Allowed public read access using s3:GetObject so browsers can retrieve site files.

---

## Setup CloudFront Distribution
    CloudFront CDN
        Configured S3 bucket as origin
            \Allows CloudFront to serve content securely.

        Set default root object
            \Configured index.html for root requests.

        Enabled HTTPS delivery
            \Provides secure access via SSL/TLS.

        Deployed CloudFront distribution
            \Makes site globally accessible with caching.

---

## Configure Custom Domain
    Domain & DNS
        Registered domain via Route 53: brandon-tucker.com
            \Provides a custom domain for the project.

        Created hosted zone
            \Manages DNS records for the domain.

        Requested SSL certificate via ACM
            \Enables HTTPS for custom domain.

        Validated certificate using DNS
            \Ensures domain ownership.

        Created Route 53 records
            \Mapped domain to CloudFront distribution.


# Day 2 — URL Shortener Project

## Setup API Gateway
    API Gateway
        Created HTTP API for URL shortener service in us-east-2
            \Serves as the entry point for all frontend and redirect requests.

        Defined POST /shorten route
            \Handles incoming requests to create shortened URLs.

        Defined GET /{short_id} route
            \Handles redirect requests by passing short_id to Lambda.

        Configured CORS via Terraform
            \Allows browser-based frontend to communicate with API without cross-origin errors.

## Setup Lambda Function
    Lambda
        Created Lambda function to handle URL creation and redirection
            \Acts as the core application logic layer.

        Implemented POST logic
            \Parses incoming URL, generates short ID, and stores mapping in DynamoDB.

        Implemented GET logic
            \Retrieves original URL from DynamoDB and returns HTTP 302 redirect.

        Added URL normalization
            \Ensures inputs like "google.com" are converted to valid URLs (https://google.com).

        Returned structured API responses
            \Provides JSON responses for POST and proper redirect headers for GET.

## Setup DynamoDB
    DynamoDB
        Created table: url-shortener-links
            \Stores mapping between short_id and original_url.

        Configured partition key: short_id
            \Allows fast lookup for redirect requests.

        Integrated with Lambda (PutItem / GetItem)
            \Enables persistent storage and retrieval of URLs.

## Configure IAM Permissions
    IAM
        Created Lambda execution role
            \Defines permissions for Lambda to interact with AWS services.

        Added DynamoDB permissions (PutItem, GetItem)
            \Allows Lambda to store and retrieve URL mappings.

        Added CloudWatch logging permissions
            \Enables debugging and monitoring via logs.

        Corrected misuse of assume_role_policy
            \Separated trust relationship from permission policies.

## Infrastructure as Code (Terraform)
    Terraform
        Defined API Gateway, Lambda, DynamoDB, and IAM resources
            \Automates infrastructure deployment and ensures consistency.

        Added GET redirect route
            \Enabled full URL redirection functionality.

        Managed Lambda deployment via zip and source_code_hash
            \Ensures updates are detected and deployed correctly.

        Resolved Terraform drift issues
            \Identified that manual AWS changes (CORS, routes) were overwritten by Terraform.

## Build Frontend
    Frontend (HTML/JavaScript)
        Created simple UI for submitting URLs
            \Allows user interaction with API.

        Integrated fetch() POST request to API Gateway
            \Sends URL data to backend service.

        Displayed returned short URL as clickable link
            \Provides immediate feedback and usability.

        Debugged browser issues (file:// vs localhost)
            \Resolved fetch failures by serving frontend via local HTTP server.

## Enable CORS
    API Gateway / Lambda
        Configured CORS in API Gateway via Terraform
            \Ensures browser requests succeed with proper headers.

        Handled preflight OPTIONS requests
            \Prevents browser blocking due to missing CORS configuration.

## Implement Redirect Logic
    Redirect Flow
        Extracted short_id from path parameters
            \Allows dynamic routing based on URL.

        Queried DynamoDB for matching record
            \Retrieves original URL for redirect.

        Returned HTTP 302 with Location header
            \Redirects user to original destination.

## Deploy Frontend
    S3 + CloudFront
        Created S3 bucket for frontend hosting
            \Hosts static HTML/JS for URL shortener UI.

        Configured bucket policy for public access
            \Allows browser access to frontend files.

        Created CloudFront distribution
            \Provides HTTPS and global CDN delivery.

        Set default root object (index.html)
            \Ensures site loads correctly at root URL.

## Configure Custom Domains
    Route 53 / ACM / API Gateway
        Created subdomains:
            \short.brandon-tucker.com (frontend)
            \go.brandon-tucker.com (redirect service)

        Requested ACM certificates in correct regions
            \us-east-1 for CloudFront, us-east-2 for API Gateway.

        Configured API Gateway custom domain
            \Mapped go.brandon-tucker.com to backend API.

        Created Route 53 alias records
            \Directed traffic to CloudFront and API Gateway.

        Updated Lambda to return branded short URLs
            \Ensures generated links use go.brandon-tucker.com.

## Outcome
    Fully functional serverless URL shortener
        \Users can create short links and be redirected to original URLs.

    Publicly accessible frontend and API
        \Application is live and usable via custom domains.

    End-to-end architecture completed
        \Frontend → API Gateway → Lambda → DynamoDB → redirect.

## Request Flow
    Create URL
        User → Frontend → API Gateway (POST /shorten)
        → Lambda → DynamoDB (store)
        → Response (short URL returned)

    Use Short URL
        User → go.brandon-tucker.com/{short_id}
        → API Gateway → Lambda
        → DynamoDB (lookup)
        → HTTP 302 → Original URL

# Day 3 — Resume Integration & Deployment Polish

## Refine Resume Content
    Resume Site
        Added Serverless URL Shortener project to Projects section
            \Expands portfolio to include backend/API-focused system.

        Structured project to match existing formatting
            \Maintains visual and structural consistency across projects.

        Highlighted core architecture components
            \Emphasized API Gateway, Lambda, and DynamoDB as primary system components.

        Included live demo link
            \Provides direct access to working application for recruiters.

        Adjusted wording for stronger impact
            \Shifted language from descriptive to outcome-driven phrasing.

---

## Improve Project Alignment
    Resume Strategy
        Balanced Cloud Resume and URL Shortener projects
            \Ensures both projects present at the same engineering depth.

        Refined Cloud Resume phrasing
            \Improved wording to emphasize design and deployment over configuration steps.

        Established full-stack cloud narrative
            \Frontend (Cloud Resume) + Backend (URL Shortener)

---

## Deploy Resume Updates
    Deployment
        Used Git-based workflow for deployment
            \Push triggers automated deployment via GitHub Actions.

        Verified CI/CD pipeline execution
            \Ensures changes are automatically uploaded to S3.

        Confirmed CloudFront cache refresh
            \Validated that updated content appears on live site.

        Tested live resume site
            \Verified project section displays correctly and links function.

---

## Validate Live Applications
    End-to-End Testing
        Confirmed frontend URL shortener functionality
            \short.brandon-tucker.com successfully creates short links.

        Verified redirect domain behavior
            \go.brandon-tucker.com correctly resolves and redirects.

        Ensured consistency between frontend and backend
            \Generated links match custom domain configuration.

---

## Final Architecture Review
    System Overview
        Frontend
            \CloudFront + S3 serving static resume and shortener UI.

        Backend
            \API Gateway + Lambda handling URL creation and redirects.

        Database
            \DynamoDB storing URL mappings.

        DNS & TLS
            \Route 53 + ACM managing domains and HTTPS certificates.

---

## Outcome
    Resume Site Enhanced
        \Now showcases multiple real-world AWS projects.

    Portfolio Strength Increased
        \Demonstrates both frontend delivery and backend API design.

    Deployment Workflow Established
        \Uses CI/CD pipeline for repeatable updates.

    Production-Ready Architecture
        \Custom domains, HTTPS, and global CDN fully implemented.
