HR Leave & Policy Assistant (HRLPA)
Overview

Tech Stack: Amazon S3, AWS Lambda, API Gateway, Python, HTML Form (Web Interface)

The HR Leave & Policy Assistant is a web-based automation tool that allows employees and HR personnel to query company policies and leave information in real-time using a simple browser form. The assistant reads HR documents stored in S3 and provides instant, document-driven answers via a web interface.

It leverages AWS cloud services and lightweight NLP to deliver secure and scalable responses to HR-related queries.

Architecture

Architecture Diagram (assests/hr_architecture_diagram.png )

[![Watch the demo](https://img.youtube.com/vi/pOrIa1mBbT8/0.jpg)](https://youtube.com/shorts/pOrIa1mBbT8?si=hZ5X98PByIdykljS)

Key Features

- Submit HR queries through a browser-based HTML form
- Fetch answers from structured HR documents stored in S3
- Provides instant, automated responses to employee questions
- Fully serverless and scalable (built on AWS)
- Secure integration via API Gateway
- JSON event testing support (for Lambda testing)

Premium / Planned Features:

- AI-powered natural language understanding for complex queries
- Multi-language support for diverse workforces
- Analytics & reporting dashboard for HR managers
- Integration with internal HR systems (future)

Tech Stack

- Python – Core Lambda function
- AWS S3 – Stores HR policy and leave documents
- AWS Lambda – Processes user queries and generates answers
- API Gateway – Exposes Lambda as a REST endpoint for web access

CloudWatch – Logging and monitoring

- HTML / Browser Form – User interface for submitting queries
- JSON Simulation – Offline testing during development
- Visual Studio Code – Code editor
- Terraform – Infrastructure as code for automated deployment 

Flow Description:

- User opens the HR Leave & Policy Assistant web page.
- The user submits a question via the HTML form.
- The form sends a POST request to the AWS API Gateway endpoint.
- API Gateway triggers the Lambda function.
- Lambda fetches the relevant HR document(s) from S3 and uses NLP to process the query.
- A structured response is generated and sent back to the browser.
- The user sees the answer instantly in the web form interface.

Business Value

- This project demonstrates how cloud automation can streamline HR operations:
- Employees get instant answers to policy questions without emailing HR
- HR teams save time on repetitive queries and reduce response delays
- Fully serverless design minimizes operational costs
- Scales easily across multiple departments or company locations

Note: Sensitive configuration such as S3 bucket names and environment variables have been removed from this public version. Employers or recruiters can request demo credentials if needed.

Why This Project Matters

The HR Leave & Policy Assistant addresses a common organizational challenge: repetitive HR queries that consume time and slow down operations.

Universal Use Case: Every company receives HR questions about policies and leave. This assistant automates answers in real-time.

End-to-End Automation: Demonstrates integration of AWS cloud services, serverless architecture, and a browser-based interface.

AI + Cloud + Automation: Combines lightweight NLP with serverless cloud architecture for practical HR automation.

Job-Ready & Client-Ready: Structured for real-world deployment with clear documentation, architecture, and testing workflows.

Security-Aware: Environment variables, S3 buckets, and endpoints follow best practices for production-ready applications.

Scalable & Monetizable: Serverless design allows scaling across multiple teams, with the potential for SaaS deployment.

Author

Valencia Lukhele
AI & Cloud Automation Engineer
Building scalable automation solutions for businesses