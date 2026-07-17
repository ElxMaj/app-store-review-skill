#!/usr/bin/env python3
"""Render an App Store review JSON report as a self-contained HTML artifact."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence


SEVERITY_ORDER = ("blocker", "warning", "manual_check", "info")
SEVERITY_LABEL = {
    "blocker": "Blocker",
    "warning": "Warning",
    "manual_check": "Manual check",
    "info": "Info",
}
VERDICT_LABEL = {
    "NO_STATIC_BLOCKERS_FOUND": "No static blockers found",
    "NEEDS_REVIEW": "Needs review",
    "NOT_READY": "Not ready",
}
MODE_LABEL = {
    "pre_submission": "Pre-submission",
    "rejection_recovery": "Rejection recovery",
    "human_craft": "Human-craft audit",
}


STYLES = r"""
:root {
  color-scheme: light dark;
  --canvas: #e9e8e3;
  --paper: #f8f7f3;
  --ink: #181817;
  --muted: #666662;
  --quiet: #8b8b84;
  --rule: rgba(24, 24, 23, 0.18);
  --rule-strong: rgba(24, 24, 23, 0.5);
  --wash: rgba(24, 24, 23, 0.045);
  --danger: #b52a22;
  --warning: #95620a;
  --success: #26734d;
  --link: #1256a0;
  --accent: var(--danger);
}

* { box-sizing: border-box; }

html { max-width: 100%; overflow-x: hidden; background: var(--canvas); }

body {
  margin: 0;
  padding: 28px 0 64px;
  max-width: 100%;
  overflow-x: hidden;
  background: var(--canvas);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  line-height: 1.55;
  font-optical-sizing: auto;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

a { color: var(--link); text-underline-offset: 0.16em; }
code, pre, .mono {
  font-family: ui-monospace, "SFMono-Regular", SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

.report {
  width: min(1080px, calc(100% - 32px));
  margin: 0 auto;
  overflow: clip;
  border: 1px solid var(--rule);
  border-top: 4px solid var(--accent);
  background: var(--paper);
}

.shell { padding-inline: clamp(22px, 5vw, 56px); }

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding-top: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--rule);
}

