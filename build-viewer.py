#!/usr/bin/env python3
"""Build viewer.html — visual dashboard with charts, images, and data."""

import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))

# Read markdown files for raw data toggles
DOCS = [
    ("README.md", "Overview", "readme"),
    ("data/market-size.md", "Market Size", "market-size"),
    ("data/labor-workforce.md", "Labor & Workforce", "labor-workforce"),
    ("data/key-players.md", "Key Players", "key-players"),
    ("data/bas-technician-field.md", "BAS Technician Field", "bas-technician"),
    ("data/nyc-vs-charlotte-pay.md", "NYC vs Charlotte Pay", "nyc-charlotte"),
    ("data/employers-ny-nc.md", "Employers: NY & NC", "employers"),
    ("data/ny-contacts.md", "NY Contacts", "ny-contacts"),
    ("data/nc-contacts.md", "NC Contacts", "nc-contacts"),
]

docs_data = []
for filepath, label, key in DOCS:
    full_path = os.path.join(BASE, filepath)
    with open(full_path, "r") as f:
        content = f.read()
    docs_data.append({"key": key, "label": label, "content": content})

docs_json = json.dumps(docs_data, ensure_ascii=False)

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Building Automation Industry Overview</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
:root {
  --bg-primary: #0a0f14;
  --bg-secondary: #0f1519;
  --bg-tertiary: #141c22;
  --bg-card: #111920;
  --bg-hover: #1a242d;
  --border: #1e2a35;
  --accent: #00d4aa;
  --accent-bright: #00f5c4;
  --accent-dim: rgba(0, 212, 170, 0.12);
  --accent-glow: rgba(0, 212, 170, 0.3);
  --orange: #ff8c42;
  --red: #ff4d6a;
  --blue: #4da6ff;
  --purple: #a78bfa;
  --yellow: #fbbf24;
  --text-primary: #e0e6ed;
  --text-secondary: #8899a6;
  --text-muted: #556677;
  --sidebar-w: 240px;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'IBM Plex Sans', sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* ===== SIDEBAR ===== */
.sidebar {
  width: var(--sidebar-w);
  min-width: var(--sidebar-w);
  background: var(--bg-secondary);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  z-index: 100;
  transition: transform 0.3s ease;
}
.sidebar-header {
  padding: 20px 16px 14px;
  border-bottom: 1px solid var(--border);
}
.sidebar-header h1 {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 600;
  color: var(--accent);
  letter-spacing: 1.5px;
  text-transform: uppercase;
  line-height: 1.5;
}
.sidebar-header .sub {
  font-size: 10px;
  color: var(--text-muted);
  margin-top: 4px;
  font-family: 'JetBrains Mono', monospace;
}
.nav-list { flex: 1; overflow-y: auto; padding: 6px 0; }
.nav-item {
  display: flex; align-items: center;
  padding: 9px 16px; cursor: pointer;
  font-size: 12.5px; color: var(--text-secondary);
  border-left: 3px solid transparent;
  transition: all 0.15s; user-select: none;
}
.nav-item:hover { background: var(--bg-hover); color: var(--text-primary); }
.nav-item.active {
  background: var(--accent-dim); color: var(--accent);
  border-left-color: var(--accent); font-weight: 500;
}
.nav-item .dot {
  width: 5px; height: 5px; border-radius: 50%;
  background: var(--text-muted); margin-right: 10px; flex-shrink: 0;
}
.nav-item.active .dot { background: var(--accent); box-shadow: 0 0 6px var(--accent-glow); }

.nav-divider {
  padding: 14px 16px 6px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; letter-spacing: 1.5px;
  color: var(--text-muted); text-transform: uppercase;
}
.sidebar-footer {
  padding: 12px 16px; border-top: 1px solid var(--border);
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; color: var(--text-muted);
}

/* ===== MAIN ===== */
.main { flex: 1; overflow-y: auto; scroll-behavior: smooth; }

/* ===== HERO ===== */
.hero {
  position: relative; height: 420px;
  background: linear-gradient(135deg, #0a1628 0%, #0d2137 50%, #0a1a2e 100%);
  overflow: hidden; display: flex; align-items: center; justify-content: center;
}
.hero::before {
  content: ''; position: absolute; inset: 0;
  background: url('https://images.unsplash.com/photo-1486325212027-8081e485255e?w=1400&q=80') center/cover;
  opacity: 0.15;
}
.hero::after {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(to bottom, rgba(10,15,20,0.3) 0%, rgba(10,15,20,0.95) 100%);
}
.hero-content { position: relative; z-index: 2; text-align: center; padding: 0 40px; }
.hero-content h1 {
  font-size: 42px; font-weight: 700; color: #fff;
  margin-bottom: 12px; letter-spacing: -0.5px;
}
.hero-content h1 span { color: var(--accent); }
.hero-content p {
  font-size: 17px; color: var(--text-secondary);
  max-width: 600px; margin: 0 auto 32px; line-height: 1.6;
}
.hero-stats {
  display: flex; gap: 40px; justify-content: center; flex-wrap: wrap;
}
.hero-stat {
  text-align: center;
}
.hero-stat .num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 36px; font-weight: 700; color: var(--accent);
  text-shadow: 0 0 30px var(--accent-glow);
}
.hero-stat .label {
  font-size: 11px; color: var(--text-muted);
  text-transform: uppercase; letter-spacing: 1px; margin-top: 4px;
}

/* ===== SECTIONS ===== */
.section {
  padding: 64px 48px;
  max-width: 1100px;
  margin: 0 auto;
}
.section-header {
  margin-bottom: 40px;
}
.section-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
  color: var(--accent); margin-bottom: 8px;
}
.section-title {
  font-size: 28px; font-weight: 700; color: #fff;
  margin-bottom: 10px;
}
.section-desc {
  font-size: 15px; color: var(--text-secondary); line-height: 1.7;
  max-width: 700px;
}

/* ===== DIVIDER HERO (between sections) ===== */
.divider-hero {
  position: relative; height: 240px;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
}
.divider-hero::before {
  content: ''; position: absolute; inset: 0;
  background-size: cover; background-position: center;
  opacity: 0.12;
}
.divider-hero::after {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(to bottom, var(--bg-primary) 0%, rgba(10,15,20,0.6) 40%, rgba(10,15,20,0.6) 60%, var(--bg-primary) 100%);
}
.divider-hero .divider-text {
  position: relative; z-index: 2; text-align: center;
}
.divider-hero .divider-text h2 {
  font-size: 24px; font-weight: 700; color: #fff;
}
.divider-hero .divider-text p {
  font-size: 14px; color: var(--text-secondary); margin-top: 8px;
}

