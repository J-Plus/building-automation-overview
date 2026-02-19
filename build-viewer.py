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
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
:root {
  --bg-primary: #f5f5f7;
  --bg-secondary: rgba(255,255,255,0.72);
  --bg-tertiary: rgba(255,255,255,0.5);
  --bg-card: rgba(255,255,255,0.6);
  --bg-hover: rgba(0,0,0,0.03);
  --border: rgba(0,0,0,0.08);
  --border-strong: rgba(0,0,0,0.12);
  --glass: rgba(255,255,255,0.65);
  --glass-border: rgba(255,255,255,0.5);
  --accent: #0071e3;
  --accent-light: #e8f2ff;
  --accent-dim: rgba(0,113,227,0.08);
  --orange: #e8590c;
  --red: #e5383b;
  --blue: #0071e3;
  --purple: #7c3aed;
  --yellow: #ca8a04;
  --green: #16a34a;
  --text-primary: #1d1d1f;
  --text-secondary: #6e6e73;
  --text-muted: #aeaeb2;
  --sidebar-w: 240px;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  display: flex;
  height: 100vh;
  overflow: hidden;
  -webkit-font-smoothing: antialiased;
}

/* ===== SIDEBAR (frosted glass) ===== */
.sidebar {
  width: var(--sidebar-w);
  min-width: var(--sidebar-w);
  background: var(--bg-secondary);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  z-index: 100;
  transition: transform 0.3s ease;
}
.sidebar-header {
  padding: 24px 20px 18px;
  border-bottom: 1px solid var(--border);
}
.sidebar-header h1 {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.4;
  letter-spacing: -0.2px;
}
.sidebar-header .sub {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 4px;
  font-weight: 500;
}
.nav-list { flex: 1; overflow-y: auto; padding: 8px 0; }
.nav-item {
  display: flex; align-items: center;
  padding: 8px 20px; cursor: pointer;
  font-size: 13px; font-weight: 400;
  color: var(--text-secondary);
  border-radius: 0; margin: 0;
  transition: all 0.15s; user-select: none;
}
.nav-item:hover { background: var(--bg-hover); color: var(--text-primary); }
.nav-item.active {
  background: var(--accent-dim); color: var(--accent);
  font-weight: 600;
}
.nav-item .dot {
  width: 5px; height: 5px; border-radius: 50%;
  background: var(--text-muted); margin-right: 10px; flex-shrink: 0;
  transition: all 0.15s;
}
.nav-item.active .dot { background: var(--accent); }

.nav-divider {
  padding: 16px 20px 6px;
  font-size: 11px; letter-spacing: 0.5px;
  color: var(--text-muted); text-transform: uppercase;
  font-weight: 600;
}
.sidebar-footer {
  padding: 14px 20px; border-top: 1px solid var(--border);
  font-size: 11px; color: var(--text-muted); font-weight: 500;
}

/* ===== MAIN ===== */
.main { flex: 1; overflow-y: auto; scroll-behavior: smooth; background: var(--bg-primary); }

/* ===== HERO ===== */
.hero {
  position: relative; height: 440px;
  background: var(--bg-primary);
  overflow: hidden; display: flex; align-items: center; justify-content: center;
}
.hero::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: linear-gradient(135deg, #dbeafe 0%, #ede9fe 50%, #fce7f3 100%);
  opacity: 0.7;
}
.hero::after {
  content: ''; position: absolute; inset: 0; z-index: 1;
  background: url('https://images.unsplash.com/photo-1486325212027-8081e485255e?w=1400&q=80') center/cover;
  opacity: 0.05; pointer-events: none;
}
.hero-content { position: relative; z-index: 2; text-align: center; padding: 0 40px; }
.hero-content h1 {
  font-size: 48px; font-weight: 700; color: var(--text-primary);
  margin-bottom: 12px; letter-spacing: -1px; line-height: 1.1;
}
.hero-content h1 span { color: var(--accent); }
.hero-content p {
  font-size: 18px; color: var(--text-secondary);
  max-width: 560px; margin: 0 auto 36px; line-height: 1.5;
  font-weight: 400;
}
.hero-stats {
  display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;
}
.hero-stat {
  text-align: center;
  background: var(--glass);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 20px 28px;
  min-width: 140px;
}
.hero-stat .num {
  font-family: 'DM Mono', monospace;
  font-size: 28px; font-weight: 500; color: var(--text-primary);
}
.hero-stat .label {
  font-size: 11px; color: var(--text-muted);
  text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;
  font-weight: 500;
}

