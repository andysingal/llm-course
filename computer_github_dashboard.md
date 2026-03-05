# GitHub Repository Dashboard

---

## Context & Memory

Remember: I prefer dark-themed dashboards styled like Bloomberg terminals. Use amber/gold accent colors, monospace fonts for data, and a financial terminal aesthetic. All visualizations should use Python libraries (matplotlib, plotly) — never AI-generated images for charts or data.

## Task

Build and deploy an interactive GitHub repository monitoring dashboard for this repo: [YOUR_GITHUB_URL]
This is a two-phase job: **research first, then build**.

--- 

## Phase 1: Data Collection


Use the GitHub integration (or browse github.com directly) to collect ALL of the following data for the repository. Save everything to a structured JSON file in the workspace before building anything.


### General Metadata
- Repository name, description, primary language, license, creation date, last push date
- Stars, Forks, Watchers, Open Issues count, Open PRs count, total size


### Commit Activity
- Commits per week for the last 12 weeks (use the stats/participation API or scrape the Insights → Contributors page)
- Total commits in the last 30 days
- Total unique contributors in the last 30 days


### Issues & Pull Requests
- Last 15 open issues: title, author, labels, created date, comments count
- Last 15 open PRs: title, author, created date, review status, comments count
- Issues opened vs closed in the last 30 days
- PRs opened vs merged vs closed in the last 30 days


### Contributors
- Top 10 contributors by commit count (username + commit count + avatar URL)


