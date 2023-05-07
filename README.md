## Step-by-step to deploy the docker container on GCP:
1. Create new project in GCP and activate Cloud Run API and Cloud Build API
2. Initialize Google Cloud CLI (gcloud init). To do this, you must first install gcloud CLI by following the instruction on the [link](https://cloud.google.com/sdk/docs/install)
3. Run the following command and replace PROJECT_ID to your project id on GCP, `gcloud config set project PROJECT_ID`
4. Use command `gcloud run deploy`
    1. When you are prompted for the source code location, press Enter to deploy the current folder.
    2. When you are prompted for the service name, press Enter to accept the default name, for example helloworld.
    3. If you are prompted to enable the Artifact Registry API or to allow creation of Artifact Registry repository, respond by pressing `y`.
    4. When you are prompted for region: select the region of your choice, for example us-central1.
    5 You will be prompted to allow unauthenticated invocations: respond `y`
5. Visit the deployed service. You can check the service on GCP by using cloud run feature.
---
Resource:
- https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service
- https://www.youtube.com/watch?v=vieoHqt7pxo 