/* ===== SECTIONS ===== */
.section {
  padding: 72px 48px;
  max-width: 1100px;
  margin: 0 auto;
}
.section-header { margin-bottom: 40px; }
.section-tag {
  font-family: 'DM Mono', monospace;
  font-size: 12px; letter-spacing: 0.5px;
  color: var(--accent); margin-bottom: 8px; font-weight: 500;
}
.section-title {
  font-size: 32px; font-weight: 700; color: var(--text-primary);
  margin-bottom: 10px; letter-spacing: -0.5px;
}
.section-desc {
  font-size: 16px; color: var(--text-secondary); line-height: 1.6;
  max-width: 680px;
}

/* ===== DIVIDER HERO ===== */
.divider-hero {
  position: relative; height: 200px;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
  background: linear-gradient(135deg, #f0f4ff 0%, #fdf2f8 100%);
}
.divider-hero::before {
  content: ''; position: absolute; inset: 0;
  background-size: cover; background-position: center;
  opacity: 0.08;
}
.divider-hero::after {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(to bottom, var(--bg-primary) 0%, transparent 30%, transparent 70%, var(--bg-primary) 100%);
}
.divider-hero .divider-text { position: relative; z-index: 2; text-align: center; }
.divider-hero .divider-text h2 {
  font-size: 26px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.3px;
}
.divider-hero .divider-text p {
  font-size: 15px; color: var(--text-secondary); margin-top: 6px;
}

/* ===== CARDS (glass) ===== */
.card-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px; margin: 24px 0;
}
.card {
  background: var(--bg-card);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.25s ease;
}
.card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.06); border-color: var(--border-strong); }
.card-label {
  font-size: 12px; letter-spacing: 0.3px;
  text-transform: uppercase; color: var(--text-muted);
  margin-bottom: 8px; font-weight: 600;
}
.card-value {
  font-family: 'DM Mono', monospace;
  font-size: 30px; font-weight: 500; color: var(--accent);
}
.card-value.orange { color: var(--orange); }
.card-value.red { color: var(--red); }
.card-value.blue { color: var(--blue); }
.card-value.purple { color: var(--purple); }
.card-desc {
  font-size: 13px; color: var(--text-secondary);
  margin-top: 8px; line-height: 1.5;
}

/* ===== CHARTS (glass) ===== */
.chart-container {
  background: var(--bg-card);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 28px;
  margin: 24px 0;
}
.chart-container h3 {
  font-size: 14px; font-weight: 600; letter-spacing: -0.1px;
  color: var(--text-primary); margin-bottom: 16px;
}
.chart-row {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 16px; margin: 24px 0;
}
.chart-row canvas { max-height: 320px; }

/* ===== FEEDBACK LOOP ===== */
.feedback-loop {
  background: linear-gradient(135deg, rgba(0,113,227,0.04), rgba(124,58,237,0.04));
  border: 1px solid rgba(0,113,227,0.12);
  border-radius: 20px;
  padding: 44px;
  margin: 40px 0;
  text-align: center;
}
.feedback-loop h3 {
  font-size: 22px; font-weight: 700; color: var(--text-primary); margin-bottom: 12px; letter-spacing: -0.3px;
}
.feedback-loop p {
  font-size: 15px; color: var(--text-secondary); line-height: 1.7;
  max-width: 560px; margin: 0 auto;
}
.loop-visual {
  display: flex; align-items: center; justify-content: center;
  gap: 8px; margin-top: 28px; flex-wrap: wrap;
}
.loop-step {
  background: white;
  border: 1px solid var(--border);
  border-radius: 10px; padding: 10px 18px;
  font-family: 'DM Mono', monospace;
  font-size: 12px; color: var(--text-primary); font-weight: 500;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.loop-arrow { color: var(--accent); font-size: 18px; }

/* ===== RATIO VIS ===== */
.ratio-vis {
  display: flex; align-items: center; gap: 32px;
  margin: 24px 0; padding: 32px;
  background: var(--bg-card);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border);
  border-radius: 16px;
}
.ratio-dots { display: flex; gap: 12px; align-items: center; }
.ratio-dot {
  width: 36px; height: 36px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px;
}
.ratio-dot.retire { background: rgba(229,56,59,0.1); border: 2px solid var(--red); }
.ratio-dot.replace { background: rgba(22,163,74,0.1); border: 2px solid var(--green); }
.ratio-label {
  font-family: 'DM Mono', monospace;
  font-size: 12px; color: var(--text-secondary); font-weight: 500;
}
.ratio-text { font-size: 14px; color: var(--text-secondary); line-height: 1.6; }