.identity { display: flex; align-items: baseline; gap: 11px; min-width: 0; }
.identity-title {
  margin: 0;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.identity-subtitle { margin: 0; color: var(--muted); font-size: 12px; }
.policy { color: var(--muted); font-size: 12px; white-space: nowrap; }

.hero { padding-top: clamp(54px, 8vw, 92px); padding-bottom: 50px; }
.sample-flag {
  margin: 0 0 18px;
  color: var(--accent);
  font-family: ui-monospace, "SFMono-Regular", SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.hero-heading {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(210px, 0.36fr);
  gap: clamp(34px, 7vw, 86px);
  align-items: end;
}
.hero h1 {
  margin: 0;
  max-width: 720px;
  font-size: clamp(40px, 6vw, 62px);
  font-weight: 600;
  letter-spacing: -0.045em;
  line-height: 1;
  overflow-wrap: anywhere;
}
.verdict-block { padding: 4px 0 4px 22px; border-left: 1px solid var(--rule-strong); }
.verdict-caption {
  display: block;
  margin-bottom: 7px;
  color: var(--muted);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.verdict { display: block; color: var(--accent); font-size: 22px; font-weight: 600; letter-spacing: -0.02em; }
.hero-summary {
  max-width: 780px;
  margin: 34px 0 0;
  color: var(--ink);
  font-size: clamp(19px, 2.5vw, 25px);
  line-height: 1.42;
  letter-spacing: -0.02em;
  overflow-wrap: anywhere;
}
.mode-row { display: flex; flex-wrap: wrap; gap: 0; margin-top: 27px; color: var(--muted); font-size: 12px; }
.mode-item + .mode-item::before { content: "/"; margin-inline: 10px; color: var(--quiet); }

.metrics {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  border-top: 1px solid var(--rule-strong);
  border-bottom: 1px solid var(--rule);
}
.metric { display: flex; align-items: baseline; gap: 8px; min-width: 0; padding: 15px 0; }
.metric + .metric { padding-left: 24px; border-left: 1px solid var(--rule); }
.metric-value { font-size: 20px; font-weight: 600; letter-spacing: -0.02em; }
.metric-label { color: var(--muted); font-size: 12px; }

.document-grid {
  display: grid;
  grid-template-columns: 148px minmax(0, 1fr);
  gap: clamp(38px, 6vw, 76px);
  align-items: start;
}

.report-index { position: sticky; top: 24px; margin-top: 76px; }
.index-label {
  margin: 0 0 14px;
  color: var(--muted);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.report-index ol { margin: 0; padding: 0; list-style: none; counter-reset: report-index; }
.report-index li { counter-increment: report-index; border-top: 1px solid var(--rule); }
.report-index a { display: grid; grid-template-columns: 22px 1fr; gap: 5px; padding: 8px 0; color: var(--muted); font-size: 11px; text-decoration: none; }
.report-index a::before { content: counter(report-index, decimal-leading-zero); color: var(--quiet); font-family: ui-monospace, "SFMono-Regular", SFMono-Regular, Menlo, Monaco, Consolas, monospace; }

main { min-width: 0; padding-bottom: 100px; counter-reset: report-section; }
.section { margin-top: 76px; counter-increment: report-section; }
.section-heading { padding-top: 18px; border-top: 1px solid var(--rule-strong); margin-bottom: 28px; }
.section-kicker { margin: 0 0 7px; color: var(--accent); font-size: 11px; font-weight: 600; letter-spacing: 0.09em; text-transform: uppercase; }
.section-kicker::before { content: counter(report-section, decimal-leading-zero) " / "; }
.section h2 { margin: 0; font-size: clamp(27px, 3.5vw, 36px); font-weight: 600; letter-spacing: -0.035em; line-height: 1.08; }
.section-intro { max-width: 660px; margin: 13px 0 0; color: var(--muted); font-size: 15px; overflow-wrap: anywhere; }

.scope-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); }
.scope-item { min-width: 0; padding: 19px 0; }
.scope-item + .scope-item { padding-left: 22px; border-left: 1px solid var(--rule); }
.scope-label { display: block; color: var(--muted); font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; }
.scope-value { display: block; margin-top: 7px; font-size: 15px; font-weight: 600; overflow-wrap: anywhere; }
.limitations { margin: 20px 0 0; padding: 0; list-style: none; }
.limitations li { position: relative; padding: 8px 0 8px 19px; color: var(--muted); font-size: 13px; }
.limitations li::before { content: ""; position: absolute; top: 1.05em; left: 0; width: 6px; border-top: 1px solid var(--quiet); }

.finding-list { border-top: 1px solid var(--rule); }
.finding {
  padding: 30px 0 44px;
  border-bottom: 1px solid var(--rule);
}
.finding-header { display: grid; grid-template-columns: minmax(0, 1fr) minmax(190px, 0.42fr); gap: 28px; align-items: start; }
.finding-id { margin: 0 0 7px; color: var(--tone); font-size: 10px; font-weight: 600; letter-spacing: 0.07em; }
.finding h3 { margin: 0; font-size: 24px; font-weight: 600; letter-spacing: -0.025em; line-height: 1.18; }
.finding-badges { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 0; color: var(--muted); font-size: 10px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; }
.badge + .badge::before { content: "/"; margin-inline: 7px; color: var(--quiet); }
.badge-severity { color: var(--tone); }
.finding-body { display: grid; grid-template-columns: minmax(0, 0.88fr) minmax(0, 1.12fr); gap: 34px; margin-top: 25px; }
.evidence { padding: 18px 19px; border-left: 2px solid var(--tone); background: var(--wash); }
.evidence-title, .detail-label { margin: 0 0 9px; color: var(--muted); font-size: 10px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; }
.evidence-list { margin: 0; padding: 0; list-style: none; }
.evidence-list li + li { margin-top: 12px; }
.evidence-path { display: block; font-size: 11px; font-weight: 600; overflow-wrap: anywhere; }
.evidence-excerpt { display: block; margin-top: 4px; color: var(--muted); font-size: 12px; overflow-wrap: anywhere; }
.details { display: grid; gap: 19px; }
.detail p { margin: 0; color: var(--ink); font-size: 14px; }
.detail-fix { padding: 15px 0 15px 16px; border-left: 2px solid var(--tone); }

.tone-blocker { --tone: var(--accent); }
.tone-warning { --tone: var(--warning); }
.tone-manual_check { --tone: var(--muted); }
.tone-info { --tone: var(--link); }

.manual-grid, .craft-grid { border-top: 1px solid var(--rule); }
.manual-card, .craft-card { display: grid; grid-template-columns: 155px minmax(0, 1fr); gap: 25px; padding: 21px 0 23px; border-bottom: 1px solid var(--rule); }
.row-copy { min-width: 0; }
.manual-card h3, .craft-card h3 { margin: 0 0 7px; font-size: 17px; font-weight: 600; letter-spacing: -0.012em; }
.manual-card p, .craft-card p { margin: 0; color: var(--muted); font-size: 14px; }
.manual-verify { margin-top: 11px !important; color: var(--ink) !important; }
.grade { color: var(--grade-color, var(--ink)); font-size: 10px; font-weight: 600; letter-spacing: 0.07em; text-transform: uppercase; }

.transcript-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 34px; border-top: 1px solid var(--rule); }
.panel { min-width: 0; padding: 21px 0; border-bottom: 1px solid var(--rule); }
.panel pre { margin: 0; white-space: pre-wrap; overflow-wrap: anywhere; color: var(--ink); font-size: 12px; line-height: 1.65; }
.note-panel pre { padding: 20px 21px; border-left: 2px solid var(--accent); background: var(--wash); }
.checklist { margin: 0; padding: 0; list-style: none; }
.checklist li { display: grid; grid-template-columns: 18px minmax(0, 1fr); gap: 9px; padding: 10px 0; border-top: 1px solid var(--rule); font-size: 14px; }
.checklist li:first-child { border-top: 0; }
.check-symbol { color: var(--accent); font-weight: 600; }
.text-muted { color: var(--muted); }
.fix-group { display: grid; grid-template-columns: 190px minmax(0, 1fr); gap: 30px; padding: 22px 0; border-top: 1px solid var(--rule); }
.fix-group:last-child { border-bottom: 1px solid var(--rule); }
.fix-group h3 { margin: 0; font-size: 15px; font-weight: 600; }
.fix-group ul { margin: 0; padding-left: 18px; color: var(--muted); font-size: 14px; }
.approval { display: block; grid-column: 2; margin-top: -15px; color: var(--accent); font-size: 11px; font-weight: 600; }

.empty-state { padding: 22px 0; border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); color: var(--muted); }

