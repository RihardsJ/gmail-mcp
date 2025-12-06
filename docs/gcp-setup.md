# GCP Setup

This guide will walk you through the process of setting up a Google Cloud Platform (GCP) project for the Gmail Model Context Protocol (MCP) server.

## Prerequisites

- [Google Cloud Platform Account](https://cloud.google.com/free)
- [gcloud](https://docs.cloud.google.com/sdk/docs/install-sdk)

## Create a new project

- Create a new GCP project: `gcloud projects create gmail-mcp-server`

## Setup and enable billing for the project

1. [Enable billing](https://cloud.google.com/billing/docs/how-to/modify-project)
2. Setup billing: `gcloud beta billing projects link gmail-mcp-server-480411 --billing-account=012345-6789AB-CDEF01` // 012345-6789AB-CDEF01 is an example billing account ID replace with your own billing account ID

## Check if billing is enabled on a project

- View billing status: `gcloud beta billing projects describe gmail-mcp-server-480411`

Example output:

```
billingAccountName: billingAccounts/012345-6789AB-CDEF01
billingEnabled: true
name: projects/gmail-mcp-server-12345
projectId: gmail-mcp-server-12345
```

## Enable Gmail API and setup OAuth client ID

1. Enable Gmail API: `gcloud services enable gmail.googleapis.com`
2. Check if Gmail API is enabled: `gcloud services list --enabled | grep gmail.googleapis.com`
3. Go to [APIs & Services](https://console.cloud.google.com/apis/dashboard?project=gmail-mcp-server-12345)
4. Create "external user type"
5. Fill in app information
6. Create OAuth client ID (choose "Web application")
7. Fill in redirect URI (or leave it blank and update after first deployment)
8. Download creadentails.json and sav it to your project
9. Navigate to [Data access] tab and add Gmail scopes: `gmail.readonly` and `gmail.compose`