/* ===== CAREER LADDER ===== */
.ladder { display: flex; flex-direction: column; gap: 6px; margin: 24px 0; }
.ladder-step {
  display: flex; align-items: center; gap: 16px;
  padding: 14px 20px;
  background: white;
  border: 1px solid var(--border);
  border-radius: 12px;
  transition: all 0.2s;
}
.ladder-step:hover { transform: translateX(4px); box-shadow: 0 4px 16px rgba(0,0,0,0.05); }
.ladder-level {
  font-family: 'DM Mono', monospace;
  font-size: 12px; color: var(--text-muted); font-weight: 500;
  width: 20px; text-align: center;
}
.ladder-role { font-weight: 600; font-size: 14px; color: var(--text-primary); flex: 1; }
.ladder-salary {
  font-family: 'DM Mono', monospace;
  font-size: 13px; color: var(--accent); font-weight: 500;
}
.ladder-bar {
  height: 4px; border-radius: 2px;
  background: linear-gradient(90deg, var(--accent), #764ba2);
  opacity: 0.35;
}

/* ===== SPLIT COMPARE ===== */
.split-hero {
  display: grid; grid-template-columns: 1fr 1fr;
  height: 180px; position: relative; overflow: hidden;
}
.split-side {
  position: relative; display: flex; align-items: center;
  justify-content: center; overflow: hidden;
}
.split-side::before {
  content: ''; position: absolute; inset: 0;
  background-size: cover; background-position: center;
  opacity: 0.35;
}
.split-side::after {
  content: ''; position: absolute; inset: 0;
  background: rgba(255,255,255,0.5);
  backdrop-filter: blur(2px);
}
.split-side .city-name {
  position: relative; z-index: 2;
  font-size: 28px; font-weight: 700;
  letter-spacing: -0.5px;
}
.split-divider {
  position: absolute; left: 50%; top: 0; bottom: 0;
  width: 2px; background: white; z-index: 3; opacity: 0.8;
}

/* ===== FLOW DIAGRAM ===== */
.flow-diagram {
  display: flex; align-items: center; justify-content: center;
  gap: 16px; margin: 32px 0; flex-wrap: wrap;
}
.flow-box {
  background: white;
  border: 1px solid var(--border);
  border-radius: 16px; padding: 20px 24px;
  text-align: center; min-width: 180px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.flow-box h4 {
  font-size: 12px; color: var(--accent);
  text-transform: uppercase; letter-spacing: 0.5px;
  margin-bottom: 8px; font-weight: 700;
}
.flow-box p { font-size: 13px; color: var(--text-secondary); line-height: 1.5; }
.flow-arrow { font-size: 24px; color: var(--text-muted); }

/* ===== STAT COMPARE CARDS ===== */
.compare-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 24px 0; }
.compare-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: 16px; padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.compare-card h4 { font-size: 15px; font-weight: 700; margin-bottom: 16px; }
.compare-card.ny h4 { color: var(--blue); }
.compare-card.nc h4 { color: var(--orange); }
.compare-stat {
  display: flex; justify-content: space-between;
  padding: 8px 0; border-bottom: 1px solid var(--border);
  font-size: 13px;
}
.compare-stat:last-child { border-bottom: none; }
.compare-stat .k { color: var(--text-secondary); }
.compare-stat .v { color: var(--text-primary); font-weight: 600; font-family: 'DM Mono', monospace; font-size: 12px; }

/* ===== CERT BADGES ===== */
.cert-badges { display: flex; gap: 10px; flex-wrap: wrap; margin: 24px 0; }
.cert-badge {
  background: white;
  border: 1px solid var(--border);
  border-radius: 12px; padding: 12px 18px;
  text-align: center; min-width: 120px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.cert-badge .cert-name {
  font-family: 'DM Mono', monospace;
  font-size: 12px; font-weight: 500; color: var(--accent);
}
.cert-badge .cert-org { font-size: 10px; color: var(--text-muted); margin-top: 4px; font-weight: 500; }

/* ===== DATA TOGGLE ===== */
.data-toggle {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 8px 18px; margin: 20px 0;
  background: white;
  border: 1px solid var(--border);
  border-radius: 10px; cursor: pointer;
  font-size: 12px; color: var(--text-secondary);
  transition: all 0.2s; font-weight: 500;
}
.data-toggle:hover { border-color: var(--accent); color: var(--accent); box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
.data-toggle svg { width: 14px; height: 14px; }
.raw-data {
  display: none;
  background: white;
  border: 1px solid var(--border);
  border-radius: 16px; padding: 32px;
  margin: 12px 0 32px;
  max-height: 600px; overflow-y: auto;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.raw-data.open { display: block; }

/* Markdown inside raw-data */
.raw-data h1 { font-size: 24px; font-weight: 700; color: var(--text-primary); margin: 0 0 12px; padding-bottom: 12px; border-bottom: 2px solid var(--accent); }
.raw-data h2 { font-size: 18px; font-weight: 600; color: var(--accent); margin: 28px 0 12px; }
.raw-data h3 { font-size: 15px; font-weight: 600; color: var(--text-primary); margin: 20px 0 10px; }
.raw-data p { font-size: 14px; line-height: 1.7; margin-bottom: 12px; color: var(--text-secondary); }
.raw-data ul, .raw-data ol { margin: 0 0 12px 20px; font-size: 14px; line-height: 1.7; }
.raw-data li { margin-bottom: 4px; color: var(--text-secondary); }
.raw-data li::marker { color: var(--accent); }
.raw-data strong { color: var(--text-primary); }
.raw-data a { color: var(--accent); text-decoration: none; }
.raw-data blockquote { border-left: 3px solid var(--accent); padding: 8px 16px; margin: 12px 0; background: var(--accent-dim); border-radius: 0 8px 8px 0; font-style: italic; color: var(--text-secondary); font-size: 13px; }
.raw-data table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 12px; }
.raw-data th { background: var(--bg-primary); color: var(--accent); font-weight: 600; text-align: left; padding: 8px 10px; border: 1px solid var(--border); font-size: 11px; }
.raw-data td { padding: 7px 10px; border: 1px solid var(--border); vertical-align: top; color: var(--text-secondary); }
.raw-data tbody tr:hover { background: var(--bg-hover); }
.raw-data code { font-family: 'DM Mono', monospace; font-size: 12px; background: var(--bg-primary); padding: 1px 5px; border-radius: 4px; color: var(--accent); }
.raw-data pre { background: var(--bg-primary); border: 1px solid var(--border); border-radius: 10px; padding: 12px; overflow-x: auto; margin: 12px 0; }
.raw-data pre code { background: none; padding: 0; color: var(--text-primary); }

/* Section dividers */
.section-line {
  height: 1px;
  background: linear-gradient(to right, transparent, var(--border-strong), transparent);
  margin: 0; max-width: 1100px; margin-left: auto; margin-right: auto;
}

/* ===== HAMBURGER ===== */
.hamburger {
  display: none; position: fixed; top: 14px; left: 14px; z-index: 200;
  width: 38px; height: 38px;
  background: var(--glass); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border);
  border-radius: 10px; cursor: pointer;
  align-items: center; justify-content: center;
}
.hamburger span { display: block; width: 16px; height: 1.5px; background: var(--text-primary); margin: 3px auto; border-radius: 1px; }
.overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.2); backdrop-filter: blur(4px); z-index: 90; }