.footer { padding-top: 25px; padding-bottom: 32px; border-top: 1px solid var(--rule-strong); color: var(--muted); font-size: 11px; }
.footer-row { display: flex; justify-content: space-between; gap: 24px; }

@media (prefers-color-scheme: dark) {
  :root {
    --canvas: #11110f;
    --paper: #1b1b18;
    --ink: #f1f0ea;
    --muted: #aaa9a2;
    --quiet: #7f7e78;
    --rule: rgba(241, 240, 234, 0.16);
    --rule-strong: rgba(241, 240, 234, 0.45);
    --wash: rgba(241, 240, 234, 0.055);
    --danger: #ff6b62;
    --warning: #e4ad51;
    --success: #69c794;
    --link: #74aef0;
  }
}

@media (max-width: 820px) {
  body { padding-top: 0; padding-bottom: 0; }
  .report { width: 100%; border-right: 0; border-left: 0; border-bottom: 0; }
  .document-grid { grid-template-columns: 1fr; gap: 0; }
  .report-index { position: static; margin-top: 48px; padding-bottom: 16px; border-bottom: 1px solid var(--rule); }
  .report-index ol { display: flex; flex-wrap: wrap; gap: 0 18px; }
  .report-index li { border-top: 0; }
  .report-index a { grid-template-columns: 19px auto; padding: 4px 0; }
  .section { margin-top: 64px; }
}