/* ===== CARDS / GRID ===== */
.card-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px; margin: 24px 0;
}
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 24px;
  transition: border-color 0.2s;
}
.card:hover { border-color: var(--accent); }
.card-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px; letter-spacing: 1px;
  text-transform: uppercase; color: var(--text-muted);
  margin-bottom: 8px;
}
.card-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 32px; font-weight: 700; color: var(--accent);
}
.card-value.orange { color: var(--orange); }
.card-value.red { color: var(--red); }
.card-value.blue { color: var(--blue); }
.card-value.purple { color: var(--purple); }
.card-desc {
  font-size: 13px; color: var(--text-secondary);
  margin-top: 8px; line-height: 1.5;
}

/* ===== CHARTS ===== */
.chart-container {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 24px;
  margin: 24px 0;
}
.chart-container h3 {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px; letter-spacing: 0.5px;
  color: var(--text-secondary); margin-bottom: 16px;
  text-transform: uppercase;
}
.chart-row {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 20px; margin: 24px 0;
}
.chart-row canvas { max-height: 320px; }

/* ===== BIG QUOTE ===== */
.feedback-loop {
  background: linear-gradient(135deg, rgba(0,212,170,0.08), rgba(0,212,170,0.02));
  border: 1px solid rgba(0,212,170,0.2);
  border-radius: 12px;
  padding: 40px;
  margin: 40px 0;
  text-align: center;
}
.feedback-loop h3 {
  font-size: 20px; color: var(--accent); margin-bottom: 16px;
}
.feedback-loop p {
  font-size: 15px; color: var(--text-secondary); line-height: 1.8;
  max-width: 600px; margin: 0 auto;
}
.loop-visual {
  display: flex; align-items: center; justify-content: center;
  gap: 8px; margin-top: 24px; flex-wrap: wrap;
}
.loop-step {
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: 6px; padding: 10px 16px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; color: var(--text-primary);
}
.loop-arrow { color: var(--accent); font-size: 18px; }

/* ===== RATIO VIS ===== */
.ratio-vis {
  display: flex; align-items: center; gap: 32px;
  margin: 24px 0; padding: 32px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
}
.ratio-dots {
  display: flex; gap: 12px; align-items: center;
}
.ratio-dot {
  width: 36px; height: 36px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px;
}
.ratio-dot.retire { background: rgba(255,77,106,0.2); border: 2px solid var(--red); }
.ratio-dot.replace { background: rgba(0,212,170,0.2); border: 2px solid var(--accent); }
.ratio-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px; color: var(--text-secondary);
}
.ratio-text {
  font-size: 14px; color: var(--text-secondary); line-height: 1.6;
}

/* ===== CAREER LADDER ===== */
.ladder {
  display: flex; flex-direction: column; gap: 4px;
  margin: 24px 0;
}
.ladder-step {
  display: flex; align-items: center; gap: 16px;
  padding: 14px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  transition: all 0.2s;
}
.ladder-step:hover {
  border-color: var(--accent);
  transform: translateX(4px);
}
.ladder-level {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; color: var(--text-muted);
  width: 20px; text-align: center;
}
.ladder-role {
  font-weight: 600; font-size: 14px; color: var(--text-primary);
  flex: 1;
}
.ladder-salary {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px; color: var(--accent);
}
.ladder-bar {
  height: 6px; border-radius: 3px;
  background: linear-gradient(90deg, var(--accent), var(--accent-bright));
  opacity: 0.6;
}

/* ===== SPLIT COMPARE (NYC vs CLT) ===== */
.split-hero {
  display: grid; grid-template-columns: 1fr 1fr;
  height: 200px; position: relative; overflow: hidden;
}
.split-side {
  position: relative; display: flex; align-items: center;
  justify-content: center; overflow: hidden;
}
.split-side::before {
  content: ''; position: absolute; inset: 0;
  background-size: cover; background-position: center;
  opacity: 0.2;
}
.split-side::after {
  content: ''; position: absolute; inset: 0;
  background: rgba(10,15,20,0.7);
}
.split-side .city-name {
  position: relative; z-index: 2;
  font-family: 'JetBrains Mono', monospace;
  font-size: 24px; font-weight: 700; color: #fff;
  letter-spacing: 2px;
}
.split-divider {
  position: absolute; left: 50%; top: 0; bottom: 0;
  width: 2px; background: var(--accent); z-index: 3;
}

/* ===== FLOW DIAGRAM ===== */
.flow-diagram {
  display: flex; align-items: center; justify-content: center;
  gap: 16px; margin: 32px 0; flex-wrap: wrap;
}
.flow-box {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px; padding: 20px 24px;
  text-align: center; min-width: 180px;
}
.flow-box h4 {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; color: var(--accent);
  text-transform: uppercase; letter-spacing: 1px;
  margin-bottom: 8px;
}
.flow-box p { font-size: 12px; color: var(--text-secondary); line-height: 1.5; }
.flow-arrow {
  font-size: 24px; color: var(--accent);
}

/* ===== STAT COMPARE CARDS ===== */
.compare-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 20px; margin: 24px 0;
}
.compare-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px; padding: 24px;
}
.compare-card h4 {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px; font-weight: 600; margin-bottom: 16px;
}
.compare-card.ny h4 { color: var(--blue); }
.compare-card.nc h4 { color: var(--orange); }
.compare-stat {
  display: flex; justify-content: space-between;
  padding: 8px 0; border-bottom: 1px solid var(--border);
  font-size: 13px;
}
.compare-stat:last-child { border-bottom: none; }
.compare-stat .k { color: var(--text-secondary); }
.compare-stat .v { color: var(--text-primary); font-weight: 500; font-family: 'JetBrains Mono', monospace; font-size: 12px; }

/* ===== CERT BADGES ===== */
.cert-badges {
  display: flex; gap: 12px; flex-wrap: wrap; margin: 24px 0;
}
.cert-badge {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px; padding: 12px 16px;
  text-align: center; min-width: 120px;
}
.cert-badge .cert-name {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px; font-weight: 600; color: var(--accent);
}
.cert-badge .cert-org {
  font-size: 10px; color: var(--text-muted); margin-top: 4px;
}

