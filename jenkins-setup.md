# Simple Jenkins Setup

## Step 1: Test Locally First

Make sure your BrowserStack tests work:

```bash
# Set your credentials
export BROWSERSTACK_USERNAME=your_username
export BROWSERSTACK_ACCESS_KEY=your_access_key

# Run the test script
./test-pipeline-local.sh
```

## Step 2: Run Jenkins with Docker

```bash
# Start Jenkins
docker run -p 8080:8080 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts

# Get the admin password (wait 2 minutes for startup)
docker ps
docker exec [CONTAINER_ID] cat /var/jenkins_home/secrets/initialAdminPassword
```

## Step 3: Configure Jenkins

1. Open http://localhost:8080
2. Enter admin password
3. Install suggested plugins
4. Create admin user

## Step 4: Add BrowserStack Credentials

1. Go to **Manage Jenkins > Credentials > System > Global credentials**
2. Add **Username with password** credential:
   - Kind: Username with password
   - Username: your BrowserStack username
   - Password: your BrowserStack access key
   - ID: `browserstack-creds`

## Step 5: Create Pipeline Job

1. **New Item** > **Pipeline**
2. Name: `galaxy-s20-tests`
3. **Pipeline section**: 
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: your git repository URL (e.g., https://github.com/username/repo.git)
   - **Branch Specifier**: */master (or */main)
   - **Script Path**: `Jenkinsfile`
4. **Save** and **Build Now**

**Important**: Use "Pipeline script from SCM" not "Pipeline script" so Jenkins can automatically checkout your code!

## Step 6: View Results

- **Console Output**: See live build logs
- **Test Results**: JUnit test results
- **Test Results** link: View HTML report

That's it! Your pipeline will:
1. **Install dependencies** using uv (including dev tools)
2. **Run code quality checks** (Black formatting, Ruff linting, MyPy type checking)
3. **Execute BrowserStack tests** in parallel across 3 browsers
4. **Generate comprehensive reports** and archive artifacts 