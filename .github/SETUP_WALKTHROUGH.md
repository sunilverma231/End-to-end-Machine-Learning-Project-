# 🚀 Step-by-Step CI/CD Setup Guide

**Time Required:** 10-15 minutes  
**Goal:** Enable automated deployments from GitHub to AWS

---

## ✅ Prerequisites Checklist

Before starting, make sure you have:
- [ ] AWS Account (with console access)
- [ ] GitHub Account (repository owner/admin access)
- [ ] Browser open with both AWS and GitHub

---

## Part 1: AWS Setup (Create IAM User)

### Step 1: Login to AWS Console

1. Open browser and go to: https://aws.amazon.com/console/
2. Click **"Sign In to the Console"**
3. Enter your AWS credentials
4. You should see the AWS Management Console dashboard

---

### Step 2: Navigate to IAM

**Option A - Search Method:**
1. At the top of AWS Console, find the search bar
2. Type `IAM`
3. Click on **"IAM"** (Identity and Access Management)

**Option B - Services Menu:**
1. Click **"Services"** in top-left
2. Under "Security, Identity, & Compliance"
3. Click **"IAM"**

You should now see the IAM Dashboard.

---

### Step 3: Create New IAM User

1. On the left sidebar, click **"Users"**
2. Click the orange **"Create user"** button (top-right)
3. You'll see "Specify user details" page

**Fill in the form:**
```
User name: github-actions-deployer
```

4. **DO NOT** check "Provide user access to AWS Management Console" (leave unchecked)
5. Click **"Next"** button at bottom

---

### Step 4: Set Permissions

You're now on "Set permissions" page.

**Method 1 - Quick (Using AWS Managed Policies):**

1. Select **"Attach policies directly"** option
2. In the search box, type: `ElasticBeanstalk`
3. Find and **CHECK** the box for: `AWSElasticBeanstalkFullAccess`
4. In the search box, type: `S3`
5. Find and **CHECK** the box for: `AmazonS3FullAccess`
6. You should now have 2 policies selected
7. Click **"Next"** at bottom

**Method 2 - Secure (Custom Policy):**
<details>
<summary>Click to expand for custom policy (more secure)</summary>