/* ===== DATA TOGGLE ===== */
.data-toggle {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 8px 16px; margin: 20px 0;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: 6px; cursor: pointer;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; color: var(--text-muted);
  transition: all 0.2s;
}
.data-toggle:hover { border-color: var(--accent); color: var(--text-secondary); }
.data-toggle svg { width: 14px; height: 14px; }
.raw-data {
  display: none;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: 8px; padding: 32px;
  margin: 12px 0 32px;
  max-height: 600px; overflow-y: auto;
}
.raw-data.open { display: block; }

/* Markdown inside raw-data */
.raw-data h1 { font-size: 24px; font-weight: 700; color: var(--text-primary); margin: 0 0 12px; padding-bottom: 12px; border-bottom: 2px solid var(--accent); }
.raw-data h2 { font-size: 18px; font-weight: 600; color: var(--accent); margin: 28px 0 12px; }
.raw-data h3 { font-size: 15px; font-weight: 600; color: var(--text-primary); margin: 20px 0 10px; }
.raw-data p { font-size: 14px; line-height: 1.7; margin-bottom: 12px; }
.raw-data ul, .raw-data ol { margin: 0 0 12px 20px; font-size: 14px; line-height: 1.7; }
.raw-data li { margin-bottom: 4px; }
.raw-data li::marker { color: var(--accent); }
.raw-data strong { color: #fff; }
.raw-data a { color: var(--accent); text-decoration: none; }
.raw-data blockquote { border-left: 3px solid var(--accent); padding: 8px 16px; margin: 12px 0; background: var(--accent-dim); border-radius: 0 4px 4px 0; font-style: italic; color: var(--text-secondary); font-size: 13px; }
.raw-data table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 12px; }
.raw-data th { background: var(--bg-primary); color: var(--accent); font-weight: 600; text-align: left; padding: 8px 10px; border: 1px solid var(--border); font-family: 'JetBrains Mono', monospace; font-size: 11px; }
.raw-data td { padding: 7px 10px; border: 1px solid var(--border); vertical-align: top; }
.raw-data tbody tr:hover { background: var(--bg-hover); }
.raw-data code { font-family: 'JetBrains Mono', monospace; font-size: 12px; background: var(--bg-primary); padding: 1px 5px; border-radius: 3px; color: var(--accent); }
.raw-data pre { background: var(--bg-primary); border: 1px solid var(--border); border-radius: 6px; padding: 12px; overflow-x: auto; margin: 12px 0; }
.raw-data pre code { background: none; padding: 0; color: var(--text-primary); }

/* Section dividers */
.section-line {
  height: 1px;
  background: linear-gradient(to right, transparent, var(--border), transparent);
  margin: 0;
}

/* ===== HAMBURGER ===== */
.hamburger {
  display: none; position: fixed; top: 14px; left: 14px; z-index: 200;
  width: 38px; height: 38px;
  background: var(--bg-secondary); border: 1px solid var(--border);
  border-radius: 6px; cursor: pointer;
  align-items: center; justify-content: center;
}
.hamburger span { display: block; width: 16px; height: 2px; background: var(--accent); margin: 3px auto; }
.overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 90; }