### Languages
- Language breakdown with percentages (from the repo's language bar)


### Releases
- Latest release tag, date, and name (if any)


### Repository Health Signals
- Has README? Has LICENSE? Has CONTRIBUTING.md? Has CI/CD config?
- Dependabot alerts count (if visible)
- Average time to close issues (estimate from last 20 closed issues)
- Average time to merge PRs (estimate from last 20 merged PRs)


Save all collected data as `repo_data.json` in the workspace.


---


## Phase 2: Build the Dashboard Website


Load the `website-building` skill. Build a single-page static site and deploy it.


### Aesthetic Direction: Bloomberg Terminal


This is a **financial terminal / Bloomberg-style dark dashboard**. Every design choice should evoke a professional trading terminal.


**Color System (use CSS variables):**
```
--bg-primary: #0A0E17        /* deep navy-black */
--bg-card: #131722           /* card/panel background */
--bg-card-hover: #1A1F2E     /* card hover state */
--border: #1E2330            /* subtle borders */
--accent-primary: #F5A623    /* Bloomberg amber/gold — primary accent */
--accent-green: #00D4AA      /* positive values, uptrends */
--accent-red: #FF4757        /* negative values, alerts, downtrends */
--accent-blue: #3B82F6       /* informational, links */
--text-primary: #D1D4DC      /* main text */
--text-secondary: #787B86    /* labels, secondary text */
--text-muted: #4A4E5A        /* very subtle text */
```


**Typography:**
- Data/numbers: `'JetBrains Mono', 'SF Mono', 'Fira Code', monospace` — load JetBrains Mono from Google Fonts
- Labels/headings: `'Inter', sans-serif` — load Inter from Google Fonts
- All numbers should use tabular figures and be monospaced


**Visual Rules:**
- Border-radius: 4px maximum (terminal feel, not rounded cards)
- 1px solid borders on all panels using --border color
- Subtle amber glow on hover (`box-shadow: 0 0 12px rgba(245, 166, 35, 0.15)`)
- CRT scanline overlay effect across the entire page (CSS pseudo-element with repeating linear gradient, very subtle, ~0.03 opacity)
- Thin amber line at the top of each card (3px top border in --accent-primary)
- No drop shadows except the hover glow
- Dense, information-rich layout — minimize whitespace like a real terminal


### Dashboard Layout


Build these sections in order, top to bottom:


#### 1. Header Bar
- GitHub icon (SVG inline) + repo full name (org/repo) as the title
- Colored badge showing primary language
- "Last updated: [timestamp]" indicator with a subtle pulse animation on the dot
- Stars / Forks / Watchers as inline KPI pills with icons


#### 2. KPI Row (6 cards in a single row, equal width)
Each card has: a small icon (use inline SVG), large numeric value (2rem+ font, monospace), label below (small caps, muted), and a trend indicator (green up arrow or red down arrow with percentage).


| Card | Value | Trend Logic |
|------|-------|-------------|
| Total Stars | star count | show as static if no history |
| Total Forks | fork count | static |
| Open Issues | count | color green if < 20, amber if 20-50, red if > 50 |
| Open PRs | count | color amber if > 10 |
| Contributors (30d) | active count | — |
| Commits (30d) | commit count | — |


#### 3. Charts Row (2 columns, ~60/40 split)
- **Left — Commit Activity (area chart):** 12-week commit history as an area chart with gradient fill (amber to transparent). X-axis = week labels, Y-axis = commit count. Built with Chart.js loaded from CDN (cdnjs.cloudflare.com). Use the Bloomberg amber color for the line and fill gradient.
- **Right — Top Contributors (horizontal bar chart):** Top 10 contributors ranked by commits. Show avatar thumbnails (img tags) next to usernames. Bars in gradient from amber to a darker shade. Show commit count at the end of each bar.


#### 4. Analytics Row (3 columns, equal width)
- **Language Distribution (donut chart):** Use GitHub's actual language colors (search for the correct hex per language). Center of donut shows the primary language name and percentage. Built with Chart.js.
- **Issues Velocity (grouped bar chart):** Two groups — "Last 30 Days" showing opened vs closed issues side by side. Use accent-red for opened, accent-green for closed.
- **PR Velocity (grouped bar chart):** Three groups — opened / merged / closed in last 30 days. Use accent-blue for opened, accent-green for merged, accent-red for closed.


#### 5. Data Tables Row (2 columns, equal width)
- **Recent Open Issues table:** Columns: # (issue number), Title (truncated to 50 chars), Author, Labels (as small colored badges), Age (relative time like "3d ago"). Striped rows with --bg-card and --bg-primary alternating. Hover highlight in amber (very subtle). Max 10 rows, scrollable if more.
- **Recent Open PRs table:** Columns: # (PR number), Title, Author, Status (Draft/Review/Approved as colored badge), Age. Same styling as issues table.


#### 6. Repository Health Score Panel (full width)
Calculate a health score from 0-100:


| Factor | Weight | Scoring Logic |
|--------|--------|---------------|
| Commit Frequency | 25% | >10/week = 100, 5-10 = 75, 1-5 = 50, 0 = 0 |
| Issue Close Ratio | 25% | closed/(opened+closed) × 100 in last 30 days |
| PR Merge Time | 20% | <1 day = 100, 1-3 days = 75, 3-7 = 50, >7 = 25 |
| Active Contributors | 15% | >10 = 100, 5-10 = 75, 2-5 = 50, 1 = 25 |
| Documentation | 15% | README + LICENSE + CONTRIBUTING = 100, 2/3 = 66, 1/3 = 33 |


Display as:
- Large semicircular gauge (SVG or canvas) with gradient from red (0) → amber (50) → green (100)
- Large number in the center of the gauge
- Below: 5 horizontal progress bars, one per factor, with label, individual score, and the bar filled proportionally. Use the corresponding color (green/amber/red based on score).


#### 7. Footer
- "Dashboard generated [date] • Data from GitHub API" in muted text
- Link to the repository (opens in new tab: `target="_blank" rel="noopener noreferrer"`)
- "Built with Perplexity Computer" badge


### Technical Requirements
- Single `index.html` file with all CSS and JS inline
- Chart.js loaded from CDN: `https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js`
- Google Fonts loaded for JetBrains Mono and Inter
- All repo data hardcoded in a `const REPO_DATA = {...}` object at the top of the script section (read from the JSON file created in Phase 1)
- No localStorage or sessionStorage
- Fully responsive: looks great at 1920px, adapts gracefully to 1366px
- Smooth fade-in animation on load for each section (staggered by 100ms using CSS animation-delay)
- All external links use `target="_blank" rel="noopener noreferrer"`


### After Building
1. Deploy the site with `deploy_website()`
2. Take a screenshot of the deployed page to verify it looks correct
3. If anything looks off, fix it and re-deploy
4. Share the live URL with me