1. Select **"Attach policies directly"**
2. Click **"Create policy"** (opens new tab)
3. Click **"JSON"** tab
4. Delete everything in the editor
5. Paste this:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "elasticbeanstalk:*",
        "s3:*",
        "ec2:Describe*",
        "autoscaling:Describe*",
        "cloudformation:Describe*"
      ],
      "Resource": "*"
    }
  ]
}
```

6. Click **"Next: Tags"** → **"Next: Review"**
7. Policy name: `GitHubActionsDeployPolicy`
8. Click **"Create policy"**
9. Go back to previous tab
10. Refresh the policies list
11. Search for `GitHubActionsDeployPolicy` and check it
12. Click **"Next"**
</details>

---

### Step 5: Review and Create

1. Review page shows:
   - User name: `github-actions-deployer`
   - Permissions: 2 policies attached
2. Click **"Create user"** button

✅ **Success!** You should see "User created successfully" message.

---

### Step 6: Create Access Keys

**Important:** This is the MOST CRITICAL step - you'll get credentials you can only see once!

1. Click on the username **"github-actions-deployer"** (blue link)
2. Click the **"Security credentials"** tab
3. Scroll down to **"Access keys"** section
4. Click **"Create access key"** button

**On "Access key best practices" page:**
1. Select **"Third-party service"** option
2. Check the box: "I understand the above recommendation..."
3. Click **"Next"**

**On "Set description tag" page:**
1. Description (optional): `GitHub Actions CI/CD`
2. Click **"Create access key"**

---

### Step 7: SAVE Your Credentials ⚠️

**🚨 CRITICAL: You can ONLY see these credentials ONCE!**

You'll see a page with:
```
Access key ID: AKIA...........
Secret access key: wJalr.........
```

**DO THIS NOW:**

**Option A - Manual Copy (Recommended):**
1. Open a text editor (Notepad, TextEdit, VS Code)
2. Copy **Access key ID** → Paste in text file
3. Copy **Secret access key** → Paste in text file
4. Label them clearly:
```
AWS_ACCESS_KEY_ID=AKIA...........
AWS_SECRET_ACCESS_KEY=wJalr.........
```
5. Keep this text file open (you'll need it in Part 2)

**Option B - Download CSV:**
1. Click **"Download .csv file"** button
2. Save it somewhere safe
3. Open the CSV file to see the credentials

**After saving:**
- Click **"Done"** button
- You're back at the user details page

---

### Step 8: Get Your AWS Account ID

**Method 1 - From Console:**
1. Top-right corner, click on your account name/email
2. You'll see a dropdown menu
3. Look for **"Account ID:"** (12 digits)
4. Example: `474369734726`
5. Copy this number

**Method 2 - From Terminal:**
```bash
aws sts get-caller-identity --query Account --output text
```

**Save this too:**
```
AWS_ACCOUNT_ID=474369734726
```

---

## Part 2: GitHub Setup (Add Secrets)

### Step 9: Navigate to Repository Settings

1. Go to: https://github.com/sunilverma231/End-to-end-Machine-Learning-Project-
2. Click the **"Settings"** tab (top menu, far right)
   - If you don't see it, you're not the repo owner/admin
3. You'll see the repository settings page

---

### Step 10: Access Secrets and Variables

1. In the left sidebar, look for **"Security"** section
2. Click **"Secrets and variables"** (it will expand)
3. Click **"Actions"**
4. You should see "Actions secrets and variables" page

---

### Step 11: Add First Secret (AWS_ACCESS_KEY_ID)

1. Click the green **"New repository secret"** button (top-right)

**On "Actions secrets / New secret" page:**

```
Name: AWS_ACCESS_KEY_ID
Secret: [Paste your Access Key ID from Step 7]
```

Example:
```
Name: AWS_ACCESS_KEY_ID
Secret: AKIAIOSFODNN7EXAMPLE
```

2. Click **"Add secret"** button

✅ You should see it in the list now (value will be hidden with ***)

---

### Step 12: Add Second Secret (AWS_SECRET_ACCESS_KEY)

1. Click **"New repository secret"** again

```
Name: AWS_SECRET_ACCESS_KEY
Secret: [Paste your Secret Access Key from Step 7]
```

Example:
```
Name: AWS_SECRET_ACCESS_KEY
Secret: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

2. Click **"Add secret"**

✅ You should now see 2 secrets in the list

---

### Step 13: Add Third Secret (AWS_ACCOUNT_ID)

1. Click **"New repository secret"** one more time

```
Name: AWS_ACCOUNT_ID
Secret: [Paste your 12-digit Account ID from Step 8]
```

Example:
```
Name: AWS_ACCOUNT_ID
Secret: 474369734726
```

2. Click **"Add secret"**

✅ **You should now see 3 secrets:**
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_ACCOUNT_ID

---

## Part 3: Test the CI/CD Pipeline

### Step 14: Trigger First Deployment

**Option A - Make a Small Change:**

In your terminal:
```bash
cd /Users/sunilverma/Desktop/End-to-end-Machine-Learning-Project-

# Add all CI/CD files
git add .

# Commit with meaningful message
git commit -m "feat: Add CI/CD pipeline with GitHub Actions

- Automated testing with pytest and flake8
- Auto-deployment to AWS Elastic Beanstalk
- Integrated health checks and rollback support
- Zero-touch deployment from git push"

# Push to trigger deployment
git push origin main
```

**Option B - Manual Trigger (Testing Only):**

1. Go to: https://github.com/sunilverma231/End-to-end-Machine-Learning-Project-/actions
2. Click **"CI/CD Pipeline - Deploy to AWS Elastic Beanstalk"** (left sidebar)
3. Click **"Run workflow"** dropdown (right side)
4. Select branch: **main**
5. Click green **"Run workflow"** button