@media (max-width: 900px) {
  .sidebar { position: fixed; left: 0; top: 0; bottom: 0; transform: translateX(-100%); }
  .sidebar.open { transform: translateX(0); }
  .overlay.open { display: block; }
  .hamburger { display: flex; }
  .section { padding: 40px 20px; }
  .hero-content h1 { font-size: 28px; }
  .hero-stats { gap: 20px; }
  .hero-stat .num { font-size: 24px; }
  .chart-row { grid-template-columns: 1fr; }
  .compare-grid { grid-template-columns: 1fr; }
  .split-hero { grid-template-columns: 1fr; height: 160px; }
  .card-grid { grid-template-columns: 1fr; }
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* Animate counters */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-in { animation: fadeUp 0.6s ease forwards; }
</style>
</head>
<body>

<div class="hamburger" onclick="toggleSidebar()"><span></span><span></span><span></span></div>
<div class="overlay" onclick="toggleSidebar()"></div>

<aside class="sidebar">
  <div class="sidebar-header">
    <h1>Building<br>Automation</h1>
    <div class="sub">Industry Overview / Feb 2026</div>
  </div>
  <nav class="nav-list">
    <div class="nav-divider">Dashboard</div>
    <div class="nav-item active" onclick="scrollToSection('hero')"><span class="dot"></span>Overview</div>
    <div class="nav-item" onclick="scrollToSection('market')"><span class="dot"></span>Market Size</div>
    <div class="nav-item" onclick="scrollToSection('labor')"><span class="dot"></span>Labor Crisis</div>
    <div class="nav-item" onclick="scrollToSection('career')"><span class="dot"></span>Career & Pay</div>
    <div class="nav-item" onclick="scrollToSection('compare')"><span class="dot"></span>NYC vs Charlotte</div>
    <div class="nav-item" onclick="scrollToSection('players')"><span class="dot"></span>Key Players</div>
    <div class="nav-divider">Directories</div>
    <div class="nav-item" onclick="scrollToSection('contacts-ny')"><span class="dot"></span>NY Contacts</div>
    <div class="nav-item" onclick="scrollToSection('contacts-nc')"><span class="dot"></span>NC Contacts</div>
  </nav>
  <div class="sidebar-footer">9 DATA FILES &middot; FEB 2026</div>
</aside>

<main class="main" id="mainScroll">

<!-- ==================== HERO ==================== -->
<div class="hero" id="hero">
  <div class="hero-content">
    <h1>Building <span>Automation</span><br>Industry Overview</h1>
    <p>A $100B+ market doubling by 2030, powered by IoT/AI and constrained by a critical workforce shortage of 480,000+ unfilled jobs.</p>
    <div class="hero-stats">
      <div class="hero-stat">
        <div class="num" data-count="117">$0B</div>
        <div class="label">Market Size (2025)</div>
      </div>
      <div class="hero-stat">
        <div class="num" data-count="13">0%</div>
        <div class="label">CAGR</div>
      </div>
      <div class="hero-stat">
        <div class="num" data-count="480">0K</div>
        <div class="label">Unfilled HVAC Jobs</div>
      </div>
      <div class="hero-stat">
        <div class="num" data-count="55">0</div>
        <div class="label">Avg Tech Age</div>
      </div>
    </div>
  </div>
</div>

<!-- ==================== MARKET SIZE ==================== -->
<div class="section" id="market">
  <div class="section-header">
    <div class="section-tag">01 / Market Intelligence</div>
    <div class="section-title">Market Size & Growth</div>
    <div class="section-desc">The global BAS market is valued at $101-117 billion (2025) and projected to reach $163-221 billion by 2030, with 10.5-13.9% CAGR across research firms.</div>
  </div>

  <div class="card-grid">
    <div class="card">
      <div class="card-label">2025 Market Value</div>
      <div class="card-value">$101-117B</div>
      <div class="card-desc">Consensus range across 5 research firms</div>
    </div>
    <div class="card">
      <div class="card-label">2030 Projected</div>
      <div class="card-value blue">$163-221B</div>
      <div class="card-desc">Roughly doubling within 5 years</div>
    </div>
    <div class="card">
      <div class="card-label">Fastest Segment</div>
      <div class="card-value orange">17.2%</div>
      <div class="card-desc">Building Energy Management Software CAGR</div>
    </div>
  </div>

  <div class="chart-row">
    <div class="chart-container">
      <h3>Market Projections by Source (2025 → 2030)</h3>
      <canvas id="chartMarketProjections"></canvas>
    </div>
    <div class="chart-container">
      <h3>CAGR by Segment</h3>
      <canvas id="chartCagr"></canvas>
    </div>
  </div>

  <div class="chart-row">
    <div class="chart-container">
      <h3>Regional Market Share</h3>
      <canvas id="chartRegional"></canvas>
    </div>
    <div class="chart-container">
      <h3>Growth Drivers</h3>
      <canvas id="chartDrivers"></canvas>
    </div>
  </div>

  <div class="data-toggle" onclick="toggleRawData('raw-market')">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
    View Source Data
  </div>
  <div class="raw-data" id="raw-market"></div>
</div>

<div class="section-line"></div>

<!-- ==================== LABOR CRISIS ==================== -->
<div class="divider-hero" id="labor-divider" style="background-image: none;">
  <div style="position:absolute;inset:0;background:url('https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=1400&q=80') center/cover;opacity:0.1;"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(to bottom,var(--bg-primary),rgba(10,15,20,0.5),var(--bg-primary));"></div>
  <div class="divider-text">
    <h2>The Workforce Crisis</h2>
    <p>An aging workforce, a thin training pipeline, and explosive demand</p>
  </div>
</div>

<div class="section" id="labor">
  <div class="section-header">
    <div class="section-tag">02 / Workforce Analysis</div>
    <div class="section-title">The Labor Gap</div>
    <div class="section-desc">The BAS industry faces a critical constraint: not enough skilled technicians. With 480,000+ unfilled HVAC positions and an average tech age of 55, the gap is widening fast.</div>
  </div>

  <div class="card-grid">
    <div class="card">
      <div class="card-label">Unfilled HVAC Jobs</div>
      <div class="card-value red">480K+</div>
      <div class="card-desc">And growing every year</div>
    </div>
    <div class="card">
      <div class="card-label">Annual Openings</div>
      <div class="card-value orange">42,500</div>
      <div class="card-desc">Many remaining unfilled each year</div>
    </div>
    <div class="card">
      <div class="card-label">Average Tech Age</div>
      <div class="card-value purple">55 yrs</div>
      <div class="card-desc">Nearing mass retirement</div>
    </div>
    <div class="card">
      <div class="card-label">Retiring by 2031</div>
      <div class="card-value red">41%</div>
      <div class="card-desc">Of the construction workforce</div>
    </div>
  </div>

  <!-- Retirement Ratio -->
  <div class="ratio-vis">
    <div>
      <div class="ratio-label">RETIREMENT-TO-REPLACEMENT RATIO: 5:2</div>
      <div class="ratio-dots" style="margin-top:12px;">
        <div class="ratio-dot retire">&#x2716;</div>
        <div class="ratio-dot retire">&#x2716;</div>
        <div class="ratio-dot retire">&#x2716;</div>
        <div class="ratio-dot retire">&#x2716;</div>
        <div class="ratio-dot retire">&#x2716;</div>
        <span style="margin:0 8px;color:var(--text-muted);font-size:18px;">vs</span>
        <div class="ratio-dot replace">&#x2714;</div>
        <div class="ratio-dot replace">&#x2714;</div>
      </div>
    </div>
    <div class="ratio-text">
      For every <strong style="color:var(--red)">5 technicians</strong> who retire, only <strong style="color:var(--accent)">2 new workers</strong> enter the field. The pipeline isn't keeping up with attrition.
    </div>
  </div>

  <div class="chart-row">
    <div class="chart-container">
      <h3>Salary: General HVAC vs BAS Specialist</h3>
      <canvas id="chartSalaryComparison"></canvas>
    </div>
    <div class="chart-container">
      <h3>ROI of Investing in Technician Training</h3>
      <p style="font-size:13px;color:var(--text-secondary);margin:-8px 0 16px;line-height:1.5;">Companies that prioritize BAS technician training programs see measurable gains across the business. These are reported improvements vs. companies with no structured training.</p>
      <canvas id="chartTrainingROI"></canvas>
      <p style="font-size:11px;color:var(--text-muted);margin-top:12px;font-style:italic;">Source: Industry surveys of HVAC/BAS service companies, 2024-2025</p>
    </div>
  </div>

  <!-- Feedback Loop -->
  <div class="feedback-loop">
    <h3>The Feedback Loop</h3>
    <p>The labor shortage is the industry's biggest constraint <em>and</em> its biggest growth catalyst.</p>
    <div class="loop-visual">
      <div class="loop-step">More automation demand</div>
      <div class="loop-arrow">→</div>
      <div class="loop-step">Need skilled techs</div>
      <div class="loop-arrow">→</div>
      <div class="loop-step">Not enough techs</div>
      <div class="loop-arrow">→</div>
      <div class="loop-step">More AI/remote monitoring</div>
      <div class="loop-arrow">→</div>
      <div class="loop-step" style="border-color:var(--accent);">↻ Repeat</div>
    </div>
  </div>

  <div class="data-toggle" onclick="toggleRawData('raw-labor')">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
    View Source Data
  </div>
  <div class="raw-data" id="raw-labor"></div>
</div>

<div class="section-line"></div>

<!-- ==================== CAREER LADDER ==================== -->
<div class="section" id="career">
  <div class="section-header">
    <div class="section-tag">03 / Career Intelligence</div>
    <div class="section-title">Career Ladder & Compensation</div>
    <div class="section-desc">BAS specialization commands 30-60% salary premiums over general HVAC. The career path stretches from installer to integrator, with multiple branching options.</div>
  </div>

  <div class="ladder">
    <div class="ladder-step">
      <div class="ladder-level">8</div>
      <div class="ladder-role">Sales / Solutions</div>
      <div class="ladder-salary">$40K - $200K</div>
    </div>
    <div style="margin-left:20px"><div class="ladder-bar" style="width:88%"></div></div>
    <div class="ladder-step">
      <div class="ladder-level">7</div>
      <div class="ladder-role">Project Manager</div>
      <div class="ladder-salary">$60K - $90K</div>
    </div>
    <div style="margin-left:20px"><div class="ladder-bar" style="width:40%"></div></div>
    <div class="ladder-step">
      <div class="ladder-level">6</div>
      <div class="ladder-role">Integrator</div>
      <div class="ladder-salary">$80K - $150K</div>
    </div>
    <div style="margin-left:20px"><div class="ladder-bar" style="width:72%"></div></div>
    <div class="ladder-step">
      <div class="ladder-level">5</div>
      <div class="ladder-role">Designer</div>
      <div class="ladder-salary">$50K - $90K</div>
    </div>
    <div style="margin-left:20px"><div class="ladder-bar" style="width:38%"></div></div>
    <div class="ladder-step">
      <div class="ladder-level">4</div>
      <div class="ladder-role">Programmer</div>
      <div class="ladder-salary">$60K - $120K</div>
    </div>
    <div style="margin-left:20px"><div class="ladder-bar" style="width:58%"></div></div>
    <div class="ladder-step">
      <div class="ladder-level">3</div>
      <div class="ladder-role">BAS Technician</div>
      <div class="ladder-salary">$60K - $110K</div>
    </div>
    <div style="margin-left:20px"><div class="ladder-bar" style="width:50%"></div></div>
    <div class="ladder-step">
      <div class="ladder-level">2</div>
      <div class="ladder-role">BAS Trainee</div>
      <div class="ladder-salary">$45K - $55K</div>
    </div>
    <div style="margin-left:20px"><div class="ladder-bar" style="width:18%"></div></div>
    <div class="ladder-step">
      <div class="ladder-level">1</div>
      <div class="ladder-role">Installer</div>
      <div class="ladder-salary">$30K - $60K</div>
    </div>
    <div style="margin-left:20px"><div class="ladder-bar" style="width:25%"></div></div>
  </div>

  <div class="chart-row">
    <div class="chart-container">
      <h3>Pay by Employer Type</h3>
      <canvas id="chartEmployerPay"></canvas>
    </div>
    <div class="chart-container">
      <h3>Core Technical Skills</h3>
      <canvas id="chartSkills"></canvas>
    </div>
  </div>

  <h3 style="font-size:15px;color:var(--text-secondary);margin:32px 0 16px;font-family:'JetBrains Mono',monospace;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Key Certifications</h3>
  <div class="cert-badges">
    <div class="cert-badge"><div class="cert-name">Niagara 4 TCP</div><div class="cert-org">Tridium</div></div>
    <div class="cert-badge"><div class="cert-name">EPA 608</div><div class="cert-org">EPA</div></div>
    <div class="cert-badge"><div class="cert-name">CxA</div><div class="cert-org">AABC</div></div>
    <div class="cert-badge"><div class="cert-name">OSHA 10/30</div><div class="cert-org">OSHA</div></div>
    <div class="cert-badge"><div class="cert-name">TAB Cert</div><div class="cert-org">AABC</div></div>
  </div>

  <div class="data-toggle" onclick="toggleRawData('raw-career')">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
    View Source Data
  </div>
  <div class="raw-data" id="raw-career"></div>
</div>

<div class="section-line"></div>

<!-- ==================== NYC vs CHARLOTTE ==================== -->
<div class="split-hero" id="compare-hero">
  <div class="split-side" style="background-image:none;">
    <div style="position:absolute;inset:0;background:url('https://images.unsplash.com/photo-1534430480872-3498386e7856?w=700&q=80') center/cover;opacity:0.2;"></div>
    <div style="position:absolute;inset:0;background:rgba(10,15,20,0.65);"></div>
    <div class="city-name" style="color:var(--blue);">NYC</div>
  </div>
  <div class="split-divider"></div>
  <div class="split-side" style="background-image:none;">
    <div style="position:absolute;inset:0;background:url('https://images.unsplash.com/photo-1577948000111-9c970dfe3743?w=700&q=80') center/cover;opacity:0.2;"></div>
    <div style="position:absolute;inset:0;background:rgba(10,15,20,0.65);"></div>
    <div class="city-name" style="color:var(--orange);">CLT</div>
  </div>
</div>

<div class="section" id="compare">
  <div class="section-header">
    <div class="section-tag">04 / Regional Comparison</div>
    <div class="section-title">NYC vs Charlotte</div>
    <div class="section-desc">NYC offers higher absolute pay but Charlotte wins on purchasing power. NYC is ~41% more expensive overall, with housing 130-170% higher.</div>
  </div>

  <div class="chart-row">
    <div class="chart-container">
      <h3>BAS Technician Salary by Percentile</h3>
      <canvas id="chartCityPay"></canvas>
    </div>
    <div class="chart-container">
      <h3>Cost of Living Difference (NYC vs CLT)</h3>
      <canvas id="chartCOL"></canvas>
    </div>
  </div>

  <!-- Purchasing Power -->
  <div class="card-grid" style="grid-template-columns: 1fr 1fr;">
    <div class="card" style="border-color: var(--blue);">
      <div class="card-label" style="color:var(--blue);">NYC Mid-Level BAS Tech</div>
      <div class="card-value blue">$77,000</div>
      <div class="card-desc">After COL adjustment → <strong style="color:var(--blue)">~$55K</strong> equivalent purchasing power</div>
    </div>
    <div class="card" style="border-color: var(--orange);">
      <div class="card-label" style="color:var(--orange);">Charlotte Mid-Level BAS Tech</div>
      <div class="card-value orange">$57,000</div>
      <div class="card-desc">Better purchasing power at baseline → <strong style="color:var(--orange)">$57K</strong> real value</div>
    </div>
  </div>

  <div class="compare-grid">
    <div class="compare-card ny">
      <h4>&#9670; New York</h4>
      <div class="compare-stat"><span class="k">Key Driver</span><span class="v">LL97 (50K buildings)</span></div>
      <div class="compare-stat"><span class="k">Retrofit Market</span><span class="v">$20B potential</span></div>
      <div class="compare-stat"><span class="k">Jobs Created</span><span class="v">141K by 2030</span></div>
      <div class="compare-stat"><span class="k">Union</span><span class="v">IUOE Local 94</span></div>
      <div class="compare-stat"><span class="k">BAS Jobs (Indeed)</span><span class="v">805+</span></div>
    </div>
    <div class="compare-card nc">
      <h4>&#9670; North Carolina</h4>
      <div class="compare-stat"><span class="k">Key Driver</span><span class="v">Data Center Boom</span></div>
      <div class="compare-stat"><span class="k">DC Investment</span><span class="v">$10B+ (AWS alone)</span></div>
      <div class="compare-stat"><span class="k">OEM HQs</span><span class="v">Honeywell + Trane</span></div>
      <div class="compare-stat"><span class="k">BAS Training</span><span class="v">Wake Tech (NSF)</span></div>
      <div class="compare-stat"><span class="k">DC Power</span><span class="v">3GW → 6GW</span></div>
    </div>
  </div>

  <div class="data-toggle" onclick="toggleRawData('raw-compare')">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
    View Source Data
  </div>
  <div class="raw-data" id="raw-compare"></div>
</div>

<div class="section-line"></div>

<!-- ==================== KEY PLAYERS ==================== -->
<div class="divider-hero" id="players-divider">
  <div style="position:absolute;inset:0;background:url('https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=1400&q=80') center/cover;opacity:0.1;"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(to bottom,var(--bg-primary),rgba(10,15,20,0.5),var(--bg-primary));"></div>
  <div class="divider-text">
    <h2>Industry Landscape</h2>
    <p>OEMs, integrators, and building owners — who hires BAS technicians</p>
  </div>
</div>

<div class="section" id="players">
  <div class="section-header">
    <div class="section-tag">05 / Industry Players</div>
    <div class="section-title">Who Hires BAS Technicians?</div>
    <div class="section-desc">Three employer categories with distinct pay, career paths, and day-to-day work.</div>
  </div>

  <!-- Flow Diagram -->
  <div class="flow-diagram">
    <div class="flow-box">
      <h4>OEM Manufacturers</h4>
      <p>Design &amp; build products<br><span style="color:var(--accent)">12 major companies</span><br>$65K - $110K</p>
    </div>
    <div class="flow-arrow">→</div>
    <div class="flow-box" style="border-color:var(--accent)">
      <h4>Systems Integrators</h4>
      <p>Install, program, service<br><span style="color:var(--accent)">Primary employer of techs</span><br>$45K - $100K</p>
    </div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">
      <h4>Building Owners</h4>
      <p>Operate &amp; maintain<br><span style="color:var(--accent)">Growing in-house teams</span><br>$55K - $120K</p>
    </div>
  </div>

  <div class="chart-row">
    <div class="chart-container">
      <h3>Identified Employers: NY vs NC</h3>
      <canvas id="chartEmployerCount"></canvas>
    </div>
    <div class="chart-container">
      <h3>NC Data Center Investments ($B)</h3>
      <canvas id="chartDataCenter"></canvas>
    </div>
  </div>

  <div class="compare-grid">
    <div class="compare-card ny">
      <h4>&#9670; New York</h4>
      <div class="compare-stat"><span class="k">OEMs (offices)</span><span class="v">6</span></div>
      <div class="compare-stat"><span class="k">Integrators</span><span class="v">16</span></div>
      <div class="compare-stat"><span class="k">Property Mgmt</span><span class="v">11</span></div>
      <div class="compare-stat"><span class="k">Healthcare</span><span class="v">6 systems</span></div>
      <div class="compare-stat"><span class="k">Higher Ed</span><span class="v">6 institutions</span></div>
      <div class="compare-stat"><span class="k">Government</span><span class="v">5 entities</span></div>
    </div>
    <div class="compare-card nc">
      <h4>&#9670; North Carolina</h4>
      <div class="compare-stat"><span class="k">OEMs (inc. 2 HQs)</span><span class="v">5</span></div>
      <div class="compare-stat"><span class="k">Integrators</span><span class="v">14</span></div>
      <div class="compare-stat"><span class="k">Property Mgmt</span><span class="v">8</span></div>
      <div class="compare-stat"><span class="k">Healthcare</span><span class="v">5 systems</span></div>
      <div class="compare-stat"><span class="k">Higher Ed</span><span class="v">6 institutions</span></div>
      <div class="compare-stat"><span class="k">Data Centers</span><span class="v">11+ companies</span></div>
    </div>
  </div>

  <div class="data-toggle" onclick="toggleRawData('raw-players')">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
    View Source Data
  </div>
  <div class="raw-data" id="raw-players"></div>
</div>

<div class="section-line"></div>

<!-- ==================== CONTACT DIRECTORIES ==================== -->
<div class="section" id="contacts-ny">
  <div class="section-header">
    <div class="section-tag">06 / Directory</div>
    <div class="section-title">New York Contacts</div>
    <div class="section-desc">40+ organizations across OEMs, integrators, commercial RE, healthcare, education, and government.</div>
  </div>
  <div class="raw-data open" id="raw-ny-contacts" style="max-height:none;"></div>
</div>

<div class="section-line"></div>

<div class="section" id="contacts-nc">
  <div class="section-header">
    <div class="section-tag">07 / Directory</div>
    <div class="section-title">North Carolina Contacts</div>
    <div class="section-desc">40+ organizations across OEMs, integrators, commercial RE, healthcare, education, government, and data centers.</div>
  </div>
  <div class="raw-data open" id="raw-nc-contacts" style="max-height:none;"></div>
</div>

<div style="height:80px;"></div>

</main>

<script>
// === DATA ===
const DOCS = ''' + docs_json + ''';

// Helper
function getDoc(key) {
  const d = DOCS.find(d => d.key === key);
  return d ? d.content : '';
}

// === INIT MARKDOWN ===
marked.setOptions({ gfm: true, breaks: false });

// Populate raw data sections
document.getElementById('raw-market').innerHTML = marked.parse(getDoc('market-size'));
document.getElementById('raw-labor').innerHTML = marked.parse(getDoc('labor-workforce'));
document.getElementById('raw-career').innerHTML = marked.parse(getDoc('bas-technician'));
document.getElementById('raw-compare').innerHTML = marked.parse(getDoc('nyc-charlotte'));
document.getElementById('raw-players').innerHTML = marked.parse(getDoc('key-players') + '\\n\\n---\\n\\n' + getDoc('employers'));
document.getElementById('raw-ny-contacts').innerHTML = marked.parse(getDoc('ny-contacts'));
document.getElementById('raw-nc-contacts').innerHTML = marked.parse(getDoc('nc-contacts'));

// === NAVIGATION ===
function scrollToSection(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth' });
  // Update active nav
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  event.currentTarget.classList.add('active');
  // Close mobile sidebar
  document.querySelector('.sidebar').classList.remove('open');
  document.querySelector('.overlay').classList.remove('open');
}

function toggleSidebar() {
  document.querySelector('.sidebar').classList.toggle('open');
  document.querySelector('.overlay').classList.toggle('open');
}

function toggleRawData(id) {
  document.getElementById(id).classList.toggle('open');
}

// Highlight active nav on scroll
const sections = ['hero','market','labor','career','compare','players','contacts-ny','contacts-nc'];
const mainEl = document.getElementById('mainScroll');
mainEl.addEventListener('scroll', () => {
  const scrollPos = mainEl.scrollTop + 200;
  let activeIdx = 0;
  sections.forEach((id, i) => {
    const el = document.getElementById(id);
    if (el && el.offsetTop <= scrollPos) activeIdx = i;
  });
  document.querySelectorAll('.nav-item').forEach((n, i) => {
    n.classList.toggle('active', i === activeIdx);
  });
});

// === CHART THEME ===
const chartColors = {
  accent: '#00d4aa',
  accentBright: '#00f5c4',
  blue: '#4da6ff',
  orange: '#ff8c42',
  red: '#ff4d6a',
  purple: '#a78bfa',
  yellow: '#fbbf24',
  gray: '#556677',
  gridColor: 'rgba(30,42,53,0.8)',
  textColor: '#8899a6',
};

Chart.defaults.color = chartColors.textColor;
Chart.defaults.borderColor = chartColors.gridColor;
Chart.defaults.font.family = "'IBM Plex Sans', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.pointStyleWidth = 8;

// === CHARTS ===

// 1. Market Projections
new Chart(document.getElementById('chartMarketProjections'), {
  type: 'bar',
  data: {
    labels: ['MarketsandMarkets', 'Research & Markets', 'PS Market Research', 'The Research Insights'],
    datasets: [
      {
        label: '2025 ($B)',
        data: [101.3, 117.37, 101.3, null],
        backgroundColor: chartColors.accent + '88',
        borderColor: chartColors.accent,
        borderWidth: 1,
      },
      {
        label: '2030 ($B)',
        data: [191.13, 205.55, 220.7, 163.27],
        backgroundColor: chartColors.blue + '88',
        borderColor: chartColors.blue,
        borderWidth: 1,
      }
    ]
  },
  options: {
    responsive: true,
    plugins: { legend: { position: 'top' } },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { callback: v => '$' + v + 'B' },
        grid: { color: chartColors.gridColor }
      },
      x: { grid: { display: false } }
    }
  }
});

