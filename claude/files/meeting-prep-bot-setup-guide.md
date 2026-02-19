# Meeting Prep Bot -- Claude Code Setup Guide

## Overview

This guide walks you step-by-step through building and deploying an
automated meeting prep bot using Claude Code and Railway.

The bot: - Runs every morning at 7am ET - Pulls your Google Calendar
events via Unipile - Filters external attendees - Researches each person
in parallel using Exa + Perplexity - Formats a clean plain-text dossier
using Claude - Sends one email per meeting via Resend

------------------------------------------------------------------------

## Prerequisites

-   Node.js 18+
-   Claude Code CLI installed
-   Railway account
-   API keys for:
    -   Unipile
    -   Exa
    -   Perplexity
    -   Claude
    -   Resend

------------------------------------------------------------------------

## 1. Install Claude Code

``` bash
npm install -g @anthropic-ai/claude-code
claude --version
```

------------------------------------------------------------------------

## 2. Create Project Folder

``` bash
mkdir meeting-prep-bot
cd meeting-prep-bot
claude
```

Paste the project build prompt into Claude Code to generate the full
project.

------------------------------------------------------------------------

## 3. Environment Variables

Create a `.env` file:

    UNIPILE_API_KEY=
    UNIPILE_ACCOUNT_ID=
    EXA_API_KEY=
    PERPLEXITY_API_KEY=
    CLAUDE_API_KEY=
    RESEND_API_KEY=
    MY_EMAIL=

------------------------------------------------------------------------

## 4. Run Locally

``` bash
npm install
npm run build
node dist/index.js
```

You should see logs for: - Fetching meetings - Researching attendees -
Sending email

------------------------------------------------------------------------

## 5. Deploy to Railway

### Push to GitHub

``` bash
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

### Deploy on Railway

1.  Create new project
2.  Deploy from GitHub
3.  Add environment variables
4.  Add cron job:

```{=html}
<!-- -->
```
    0 7 * * *

Timezone: America/New_York

------------------------------------------------------------------------

## Parallel Research Pattern

Per attendee:

``` ts
const [linkedin, website, bio, companySummary] = await Promise.all([
  findLinkedIn(),
  findCompanyWebsite(),
  getBio(),
  getCompanySummary()
]);
```

This ensures fast concurrent execution.

------------------------------------------------------------------------

## Suggested Improvements

-   Add Redis caching
-   Store dossiers in Supabase
-   Add Slack delivery option
-   Add funding/news enrichment
-   Add conversation starters
-   Add brief vs deep-dive mode

------------------------------------------------------------------------

## Architecture Flow

1.  Railway cron triggers app
2.  Unipile fetches meetings
3.  Filter attendees
4.  Run Exa + Perplexity in parallel
5.  Format via Claude
6.  Send via Resend
7.  Exit

------------------------------------------------------------------------

You're now fully automated.

Upgrade it. Ship it. Iterate.
