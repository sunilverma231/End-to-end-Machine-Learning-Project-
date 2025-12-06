# CI/CD Pipeline Architecture

## Full Automation Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DEVELOPER WORKFLOW                          │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │   git push origin main    │
                    └───────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          GITHUB ACTIONS                             │
│                                                                     │
│   ┌─────────────┐      ┌──────────────┐      ┌─────────────┐      │
│   │   STAGE 1   │      │   STAGE 2    │      │   STAGE 3   │      │
│   │   Testing   │ ───> │   Building   │ ───> │  Deployment │      │
│   └─────────────┘      └──────────────┘      └─────────────┘      │
│         │                      │                      │            │
│         ▼                      ▼                      ▼            │
│   • Flake8 Lint          • Create Zip           • AWS Auth        │
│   • Pytest Run           • Exclude Dev          • S3 Upload       │
│   • Code Quality         • Version Tag          • EB Deploy       │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         AWS INFRASTRUCTURE                          │
│                                                                     │
│   ┌─────────────────┐          ┌──────────────────┐                │
│   │   S3 Bucket     │   ────>  │ Elastic Beanstalk│                │
│   │ (Deploy Zips)   │          │   Environment    │                │
│   └─────────────────┘          └──────────────────┘                │
│                                         │                           │
│                                         ▼                           │
│                          ┌──────────────────────────┐               │
│                          │   Health Check Pass?     │               │
│                          └──────────────────────────┘               │
│                                    │                                │
│                          ┌─────────┴─────────┐                      │
│                          ▼                   ▼                      │
│                    ┌──────────┐       ┌──────────┐                 │
│                    │  Success │       │  Rollback│                 │
│                    │  Deploy  │       │  (Auto)  │                 │
│                    └──────────┘       └──────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                        ┌───────────────────────┐
                        │   LIVE PRODUCTION     │
                        │  studentperformance   │
                        │    env1-env.eba...    │
                        └───────────────────────┘
```

## Pipeline Stages Breakdown

### Stage 1: Testing (2-3 minutes)
```
┌────────────────────────────────────────┐
│ Checkout Code                          │
│ ↓                                      │
│ Setup Python 3.11                      │
│ ↓                                      │
│ Install Dependencies (with cache)      │
│ ↓                                      │
│ Lint with Flake8                       │
│ ↓                                      │
│ Run Pytest                             │
│ ↓                                      │
│ ✅ All Tests Pass → Proceed            │
│ ❌ Tests Fail → Stop Deployment        │
└────────────────────────────────────────┘
```

### Stage 2: Building (30 seconds)
```
┌────────────────────────────────────────┐
│ Create deployment.zip                  │
│ ↓                                      │
│ Include:                               │
│   • application.py                     │
│   • wsgi.py                            │
│   • Procfile                           │
│   • requirements.txt                   │
│   • src/                               │
│   • artifacts/                         │
│   • .ebextensions/                     │
│ ↓                                      │
│ Exclude:                               │
│   • .git/                              │
│   • venv/, myenv/                      │
│   • __pycache__/                       │
│   • notebook/                          │
│   • tests/                             │
│ ↓                                      │
│ ✅ Package Ready (< 100MB)             │
└────────────────────────────────────────┘
```

### Stage 3: Deployment (3-5 minutes)
```
┌────────────────────────────────────────┐
│ Configure AWS Credentials              │
│ ↓                                      │
│ Upload to S3                           │
│   elasticbeanstalk-{region}-{account}  │
│ ↓                                      │
│ Create EB Application Version          │
│   Label: {git-sha}                     │
│ ↓                                      │
│ Update EB Environment                  │
│   studentperformanceenv1-env           │
│ ↓                                      │
│ Wait for Health Check                  │
│   /health endpoint → 200 OK            │
│ ↓                                      │
│ ✅ Deployment Complete                 │
│ 🚀 Live at EB URL                      │
└────────────────────────────────────────┘
```

## Benefits vs Manual Deployment

| Feature | Manual (Zip Upload) | Automated (CI/CD) |
|---------|-------------------|-------------------|
| **Speed** | 5-10 min (human) | 5-7 min (automated) |
| **Consistency** | ❌ Human error prone | ✅ Same every time |
| **Testing** | ❌ Optional | ✅ Enforced |
| **Rollback** | ❌ Manual | ✅ One-click |
| **Audit Trail** | ❌ Limited | ✅ Full history |
| **Multiple Envs** | ❌ Tedious | ✅ Easy (dev/staging/prod) |
| **Code Quality** | ❌ No checks | ✅ Automated linting |
| **Deployment at** | ❌ Working hours | ✅ Anytime |

## Security & Secrets Management

```
GitHub Secrets (Encrypted)
    ├── AWS_ACCESS_KEY_ID
    ├── AWS_SECRET_ACCESS_KEY
    └── AWS_ACCOUNT_ID
           ↓
    GitHub Actions Runner
           ↓
    AWS IAM Authentication
           ↓
    Elastic Beanstalk Deployment
```

**Never exposed in:**
- Logs
- Code
- Version control
- Error messages

## Monitoring & Notifications

```
Deployment Status
    ├── Success → Green checkmark in GitHub
    ├── Failure → Red X + Email notification
    └── In Progress → Yellow dot
           ↓
    GitHub Actions Tab
           ↓
    View detailed logs for each step
```

## Future Enhancements

- [ ] Add staging environment
- [ ] Blue-Green deployments
- [ ] Automated integration tests
- [ ] Performance benchmarking
- [ ] Slack/Discord notifications
- [ ] Code coverage reports
- [ ] Dependency security scanning
