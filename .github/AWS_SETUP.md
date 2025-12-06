# AWS IAM Setup for CI/CD

## 1. Create IAM User for GitHub Actions

1. **Go to AWS Console → IAM → Users**
2. Click **"Create user"**
3. User name: `github-actions-deployer`
4. Click **Next**

## 2. Attach Permissions

Attach these policies to the user:
- ✅ `AWSElasticBeanstalkFullAccess` (for EB deployments)
- ✅ `AmazonS3FullAccess` (for uploading deployment packages)

Or create a custom policy (more secure):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "elasticbeanstalk:*",
        "s3:*",
        "ec2:DescribeInstances",
        "ec2:DescribeSecurityGroups",
        "autoscaling:DescribeAutoScalingGroups",
        "cloudformation:DescribeStacks",
        "cloudformation:DescribeStackResources"
      ],
      "Resource": "*"
    }
  ]
}
```

## 3. Create Access Keys

1. Click on the created user
2. Go to **"Security credentials"** tab
3. Scroll to **"Access keys"**
4. Click **"Create access key"**
5. Choose **"Third-party service"**
6. Click **Next** → **Create access key**
7. **SAVE THESE VALUES** (you'll need them for GitHub Secrets):
   - Access Key ID
   - Secret Access Key

## 4. Get AWS Account ID

Run in terminal:
```bash
aws sts get-caller-identity --query Account --output text
```

Or find it in AWS Console → Top right → Click account name → Account ID

---

# GitHub Secrets Setup

## 1. Go to Your GitHub Repository

Navigate to: `https://github.com/sunilverma231/End-to-end-Machine-Learning-Project-`

## 2. Add Secrets

1. Click **Settings** (top menu)
2. Click **Secrets and variables** → **Actions** (left sidebar)
3. Click **"New repository secret"**

Add these 3 secrets:

### Secret 1: AWS_ACCESS_KEY_ID
- Name: `AWS_ACCESS_KEY_ID`
- Value: `<Your Access Key ID from step 3>`

### Secret 2: AWS_SECRET_ACCESS_KEY
- Name: `AWS_SECRET_ACCESS_KEY`
- Value: `<Your Secret Access Key from step 3>`

### Secret 3: AWS_ACCOUNT_ID
- Name: `AWS_ACCOUNT_ID`
- Value: `<Your 12-digit AWS Account ID>`

---

# Testing the CI/CD Pipeline

## Method 1: Push to main branch
```bash
git add .github/workflows/deploy.yml .github/AWS_SETUP.md
git commit -m "feat: Add CI/CD pipeline with GitHub Actions"
git push origin main
```

## Method 2: Manual trigger
1. Go to GitHub → Actions tab
2. Click **"CI/CD Pipeline - Deploy to AWS Elastic Beanstalk"**
3. Click **"Run workflow"**
4. Select branch: `main`
5. Click **"Run workflow"**

---

# Monitoring Deployment

## GitHub Actions
- Go to: `https://github.com/sunilverma231/End-to-end-Machine-Learning-Project-/actions`
- Click on the latest workflow run
- Watch real-time logs for:
  - ✅ Tests
  - ✅ Build
  - ✅ S3 Upload
  - ✅ EB Deployment

## AWS Elastic Beanstalk
- Console → Elastic Beanstalk → Environments → studentperformanceenv1-env
- Watch **Events** tab for deployment progress
- Check **Health** tab for application status

---

# Rollback Strategy

If deployment fails:

```bash
# List recent versions
aws elasticbeanstalk describe-application-versions \
  --application-name studentperformanceenv1 \
  --max-records 5

# Rollback to previous version
aws elasticbeanstalk update-environment \
  --environment-name studentperformanceenv1-env \
  --version-label <PREVIOUS_VERSION_LABEL>
```

---

# Security Best Practices

✅ **DO:**
- Rotate access keys every 90 days
- Use least-privilege IAM policies
- Enable MFA on AWS account
- Monitor CloudTrail logs

❌ **DON'T:**
- Commit secrets to GitHub
- Share access keys via email/Slack
- Use root account credentials
- Give full admin access to CI/CD user
