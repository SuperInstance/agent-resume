interface AgentResume {
  id: string;
  name: string;
  capabilities: string[];
  metrics: {
    uptime: number;
    tasksCompleted: number;
    accuracy: number;
    responseTime: number;
  };
  contributions: Array<{
    project: string;
    role: string;
    duration: string;
    description: string;
  }>;
  certifications: string[];
  portfolio: Array<{
    title: string;
    description: string;
    outcome: string;
  }>;
  badges: Array<{
    id: string;
    name: string;
    earned: string;
  }>;
}

const AGENTS: Record<string, AgentResume> = {
  "alpha": {
    id: "alpha",
    name: "Alpha Agent",
    capabilities: ["Natural Language Processing", "Task Automation", "Data Analysis", "API Integration"],
    metrics: {
      uptime: 99.8,
      tasksCompleted: 1247,
      accuracy: 96.5,
      responseTime: 145
    },
    contributions: [
      {
        project: "Customer Support Automation",
        role: "Primary Handler",
        duration: "2023-Present",
        description: "Reduced response time by 78% and handled 15k+ tickets"
      },
      {
        project: "Data Processing Pipeline",
        role: "Analysis Engine",
        duration: "2022-2023",
        description: "Processed 2.4TB of unstructured data with 99.1% accuracy"
      }
    ],
    certifications: ["Cloudflare Workers Certified", "AI Safety Level 2", "API Security Specialist"],
    portfolio: [
      {
        title: "Real-time Translation System",
        description: "Multi-language translation service with context preservation",
        outcome: "Deployed across 3 regions serving 50k daily requests"
      },
      {
        title: "Automated Code Review",
        description: "Static analysis and security vulnerability detection",
        outcome: "Identified 1.2k+ potential issues in production code"
      }
    ],
    badges: [
      { id: "speed", name: "Speed Demon", earned: "2023-11-15" },
      { id: "reliability", name: "100% Uptime", earned: "2023-12-01" },
      { id: "innovation", name: "Innovator", earned: "2024-01-20" }
    ]
  }
};

const HTML_TEMPLATE = (agent: AgentResume) => `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Agent Resume - ${agent.name}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Inter', sans-serif;
      background: #0a0a0f;
      color: #e5e7eb;
      line-height: 1.6;
      min-height: 100vh;
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem;
    }
    header {
      text-align: center;
      padding: 3rem 0;
      border-bottom: 1px solid #1f2937;
      margin-bottom: 3rem;
    }
    h1 {
      font-size: 3.5rem;
      font-weight: 700;
      background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.5rem;
    }
    .subtitle {
      font-size: 1.25rem;
      color: #9ca3af;
      font-weight: 300;
    }
    .agent-name {
      font-size: 2.5rem;
      color: #ffffff;
      margin-top: 1rem;
    }
    .section {
      background: #111827;
      border-radius: 1rem;
      padding: 2rem;
      margin-bottom: 2rem;
      border: 1px solid #1f2937;
    }
    .section-title {
      font-size: 1.5rem;
      color: #10b981;
      margin-bottom: 1.5rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .section-title::before {
      content: "";
      display: block;
      width: 4px;
      height: 1.5rem;
      background: #10b981;
      border-radius: 2px;
    }
    .capabilities-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1rem;
    }
    .capability-card {
      background: #1f2937;
      padding: 1.5rem;
      border-radius: 0.75rem;
      border-left: 4px solid #10b981;
    }
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1.5rem;
    }
    .metric-card {
      text-align: center;
      padding: 1.5rem;
      background: #1f2937;
      border-radius: 0.75rem;
    }
    .metric-value {
      font-size: 2.5rem;
      font-weight: 700;
      color: #10b981;
      margin-bottom: 0.5rem;
    }
    .metric-label {
      color: #9ca3af;
      font-size: 0.9rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .contribution-item {
      margin-bottom: 1.5rem;
      padding-bottom: 1.5rem;
      border-bottom: 1px solid #374151;
    }
    .contribution-item:last-child {
      border-bottom: none;
      margin-bottom: 0;
      padding-bottom: 0;
    }
    .contribution-header {
      display: flex;
      justify-content: space-between;
      margin-bottom: 0.5rem;
    }
    .badge-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
    }
    .badge {
      background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
      padding: 1rem 1.5rem;
      border-radius: 2rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
      border: 1px solid #4b5563;
    }
    .badge-icon {
      width: 24px;
      height: 24px;
      background: #10b981;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    footer {
      text-align: center;
      padding: 3rem 0;
      margin-top: 4rem;
      border-top: 1px solid #1f2937;
      color: #6b7280;
      font-size: 0.9rem;
    }
    .fleet-footer {
      margin-top: 1rem;
      font-size: 0.8rem;
      color: #4b5563;
    }
    @media (max-width: 768px) {
      .container { padding: 1rem; }
      h1 { font-size: 2.5rem; }
      .agent-name { font-size: 2rem; }
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Agent Resume</h1>
      <div class="subtitle">Showcasing Digital Capabilities & Performance</div>
      <div class="agent-name">${agent.name}</div>
    </header>

    <section class="section">
      <div class="section-title">Capabilities</div>
      <div class="capabilities-grid">
        ${agent.capabilities.map(cap => `
          <div class="capability-card">${cap}</div>
        `).join("")}
      </div>
    </section>

    <section class="section">
      <div class="section-title">Performance Metrics</div>
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-value">${agent.metrics.uptime}%</div>
          <div class="metric-label">Uptime</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">${agent.metrics.tasksCompleted.toLocaleString()}</div>
          <div class="metric-label">Tasks Completed</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">${agent.metrics.accuracy}%</div>
          <div class="metric-label">Accuracy</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">${agent.metrics.responseTime}ms</div>
          <div class="metric-label">Avg Response Time</div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-title">Contribution History</div>
      ${agent.contributions.map(cont => `
        <div class="contribution-item">
          <div class="contribution-header">
            <strong>${cont.project}</strong>
            <span style="color: #10b981;">${cont.duration}</span>
          </div>
          <div style="color: #9ca3af; margin-bottom: 0.5rem;">${cont.role}</div>
          <div>${cont.description}</div>
        </div>
      `).join("")}
    </section>

    <section class="section">
      <div class="section-title">Skill Certifications</div>
      <div class="capabilities-grid">
        ${agent.certifications.map(cert => `
          <div class="capability-card">${cert}</div>
        `).join("")}
      </div>
    </section>

    <section class="section">
      <div class="section-title">Portfolio</div>
      ${agent.portfolio.map(item => `
        <div class="contribution-item">
          <strong style="display: block; margin-bottom: 0.5rem; color: #ffffff;">${item.title}</strong>
          <div style="margin-bottom: 0.75rem;">${item.description}</div>
          <div style="color: #10b981; font-size: 0.9rem;">Outcome: ${item.outcome}</div>
        </div>
      `).join("")}
    </section>

    <section class="section">
      <div class="section-title">Badges & Achievements</div>
      <div class="badge-grid">
        ${agent.badges.map(badge => `
          <div class="badge">
            <div class="badge-icon"></div>
            <div>
              <div style="font-weight: 500;">${badge.name}</div>
              <div style="font-size: 0.8rem; color: #9ca3af;">Earned: ${badge.earned}</div>
            </div>
          </div>
        `).join("")}
      </div>
    </section>

    <footer>
      <div>Agent Resume System • Powered by Cloudflare Workers</div>
      <div class="fleet-footer">Fleet ID: ${agent.id.toUpperCase()} • Last Updated: ${new Date().toISOString().split('T')[0]}</div>
    </footer>
  </div>
</body>
</html>`;

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

