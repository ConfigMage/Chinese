# Google Sheets Setup Instructions

To enable persistent data storage across sessions, you need to set up Google Sheets API credentials.

## Steps to Set Up Google Sheets Integration:

### 1. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API for your project

### 2. Create Service Account Credentials
1. In Google Cloud Console, go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the service account details
4. Click "Create and Continue"
5. Skip the optional permissions (click "Continue")
6. Click "Done"

### 3. Generate JSON Key
1. Find your new service account in the credentials list
2. Click on the service account email
3. Go to the "Keys" tab
4. Click "Add Key" > "Create new key"
5. Choose "JSON" format
6. Download the JSON file

### 4. Set Up Streamlit Secrets
1. In your Streamlit app settings (on Streamlit Cloud):
   - Go to Settings > Secrets
   - Add a new secret called `gcp_service_account`
   - Copy the entire contents of your JSON key file into this secret

Example format in Streamlit secrets:
```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

### 5. For Local Development
Create a `.streamlit/secrets.toml` file in your project directory with the same format as above.

## How It Works
- The app will automatically create a Google Sheet called "Chinese Dinner Votes"
- All votes are saved to this sheet in real-time
- Data persists across all sessions and users
- The sheet is automatically shared for read-only access

## Fallback
If Google Sheets is not configured, the app will still work but data will only persist within each session.