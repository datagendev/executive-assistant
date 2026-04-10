# Meeting Prep: Chehan Karunaratne

**Meeting**: Thursday, April 9, 2026 | 10:00am - 10:30am (America/Chicago)
**Attendees**: Yusheng Kuo, Chehan Karunaratne
**Location**: Google Meet (https://meet.google.com/xjt-uuzf-big)

---

## 1. Background

### Current Role & Company
- **Position**: GTM Engineer - ABM & AI at **xGrowth** (since January 2026)
- **Location**: Sri Lanka (company based in Melbourne, VIC)
- **Focus Areas**:
  - Building and iterating Clay workflows (filters, multi-source enrichment, de-duplication, QA, exports)
  - Prototyping AI tools that speed internal work and evolve into client offerings
  - Orchestrating light automations across data sources and spreadsheets
  - Collaborating with strategists/SDRs to refine ICPs and buying-group definitions

### Education & Background
- **Current Student**: BS in Computer Science and Statistics, University of Peradeniya (2023-2026)
- **Certifications**: Clay AI Skills Certification, Clay Outbound Automation Certification
- **Previous Experience**:
  - Head of Sales & Operations at Studyingermany.lk (Dec 2024 - Present)
  - Business Development Specialist at Fit4Travel (Sept 2024 - Feb 2026)
  - Customer service and sales roles at British Council, LoviTech.lk

### Key Skills & Tools
Anthropic Claude, Clay, AI-Driven Content, Account Marketing, B2B Marketing Strategy, Go-to-Market Strategy, Automation, Python, Data Scraping, CRM (HubSpot, Salesforce)

### LinkedIn Activity & Interests
Recent posts reveal Chehan's thinking on **GTM Alpha** (March 2026):
- *"GTM Alpha isn't some fancy strategy. It's just your edge. The thing that makes your outreach hit different from everyone else's."*
- Focus on **relevance over volume** in ABM: "Less spray. More signal."
- Using AI to reach the right person at the right moment with relevant messaging
- Selected for Clay Cohort, actively learning from Izzy Kim and Sayli Godse

**Content themes**: ABM/GTM strategy, AI-powered automation, Clay workflows, relevance-driven outreach, scalable outbound systems

---

## 2. Prior Interactions

### Email
**1 thread found** (March 2026):
- Calendar acceptance for "Discussion of agent build" meeting on March 21, 2026

### Meetings (Fireflies Transcripts)
**3 meetings found**:

1. **April 9, 2026** (Yesterday! - 59.5 min):
   - **Topic**: Integration of research agent and snippet agent
   - **Key Discussion**: Consolidating agents to streamline workflow and reduce fragility; using Cloud Code; challenges in scaling for parallel processing; proposing validation agent for signal accuracy
   - **Action Items for Chehan**:
     - Finalize combination of research and snippet agents into single repo with proper skill structure
     - Convert existing commands into formal skills using folder and skill.md structure
     - Share GitHub repo for deployment assistance on DataGen platform
     - Iterate on AI signals agent to refine signal detection quality
     - Explore deploying validation and snippet generation agents on cloud platforms

2. **March 23, 2026** (91.75 min):
   - **Topic**: Cloud Code tools setup and integration for automating research workflows
   - **Key Discussion**: Installation of DataGen CLI, MCP agents, GitHub CLI; OAuth tokens for deployment; managing large markdown outputs; Clay integration via webhooks; addressing Clay's size limits with S3 storage
   - **Action Items for Chehan**:
     - Complete GitHub account setup
     - Save OAuth token and insert API keys
     - Adjust JSON payload inputs to match Clay data keys
     - Set up Clay tables with webhook URLs to trigger cloud agents
     - Decide on markdown output storage solution (S3/R2 or Google Sheets)

3. **March 20, 2026** (13.3 min):
   - Short meeting, no summary available

### HeyReach Conversations (LinkedIn DMs)
**2 conversation threads with 89 total messages**:

**Initial Outreach** (February 13, 2026):
- Contacted via LinkedIn Post Activity (Claude Code Bootcamp) - Chehan commented "APPLY"
- **Chehan's Agent Idea**: *"Creating some sort of agent to look for AI signals, like looking for signals in ABM marketing (basically using SignalBase or something like that)"*
- Mentioned he built a CRM using Claude Code previously
- Expressed excitement about learning to build custom agents (not just vibe coding)

**Key Conversation Highlights**:
- Feb 18: Shared GitHub repo (https://github.com/datagendev/how-to-build-agents) and Fireflies transcript
- March 4: Introduced DataGen plugin (https://datagen.dev/plugin)
- March 20: Chehan reached out asking how DataGen could help with "AI researcher using Claude code + parallelization + Exa MCP"
- March 20-21: Rescheduled meetings due to Chehan being unwell
- March 23: Offered free end-to-end deployment assistance as case study
- March 26: Connected on Clay community Slack
- March 30: Shared blog post: https://datagen.dev/agents-guide/clay-claude-code-skill
- **April 8-9**: Switched to Discord for easier communication (yusheng0130)

---

## 3. How DataGen Can Help

Based on Chehan's role, pain points, and LinkedIn activity, here's how DataGen maps to his needs:

### 🎯 Core Use Case: AI Signals Agent for ABM
**Chehan's Vision**: "Look for AI signals in ABM marketing (like SignalBase)"
- **DataGen Solution**: Build autonomous agents that continuously monitor buyer signals (LinkedIn activity, company news, tech stack changes, hiring patterns) and trigger personalized outreach workflows
- **Why it matters**: Aligns with his "less spray, more signal" philosophy and xGrowth's ABM focus

### 🔧 Technical Capabilities Chehan Needs
1. **Skill Development & Agent Structuring**
   - Converting commands into formal skills (already in progress)
   - Combining research + snippet agents into unified workflow
   - **DataGen's role**: Platform for deploying, scheduling, and chaining these agents

2. **Clay Integration at Scale**
   - Current challenge: Clay size limits, managing large markdown outputs
   - **DataGen Solution**: Cloud agents that trigger via webhooks, store results in S3/R2, return URLs to Clay
   - Enables continuous agent runs with feedback loops on lead generation

3. **Parallelization & Reliability**
   - Pain point: Fragility of separate agents, scaling challenges
   - **DataGen Solution**: Managed cloud deployment with error handling, retries, and parallel execution
   - Validation agents to ensure signal accuracy before triggering outreach

### 💡 Value Propositions
- **"Claude Code as an OS, not just a vibe code tool"**: DataGen makes agents operational, not just conversational toys
- **GTM Alpha through automation**: Find edge cases faster by running agents 24/7 across multiple data sources (Exa, LinkedIn, company databases)
- **Hands-on learning**: Deploy together as case study (already offered and accepted)
- **Community & best practices**: Access to how-to guides, skills repo, live support

### 🚨 Potential Objections & Responses
| Objection | Response |
|-----------|----------|
| "Can't I just run this locally in Claude Code?" | Yes, but DataGen lets it run autonomously on schedule or event triggers (e.g., when Clay enriches a new company). Your agents become infrastructure, not manual tasks. |
| "Isn't this overkill for my use case?" | You're already hitting Clay's limits and thinking about S3 storage. That's the inflection point where DataGen saves time vs. duct-taping solutions. Plus, you get to learn architecture patterns. |
| "What's the pricing?" | We're offering free deployment as a case study since your AI signals agent aligns with our roadmap. Win-win. |

---

## 4. Suggested Agenda

### Opening (2 min)
Reference yesterday's meeting: *"Hey Chehan! Following up on our chat yesterday about combining the research and snippet agents—how's the repo structuring going?"*

### Discovery Questions (8 min)
1. **Signal Detection**: *"You mentioned wanting to build an AI signals agent back in February. How are you thinking about signal sources now? LinkedIn activity, tech stack changes, hiring patterns?"*
2. **Current Workflow**: *"Walk me through your current Clay → research → output flow. Where are the bottlenecks?"*
3. **Validation Needs**: *"We talked about a validation agent yesterday. What does 'accurate signal' mean for your use case? What's a false positive vs. true buying signal?"*
4. **Scale Goals**: *"When you say 'run at scale,' what's the target? 10 companies/day? 100? Continuous monitoring?"*

### Demo Focus Areas (12 min)
Based on answers, demo:
1. **Agent deployment flow**: Show how to push skill repo → DataGen → deploy as scheduled/webhook-triggered agent
2. **Clay integration**: Live example of webhook → agent run → S3 output → return URL to Clay
3. **Chaining agents**: Research → validation → snippet generation → CRM update (end-to-end)
4. **Monitoring & logs**: Show CloudWatch logs, error handling, retry logic

### Collaboration & Next Steps (8 min)
1. **Immediate**: Help Chehan finalize the combined agent repo structure (if needed)
2. **This week**: Deploy first version to DataGen, test with sample Clay data
3. **Ongoing**: Iterate on signal detection quality based on feedback, refine prompts
4. **Content**: Chehan's case study → blog post/video for DataGen (with his permission)

### Closing
*"Since we're on Discord now, ping me anytime you hit a blocker. And if this works well, I'd love to feature your setup in a write-up—could be great for your GTM Alpha thinking too."*

---

## 5. Meeting Notes & Follow-Up

**Tone**: Collaborative, educational, low-pressure. Chehan has "let me help you" energy—match that with "let's build this together" approach.

**Key Context to Remember**:
- He's a **university student** (graduating 2026) building real-world skills alongside coursework
- **Time zone**: Sri Lanka (very different from Chicago—appreciate flexibility)
- **Communication**: Prefers Discord over Slack/LinkedIn
- **Learning style**: Hands-on (he said "can also learn from it would be really time saving and helpful")

**Post-Meeting Action**:
- Share any relevant docs/repos in Discord
- Follow up with DataGen deployment link once he shares GitHub repo
- Check in after first agent run to troubleshoot

---

**🤖 Generated with Claude Code + DataGen**