@media (max-width: 620px) {
  .topbar { display: grid; gap: 5px; }
  .identity { display: grid; gap: 2px; }
  .policy { white-space: normal; }
  .hero { padding-top: 50px; padding-bottom: 38px; }
  .hero-heading { grid-template-columns: 1fr; gap: 26px; }
  .verdict-block { padding: 15px 0 0; border-top: 1px solid var(--rule-strong); border-left: 0; }
  .hero-summary { margin-top: 28px; }
  .metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .metric { padding: 12px 0; }
  .metric + .metric { padding-left: 18px; }
  .metric:nth-child(3) { padding-left: 0; border-top: 1px solid var(--rule); border-left: 0; }
  .metric:nth-child(4) { border-top: 1px solid var(--rule); }
  .scope-grid { grid-template-columns: 1fr; }
  .scope-item + .scope-item { padding-left: 0; border-top: 1px solid var(--rule); border-left: 0; }
  .finding-header { grid-template-columns: 1fr; gap: 13px; }
  .finding-badges { justify-content: flex-start; }
  .finding-body { grid-template-columns: 1fr; }
  .manual-card, .craft-card, .fix-group { grid-template-columns: 1fr; gap: 8px; }
  .approval { grid-column: 1; margin-top: 1px; }
  .transcript-grid { grid-template-columns: 1fr; gap: 0; }
  .footer-row { display: grid; }
}

@media (prefers-contrast: more) {
  :root { --rule: currentColor; --rule-strong: currentColor; }
}