@media (max-width: 900px) {
  .sidebar { position: fixed; left: 0; top: 0; bottom: 0; transform: translateX(-100%); }
  .sidebar.open { transform: translateX(0); }
  .overlay.open { display: block; }
  .hamburger { display: flex; }
  .section { padding: 40px 20px; }
  .hero-content h1 { font-size: 32px; }
  .hero-stats { gap: 10px; }
  .hero-stat .num { font-size: 22px; }
  .hero-stat { min-width: 110px; padding: 14px 18px; }
  .chart-row { grid-template-columns: 1fr; }
  .compare-grid { grid-template-columns: 1fr; }
  .split-hero { grid-template-columns: 1fr; height: 160px; }
  .card-grid { grid-template-columns: 1fr; }
}

/* Scrollbar */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.25); }

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
      <h3>Market Projections by Research Firm</h3>
      <p style="font-size:13px;color:var(--text-secondary);margin:-8px 0 16px;line-height:1.5;">How 4 major research firms project BAS market value. Teal bars = 2025 estimates, blue bars = 2030 projections. All sources agree: the market roughly doubles.</p>
      <canvas id="chartMarketProjections"></canvas>
      <p style="font-size:11px;color:var(--text-muted);margin-top:12px;font-style:italic;">Sources: MarketsandMarkets, Research & Markets, PS Market Research, The Research Insights</p>
    </div>
    <div class="chart-container">
      <h3>Annual Growth Rate (CAGR) by Segment</h3>
      <p style="font-size:13px;color:var(--text-secondary);margin:-8px 0 16px;line-height:1.5;">Compound annual growth rates. Orange = fastest-growing segments. Blue = overall market CAGR from different research firms.</p>
      <canvas id="chartCagr"></canvas>
    </div>
  </div>

  <div class="chart-row">
    <div class="chart-container">
      <h3>Regional Market Share (2024)</h3>
      <p style="font-size:13px;color:var(--text-secondary);margin:-8px 0 16px;line-height:1.5;">North America leads at 34.2%. Asia-Pacific is the fastest-growing region driven by rapid urbanization.</p>
      <canvas id="chartRegional"></canvas>
      <p style="font-size:11px;color:var(--text-muted);margin-top:12px;font-style:italic;">Source: MarketsandMarkets, 2024</p>
    </div>
    <div class="chart-container">
      <h3>What's Driving Market Growth?</h3>
      <p style="font-size:13px;color:var(--text-secondary);margin:-8px 0 16px;line-height:1.5;">Ranked by relative impact based on frequency of citation across industry reports. IoT/AI integration is the top driver.</p>
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
<div class="divider-hero" id="labor-divider">
  <div style="position:absolute;inset:0;background:url('https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=1400&q=80') center/cover;opacity:0.06;"></div>
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
      For every <strong style="color:var(--red)">5 technicians</strong> who retire, only <strong style="color:var(--green)">2 new workers</strong> enter the field. The pipeline isn't keeping up with attrition.
    </div>
  </div>

  <div class="chart-row">
    <div class="chart-container">
      <h3>The BAS Specialization Premium</h3>
      <p style="font-size:13px;color:var(--text-secondary);margin:-8px 0 16px;line-height:1.5;">BAS specialists earn 30-60% more than general HVAC techs. Data center roles command the highest premiums due to mission-critical precision cooling.</p>
      <canvas id="chartSalaryComparison"></canvas>
      <p style="font-size:11px;color:var(--text-muted);margin-top:12px;font-style:italic;">Gray = salary floor, teal = salary ceiling for each specialization</p>
    </div>
    <div class="chart-container">
      <h3>ROI of Investing in Technician Training</h3>
      <p style="font-size:13px;color:var(--text-secondary);margin:-8px 0 16px;line-height:1.5;">Companies that prioritize BAS technician training programs see measurable gains across the business. These are reported improvements vs. companies with no structured training.</p>
      <canvas id="chartTrainingROI"></canvas>
      <p style="font-size:11px;color:var(--text-muted);margin-top:12px;font-style:italic;">Source: Industry surveys of HVAC/BAS service companies, 2024-2025</p>
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
      <h3>BAS Technician Salary Range by Employer Type</h3>
      <p style="font-size:13px;color:var(--text-secondary);margin:-8px 0 16px;line-height:1.5;">Where you work matters as much as what you know. Data centers pay the most; small integrators offer the most autonomy but lower pay. Gray = floor, teal = ceiling.</p>
      <canvas id="chartEmployerPay"></canvas>
    </div>
    <div class="chart-container">
      <h3>Core Skill Areas for BAS Technicians</h3>
      <p style="font-size:13px;color:var(--text-secondary);margin:-8px 0 16px;line-height:1.5;">Relative importance of each skill domain. DDC/Controls programming is the most critical differentiator. IT/Networking is the fastest-growing requirement.</p>
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
    <div class="city-name" style="color:var(--blue);">NYC</div>
  </div>
  <div class="split-divider"></div>
  <div class="split-side" style="background-image:none;">
    <div style="position:absolute;inset:0;background:url('https://images.unsplash.com/photo-1577948000111-9c970dfe3743?w=700&q=80') center/cover;opacity:0.35;"></div>
    <div style="position:absolute;inset:0;background:rgba(255,255,255,0.5);backdrop-filter:blur(2px);"></div>
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
      <h3>BAS Technician Salary: NYC vs Charlotte</h3>
      <p style="font-size:13px;color:var(--text-secondary);margin:-8px 0 16px;line-height:1.5;">NYC pays 20-39% more in absolute dollars at every level. The gap widens at senior levels. Charlotte 90th percentile data unavailable.</p>
      <canvas id="chartCityPay"></canvas>
      <p style="font-size:11px;color:var(--text-muted);margin-top:12px;font-style:italic;">Sources: Salary.com, Glassdoor, ZipRecruiter (2025)</p>
    </div>
    <div class="chart-container">
      <h3>How Much More Expensive is NYC?</h3>
      <p style="font-size:13px;color:var(--text-secondary);margin:-8px 0 16px;line-height:1.5;">NYC cost of living premium over Charlotte by category. Housing is the biggest gap at +150%, which alone eats the entire salary premium.</p>
      <canvas id="chartCOL"></canvas>
      <p style="font-size:11px;color:var(--text-muted);margin-top:12px;font-style:italic;">Sources: Numbeo, BestPlaces.net</p>
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
<div class="divider-hero" id="players-divider" style="background:linear-gradient(135deg,#f0fdf4 0%,#ecfeff 100%);">
  <div style="position:absolute;inset:0;background:url('https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=1400&q=80') center/cover;opacity:0.06;"></div>
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
      <h3>BAS Employers Identified: NY vs NC by Category</h3>
      <p style="font-size:13px;color:var(--text-secondary);margin:-8px 0 16px;line-height:1.5;">Number of companies we identified in each category. NY leads in integrators and property management. NC dominates in data centers — a segment that barely exists in NYC.</p>
      <canvas id="chartEmployerCount"></canvas>
    </div>
    <div class="chart-container">
      <h3>North Carolina Data Center Investment</h3>
      <p style="font-size:13px;color:var(--text-secondary);margin:-8px 0 16px;line-height:1.5;">Announced/committed investments by major tech companies in NC. This boom is creating massive demand for HVAC/BAS technicians who can handle precision cooling.</p>
      <canvas id="chartDataCenter"></canvas>
      <p style="font-size:11px;color:var(--text-muted);margin-top:12px;font-style:italic;">Note: Energy Storage Solutions ($19.2B) is a planned project; others are committed/under construction</p>
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
  accent: '#0071e3',
  accentBright: '#2997ff',
  blue: '#0071e3',
  orange: '#e8590c',
  red: '#e5383b',
  purple: '#7c3aed',
  yellow: '#ca8a04',
  green: '#16a34a',
  gray: '#aeaeb2',
  gridColor: 'rgba(0,0,0,0.06)',
  textColor: '#6e6e73',
};