---

### Step 15: Monitor Deployment

1. Go to **Actions** tab on GitHub
2. You should see a new workflow run starting (yellow dot 🟡)
3. Click on the workflow run to see details

**You'll see 2 jobs:**
- **test** - Running tests (2-3 min)
- **deploy** - Deploying to AWS (3-5 min)

**Watch for:**
- ✅ Green checkmarks = Success
- ❌ Red X = Failed (click to see logs)
- 🟡 Yellow dot = In progress

---

### Step 16: Verify Deployment Success

**After ~7 minutes, check:**

1. **GitHub Actions Status:**
   - Should show green ✅
   - "This workflow run completed successfully"

2. **Application URL:**
   ```
   http://studentperformanceenv1-env.eba-wbvx3wpb.eu-north-1.elasticbeanstalk.com/
   ```
   - Should load the form
   - Should work normally

3. **AWS EB Console:**
   - Go to: AWS Console → Elastic Beanstalk
   - Environment: `studentperformanceenv1-env`
   - Health should be: **Green** / **Ok**
   - Events tab: "Environment update completed successfully"

---

## ✅ Success Checklist

You've completed setup when:

- [x] IAM user `github-actions-deployer` created in AWS
- [x] Access keys generated and saved
- [x] 3 GitHub secrets added (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ACCOUNT_ID)
- [x] Code pushed to main branch
- [x] GitHub Actions workflow completed successfully (green ✅)
- [x] Application URL still works
- [x] AWS EB shows new deployment version

---

## 🎉 What You Can Do Now

### Deploy Any Change Automatically:

```bash
# 1. Make your code changes in VS Code
# 2. Commit and push
git add .
git commit -m "feat: add new feature"
git push origin main

# 3. That's it! ✨
# Watch deployment at: 
# https://github.com/sunilverma231/End-to-end-Machine-Learning-Project-/actions
```

---

## 🆘 Troubleshooting

### Problem: "Access Denied" in GitHub Actions

**Solution:**
- Check IAM policies are attached correctly
- Verify AWS credentials in GitHub secrets (no extra spaces)
- Ensure AWS_ACCOUNT_ID is exactly 12 digits

### Problem: "Environment not found"

**Solution:**
- Check `.github/workflows/deploy.yml` line 10-11:
  ```yaml
  EB_APPLICATION_NAME: studentperformanceenv1
  EB_ENVIRONMENT_NAME: studentperformanceenv1-env
  ```
- Verify these match your AWS EB environment name

### Problem: Tests failing

**Solution:**
```bash
# Run tests locally to debug
cd /Users/sunilverma/Desktop/End-to-end-Machine-Learning-Project-
pip install pytest
pytest tests/ -v
```

### Problem: Can't see Settings tab on GitHub

**Solution:**
- You need to be the repository owner or have admin access
- Fork the repo to your account if needed

---

## 📞 Need Help?

If stuck:
1. Check GitHub Actions logs (click on failed step)
2. Check AWS CloudWatch logs
3. Verify all 3 secrets are in GitHub (Settings → Secrets → Actions)
4. Ensure IAM user has correct policies

---

## 🔒 Security Notes

**DO:**
✅ Rotate access keys every 90 days
✅ Delete access keys if compromised
✅ Use least-privilege IAM policies

**DON'T:**
❌ Commit secrets to code
❌ Share secrets via email/Slack
❌ Use root account credentials
❌ Give more permissions than needed

---

## 📊 Expected Timeline

| Step | Time |
|------|------|
| AWS IAM Setup | 5 min |
| GitHub Secrets | 2 min |
| First Deployment | 7 min |
| **Total** | **~15 min** |

---

**Next:** Once setup is complete, read [CICD_UPGRADE.md](../CICD_UPGRADE.md) for daily workflow guide.

🚀 **You're ready for automated deployments!**