@media print {
  :root {
    color-scheme: light;
    --canvas: #ffffff;
    --paper: #ffffff;
    --ink: #000000;
    --muted: #4e4e4a;
    --quiet: #777772;
    --rule: #d1d1cc;
    --rule-strong: #777772;
    --wash: #f5f5f2;
  }
  @page { margin: 15mm; }
  body { padding: 0; background: #ffffff; }
  .report { width: 100%; border-right: 0; border-bottom: 0; border-left: 0; }
  .shell { padding-inline: 0; }
  .hero { padding-top: 35px; }
  .document-grid { display: block; }
  .report-index { display: none; }
  #findings, #fix-plan { break-before: page; page-break-before: always; }
  .section-heading { break-after: avoid-page; page-break-after: avoid; }
  .finding, .manual-card, .craft-card, .panel, .fix-group { break-inside: avoid; }
  .section { margin-top: 48px; }
}
"""


def escape(value: Any, fallback: str = "Not supplied") -> str:
    if value is None or value == "":
        value = fallback
    return html.escape(str(value), quote=True)


def as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def report_counts(report: Mapping[str, Any]) -> Dict[str, int]:
    counts = {key: 0 for key in SEVERITY_ORDER}
    supplied = report.get("counts")
    if isinstance(supplied, Mapping):
        for key in counts:
            try:
                counts[key] = int(supplied.get(key, 0) or 0)
            except (TypeError, ValueError):
                counts[key] = 0
    else:
        for finding in as_list(report.get("findings")):
            if isinstance(finding, Mapping):
                severity = str(finding.get("severity", "info")).lower()
                if severity in counts:
                    counts[severity] += 1
        counts["manual_check"] = len(as_list(report.get("manual_checks")))
    return counts


def project_name(report: Mapping[str, Any]) -> str:
    if report.get("app_name"):
        return str(report["app_name"])
    root = str(report.get("root", "App"))
    return Path(root).name or "App"


def verdict_key(report: Mapping[str, Any]) -> str:
    return str(report.get("verdict", "NEEDS_REVIEW")).strip().upper().replace(" ", "_")


def join_names(values: Iterable[Any], fallback: str = "Not resolved") -> str:
    names: List[str] = []
    for item in values:
        if isinstance(item, Mapping):
            value = item.get("name") or item.get("label") or item.get("id")
        else:
            value = item
        if value:
            names.append(str(value))
    return ", ".join(names) if names else fallback


def render_modes(report: Mapping[str, Any]) -> str:
    modes = as_list(report.get("modes") or report.get("mode"))
    if not modes:
        modes = ["pre_submission"]
    chips = []
    for mode in modes:
        key = str(mode).strip().lower().replace("-", "_").replace(" ", "_")
        chips.append(f'<span class="mode-item">{escape(MODE_LABEL.get(key, str(mode)))}</span>')
    return "".join(chips)


def render_metrics(counts: Mapping[str, int]) -> str:
    items = []
    for key in SEVERITY_ORDER:
        items.append(
            '<div class="metric">'
            f'<span class="metric-value">{counts.get(key, 0)}</span>'
            f'<span class="metric-label">{escape(SEVERITY_LABEL[key])}</span>'
            "</div>"
        )
    return "".join(items)


def render_scope(report: Mapping[str, Any]) -> str:
    project = report.get("project") if isinstance(report.get("project"), Mapping) else {}
    frameworks = join_names(as_list(project.get("frameworks")))
    targets = join_names(as_list(project.get("targets")))
    native_root = project.get("native_ios_root") or "Not resolved"
    limitations = as_list(report.get("limitations"))
    limitations_html = "".join(f"<li>{escape(item)}</li>" for item in limitations)
    if not limitations_html:
        limitations_html = "<li>Runtime and App Store Connect checks remain manual unless explicitly verified.</li>"
    return f"""
    <section class="section" id="scope">
      <div class="section-heading">
        <p class="section-kicker">Scope</p>
        <h2>Review scope</h2>
        <p class="section-intro">Frameworks, native targets, and evidence limits included in this review.</p>
      </div>
      <div class="scope-grid">
        <div class="scope-item"><span class="scope-label">Frameworks</span><span class="scope-value">{escape(frameworks)}</span></div>
        <div class="scope-item"><span class="scope-label">Native iOS root</span><span class="scope-value mono">{escape(native_root)}</span></div>
        <div class="scope-item"><span class="scope-label">Targets</span><span class="scope-value">{escape(targets)}</span></div>
      </div>
      <ul class="limitations">{limitations_html}</ul>
    </section>
    """


def evidence_location(item: Mapping[str, Any]) -> str:
    path = str(item.get("path") or "Location not supplied")
    line = item.get("line")
    if line is not None and line != "":
        path += f":{line}"
    return path


def render_finding(item: Mapping[str, Any]) -> str:
    severity = str(item.get("severity", "info")).lower().replace(" ", "_")
    if severity not in SEVERITY_LABEL:
        severity = "info"
    evidence_items = []
    for evidence in as_list(item.get("evidence")):
        if not isinstance(evidence, Mapping):
            evidence_items.append(f'<li><span class="evidence-excerpt">{escape(evidence)}</span></li>')
            continue
        evidence_items.append(
            "<li>"
            f'<span class="evidence-path mono">{escape(evidence_location(evidence))}</span>'
            f'<span class="evidence-excerpt">{escape(evidence.get("excerpt"), "No excerpt supplied")}</span>'
            "</li>"
        )
    if not evidence_items:
        evidence_items.append('<li><span class="evidence-excerpt">No repository evidence supplied.</span></li>')
    confidence = str(item.get("evidence_confidence", "unverified")).replace("_", " ").upper()
    return f"""
    <article class="finding tone-{severity}">
      <header class="finding-header">
        <div>
          <p class="finding-id mono">{escape(item.get("id"), "ASR-UNVERIFIED")}</p>
          <h3>{escape(item.get("title"), "Untitled finding")}</h3>
        </div>
        <div class="finding-badges">
          <span class="badge badge-severity">{escape(SEVERITY_LABEL[severity])}</span>
          <span class="badge">{escape(item.get("guideline"), "Guideline unverified")}</span>
          <span class="badge">{escape(confidence)}</span>
        </div>
      </header>
      <div class="finding-body">
        <div class="evidence">
          <p class="evidence-title">Evidence</p>
          <ul class="evidence-list">{"".join(evidence_items)}</ul>
        </div>
        <div class="details">
          <div class="detail"><p class="detail-label">Why it matters</p><p>{escape(item.get("reason"), "Reason not supplied")}</p></div>
          <div class="detail detail-fix"><p class="detail-label">Fix</p><p>{escape(item.get("fix"), "Fix not supplied")}</p></div>
          <div class="detail"><p class="detail-label">Verify</p><p>{escape(item.get("verification"), "Verification step not supplied")}</p></div>
        </div>
      </div>
    </article>
    """


def render_findings(report: Mapping[str, Any]) -> str:
    findings = [item for item in as_list(report.get("findings")) if isinstance(item, Mapping)]
    finding_html = "".join(render_finding(item) for item in findings)
    if not finding_html:
        finding_html = '<p class="empty-state">No confirmed static findings were included in this report.</p>'
    return f"""
    <section class="section" id="findings">
      <div class="section-heading">
        <p class="section-kicker">Findings</p>
        <h2>Submission findings</h2>
        <p class="section-intro">Sorted by severity. Each item keeps the file evidence, policy basis, correction, and verification step together.</p>
      </div>
      <div class="finding-list">{finding_html}</div>
    </section>
    """


def render_manual_checks(report: Mapping[str, Any]) -> str:
    checks = [item for item in as_list(report.get("manual_checks")) if isinstance(item, Mapping)]
    if not checks:
        return ""
    cards = []
    for item in checks:
        cards.append(
            '<article class="manual-card">'
            f'<span class="grade">{escape(item.get("id"), "MANUAL CHECK")}</span>'
            '<div class="row-copy">'
            f'<h3>{escape(item.get("title"), "Manual verification")}</h3>'
            f'<p>{escape(item.get("reason"), "Repository evidence cannot establish this check.")}</p>'
            f'<p class="manual-verify"><strong>Verify:</strong> {escape(item.get("verification"), "Verification step not supplied")}</p>'
            '</div>'
            "</article>"
        )
    return f"""
    <section class="section" id="manual-checks">
      <div class="section-heading">
        <p class="section-kicker">Manual checks</p>
        <h2>Checks still open</h2>
        <p class="section-intro">These require a release build, device, reviewer account, or App Store Connect evidence.</p>
      </div>
      <div class="manual-grid">{"".join(cards)}</div>
    </section>
    """


def grade_color(grade: str) -> str:
    normalized = grade.upper().replace("_", " ")
    if normalized == "DISTINCT":
        return "var(--success)"
    if normalized == "CREDIBLE":
        return "var(--ink)"
    if normalized == "GENERIC":
        return "var(--warning)"
    if normalized == "HIGH RISK":
        return "var(--danger)"
    return "var(--muted)"


def render_craft(report: Mapping[str, Any]) -> str:
    craft = report.get("craft")
    if not isinstance(craft, Mapping):
        return ""
    dimensions = [item for item in as_list(craft.get("dimensions")) if isinstance(item, Mapping)]
    if not dimensions:
        return ""
    cards = []
    for item in dimensions:
        grade = str(item.get("grade", "UNVERIFIED")).upper().replace("_", " ")
        evidence = item.get("evidence")
        if isinstance(evidence, list):
            evidence = " ".join(str(part) for part in evidence)
        cards.append(
            '<article class="craft-card">'
            f'<span class="grade" style="--grade-color:{grade_color(grade)}">{escape(grade)}</span>'
            '<div class="row-copy">'
            f'<h3>{escape(item.get("name"), "Craft dimension")}</h3>'
            f'<p>{escape(evidence, "Evidence not supplied")}</p>'
            '</div>'
            "</article>"
        )
    return f"""
    <section class="section" id="craft">
      <div class="section-heading">
        <p class="section-kicker">Human craft</p>
        <h2>Product craft review</h2>
        <p class="section-intro">Grades summarize visible evidence. They are not approval probabilities and do not claim to detect AI authorship.</p>
      </div>
      <div class="craft-grid">{"".join(cards)}</div>
    </section>
    """


def render_recovery(report: Mapping[str, Any]) -> str:
    recovery = report.get("recovery")
    if not isinstance(recovery, Mapping):
        return ""
    classification = recovery.get("classification") or "Interpretation pending"
    apple_message = recovery.get("apple_message") or "Apple message not supplied"
    reply = recovery.get("reply_draft") or "Reply draft not supplied"
    attachments = as_list(recovery.get("attachments"))
    attachment_html = "".join(f"<li><span class=\"check-symbol\">○</span><span>{escape(item)}</span></li>" for item in attachments)
    if not attachment_html:
        attachment_html = '<li><span class="check-symbol">○</span><span>No attachments specified.</span></li>'
    return f"""
    <section class="section" id="recovery">
      <div class="section-heading">
        <p class="section-kicker">Rejection recovery</p>
        <h2>{escape(classification)}</h2>
        <p class="section-intro">Apple's supplied wording stays separate from diagnosis and the proposed Resolution Center response.</p>
      </div>
      <div class="transcript-grid">
        <div class="panel"><p class="detail-label">Apple's message</p><pre>{escape(apple_message)}</pre></div>
        <div class="panel"><p class="detail-label">Resolution Center draft</p><pre>{escape(reply)}</pre></div>
      </div>
      <div class="panel"><p class="detail-label">Attachments</p><ul class="checklist">{attachment_html}</ul></div>
    </section>
    """


def render_reviewer_experience(report: Mapping[str, Any]) -> str:
    items = as_list(report.get("reviewer_experience"))
    if not items:
        return ""
    rows = []
    for item in items:
        if isinstance(item, Mapping):
            label = item.get("label") or item.get("title") or "Reviewer check"
            status = str(item.get("status", "manual")).lower()
            detail = item.get("detail") or item.get("evidence") or ""
        else:
            label, status, detail = item, "manual", ""
        symbol = "✓" if status in {"passed", "verified", "complete"} else "○"
        suffix = f" <span class=\"text-muted\">{escape(detail)}</span>" if detail else ""
        rows.append(f'<li><span class="check-symbol">{symbol}</span><span>{escape(label)}{suffix}</span></li>')
    return f"""
    <section class="section" id="reviewer-path">
      <div class="section-heading">
        <p class="section-kicker">Reviewer path</p>
        <h2>Reviewer path</h2>
        <p class="section-intro">A checkmark means the path was executed or supported by supplied evidence. An open circle remains manual.</p>
      </div>
      <div class="panel"><ul class="checklist">{"".join(rows)}</ul></div>
    </section>
    """


def render_notes(report: Mapping[str, Any]) -> str:
    notes = report.get("app_review_notes")
    if not notes:
        return ""
    return f"""
    <section class="section" id="review-notes">
      <div class="section-heading">
        <p class="section-kicker">App Review Notes</p>
        <h2>App Review Notes</h2>
        <p class="section-intro">Exact screen names, controls, setup, credential placeholders, and expected results for the reviewer.</p>
      </div>
      <div class="panel note-panel"><pre>{escape(notes)}</pre></div>
    </section>
    """


def render_fix_groups(report: Mapping[str, Any]) -> str:
    groups = [item for item in as_list(report.get("fix_groups")) if isinstance(item, Mapping)]
    if not groups:
        return ""
    output = []
    for group in groups:
        items = "".join(f"<li>{escape(item)}</li>" for item in as_list(group.get("items")))
        if not items:
            items = "<li>No changes listed.</li>"
        approval = group.get("approval_required", True)
        approval_text = "Approval required before editing" if approval else "No repository edits required"
        output.append(
            '<div class="fix-group">'
            f'<h3>{escape(group.get("id"), "Group")} · {escape(group.get("title"), "Proposed fixes")}</h3>'
            f"<ul>{items}</ul>"
            f'<span class="approval">{escape(approval_text)}</span>'
            "</div>"
        )
    return f"""
    <section class="section" id="fix-plan">
      <div class="section-heading">
        <p class="section-kicker">Fix plan</p>
        <h2>Proposed fixes</h2>
        <p class="section-intro">Confirmed submission work stays separate from optional product and craft changes. Repository edits still require approval.</p>
      </div>
      <div class="fix-list">{"".join(output)}</div>
    </section>
    """


def render_index(report: Mapping[str, Any]) -> str:
    entries = [("scope", "Scope"), ("findings", "Findings")]
    if as_list(report.get("manual_checks")):
        entries.append(("manual-checks", "Manual checks"))
    craft = report.get("craft")
    if isinstance(craft, Mapping) and as_list(craft.get("dimensions")):
        entries.append(("craft", "Product craft"))
    if isinstance(report.get("recovery"), Mapping):
        entries.append(("recovery", "Recovery"))
    if as_list(report.get("reviewer_experience")):
        entries.append(("reviewer-path", "Reviewer path"))
    if report.get("app_review_notes"):
        entries.append(("review-notes", "Review notes"))
    if as_list(report.get("fix_groups")):
        entries.append(("fix-plan", "Proposed fixes"))
    links = "".join(f'<li><a href="#{escape(anchor)}">{escape(label)}</a></li>' for anchor, label in entries)
    return f'<nav class="report-index" aria-label="Report contents"><p class="index-label">Contents</p><ol>{links}</ol></nav>'


def render_report_html(report: Mapping[str, Any]) -> str:
    name = project_name(report)
    verdict = verdict_key(report)
    verdict_label = VERDICT_LABEL.get(verdict, verdict.replace("_", " ").title())
    verdict_color = {
        "NOT_READY": "var(--danger)",
        "NEEDS_REVIEW": "var(--warning)",
        "NO_STATIC_BLOCKERS_FOUND": "var(--success)",
    }.get(verdict, "var(--link)")
    counts = report_counts(report)
    sample = bool(report.get("sample"))
    label = "Sample report" if sample else "Independent review report"
    generated = report.get("generated_at") or "Date not supplied"
    policy = report.get("policy_verified_at") or "Unverified"
    summary = report.get("summary") or "Review evidence, open checks, and the next safe action are collected below."
    disclaimer = report.get("disclaimer") or "Independent review based on supplied evidence and public guidance. Approval is not guaranteed. Not affiliated with Apple."

    document_start = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{escape(name)} · App Store review</title>\n"
        f"<style>{STYLES}</style>\n"
        "</head>\n<body>\n"
    )
    top = f"""
    <div class="report" style="--accent:{verdict_color}">
    <header class="shell topbar">
      <div class="identity">
        <p class="identity-title">App Store review</p>
        <p class="identity-subtitle">Independent release assessment</p>
      </div>
      <div class="policy">Policy / {escape(policy)}</div>
    </header>
    <section class="shell hero">
        <p class="sample-flag">{escape(label)}</p>
        <div class="hero-heading">
          <h1>{escape(name)}</h1>
          <div class="verdict-block"><span class="verdict-caption">Release verdict</span><span class="verdict">{escape(verdict_label)}</span></div>
        </div>
        <p class="hero-summary">{escape(summary)}</p>
        <div class="mode-row">{render_modes(report)}</div>
    </section>
    <div class="shell"><div class="metrics" aria-label="Finding counts">{render_metrics(counts)}</div></div>
    <div class="shell document-grid">
      {render_index(report)}
      <main>
        {render_scope(report)}
        {render_findings(report)}
        {render_manual_checks(report)}
        {render_craft(report)}
        {render_recovery(report)}
        {render_reviewer_experience(report)}
        {render_notes(report)}
        {render_fix_groups(report)}
      </main>
    </div>
    <footer class="shell footer"><div class="footer-row"><span>{escape(disclaimer)}</span><span class="mono">Generated {escape(generated)}</span></div></footer>
    </div>
    """
    document = document_start + top + "\n</body>\n</html>\n"
    return "\n".join(line.rstrip() for line in document.splitlines()) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", help="Path to an App Store review JSON report")
    parser.add_argument("--output", help="Output HTML path; defaults beside the JSON report")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    source = Path(args.report).expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"report is not a file: {source}")
    try:
        report = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"could not read report JSON: {exc}") from exc
    if not isinstance(report, dict):
        raise SystemExit("report JSON must contain an object at the top level")
    destination = Path(args.output).expanduser().resolve() if args.output else source.with_suffix(".html")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_report_html(report), encoding="utf-8")
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