Chart.defaults.color = chartColors.textColor;
Chart.defaults.borderColor = chartColors.gridColor;
Chart.defaults.font.family = "'DM Sans', -apple-system, sans-serif";
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
        label: '2025 Estimate',
        data: [101.3, 117.37, 101.3, null],
        backgroundColor: chartColors.accent + '88',
        borderColor: chartColors.accent,
        borderWidth: 1,
        borderRadius: 4,
      },
      {
        label: '2030 Projection',
        data: [191.13, 205.55, 220.7, 163.27],
        backgroundColor: chartColors.blue + '88',
        borderColor: chartColors.blue,
        borderWidth: 1,
        borderRadius: 4,
      }
    ]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      tooltip: {
        callbacks: {
          label: ctx => ctx.dataset.label + ': $' + ctx.raw + ' billion'
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: { display: true, text: 'Market Value (USD Billions)', color: chartColors.textColor, font: { size: 11 } },
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
    labels: [
      'Energy Mgmt Software  17.2%',
      'Industrial Applications  14.7%',
      'PS Market Research  13.9%',
      'MarketsandMarkets  13.4%',
      'Research & Markets  11.8%',
      'Mordor Intelligence  11.4%',
      'The Research Insights  10.5%'
    ],
    datasets: [{
      data: [17.2, 14.7, 13.9, 13.4, 11.78, 11.4, 10.53],
      backgroundColor: [chartColors.orange + 'cc', chartColors.orange + '99', chartColors.blue + '88', chartColors.blue + '88', chartColors.blue + '88', chartColors.blue + '88', chartColors.blue + '88'],
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
          label: ctx => 'Annual growth rate: ' + ctx.raw + '% per year (2025-2030)'
        }
      }
    },
    scales: {
      x: {
        beginAtZero: true,
        title: { display: true, text: 'CAGR %', color: chartColors.textColor, font: { size: 11 } },
        ticks: { callback: v => v + '%' },
        grid: { color: chartColors.gridColor }
      },
      y: { grid: { display: false }, ticks: { font: { size: 11 } } }
    }
  }
});