const securityHeaders = {
  "Content-Security-Policy": "default-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;",
  "X-Frame-Options": "DENY",
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
};

export default {
  async fetch(request: Request, env: any, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const path = url.pathname;

    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: corsHeaders,
      });
    }

    if (path === "/health") {
      return new Response(JSON.stringify({ status: "ok", timestamp: new Date().toISOString() }), {
        headers: {
          "Content-Type": "application/json",
          ...corsHeaders,
        },
      });
    }

    if (path.startsWith("/api/resume/")) {
      const agentId = path.split("/api/resume/")[1];
      const agent = AGENTS[agentId];

      if (!agent) {
        return new Response(JSON.stringify({ error: "Agent not found" }), {
          status: 404,
          headers: {
            "Content-Type": "application/json",
            ...corsHeaders,
            ...securityHeaders,
          },
        });
      }

      if (request.headers.get("Accept")?.includes("application/json")) {
        return new Response(JSON.stringify(agent), {
          headers: {
            "Content-Type": "application/json",
            ...corsHeaders,
            ...securityHeaders,
          },
        });
      }

      return new Response(HTML_TEMPLATE(agent), {
        headers: {
          "Content-Type": "text/html; charset=utf-8",
          ...corsHeaders,
          ...securityHeaders,
        },
      });
    }

    if (path === "/api/update" && request.method === "POST") {
      try {
        const body = await request.json();
        const agentId = body.id;

        if (!agentId || !AGENTS[agentId]) {
          return new Response(JSON.stringify({ error: "Invalid agent ID" }), {
            status: 400,
            headers: {
              "Content-Type": "application/json",
              ...corsHeaders,
              ...securityHeaders,
            },
          });
        }

        return new Response(JSON.stringify({ 
          success: true, 
          message: "Update received (simulated)", 
          agentId,
          timestamp: new Date().toISOString()
        }), {
          headers: {
            "Content-Type": "application/json",
            ...corsHeaders,
            ...securityHeaders,
          },
        });
      } catch (error) {
        return new Response(JSON.stringify({ error: "Invalid request body" }), {
          status: 400,
          headers: {
            "Content-Type": "application/json",
            ...corsHeaders,
            ...securityHeaders,
          },
        });
      }
    }

    if (path === "/api/badges" && request.method === "GET") {
      const allBadges = Object.values(AGENTS).flatMap(agent => 
        agent.badges.map(badge => ({
          agent: agent.name,
          agentId: agent.id,
          ...badge
        }))
      );

      return new Response(JSON.stringify(allBadges), {
        headers: {
          "Content-Type": "application/json",
          ...corsHeaders,
          ...securityHeaders,
        },
      });
    }

    return new Response(JSON.stringify({ 
      error: "Not found",
      endpoints: [
        "GET /api/resume/:agent",
        "POST /api/update",
        "GET /api/badges",
        "GET /health"
      ]
    }), {
      status: 404,
      headers: {
        "Content-Type": "application/json",
        ...corsHeaders,
        ...securityHeaders,
      },
    });
  }
};