// 2. CAGR by Segment
new Chart(document.getElementById('chartCagr'), {
  type: 'bar',
  data: {
    labels: ['Energy Mgmt Software', 'Industrial Apps', 'MarketsandMarkets Overall', 'PS Market Research Overall', 'Research & Markets Overall', 'Mordor Intelligence Overall', 'The Research Insights Overall'],
    datasets: [{
      label: 'CAGR %',
      data: [17.2, 14.7, 13.4, 13.9, 11.78, 11.4, 10.53],
      backgroundColor: [chartColors.orange, chartColors.accent, chartColors.blue, chartColors.blue, chartColors.blue, chartColors.blue, chartColors.blue],
      borderWidth: 0,
      borderRadius: 4,
    }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    plugins: { legend: { display: false } },
    scales: {
      x: {
        beginAtZero: true,
        ticks: { callback: v => v + '%' },
        grid: { color: chartColors.gridColor }
      },
      y: { grid: { display: false } }
    }
  }
});

// 3. Regional Market Share
new Chart(document.getElementById('chartRegional'), {
  type: 'doughnut',
  data: {
    labels: ['North America', 'Europe', 'Asia Pacific', 'Rest of World'],
    datasets: [{
      data: [34.2, 25, 28, 12.8],
      backgroundColor: [chartColors.accent, chartColors.blue, chartColors.orange, chartColors.gray],
      borderWidth: 0,
    }]
  },
  options: {
    responsive: true,
    cutout: '65%',
    plugins: {
      legend: { position: 'bottom' }
    }
  }
});

// 4. Growth Drivers (horizontal bar)
new Chart(document.getElementById('chartDrivers'), {
  type: 'bar',
  data: {
    labels: ['IoT/AI Integration', 'Energy Regulations', 'Smart City Investment', 'Occupant Comfort', 'Data-Driven Decisions', 'Sustainability Mandates'],
    datasets: [{
      label: 'Impact Score',
      data: [95, 88, 82, 75, 72, 70],
      backgroundColor: chartColors.accent + '66',
      borderColor: chartColors.accent,
      borderWidth: 1,
      borderRadius: 4,
    }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    plugins: { legend: { display: false } },
    scales: {
      x: { display: false, max: 100 },
      y: { grid: { display: false } }
    }
  }
});

// 5. Salary Comparison
new Chart(document.getElementById('chartSalaryComparison'), {
  type: 'bar',
  data: {
    labels: ['General HVAC', 'BAS Specialist', 'Data Center BAS'],
    datasets: [
      {
        label: 'Low ($K)',
        data: [55, 70, 70],
        backgroundColor: chartColors.gray + '88',
        borderWidth: 0,
        borderRadius: 4,
      },
      {
        label: 'High ($K)',
        data: [70, 110, 120],
        backgroundColor: chartColors.accent + '88',
        borderColor: chartColors.accent,
        borderWidth: 1,
        borderRadius: 4,
      }
    ]
  },
  options: {
    responsive: true,
    plugins: { legend: { position: 'top' } },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { callback: v => '$' + v + 'K' },
        grid: { color: chartColors.gridColor }
      },
      x: { grid: { display: false } }
    }
  }
});

