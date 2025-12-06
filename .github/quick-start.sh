#!/bin/bash
# Quick Start Guide for CI/CD Setup
# Run this for instructions: bash .github/quick-start.sh

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║      🚀 CI/CD Setup Quick Start Guide                        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

echo "📋 What you'll do (15 minutes total):"
echo "   1. Create AWS IAM user (5 min)"
echo "   2. Add GitHub secrets (2 min)"
echo "   3. Test deployment (7 min)"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📖 STEP-BY-STEP GUIDE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "Choose your guide:"
echo ""
echo "  [1] 📖 Full Walkthrough (recommended for first time)"
echo "      → Detailed screenshots and explanations"
echo "      → File: .github/SETUP_WALKTHROUGH.md"
echo ""
echo "  [2] ✅ Printable Checklist (quick reference)"
echo "      → Simple step-by-step checklist"
echo "      → File: .github/CHECKLIST.txt"
echo ""
echo "  [3] 🎯 Quick Commands (for experienced users)"
echo "      → Command reference only"
echo "      → File: .github/QUICK_REFERENCE.md"
echo ""

read -p "Enter choice (1-3): " choice

case $choice in
  1)
    echo ""
    echo "Opening full walkthrough..."
    if command -v code &> /dev/null; then
      code .github/SETUP_WALKTHROUGH.md
    else
      cat .github/SETUP_WALKTHROUGH.md
    fi
    ;;
  2)
    echo ""
    echo "Opening checklist..."
    cat .github/CHECKLIST.txt
    echo ""
    echo "💡 Tip: Print this with: cat .github/CHECKLIST.txt | lpr"
    ;;
  3)
    echo ""
    echo "Opening quick reference..."
    if command -v code &> /dev/null; then
      code .github/QUICK_REFERENCE.md
    else
      cat .github/QUICK_REFERENCE.md
    fi
    ;;
  *)
    echo ""
    echo "❌ Invalid choice. Run script again."
    exit 1
    ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔑 WHAT YOU NEED"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Before you start, have these ready:"
echo ""
echo "  ✅ AWS Account login credentials"
echo "  ✅ GitHub account (repo owner/admin access)"
echo "  ✅ Text editor to save AWS keys temporarily"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 QUICK LINKS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  AWS Console:"
echo "  → https://aws.amazon.com/console/"
echo ""
echo "  GitHub Repository:"
echo "  → https://github.com/sunilverma231/End-to-end-Machine-Learning-Project-"
echo ""
echo "  GitHub Actions (after setup):"
echo "  → https://github.com/sunilverma231/End-to-end-Machine-Learning-Project-/actions"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 VERIFICATION STEPS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "After setup, verify:"
echo ""
echo "  1. AWS IAM → Users → github-actions-deployer exists"
echo "  2. GitHub → Settings → Secrets → 3 secrets added"
echo "  3. GitHub → Actions → Workflow runs successfully"
echo "  4. Your app still works at:"
echo "     http://studentperformanceenv1-env.eba-wbvx3wpb.eu-north-1.elasticbeanstalk.com/"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🆘 NEED HELP?"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "If stuck:"
echo "  • Check .github/SETUP_WALKTHROUGH.md for detailed steps"
echo "  • Review GitHub Actions logs for errors"
echo "  • Verify all 3 secrets are in GitHub (no typos)"
echo "  • Ensure IAM user has correct policies"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Ready to start? Good luck! 🚀"
echo ""