// 3. Regional Market Share
new Chart(document.getElementById('chartRegional'), {
  type: 'doughnut',
  data: {
    labels: ['North America — 34.2%', 'Asia Pacific — 28%', 'Europe — 25%', 'Rest of World — 12.8%'],
    datasets: [{
      data: [34.2, 28, 25, 12.8],
      backgroundColor: [chartColors.accent, chartColors.orange, chartColors.blue, chartColors.gray],
      borderWidth: 2,
      borderColor: '#0a0f14',
    }]
  },
  options: {
    responsive: true,
    cutout: '60%',
    plugins: {
      legend: { position: 'bottom', labels: { font: { size: 12 }, padding: 16 } },
      tooltip: {
        callbacks: {
          label: ctx => ctx.label + ' of global BAS market'
        }
      }
    }
  }
});

// 4. Growth Drivers (horizontal bar)
new Chart(document.getElementById('chartDrivers'), {
  type: 'bar',
  data: {
    labels: ['IoT & AI Integration', 'Energy Efficiency Regulations', 'Smart City Investment', 'Occupant Comfort & Safety', 'Data-Driven Decision Making', 'Sustainability Mandates'],
    datasets: [{
      data: [95, 88, 82, 75, 72, 70],
      backgroundColor: [
        chartColors.accent + 'cc',
        chartColors.accent + 'aa',
        chartColors.accent + '88',
        chartColors.accent + '77',
        chartColors.accent + '66',
        chartColors.accent + '55',
      ],
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
          label: ctx => 'Cited in ' + ctx.raw + '% of industry reports as a key growth driver'
        }
      }
    },
    scales: {
      x: { display: false, max: 100 },
      y: { grid: { display: false }, ticks: { font: { size: 12 } } }
    }
  }
});