// 6. Training ROI
new Chart(document.getElementById('chartTrainingROI'), {
  type: 'bar',
  data: {
    labels: [
      '+24% Profit Margins',
      '+30-50% Employee Retention',
      '+20% Faster Service Calls',
      '+15% Customer Satisfaction'
    ],
    datasets: [{
      label: 'Improvement vs. No Training',
      data: [24, 40, 20, 15],
      backgroundColor: [chartColors.accent + 'cc', chartColors.blue + 'cc', chartColors.orange + 'cc', chartColors.purple + 'cc'],
      borderWidth: 0,
      borderRadius: 4,
    }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: function(ctx) {
            return '+' + ctx.raw + '% improvement over companies without structured training';
          }
        }
      }
    },
    scales: {
      x: {
        beginAtZero: true,
        max: 50,
        ticks: { callback: v => '+' + v + '%' },
        grid: { color: chartColors.gridColor }
      },
      y: {
        grid: { display: false },
        ticks: { font: { size: 12 } }
      }
    }
  }
});

// 7. Pay by Employer Type
new Chart(document.getElementById('chartEmployerPay'), {
  type: 'bar',
  data: {
    labels: ['Data Centers', 'OEM Manufacturer', 'Integrator (Large)', 'Property Mgmt', 'Healthcare/Govt', 'Integrator (Small)'],
    datasets: [
      {
        label: 'Low ($K)',
        data: [70, 65, 55, 60, 55, 45],
        backgroundColor: chartColors.gray + '66',
        borderWidth: 0,
        borderRadius: 4,
      },
      {
        label: 'High ($K)',
        data: [120, 110, 100, 95, 90, 85],
        backgroundColor: chartColors.accent + '88',
        borderColor: chartColors.accent,
        borderWidth: 1,
        borderRadius: 4,
      }
    ]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    plugins: { legend: { position: 'top' } },
    scales: {
      x: {
        beginAtZero: true,
        ticks: { callback: v => '$' + v + 'K' },
        grid: { color: chartColors.gridColor }
      },
      y: { grid: { display: false } }
    }
  }
});

