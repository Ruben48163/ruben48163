# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 22:27:03 2026

@author: RuOlvera
"""

# -*- coding: utf-8 -*-
"""
=============================================================
 Georgia Cancer CEA — NIH vs Community Decision Tree (Web App)
=============================================================

HOW TO RUN IN SPYDER:
  1. Open this file in Spyder
  2. Press F5 (or click Run)
  3. Your browser opens automatically at http://localhost:5051
  4. Adjust sliders / chips → results update live
  5. Press Ctrl+C in the Spyder console to stop the server

HOW TO SHARE (free hosting options):
  Option A — PythonAnywhere (free):
     1. Sign up at pythonanywhere.com
     2. Upload this file
     3. Set up a Web App pointing to this script
     4. Share the URL (yourusername.pythonanywhere.com)

  Option B — Render.com (free):
     1. Push this file + a requirements.txt to GitHub
        requirements.txt contents:  flask
     2. Create a new Web Service on render.com
     3. Set start command:  python cancer_cea_app.py
     4. Share the public URL

  Option C — Run locally and share via ngrok:
     pip install pyngrok
     Then uncomment the ngrok lines at the bottom of this file.
=============================================================
"""

import webbrowser
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- HTML / CSS / JS (full single-page app) ---------------------------------
HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Georgia Cancer CEA — NIH vs Community Decision Tree</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --neon:         #FC8F8F;
    --orange:       #B44446;
    --orange-light: #FC8F8F;
    --cream:        #DFD9D8;
    --navy:         #64242F;
    --purple:       #3a1018;
    --black:        #000000;
    --gray-1:       #DFD9D8;
    --gray-2:       #FC8F8F;
    --gray-3:       #e8a0a0;
    --gray-4:       #cc7070;
    --gray-5:       #B44446;
    --gray-6:       #8a3032;
    --gray-7:       #64242F;

    --neon-dim:    #FC8F8F33;
    --orange-dim:  #B4444633;
    --border:      #B44446;
    --text:        var(--cream);
    --muted:       #e8b0b0;
    --dim:         #cc9090;
  }
  body {
    background-color: #080707;
    color: var(--text); font-family: 'Outfit', sans-serif;
    min-height: 100vh; padding: 2rem 1.5rem;
  }
  .wrap { max-width: 1320px; margin: 0 auto; }

  header { display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem; margin-bottom:1.5rem; }
  .title-block h1 {
    font-family:'DM Serif Display',serif;
    font-size: clamp(1.7rem,3vw,2.5rem); line-height:1.1; color:#ffffff;
  }
  .title-block h1 em { color:var(--neon); font-style:italic; display:block; }
  .title-block p { margin-top:.4rem; font-size:.82rem; color:var(--muted); letter-spacing:.04em; }
  .header-btns { display:flex; gap:.6rem; align-items:center; }
  .btn {
    border:none; border-radius:8px; padding:.55rem 1.2rem;
    font-family:'Outfit',sans-serif; font-size:.82rem;
    cursor:pointer; font-weight:600; transition:all .25s;
  }
  .btn-ghost { background:transparent; border:1px solid var(--border); color:var(--muted); }
  .btn-ghost:hover { border-color:var(--neon); color:var(--neon); }
  .btn-primary { background:var(--neon); color:var(--black); }
  .btn-primary:hover { opacity:.92; transform:translateY(-1px); box-shadow: 0 0 14px var(--neon-dim); }

  .selector-row { display:flex; gap:1rem; margin-bottom:1.5rem; flex-wrap:wrap; }
  .selector-group {
    flex:1; min-width:280px;
    background: linear-gradient(135deg, var(--navy), #3a1018);
    border:1px solid var(--border); border-radius:12px;
    padding:.9rem 1.1rem;
  }
  .selector-group .lbl {
    font-size:.65rem; letter-spacing:.14em; text-transform:uppercase;
    font-weight:700; color:var(--muted); margin-bottom:.55rem;
  }
  .chip-row { display:flex; gap:.4rem; flex-wrap:wrap; }
  .chip {
    border:1px solid var(--border); background:transparent;
    color:var(--muted); border-radius:6px;
    padding:.38rem .75rem; font-size:.76rem; font-weight:500;
    cursor:pointer; font-family:'Outfit'; transition:all .2s;
  }
  .chip:hover { border-color:var(--neon); color:var(--neon); }
  .chip.active { background:var(--neon); border-color:var(--neon); color:var(--black); font-weight:700; }
  .chip:disabled { cursor:default; opacity:1; }
  .chip:disabled:hover { border-color:var(--neon); color:var(--black); }

  #banner {
    border-radius:14px; padding:1.15rem 1.6rem; margin-bottom:1.6rem;
    display:flex; justify-content:space-between; align-items:center;
    flex-wrap:wrap; gap:1rem; transition:background .4s, border-color .4s;
  }
  .banner-nih    { background:linear-gradient(135deg, #4a1520, #2a0a10); border:2px solid var(--orange); }
  .banner-comm   { background:linear-gradient(135deg, #3a0a10, #1a0508); border:2px solid var(--gray-3); }
  .banner-border { background:linear-gradient(135deg, var(--navy), var(--purple)); border:2px solid var(--gray-2); }
  #banner .label { font-size:.7rem; letter-spacing:.1em; font-weight:700; text-transform:uppercase; margin-bottom:.3rem; }
  #banner h2 { font-family:'DM Serif Display',serif; font-size:1.45rem; color:#fff; }
  #banner .icer-label { font-size:.7rem; text-transform:uppercase; letter-spacing:.06em; text-align:right; }
  #banner .icer-val { font-family:'DM Mono',monospace; font-size:1.7rem; font-weight:600; color:#fff; }
  #banner .icer-sub { font-size:.72rem; color:var(--gray-1); opacity:.85; text-align:right; }

  .main-grid { display:grid; grid-template-columns:340px 1fr; gap:1.4rem; align-items:start; }
  @media (max-width:950px) { .main-grid { grid-template-columns:1fr; } }

  .card {
    background:linear-gradient(135deg, var(--navy), #3a1018);
    border:1px solid var(--border); border-radius:16px;
    padding:1.3rem; margin-bottom:1rem;
  }
  .card-title { font-size:.68rem; letter-spacing:.12em; text-transform:uppercase; font-weight:700; margin-bottom:1.1rem; }

  .slider-row { margin-bottom:1.15rem; }
  .slider-head { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:.3rem; }
  .slider-head label { font-size:.72rem; font-weight:500; color:var(--muted); letter-spacing:.04em; text-transform:uppercase; }
  .slider-head .val { font-family:'DM Mono',monospace; font-size:.95rem; font-weight:500; color:var(--text); }
  input[type=range] { width:100%; accent-color:var(--neon); cursor:pointer; height:4px; }
  .slider-hint { font-size:.68rem; color:var(--gray-4); margin-top:.25rem; line-height:1.4; }
  .slider-hint .src { color:var(--gray-3); font-style:italic; }

  .tabs { display:flex; gap:.5rem; margin-bottom:1rem; flex-wrap:wrap; }
  .tab {
    background:transparent; border:1px solid var(--border); color:var(--muted);
    border-radius:8px; padding:.5rem 1.1rem; font-size:.8rem;
    cursor:pointer; font-family:'Outfit'; font-weight:500; transition:all .2s;
  }
  .tab:hover { border-color:var(--neon); color:var(--neon); }
  .tab.active { background:var(--neon); border-color:var(--neon); color:var(--black); font-weight:700; }
  .tab-panel { display:none; }
  .tab-panel.active { display:block; }

  #tree-card { padding:1rem; }
  #tree-svg { width:100%; border-radius:8px; }

  .metric-grid { display:flex; gap:1rem; margin-bottom:1rem; flex-wrap:wrap; }
  .metric-card { flex:1; min-width:180px; border-radius:12px; padding:1rem 1.2rem; }
  .metric-card .m-title { font-size:.64rem; letter-spacing:.1em; text-transform:uppercase; font-weight:700; margin-bottom:.35rem; }
  .metric-card .m-main { font-family:'DM Mono',monospace; font-size:1.35rem; font-weight:600; color:var(--text); }
  .metric-card .m-sub { margin-top:.3rem; font-size:.72rem; color:var(--dim); font-family:'DM Mono',monospace; }

  .wtp-viz { padding:1.2rem 1.4rem; }
  .wtp-scale { position:relative; height:60px; margin:1rem 0 .4rem; }
  .wtp-bar {
    position:absolute; inset:24px 0 24px 0;
    background:linear-gradient(90deg, #B44446 0%, #B44446 33%, #e8a0a0 33%, #e8a0a0 66%, #3a1018 66%, #3a1018 100%);
    border-radius:6px; opacity:.55;
  }
  .wtp-marker {
    position:absolute; top:8px; width:2px; height:44px;
    background:#ffffff; box-shadow:0 0 12px rgba(255,255,255,.9);
    transition:left .3s;
  }
  .wtp-marker::after {
    content:""; position:absolute; top:-6px; left:-5px; width:12px; height:12px;
    background:#ffffff; border-radius:50%; box-shadow:0 0 12px rgba(255,255,255,.9);
  }
  .wtp-labels { display:flex; justify-content:space-between; font-size:.68rem; color:var(--muted); font-family:'DM Mono'; }
  .wtp-zones { display:flex; justify-content:space-between; font-size:.68rem; margin-top:.6rem; font-weight:600; }
  .wtp-zones span:nth-child(1) { color:var(--orange); }
  .wtp-zones span:nth-child(2) { color:#e8a0a0; }
  .wtp-zones span:nth-child(3) { color:#64242F; }

  table { width:100%; border-collapse:collapse; font-size:.82rem; }
  th { padding:.6rem .8rem; font-size:.68rem; letter-spacing:.08em; text-transform:uppercase; font-weight:600; text-align:left; color:var(--neon); border-bottom:1px solid var(--border); font-family:'Outfit'; }
  td { padding:.6rem .8rem; font-family:'DM Mono',monospace; font-size:.8rem; }
  tr:nth-child(even) td { background:rgba(0,0,0,.25); }
  tfoot td { font-family:'Outfit'; font-size:.82rem; font-weight:600; padding:.7rem .8rem; }
  tfoot tr:first-child td { border-top:2px solid var(--border); }

  .sources-card {
    margin-top:1.5rem; padding:1.5rem 1.7rem;
    background:linear-gradient(135deg, var(--navy), #3a1018);
    border:1px solid var(--border); border-radius:16px;
  }
  .sources-card h3 { font-family:'DM Serif Display',serif; font-size:1.25rem; color:#ffffff; margin-bottom:.3rem; }
  .sources-card .intro { font-size:.8rem; color:var(--muted); margin-bottom:1.2rem; line-height:1.6; }
  .source-item { padding:.85rem 0; border-bottom:1px solid rgba(255,255,255,.06); font-size:.78rem; line-height:1.6; }
  .source-item:last-child { border-bottom:none; }
  .source-item .num {
    display:inline-block; width:22px; height:22px;
    border-radius:50%; background:var(--neon); color:var(--black);
    text-align:center; line-height:22px; font-size:.68rem;
    font-weight:700; margin-right:.55rem; font-family:'DM Mono';
  }
  .source-item .badge-prov {
    display:inline-block; padding:1px 7px; border-radius:4px;
    background:var(--neon); color:var(--black); font-size:.62rem;
    font-weight:700; margin-right:.4rem; letter-spacing:.04em;
  }
  .source-item .badge-rec {
    display:inline-block; padding:1px 7px; border-radius:4px;
    background:var(--gray-6); color:var(--gray-1); font-size:.62rem;
    font-weight:700; margin-right:.4rem; letter-spacing:.04em;
    border:1px solid var(--gray-5);
  }
  .source-item .authors { color:var(--text); font-weight:500; }
  .source-item .title { color:var(--neon); }
  .source-item .meta { color:var(--gray-3); font-size:.72rem; margin-top:.2rem; }

  .framework-card { margin-top:1rem; padding:1.2rem 1.5rem; border-radius:10px; background:linear-gradient(135deg, var(--navy), #3a1018); border:1px solid var(--border); }
  .framework-card h4 { font-family:'DM Serif Display',serif; font-size:1rem; color:#ffffff; margin-bottom:.6rem; }
  .framework-card .grid-2 { display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:.8rem; font-size:.76rem; }
  .framework-card .kv { display:flex; justify-content:space-between; padding:.3rem 0; border-bottom:1px dashed rgba(255,255,255,.06); }
  .framework-card .kv span:first-child { color:var(--muted); }
  .framework-card .kv span:last-child { color:var(--text); font-family:'DM Mono'; font-size:.74rem; text-align:right; }

  #toast {
    position:fixed; bottom:2rem; right:2rem;
    background:var(--neon); color:var(--black); padding:.7rem 1.4rem;
    border-radius:10px; font-size:.85rem; font-weight:700;
    opacity:0; transform:translateY(10px); transition:all .3s;
    pointer-events:none; font-family:'Outfit';
    box-shadow: 0 0 20px var(--neon-dim);
  }
  #toast.show { opacity:1; transform:translateY(0); }
</style>
</head>
<body>
<div class="wrap">

  <header>
    <div class="title-block">
      <h1>Georgia Cancer CEA <em>NIH vs. Community Care Decision Model</em></h1>
      <p>Incremental cost-effectiveness analysis &nbsp;·&nbsp; Emory Winship (NCI) vs. NGMC/Piedmont &nbsp;·&nbsp; Breast · Lung · Colorectal · Prostate</p>
    </div>
    <div class="header-btns">
      <button class="btn btn-ghost" onclick="resetAll()">↺ Reset</button>
      <button class="btn btn-primary" onclick="shareLink()">⬡ Share Link</button>
    </div>
  </header>

  <div class="selector-row">
    <div class="selector-group">
      <div class="lbl">Cancer Type</div>
      <div class="chip-row" id="cancer-chips">
        <button class="chip active" data-cancer="breast">Breast</button>
        <button class="chip" data-cancer="lung">Lung (NSCLC)</button>
        <button class="chip" data-cancer="colorectal">Colorectal</button>
        <button class="chip" data-cancer="prostate">Prostate</button>
      </div>
    </div>
    <div class="selector-group">
      <div class="lbl">Analytic Perspective</div>
      <div class="chip-row">
        <button class="chip active" disabled>Healthcare Payer</button>
      </div>
    </div>
  </div>

  <div id="banner" class="banner-nih">
    <div>
      <div class="label" id="rec-label">Cost-Effectiveness Verdict</div>
      <h2 id="rec-text">✓ NIH Center Care is Cost-Effective</h2>
    </div>
    <div>
      <div class="icer-label" id="icer-label">Incremental Cost-Effectiveness Ratio</div>
      <div class="icer-val" id="icer-val">—</div>
      <div class="icer-sub" id="icer-sub">per QALY gained</div>
    </div>
  </div>

  <div class="main-grid">
    <div>
      <div class="card">
        <div class="card-title" style="color:var(--neon)">▸ Scenario A — NIH Center (Emory Winship)</div>
        <div class="slider-row">
          <div class="slider-head"><label>Lifetime Cost per Patient</label><span class="val" id="costA-val">$125,000</span></div>
          <input type="range" id="costA" min="20000" max="400000" step="1000" value="125000">
          <div class="slider-hint"><span class="src">Takvorian 2021: NCI centers 15–30% higher cost vs community.</span></div>
        </div>
        <div class="slider-row">
          <div class="slider-head"><label>Lifetime QALYs</label><span class="val" id="qalyA-val">12.50</span></div>
          <input type="range" id="qalyA" min="1" max="25" step="0.05" value="12.50">
          <div class="slider-hint"><span class="src">Onega 2009: NCI center attendance reduces mortality across all 4 cancers.</span></div>
        </div>
      </div>

      <div class="card">
        <div class="card-title" style="color:var(--gray-2)">▸ Scenario B — Community Hospital</div>
        <div class="slider-row">
          <div class="slider-head"><label>Lifetime Cost per Patient</label><span class="val" id="costB-val">$98,000</span></div>
          <input type="range" id="costB" min="15000" max="350000" step="1000" value="98000">
          <div class="slider-hint"><span class="src">NGMC, Piedmont — standard-of-care, CoC accredited.</span></div>
        </div>
        <div class="slider-row">
          <div class="slider-head"><label>Lifetime QALYs</label><span class="val" id="qalyB-val">11.40</span></div>
          <input type="range" id="qalyB" min="1" max="25" step="0.05" value="11.40">
          <div class="slider-hint">Baseline outcomes from SEER / Georgia Cancer Registry.</div>
        </div>
      </div>

      <div class="card">
        <div class="card-title" style="color:#ffffff">▸ Model Parameters</div>
        <div class="slider-row">
          <div class="slider-head"><label>WTP Threshold ($/QALY)</label><span class="val" id="wtp-val">$100,000</span></div>
          <input type="range" id="wtp" min="20000" max="200000" step="5000" value="100000">
          <div class="slider-hint"><span class="src">US range $50k–$150k; $100k base case per Second Panel 2016.</span></div>
        </div>
        <div class="slider-row">
          <div class="slider-head"><label>Discount Rate</label><span class="val" id="disc-val">3.0%</span></div>
          <input type="range" id="disc" min="0" max="0.07" step="0.005" value="0.03">
          <div class="slider-hint"><span class="src">3% base (Sanders et al. 2016); test 0%, 1.5%, 3.5%, 5%.</span></div>
        </div>
        <div class="slider-row">
          <div class="slider-head"><label>NIH P30 Per-Patient Share</label><span class="val" id="p30-val">$8,000</span></div>
          <input type="range" id="p30" min="0" max="50000" step="500" value="8000">
          <div class="slider-hint"><span class="src">Public funder perspective only. Allocated from P30 CA138292.</span></div>
        </div>
        <div class="slider-row">
          <div class="slider-head"><label>Productivity + Caregiver Costs</label><span class="val" id="prod-val">$35,000</span></div>
          <input type="range" id="prod" min="0" max="200000" step="1000" value="35000">
          <div class="slider-hint"><span class="src">Societal perspective only. Human capital approach (BLS data).</span></div>
        </div>
        <div class="slider-row">
          <div class="slider-head"><label>Probability of Recurrence (NIH)</label><span class="val" id="precA-val">22%</span></div>
          <input type="range" id="precA" min="0" max="0.8" step="0.01" value="0.22">
          <div class="slider-hint">Lifetime recurrence rate at NIH center.</div>
        </div>
        <div class="slider-row">
          <div class="slider-head"><label>Probability of Recurrence (Community)</label><span class="val" id="precB-val">30%</span></div>
          <input type="range" id="precB" min="0" max="0.8" step="0.01" value="0.30">
          <div class="slider-hint">Lifetime recurrence rate at community hospital.</div>
        </div>
      </div>
    </div>

    <div>
      <div class="tabs">
        <button class="tab active" onclick="showTab('tree',this)"> Decision Tree</button>
        <button class="tab" onclick="showTab('results',this)">ICER Results</button>
        <button class="tab" onclick="showTab('breakdown',this)">Branch Breakdown</button>
      </div>

      <div id="tab-tree" class="tab-panel active">
        <div class="card" id="tree-card">
          <svg id="tree-svg" viewBox="0 0 960 580" xmlns="http://www.w3.org/2000/svg">
            <rect width="960" height="580" fill="#000000" rx="12"/>
          </svg>
        </div>
      </div>

      <div id="tab-results" class="tab-panel">
        <div class="metric-grid">
          <div class="metric-card" style="background:linear-gradient(135deg, rgba(180,68,70,.1), rgba(0,0,0,.5));border:1px solid rgba(180,68,70,.4);">
            <div class="m-title" style="color:var(--orange)">Incremental Cost</div>
            <div class="m-main" id="inc-cost">—</div>
            <div class="m-sub">NIH – Community</div>
          </div>
          <div class="metric-card" style="background:linear-gradient(135deg, rgba(252,143,143,.08), rgba(0,0,0,.5));border:1px solid var(--gray-5);">
            <div class="m-title" style="color:var(--gray-1)">Incremental QALYs</div>
            <div class="m-main" id="inc-qaly">—</div>
            <div class="m-sub">NIH – Community</div>
          </div>
          <div class="metric-card" style="background:linear-gradient(135deg, rgba(58,16,24,.7), rgba(0,0,0,.5));border:1px solid var(--gray-5);">
            <div class="m-title" style="color:var(--orange)">ICER</div>
            <div class="m-main" id="icer-metric">—</div>
            <div class="m-sub">$/QALY gained</div>
          </div>
        </div>

        <div class="card wtp-viz">
          <div class="card-title" style="color:var(--muted)">ICER vs Willingness-to-Pay</div>
          <div class="wtp-scale">
            <div class="wtp-bar"></div>
            <div class="wtp-marker" id="wtp-marker" style="left:50%"></div>
          </div>
          <div class="wtp-labels">
            <span>$0</span><span>$50k</span><span>$100k</span><span>$150k</span><span>$200k+</span>
          </div>
          <div class="wtp-zones">
            <span>◄ Highly cost-effective</span>
            <span>Borderline</span>
            <span>Not cost-effective ►</span>
          </div>
          <div style="margin-top:1rem;font-size:.78rem;color:var(--muted);line-height:1.6">
            <strong style="color:var(--text)">Interpretation:</strong>
            <span id="interpretation">—</span>
          </div>
        </div>
      </div>

      <div id="tab-breakdown" class="tab-panel">
        <div class="card">
          <div class="card-title" style="color:var(--muted)">Cost-Consequence Breakdown</div>
          <table>
            <thead><tr><th>Component</th><th>NIH Center</th><th>Community</th><th>Δ</th></tr></thead>
            <tbody id="breakdown-body"></tbody>
            <tfoot id="breakdown-foot"></tfoot>
          </table>
        </div>
      </div>

      <div id="tab-framework-removed" style="display:none"></div>
    </div>
  </div>

  <div class="sources-card" style="display:none">
    <h3>Data Sources &amp; References</h3>
    <p class="intro">
      Citations reproduce the study design's reference list.
      <span style="color:var(--neon);font-weight:700">PROVIDED</span> sources were given by the study team;
      <span style="color:var(--gray-1);font-weight:700">RECOMMENDED</span> sources were identified during the framework analysis.
      Default parameter values are illustrative and should be re-estimated from these sources for each cancer type and perspective.
    </p>

    <div class="source-item"><span class="num">1</span><span class="badge-prov">PROVIDED</span>
      <span class="authors">Thuita LN, et al.</span>
      <span class="title">Impact of Care at Comprehensive Cancer Centers on Outcome — Results from a Population-based Study.</span>
      <div class="meta"><em>Cancer.</em> 2015;121(21):3834–3842. PMC4892698.</div>
    </div>
    <div class="source-item"><span class="num">2</span><span class="badge-prov">PROVIDED</span>
      <span class="authors">Liang W, et al.</span>
      <span class="title">Quality of Care at Cancer Centers in an Underserved Population.</span>
      <div class="meta"><em>J Oncol Pract.</em> 2016;12(7). DOI: 10.1200/JOP.2016.020446.</div>
    </div>
    <div class="source-item"><span class="num">3</span><span class="badge-prov">PROVIDED</span>
      <span class="authors">Onega T, Duell EJ, Shi X, Demidenko E, Gottlieb D, Goodman DC.</span>
      <span class="title">Influence of NCI Cancer Center Attendance on Mortality in Lung, Breast, Colorectal, and Prostate Cancer Patients.</span>
      <div class="meta"><em>Medical Care.</em> 2009. &nbsp;·&nbsp; Primary source for comparative mortality inputs.</div>
    </div>
    <div class="source-item"><span class="num">4</span><span class="badge-rec">RECOMMENDED</span>
      <span class="authors">Takvorian SU, Bekelman JE, Lee DJ, et al.</span>
      <span class="title">Differences in Cancer Care Expenditures and Utilization for Surgery by Hospital Type Among Patients With Private Insurance.</span>
      <div class="meta"><em>JAMA Network Open.</em> 2021;4(8):e2118496. PMC8335573.</div>
    </div>
    <div class="source-item"><span class="num">5</span><span class="badge-rec">RECOMMENDED</span>
      <span class="authors">Freedman RA, et al.</span>
      <span class="title">The Role of NCI-Designated Cancer Center Status: Observed Variation in Surgical Care Depends on the Level of Evidence.</span>
      <div class="meta"><em>Ann Surg.</em> 2012. PMC3428029.</div>
    </div>
    <div class="source-item"><span class="num">6</span><span class="badge-rec">RECOMMENDED</span>
      <span class="authors">Sanders GD, Neumann PJ, Basu A, et al.</span>
      <span class="title">Recommendations for Conduct, Methodological Practices, and Reporting of CEA: Second Panel on Cost-Effectiveness in Health and Medicine.</span>
      <div class="meta"><em>JAMA.</em> 2016;316(10):1093–1103.</div>
    </div>
    <div class="source-item"><span class="num">7</span><span class="badge-rec">RECOMMENDED</span>
      <span class="authors">Frick KD, Kymes SM.</span>
      <span class="title">The calculation and use of economic burden in cost-effectiveness analysis.</span>
      <div class="meta"><em>Surv Ophthalmol.</em> 2006;51 Suppl 1:S27–32.</div>
    </div>
    <div class="source-item"><span class="num">8</span><span class="badge-rec">RECOMMENDED</span>
      <span class="authors">Georgia Department of Public Health.</span>
      <span class="title">Georgia's Comprehensive Cancer Control Plan 2019–2024.</span>
      <div class="meta">Atlanta, GA: GDPH; 2019.</div>
    </div>
    <div class="source-item"><span class="num">9</span><span class="badge-rec">RECOMMENDED</span>
      <span class="authors">Ward KC, et al.</span>
      <span class="title">Cancer Mortality-to-Incidence Ratios in Georgia: Racial Cancer Disparities and Geographic Determinants.</span>
      <div class="meta"><em>Cancer.</em> 2012;118(16):4032–4045. PMC3342438.</div>
    </div>
    <div class="source-item"><span class="num">10</span><span class="badge-rec">RECOMMENDED</span>
      <span class="authors">Ghosh S, et al.</span>
      <span class="title">Understanding Geographic and Racial/Ethnic Disparities in Mortality from Four Major Cancers in Georgia, 1999–2019.</span>
      <div class="meta"><em>Sci Rep.</em> 2022. DOI: 10.1038/s41598-022-18374-7.</div>
    </div>
    <div class="source-item"><span class="num">11</span><span class="badge-rec">RECOMMENDED</span>
      <span class="authors">National Cancer Institute.</span>
      <span class="title">State Cancer Profiles — Georgia.</span>
      <div class="meta">statecancerprofiles.cancer.gov</div>
    </div>
    <div class="source-item"><span class="num">12</span><span class="badge-rec">RECOMMENDED</span>
      <span class="authors">American Cancer Society / SEER.</span>
      <span class="title">Cancer Facts &amp; Figures 2025; SEER StatFacts — Common Cancer Sites.</span>
      <div class="meta">ACS 2025; seer.cancer.gov/statfacts/html/common.html</div>
    </div>
    <div class="source-item"><span class="num">F</span><span class="badge-rec">FRAMEWORK</span>
      <span class="authors">Haddix AC, Teutsch SM, Corso PS (eds).</span>
      <span class="title">Prevention Effectiveness: A Guide to Decision Analysis and Economic Evaluation. 2nd ed.</span>
      <div class="meta">Oxford University Press; 2003.</div>
    </div>
    <div class="source-item"><span class="num">F</span><span class="badge-rec">FRAMEWORK</span>
      <span class="authors">Drummond MF, et al.</span>
      <span class="title">Methods for the Economic Evaluation of Health Care Programmes. 4th ed.</span>
      <div class="meta">Oxford University Press; 2015.</div>
    </div>
  </div>
</div>

<div id="toast">✓ Link copied to clipboard!</div>

<script>
const CANCER_DEFAULTS = {
  breast:     { costA:125000, costB:98000,  qalyA:12.5, qalyB:11.4, precA:0.22, precB:0.30 },
  lung:       { costA:185000, costB:152000, qalyA:3.4,  qalyB:2.7,  precA:0.45, precB:0.55 },
  colorectal: { costA:155000, costB:122000, qalyA:9.8,  qalyB:8.9,  precA:0.28, precB:0.36 },
  prostate:   { costA:85000,  costB:68000,  qalyA:14.2, qalyB:13.6, precA:0.15, precB:0.20 },
};
const MODEL_DEFAULTS = { wtp:100000, disc:0.03, p30:8000, prod:35000 };

let currentCancer = 'breast';
let currentPerspective = 'payer';

const fmt = n => { if (!isFinite(n)) return "∞"; const sign=n<0?'−':''; return sign+"$"+Math.round(Math.abs(n)).toLocaleString(); };
const fmtK = n => { if (!isFinite(n)) return "∞"; const sign=n<0?'−':''; return sign+"$"+(Math.abs(n)/1000).toFixed(1)+"k"; };
const pct  = n => (n*100).toFixed(0) + "%";

function calc(p) {
  let costA = p.costA, costB = p.costB;
  if (p.perspective === 'funder')   { costA += p.p30; }
  if (p.perspective === 'societal') { costA += p.p30*0.5 + p.prod*0.85; costB += p.prod; }
  const df = 1 + p.disc*0.5;
  costA /= df; costB /= df;
  const incCost = costA - costB;
  const incQaly = p.qalyA - p.qalyB;
  const icer = incQaly > 0 ? incCost / incQaly : (incCost <= 0 ? -Infinity : Infinity);
  const evA_rec = p.costA * 1.35;
  const evA_ok  = p.costA * 0.85;
  const evB_rec = p.costB * 1.30;
  const evB_ok  = p.costB * 0.85;
  return { costA, costB, incCost, incQaly, icer, evA_rec, evA_ok, evB_rec, evB_ok };
}

function getParams() {
  return {
    costA:+document.getElementById('costA').value,
    costB:+document.getElementById('costB').value,
    qalyA:+document.getElementById('qalyA').value,
    qalyB:+document.getElementById('qalyB').value,
    wtp:+document.getElementById('wtp').value,
    disc:+document.getElementById('disc').value,
    p30:+document.getElementById('p30').value,
    prod:+document.getElementById('prod').value,
    precA:+document.getElementById('precA').value,
    precB:+document.getElementById('precB').value,
    perspective: currentPerspective,
    cancer: currentCancer,
  };
}

function loadFromURL() {
  const hash = window.location.hash.slice(1);
  if (!hash) return;
  try {
    const state = JSON.parse(atob(hash));
    if (state.cancer) currentCancer = state.cancer;
    if (state.perspective) currentPerspective = state.perspective;
    ['costA','costB','qalyA','qalyB','wtp','disc','p30','prod','precA','precB'].forEach(k => {
      if (state[k] != null) document.getElementById(k).value = state[k];
    });
    syncChips();
  } catch(e) {}
}

function shareLink() {
  const p = getParams();
  const state = { cancer:p.cancer, perspective:p.perspective,
    costA:p.costA, costB:p.costB, qalyA:p.qalyA, qalyB:p.qalyB,
    wtp:p.wtp, disc:p.disc, p30:p.p30, prod:p.prod,
    precA:p.precA, precB:p.precB };
  const encoded = btoa(JSON.stringify(state));
  const url = window.location.origin + window.location.pathname + '#' + encoded;
  window.history.replaceState(null,'','#'+encoded);
  navigator.clipboard.writeText(url).then(() => {
    const t = document.getElementById('toast');
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2500);
  });
}

function resetAll() {
  currentCancer = 'breast'; currentPerspective = 'payer';
  applyCancerDefaults();
  Object.entries(MODEL_DEFAULTS).forEach(([k,v]) => { document.getElementById(k).value = v; });
  syncChips();
  window.history.replaceState(null,'',window.location.pathname);
  update();
}

function applyCancerDefaults() {
  const d = CANCER_DEFAULTS[currentCancer];
  Object.entries(d).forEach(([k,v]) => {
    const el = document.getElementById(k); if (el) el.value = v;
  });
}

function syncChips() {
  document.querySelectorAll('#cancer-chips .chip').forEach(c =>
    c.classList.toggle('active', c.dataset.cancer === currentCancer));
}

function showTab(name, btn) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-'+name).classList.add('active');
  btn.classList.add('active');
}

function drawTree(p, r) {
  const W=960, H=580;
  const CORAL   = '#FC8F8F';
  const RED     = '#B44446';
  const BURGUNDY= '#64242F';
  const OFFWHITE= '#DFD9D8';
  const DARK    = '#3a1018';
  const LINE    = '#B44446';

  const dec={x:65,y:290};
  const cA={x:235,y:165}, cB={x:235,y:415};
  const PX=600;
  const PY={A1:90,A2:240,B1:370,B2:520};

  let s = `<rect width="${W}" height="${H}" fill="#000000" rx="12"/>`;
  const ln = (x1,y1,x2,y2,c=LINE) =>
    `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="1.8" stroke-linecap="round"/>`;

  s += ln(dec.x+22,dec.y,cA.x-28,cA.y);
  s += ln(dec.x+22,dec.y,cB.x-28,cB.y);
  s += ln(cA.x+28,cA.y,PX,PY.A1);
  s += ln(cA.x+28,cA.y,PX,PY.A2);
  s += ln(cB.x+28,cB.y,PX,PY.B1);
  s += ln(cB.x+28,cB.y,PX,PY.B2);

  const lbl = (x,y,txt,col,anchor='start',fs=9.5) =>
    `<text x="${x}" y="${y}" fill="${col}" font-size="${fs}" font-family="Outfit" font-style="italic" font-weight="600" text-anchor="${anchor}">${txt}</text>`;

  const pA=p.precA.toFixed(2), pAn=(1-p.precA).toFixed(2);
  const pB=p.precB.toFixed(2), pBn=(1-p.precB).toFixed(2);

  s += lbl(135,218,"NIH Center",CORAL,'middle',10);
  s += lbl(135,378,"Community",OFFWHITE,'middle',10);
  s += lbl(cA.x+34,cA.y-48,`Recurrence  P=${pA}`,OFFWHITE);
  s += lbl(cA.x+34,cA.y+55,`Disease-free  P=${pAn}`,CORAL);
  s += lbl(cB.x+34,cB.y-48,`Recurrence  P=${pB}`,OFFWHITE);
  s += lbl(cB.x+34,cB.y+55,`Disease-free  P=${pBn}`,CORAL);

  s += `<rect x="${dec.x-24}" y="${dec.y-24}" width="48" height="48" rx="4" fill="${BURGUNDY}" stroke="${CORAL}" stroke-width="2.5"/>
        <text x="${dec.x}" y="${dec.y-5}" text-anchor="middle" fill="${CORAL}" font-size="9" font-family="Outfit" font-weight="700">CARE</text>
        <text x="${dec.x}" y="${dec.y+10}" text-anchor="middle" fill="${CORAL}" font-size="9" font-family="Outfit" font-weight="700">SETTING</text>`;

  const circ = (cx,cy,rad,stroke,label1,label2) =>
    `<circle cx="${cx}" cy="${cy}" r="${rad}" fill="${BURGUNDY}" stroke="${stroke}" stroke-width="2"/>
     <text x="${cx}" y="${cy-5}" text-anchor="middle" fill="#ffffff" font-size="9" font-family="Outfit" font-weight="600">${label1}</text>
     <text x="${cx}" y="${cy+8}" text-anchor="middle" fill="#ffffff" font-size="9" font-family="Outfit" font-weight="600">${label2}</text>`;

  s += circ(cA.x,cA.y,28,CORAL,"CHANCE","NODE");
  s += circ(cB.x,cB.y,28,OFFWHITE,"CHANCE","NODE");

  const box = (y,topLbl,qaly,cost,badOutcome) => {
    const bg = badOutcome ? DARK : BURGUNDY;
    const ec = badOutcome ? OFFWHITE : CORAL;
    const tc = badOutcome ? OFFWHITE : CORAL;
    return `<rect x="${PX}" y="${y-32}" width="335" height="64" rx="8" fill="${bg}" stroke="${ec}" stroke-width="1.5"/>
            <text x="${PX+14}" y="${y-14}" fill="#cc9090" font-size="9" font-family="DM Mono">${topLbl}</text>
            <text x="${PX+14}" y="${y+3}" fill="${tc}" font-size="10" font-family="DM Mono" font-weight="500">QALYs ≈ ${qaly}</text>
            <text x="${PX+14}" y="${y+20}" fill="#ffffff" font-size="11" font-family="DM Mono" font-weight="500">Cost ≈ ${fmtK(cost)}</text>`;
  };

  const qalyA_rec = (p.qalyA*0.6).toFixed(1);
  const qalyA_ok  = (p.qalyA*1.15).toFixed(1);
  const qalyB_rec = (p.qalyB*0.6).toFixed(1);
  const qalyB_ok  = (p.qalyB*1.15).toFixed(1);

  s += box(PY.A1,`NIH + Recurrence`,qalyA_rec,r.evA_rec,true);
  s += box(PY.A2,`NIH + Disease-free`,qalyA_ok,r.evA_ok,false);
  s += box(PY.B1,`Community + Recurrence`,qalyB_rec,r.evB_rec,true);
  s += box(PY.B2,`Community + Disease-free`,qalyB_ok,r.evB_ok,false);

  s += `<text x="80" y="16" fill="#cc9090" font-size="9" font-family="Outfit" font-weight="600" letter-spacing="2" text-anchor="middle">DECISION</text>`;
  s += `<text x="${PX+170}" y="16" fill="#cc9090" font-size="9" font-family="Outfit" font-weight="600" letter-spacing="2" text-anchor="middle">TERMINAL OUTCOMES</text>`;

  const cancerName = {breast:'Breast Cancer',lung:'Lung Cancer (NSCLC)',colorectal:'Colorectal Cancer',prostate:'Prostate Cancer'}[p.cancer];
  s += `<text x="480" y="565" fill="#cc9090" font-size="10" font-family="Outfit" font-weight="500" letter-spacing="2" text-anchor="middle">${cancerName.toUpperCase()} · ${p.perspective.toUpperCase()} PERSPECTIVE</text>`;

  document.getElementById('tree-svg').innerHTML = s;
}

function update() {
  const p = getParams();
  const r = calc(p);

  document.getElementById('costA-val').textContent = fmt(p.costA);
  document.getElementById('costB-val').textContent = fmt(p.costB);
  document.getElementById('qalyA-val').textContent = p.qalyA.toFixed(2);
  document.getElementById('qalyB-val').textContent = p.qalyB.toFixed(2);
  document.getElementById('wtp-val').textContent = fmt(p.wtp);
  document.getElementById('disc-val').textContent = (p.disc*100).toFixed(1)+"%";
  document.getElementById('p30-val').textContent = fmt(p.p30);
  document.getElementById('prod-val').textContent = fmt(p.prod);
  document.getElementById('precA-val').textContent = pct(p.precA);
  document.getElementById('precB-val').textContent = pct(p.precB);

  const banner = document.getElementById('banner');
  const icerVal = r.icer;
  let verdict, bannerClass, icerText, sub;
  if (r.incQaly <= 0 && r.incCost > 0) {
    verdict = '✗ NIH Care Dominated'; bannerClass='banner-comm';
    icerText = 'Dominated'; sub='Higher cost, no QALY gain';
  } else if (r.incQaly > 0 && r.incCost <= 0) {
    verdict = '✓✓ NIH Care Dominates'; bannerClass='banner-nih';
    icerText = 'Dominant'; sub='Higher QALYs, lower cost';
  } else if (icerVal < p.wtp * 0.5) {
    verdict = '✓ Highly Cost-Effective'; bannerClass='banner-nih';
    icerText = fmt(icerVal); sub='Well below WTP threshold';
  } else if (icerVal < p.wtp) {
    verdict = '✓ Cost-Effective'; bannerClass='banner-nih';
    icerText = fmt(icerVal); sub='Below WTP threshold';
  } else if (icerVal < p.wtp * 1.5) {
    verdict = '⚠ Borderline'; bannerClass='banner-border';
    icerText = fmt(icerVal); sub='Above WTP threshold';
  } else {
    verdict = '✗ Not Cost-Effective'; bannerClass='banner-comm';
    icerText = fmt(icerVal); sub='Well above WTP threshold';
  }
  banner.className = bannerClass;
  document.getElementById('rec-text').textContent = verdict;
  document.getElementById('icer-val').textContent = icerText;
  document.getElementById('icer-sub').textContent = sub;

  document.getElementById('inc-cost').textContent = fmt(r.incCost);
  document.getElementById('inc-qaly').textContent = r.incQaly.toFixed(2);
  document.getElementById('icer-metric').textContent = isFinite(r.icer) ? fmt(r.icer) : (r.icer===-Infinity ? 'Dominant' : 'Dominated');

  const icerForMarker = isFinite(r.icer) && r.icer > 0 ? r.icer : 0;
  const markerPct = Math.min(100, Math.max(0, icerForMarker/200000*100));
  document.getElementById('wtp-marker').style.left = markerPct+'%';

  let interp;
  if (r.incQaly <= 0) {
    interp = `NIH care does not produce QALY gains in this scenario — fundamental re-evaluation of inputs needed.`;
  } else if (r.icer <= 0) {
    interp = `NIH care is the dominant strategy: lower cost AND higher QALYs. Adoption is unambiguously supported.`;
  } else {
    const ratio = r.icer / p.wtp;
    interp = `At an ICER of ${fmt(r.icer)}/QALY and a WTP of ${fmt(p.wtp)}/QALY (ratio ${ratio.toFixed(2)}), `+
             (ratio < 1 ? `NIH care is cost-effective.` :
              `NIH care exceeds the WTP threshold. Sensitivity analyses (PSA, threshold) are needed before adoption.`);
  }
  document.getElementById('interpretation').textContent = interp;

  const rows = [ {c:'Direct medical (lifetime)', a:p.costA, b:p.costB} ];
  if (p.perspective === 'funder' || p.perspective === 'societal') {
    rows.push({c:'NIH P30 infrastructure share', a:p.p30*(p.perspective==='societal'?0.5:1), b:0});
  }
  if (p.perspective === 'societal') {
    rows.push({c:'Productivity + caregiver losses', a:p.prod*0.85, b:p.prod});
  }
  rows.push({c:'Total discounted cost', a:r.costA, b:r.costB, bold:true});
  rows.push({c:'Lifetime QALYs', a:p.qalyA, b:p.qalyB, qaly:true});

  document.getElementById('breakdown-body').innerHTML = rows.map(r => {
    const delta = (r.a - r.b);
    const dColor = delta > 0 ? '#e8a0a0' : delta < 0 ? '#B44446' : '#cc9090';
    const formatter = r.qaly ? v=>v.toFixed(2) : fmt;
    const weight = r.bold ? 'font-weight:700;color:#ffffff' : '';
    return `<tr>
      <td style="font-family:Outfit;font-size:.8rem;color:#DFD9D8;${weight}">${r.c}</td>
      <td style="color:#FC8F8F;${weight}">${formatter(r.a)}</td>
      <td style="color:#DFD9D8;${weight}">${formatter(r.b)}</td>
      <td style="color:${dColor}">${r.qaly ? (delta>0?'+':'')+delta.toFixed(2) : (delta>0?'+':'')+fmt(delta).replace('−','')}</td>
    </tr>`;
  }).join('');

  const icerFmt = isFinite(r.icer) ? fmt(r.icer)+'/QALY' : (r.icer===-Infinity ? 'Dominant' : 'Dominated');
  document.getElementById('breakdown-foot').innerHTML = `
    <tr><td colspan="3" style="color:#FC8F8F">Incremental Cost-Effectiveness Ratio</td>
        <td style="color:#FC8F8F;font-family:'DM Mono';font-weight:700">${icerFmt}</td></tr>`;

  drawTree(p, r);
}

['costA','costB','qalyA','qalyB','wtp','disc','p30','prod','precA','precB'].forEach(id => {
  document.getElementById(id).addEventListener('input', update);
});

document.querySelectorAll('#cancer-chips .chip').forEach(c => {
  c.addEventListener('click', () => {
    currentCancer = c.dataset.cancer;
    applyCancerDefaults();
    syncChips();
    update();
  });
});

loadFromURL();
update();
</script>
</body>
</html>
'''


# --- Flask routes -----------------------------------------------------------
@app.route("/")
def index():
    return HTML


@app.route("/calc", methods=["POST"])
def calculate():
    """Optional server-side CEA calculation endpoint (JS handles this client-side too)."""
    d = request.json
    df = 1 + d["disc"] * 0.5
    costA = d["costA"] / df
    costB = d["costB"] / df
    inc_cost = costA - costB
    inc_qaly = d["qalyA"] - d["qalyB"]
    if inc_qaly > 0:
        icer = inc_cost / inc_qaly
    elif inc_cost <= 0:
        icer = "Dominant"
    else:
        icer = "Dominated"

    return jsonify({
        "costA_disc": round(costA),
        "costB_disc": round(costB),
        "inc_cost":   round(inc_cost),
        "inc_qaly":   round(inc_qaly, 3),
        "icer":       icer if isinstance(icer, str) else round(icer),
    })


# --- Launch -----------------------------------------------------------------
PORT = 5051


def open_browser():
    webbrowser.open(f"http://localhost:{PORT}")


if __name__ == "__main__":
    print("=" * 60)
    print("  Georgia Cancer CEA — NIH vs Community")
    print(f"  Running at: http://localhost:{PORT}")
    print("  Press Ctrl+C in the console to stop")
    print("=" * 60)

    threading.Timer(1.2, open_browser).start()

    # --- Optional: share over the internet with ngrok ---------------
    # Uncomment to get a public share URL:
    #
    # from pyngrok import ngrok
    # public_url = ngrok.connect(PORT)
    # print(f"\n  Public URL: {public_url}")
    # print("  Share this URL with anyone!\n")

    app.run(port=PORT, debug=False)
