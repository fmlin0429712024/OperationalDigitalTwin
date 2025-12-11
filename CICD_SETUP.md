# CI/CD Setup Instructions

To enable the Automated Deployment pipeline (`.github/workflows/firebase-deploy.yml`), you must perform these one-time setup steps in Google Cloud and GitHub.

## 1. Google Cloud Setup
1.  Go to the [Google Cloud Console](https://console.cloud.google.com/) for project `prescientdemos`.
2.  **Enable APIs**: Search for and enable:
    *   **Cloud Run Admin API**
    *   **Cloud Build API**
    *   **Artifact Registry API** (or Container Registry)
3.  **Create Service Account**:
    *   Go to **IAM & Admin** > **Service Accounts**.
    *   Create a new account (e.g., `github-deployer`).
    *   Grant the following roles:
        *   `Cloud Run Admin`
        *   `Service Account User`
        *   `Storage Admin` (for building images)
        *   `Firebase Admin`
    *   **Keys**: Click the Service Account > **Keys** tab > **Add Key** > **Create new key** (JSON).
    *   **Download** or copy the content of this JSON file.

## 2. GitHub Setup
1.  Go to your Repository Settings on GitHub.
2.  Navigate to **Secrets and variables** > **Actions**.
3.  Click **New repository secret**.
4.  **Name**: `GCP_SA_KEY`
5.  **Value**: Paste the entire content of the JSON key you downloaded in Step 1.
6.  Save `GCP_SA_KEY`.

## 3. Trigger Deployment
Simply push a change to the `main` branch:

```bash
git add .
git commit -m "Enable CI/CD"
git push
```

## 4. Where is my App?
Once the Action completes (check the "Actions" tab in GitHub), your app will be live at acts:
`https://prescientdemos.web.app`

*(Note: The Simulator script runs on your laptop/Edge device. The Web App simply visualizes the data it receives.)*