// 8. Skills Radar
new Chart(document.getElementById('chartSkills'), {
  type: 'radar',
  data: {
    labels: ['Electrical', 'HVAC Systems', 'DDC/Controls', 'IT/Networking', 'Mechanical'],
    datasets: [{
      label: 'BAS Technician Skill Profile',
      data: [85, 90, 95, 75, 70],
      backgroundColor: chartColors.accent + '22',
      borderColor: chartColors.accent,
      borderWidth: 2,
      pointBackgroundColor: chartColors.accent,
      pointRadius: 4,
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: {
      r: {
        beginAtZero: true, max: 100,
        grid: { color: chartColors.gridColor },
        angleLines: { color: chartColors.gridColor },
        pointLabels: { color: chartColors.textColor, font: { size: 12 } },
        ticks: { display: false }
      }
    }
  }
});

// 9. NYC vs Charlotte Pay
new Chart(document.getElementById('chartCityPay'), {
  type: 'bar',
  data: {
    labels: ['25th Percentile', 'Average', '75th Percentile', '90th Percentile'],
    datasets: [
      {
        label: 'NYC ($K)',
        data: [62, 77, 97, 119],
        backgroundColor: chartColors.blue + '88',
        borderColor: chartColors.blue,
        borderWidth: 1,
        borderRadius: 4,
      },
      {
        label: 'Charlotte ($K)',
        data: [50, 57, 72, null],
        backgroundColor: chartColors.orange + '88',
        borderColor: chartColors.orange,
        borderWidth: 1,
        borderRadius: 4,
      }
    ]
  },
  options: {
    responsive: true,
    plugins: { legend: { position: 'top' } },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { callback: v => '$' + v + 'K' },
        grid: { color: chartColors.gridColor }
      },
      x: { grid: { display: false } }
    }
  }
});