// 5. Salary Comparison
new Chart(document.getElementById('chartSalaryComparison'), {
  type: 'bar',
  data: {
    labels: ['General HVAC\\n$55-70K', 'BAS Specialist\\n$70-110K', 'Data Center BAS\\n$70-120K'],
    datasets: [
      {
        label: 'Salary Floor',
        data: [55, 70, 70],
        backgroundColor: chartColors.gray + '88',
        borderWidth: 0,
        borderRadius: 4,
      },
      {
        label: 'Salary Ceiling',
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
    plugins: {
      legend: { position: 'top' },
      tooltip: {
        callbacks: {
          label: ctx => ctx.dataset.label + ': $' + ctx.raw + ',000/year'
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: { display: true, text: 'Annual Salary (USD)', color: chartColors.textColor, font: { size: 11 } },
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
    labels: [
      'Data Centers  $70-120K',
      'OEM Manufacturer  $65-110K',
      'Large Integrator  $55-100K',
      'Property Mgmt  $60-95K',
      'Healthcare/Govt  $55-90K',
      'Small Integrator  $45-85K'
    ],
    datasets: [
      {
        label: 'Salary Floor',
        data: [70, 65, 55, 60, 55, 45],
        backgroundColor: chartColors.gray + '66',
        borderWidth: 0,
        borderRadius: 4,
      },
      {
        label: 'Salary Ceiling',
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
    plugins: {
      legend: { position: 'top' },
      tooltip: {
        callbacks: {
          label: ctx => ctx.dataset.label + ': $' + ctx.raw + ',000/year'
        }
      }
    },
    scales: {
      x: {
        beginAtZero: true,
        title: { display: true, text: 'Annual Salary (USD)', color: chartColors.textColor, font: { size: 11 } },
        ticks: { callback: v => '$' + v + 'K' },
        grid: { color: chartColors.gridColor }
      },
      y: { grid: { display: false }, ticks: { font: { size: 11 } } }
    }
  }
});

// 8. Skills Radar
new Chart(document.getElementById('chartSkills'), {
  type: 'radar',
  data: {
    labels: ['Electrical\\n(AC/DC, Circuits)', 'HVAC Systems\\n(AHUs, VAVs, Chillers)', 'DDC / Controls\\n(BACnet, Programming)', 'IT / Networking\\n(Fastest Growing)', 'Mechanical\\n(Schematics, Spatial)'],
    datasets: [{
      label: 'Importance Level',
      data: [85, 90, 95, 75, 70],
      backgroundColor: chartColors.accent + '22',
      borderColor: chartColors.accent,
      borderWidth: 2,
      pointBackgroundColor: chartColors.accent,
      pointRadius: 5,
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: ctx => 'Importance: ' + ctx.raw + '/100'
        }
      }
    },
    scales: {
      r: {
        beginAtZero: true, max: 100,
        grid: { color: chartColors.gridColor },
        angleLines: { color: chartColors.gridColor },
        pointLabels: { color: chartColors.textColor, font: { size: 11 } },
        ticks: { display: false }
      }
    }
  }
});

// 9. NYC vs Charlotte Pay
new Chart(document.getElementById('chartCityPay'), {
  type: 'bar',
  data: {
    labels: ['25th Percentile\\n(Entry/Mid)', 'Average', '75th Percentile\\n(Experienced)', '90th Percentile\\n(Senior)'],
    datasets: [
      {
        label: 'New York City',
        data: [62, 77, 97, 119],
        backgroundColor: chartColors.blue + '88',
        borderColor: chartColors.blue,
        borderWidth: 1,
        borderRadius: 4,
      },
      {
        label: 'Charlotte, NC',
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
    plugins: {
      legend: { position: 'top' },
      tooltip: {
        callbacks: {
          label: ctx => {
            if (ctx.raw === null) return ctx.dataset.label + ': No data available';
            return ctx.dataset.label + ': $' + ctx.raw + ',000/year';
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: { display: true, text: 'Annual Salary (USD)', color: chartColors.textColor, font: { size: 11 } },
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
    labels: [
      'Housing  +150%',
      'Overall Cost of Living  +41%',
      'Transportation  +25%',
      'Groceries  +20%',
      'Utilities  +17%',
      'Healthcare  +12%'
    ],
    datasets: [{
      data: [150, 41, 25, 20, 17, 12],
      backgroundColor: [chartColors.red + 'aa', chartColors.orange + '99', chartColors.yellow + '88', chartColors.blue + '88', chartColors.purple + '88', chartColors.accent + '88'],
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
          label: ctx => 'NYC costs ' + ctx.raw + '% more than Charlotte for this category'
        }
      }
    },
    scales: {
      x: {
        beginAtZero: true,
        title: { display: true, text: 'NYC Premium Over Charlotte (%)', color: chartColors.textColor, font: { size: 11 } },
        ticks: { callback: v => '+' + v + '%' },
        grid: { color: chartColors.gridColor }
      },
      y: { grid: { display: false }, ticks: { font: { size: 11 } } }
    }
  }
});

// 11. Employer Count by Category
new Chart(document.getElementById('chartEmployerCount'), {
  type: 'bar',
  data: {
    labels: ['Systems\\nIntegrators', 'Property\\nMgmt', 'Data\\nCenters', 'Healthcare\\nSystems', 'Higher\\nEd', 'OEMs', 'Government'],
    datasets: [
      {
        label: 'New York',
        data: [16, 11, 0, 6, 6, 6, 5],
        backgroundColor: chartColors.blue + '88',
        borderColor: chartColors.blue,
        borderWidth: 1,
        borderRadius: 4,
      },
      {
        label: 'North Carolina',
        data: [14, 8, 11, 5, 6, 5, 5],
        backgroundColor: chartColors.orange + '88',
        borderColor: chartColors.orange,
        borderWidth: 1,
        borderRadius: 4,
      }
    ]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      tooltip: {
        callbacks: {
          label: ctx => ctx.dataset.label + ': ' + ctx.raw + ' companies identified'
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: { display: true, text: 'Number of Companies', color: chartColors.textColor, font: { size: 11 } },
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
    labels: [
      'Energy Storage Sol.\\n$19.2B (planned)',
      'AWS\\n$10B (committed)',
      'Google\\n$1.2B+',
      'Apple\\n$175M expansion',
      'Microsoft\\n$27M land'
    ],
    datasets: [{
      data: [19.2, 10, 1.2, 0.175, 0.027],
      backgroundColor: [chartColors.accent + 'cc', chartColors.orange + 'cc', chartColors.blue + 'cc', chartColors.purple + 'cc', chartColors.yellow + 'cc'],
      borderWidth: 0,
      borderRadius: 4,
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: ctx => '$' + ctx.raw + ' billion investment in North Carolina'
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: { display: true, text: 'Investment (USD Billions)', color: chartColors.textColor, font: { size: 11 } },
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
