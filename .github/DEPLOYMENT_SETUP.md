# Dashboard Deployment Setup

This document explains how to set up automated deployment for the microcalibration dashboard using GitHub Pages.

## Overview

The dashboard is deployed as a static site using GitHub Pages with GitHub Actions automation:
- **PR Build Validation**: Builds and tests dashboard on every pull request
- **Local Testing Workflow**: PRs include instructions for local testing and review
- **Automatic Production Deployment**: Deploys to GitHub Pages on merge to main branch
- **No External Dependencies**: Uses only GitHub infrastructure, no tokens required

## Setup Instructions

### 1. Enable GitHub Pages

1. Go to your repository settings
2. Navigate to `Settings > Pages`
3. Under "Source", select "GitHub Actions"
4. The workflow will automatically deploy on the next push to main

### 2. Repository Configuration

No additional secrets or configuration needed! The workflow uses built-in GitHub tokens.

### 3. Local Development Setup

```bash
# Install dependencies
make dashboard-install

# Start development server
make dashboard-dev

# Build static export
make dashboard-static

# Preview static build locally
make dashboard-preview

# Run full build check (lint + static export)
make dashboard-check
```

### 4. Dashboard URL

Once deployed, your dashboard will be available at:
```
https://[username].github.io/microcalibrate/
```

Replace `[username]` with your GitHub username or organization name.

## Workflow Features

### Build Validation on PRs (`dashboard-deploy-pages.yml`)
- Triggers on PRs that modify dashboard files
- Builds static export and runs comprehensive tests
- Adds detailed comment to PR with local testing instructions
- Provides step-by-step commands to test changes locally
- Includes comprehensive testing checklist for reviewers
- **No live preview deployment** - testing done locally for simplicity

### Production Deployment (`dashboard-deploy-pages.yml`)
- Triggers on push to main branch
- Runs linting, builds, and deploys to GitHub Pages
- Updates commit status with deployment URL
- Publicly accessible at your GitHub Pages URL

## PR Review Process

When a PR is created, reviewers can test changes locally:

1. **Automated Comment**: The workflow adds a comment with testing instructions
2. **Local Setup**: Reviewers use provided git commands to check out the PR branch
3. **Interactive Testing**: Run `make dashboard-dev` to test at `http://localhost:3000`
4. **Testing Checklist**: Follow the comprehensive checklist in the PR comment

### Benefits of Local Testing:
- ✅ **Full interactivity** - Test all features including file uploads
- ✅ **No deployment delays** - Immediate testing after checkout
- ✅ **No external services** - Everything runs locally
- ✅ **Real development environment** - Same as contributors use
- ✅ **Debug-friendly** - Access to browser dev tools and console

## Dashboard Features

The deployed dashboard includes:
- 📊 **Sample Data**: Pre-loaded calibration data for immediate testing
- 📁 **File Upload**: Drag & drop CSV file support with comprehensive error handling
- 🌐 **URL Loading**: Load CSV files from remote URLs with validation
- 📈 **Interactive Visualizations**: Charts and metrics powered by Recharts
- 🎨 **Responsive Design**: Works on desktop and mobile devices
- ⚡ **Fast Loading**: Optimized static build with GitHub Pages CDN

## Troubleshooting

### Common Issues

1. **Deployment fails with build errors**
   - Check that all dependencies are in `package.json`
   - Ensure TypeScript types are correct
   - Run `make dashboard-check` locally to test

2. **GitHub Pages not enabled**
   - Go to repository Settings > Pages
   - Select "GitHub Actions" as the source
   - Ensure the workflow has proper permissions

3. **CSV sample file not loading**
   - Ensure `sample.csv` is in the `public/` directory
   - Check that the file is copied to `out/` during build
   - Verify the basePath configuration in `next.config.ts`

4. **404 errors on GitHub Pages**
   - Check that `basePath` is correctly set to `/microcalibrate`
   - Ensure `trailingSlash: true` is enabled
   - Verify `.nojekyll` file is created during build

5. **Local testing issues**
   - Make sure Node.js 20+ is installed
   - Run `make dashboard-install` before `make dashboard-dev`
   - Check that port 3000 is available

### Support

For deployment issues:
1. Check GitHub Actions logs in the "Actions" tab
2. Review build output for error messages
3. Test locally with `make dashboard-check`
4. For PR testing issues, follow the commands in the automated PR comment
5. Create an issue in the repository

## Security Notes

- Only HTTPS URLs are allowed for CSV loading
- File size limit of 50MB for uploads
- All uploads are client-side only (no server storage)
- CORS restrictions apply to remote CSV URLs
- Static site - no server-side vulnerabilities
- Hosted on GitHub's secure CDN infrastructure
- Local testing keeps sensitive data on reviewer's machine