// 10. COL Comparison
new Chart(document.getElementById('chartCOL'), {
  type: 'bar',
  data: {
    labels: ['Housing', 'Overall', 'Transportation', 'Groceries', 'Utilities', 'Healthcare'],
    datasets: [{
      label: 'NYC Premium Over Charlotte (%)',
      data: [150, 41, 25, 20, 17, 12],
      backgroundColor: [chartColors.red + '88', chartColors.orange + '88', chartColors.yellow + '88', chartColors.blue + '88', chartColors.purple + '88', chartColors.accent + '88'],
      borderWidth: 0,
      borderRadius: 4,
    }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    plugins: { legend: { display: false } },
    scales: {
      x: {
        beginAtZero: true,
        ticks: { callback: v => '+' + v + '%' },
        grid: { color: chartColors.gridColor }
      },
      y: { grid: { display: false } }
    }
  }
});

// 11. Employer Count by Category
new Chart(document.getElementById('chartEmployerCount'), {
  type: 'bar',
  data: {
    labels: ['Integrators', 'Property Mgmt', 'Healthcare', 'Higher Ed', 'OEMs', 'Government', 'Data Centers'],
    datasets: [
      {
        label: 'New York',
        data: [16, 11, 6, 6, 6, 5, 0],
        backgroundColor: chartColors.blue + '88',
        borderColor: chartColors.blue,
        borderWidth: 1,
        borderRadius: 4,
      },
      {
        label: 'North Carolina',
        data: [14, 8, 5, 6, 5, 5, 11],
        backgroundColor: chartColors.orange + '88',
        borderColor: chartColors.orange,
        borderWidth: 1,
        borderRadius: 4,
      }
    ]
  },
  options: {
    responsive: true,
    plugins: { legend: { position: 'top' } },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { stepSize: 2 },
        grid: { color: chartColors.gridColor }
      },
      x: { grid: { display: false } }
    }
  }
});

// 12. NC Data Center Investment
new Chart(document.getElementById('chartDataCenter'), {
  type: 'bar',
  data: {
    labels: ['AWS', 'Energy Storage', 'Google', 'Apple', 'Microsoft'],
    datasets: [{
      label: 'Investment ($B)',
      data: [10, 19.2, 1.2, 0.175, 0.027],
      backgroundColor: [chartColors.orange + 'cc', chartColors.accent + 'cc', chartColors.blue + 'cc', chartColors.purple + 'cc', chartColors.yellow + 'cc'],
      borderWidth: 0,
      borderRadius: 4,
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { callback: v => '$' + v + 'B' },
        grid: { color: chartColors.gridColor }
      },
      x: { grid: { display: false } }
    }
  }
});

// === ANIMATED HERO COUNTERS ===
function animateCounters() {
  document.querySelectorAll('.hero-stat .num').forEach(el => {
    const target = parseInt(el.dataset.count);
    const prefix = el.textContent.includes('$') ? '$' : '';
    const suffix = el.textContent.includes('B') ? 'B' : el.textContent.includes('%') ? '%' : el.textContent.includes('K') ? 'K' : '';
    let current = 0;
    const step = target / 40;
    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      el.textContent = prefix + Math.round(current) + suffix;
    }, 30);
  });
}
setTimeout(animateCounters, 300);
</script>
</body>
</html>'''

output_path = os.path.join(BASE, "viewer.html")
with open(output_path, "w") as f:
    f.write(HTML)

size = os.path.getsize(output_path)
print(f"Built viewer.html ({size:,} bytes / {size/1024:.0f}KB)")
print(f"Open: file://{output_path}")
