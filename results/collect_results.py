#!/usr/bin/env python3
"""Rebuild results/results.csv from the GitHub Actions artifacts of every run in results/runs_index.csv.

For each run it:
- downloads the run's artifacts with `gh` (cached in results/.cache/<run_id>/);
- mirrors the small evidence files into results/evidence/<run_id>/ (artifacts expire after 90 days; the
  session transcripts are left out because of their size, and the command lists are kept);
- derives the per-stage outcome, retries, tokens, duration, PR, CI and the review verdict;
- optionally (with --clone) rebuilds the exact code of the run's PR from `base_sha` + `diff.patch`, and runs
  the hidden tests for that issue against it (fork issue N -> hidden tests issue_{N-2}).

Usage (from the autose-a3 root):
    python3 results/collect_results.py --clone /path/to/python-markdown-clone --python /path/to/python3.11
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
REPO = "MittalManas2005/markdown"
EVIDENCE_FILES = {"spec.md", "design.md", "build_check.md", "test_report.md", "tester_notes.md", "STOPPED.md",
                  "diff.patch", "run_state.json", "usage.json", "pr.md", "release.json", "review.md",
                  "verdict.json", "review_findings.md", "posted.json", "rejected_verdict.json", "issue.md"}
FIELDS = ["run_id", "experiment", "attempt", "issue", "variant", "reviewer_model", "mode", "outcome",
          "rounds", "stopped_at_stage", "stage1", "stage2", "stage3", "stage4", "stage5_ci", "stage6_review", "retries",
          "failed_checks", "agent_calls", "pr", "review_findings", "reviewer_commands_ok", "hidden_passed", "hidden_total",
          "output_tokens", "input_tokens", "cache_read_tokens", "cache_creation_tokens", "cost_usd_list_price",
          "permission_denials", "duration_min", "run_url", "pr_url", "review_url", "notes"]


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], text=True, capture_output=True, check=True).stdout


def download(run_id: str) -> Path:
    cache = RESULTS / ".cache" / run_id
    if not cache.exists():
        tmp = Path(tempfile.mkdtemp())
        subprocess.run(["gh", "run", "download", run_id, "--repo", REPO, "--dir", str(tmp)], capture_output=True)
        shutil.move(str(tmp), cache)
    return cache


def mirror(run_id: str, cache: Path) -> None:
    for art in sorted(p for p in cache.iterdir() if p.is_dir()):
        dest = RESULTS / "evidence" / run_id / art.name
        for f in art.rglob("*"):
            keep = f.name in EVIDENCE_FILES or f.name.endswith(".commands.json")
            if f.is_file() and keep:
                target = dest / f.relative_to(art)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(f, target)


def review_url(pr: str, t0: str, t1: str) -> str:
    """The review this run posted: the github-actions review on the PR submitted during the run."""
    reviews = json.loads(gh("api", f"repos/{REPO}/pulls/{pr}/reviews", "--paginate"))
    hits = [r for r in reviews if (r.get("user") or {}).get("login") == "github-actions[bot]"
            and t0 <= (r.get("submitted_at") or "") <= t1]
    return hits[-1]["html_url"] if hits else ""


def load(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def stage_status(state: dict | None, stage: int) -> str:
    if not state:
        return ""
    checks = [c for c in state.get("checks", []) if c.get("stage") == stage]
    if checks:
        return "pass" if checks[-1].get("ok") else "fail"
    if state.get("status") == "needs_input" and stage == 1:
        return "needs_input"
    return ""


def hidden(clone: Path, python: str, base: str, patch: Path, issue: int) -> tuple[int, int]:
    n = issue - 2
    tests = ROOT / "experiment" / "hidden_tests" / f"issue_{n}"
    if n < 1 or not tests.exists() or not patch.exists():
        return 0, 0
    wt = Path(tempfile.mkdtemp()) / "wt"
    subprocess.run(["git", "worktree", "add", "-q", "--detach", str(wt), base], cwd=clone, check=True)
    try:
        subprocess.run(["git", "apply", str(patch)], cwd=wt, check=True)
        out = subprocess.run(["bash", str(ROOT / "experiment" / "hidden_tests" / "run_hidden.sh"), str(wt), str(n),
                              python], text=True, capture_output=True)
        text = out.stdout + out.stderr
        ran = next((int(line.split()[1]) for line in text.splitlines() if line.startswith("Ran ")), 0)
        # Count failing test methods, not subtest failures (one method can fail several subtests).
        failing = {line.split()[1] for line in text.splitlines() if line.startswith(("FAIL:", "ERROR:"))}
        return ran - min(len(failing), ran), ran
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(wt)], cwd=clone, capture_output=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clone", type=Path, help="Python-Markdown clone (for hidden tests)")
    ap.add_argument("--python", default="python3")
    a = ap.parse_args()
    if a.clone:
        subprocess.run(["git", "fetch", "-q", f"https://github.com/{REPO}.git", "main"], cwd=a.clone, check=True)
    rows = []
    for idx in csv.DictReader((RESULTS / "runs_index.csv").open()):
        rid = idx["run_id"]
        info = json.loads(gh("run", "view", rid, "--repo", REPO, "--json", "createdAt,updatedAt,url,status"))
        t0, t1 = info["createdAt"], info["updatedAt"]
        if info["status"] != "completed":  # never cache a running run's partial artifacts
            print(f"{rid} still {info['status']}: skipped")
            continue
        cache = download(rid)
        mirror(rid, cache)
        dur = (datetime.fromisoformat(info["updatedAt"].replace("Z", "+00:00"))
               - datetime.fromisoformat(info["createdAt"].replace("Z", "+00:00"))).total_seconds() / 60
        def by_round(kind: str) -> list[Path]:
            found = [(int(m.group(1)), d) for d in cache.iterdir()
                     if (m := re.search(rf"-r(\d+)-{kind}$", d.name))]
            return [d for _, d in sorted(found)]
        builds, rels, revs = by_round("build"), by_round("release"), by_round("review")
        rounds = max([len(builds), len(revs), 1])
        build = builds[-1] if builds else None          # the last round decides the outcome
        rel = rels[-1] if rels and len(rels) == len(builds) else None
        rev = revs[-1] if revs and (not builds or len(revs) == len(builds)) else None
        state = load(build / "run_state.json") if build else None
        release = load(rel / "release.json") if rel else None
        verdict = load(rev / "verdict.json") if rev else None
        usage = []                                      # tokens are summed over every round
        for art in builds + revs:
            usage += load(art / "usage.json") or []
        review_md = (rev / "review.md").read_text() if rev and (rev / "review.md").exists() else ""
        if verdict:
            review = verdict["verdict"] if rev or not builds else f"{verdict['verdict']} (round {len(revs)})"
        elif "verdict: error" in review_md:
            review = "error"
        else:
            review = ""
        ci = (release or {}).get("ci", "")
        status = (state or {}).get("status", "")
        if idx["mode"] == "review-only":
            outcome = {"approve": "approved", "request_changes": "changes_requested"}.get(review, review or "error")
        elif status == "needs_input":
            outcome = "needs_input"
        elif status and status != "ready":
            outcome = "stopped"
        elif status == "ready" and not release and idx["mode"] != "review-only":
            outcome = "release_failed"
        elif ci and ci != "success":
            outcome = "stopped_ci"
        else:
            outcome = {"approve": "approved", "request_changes": "changes_requested"}.get(review, review or "error")
        retries = [t["reason"] for t in (state or {}).get("transitions", [])
                   if any(k in t["reason"] for k in ("retr", "back to", "failed;"))]
        cmds = []
        for art in revs:
            for f in art.glob("logs/*.commands.json"):
                cmds += json.loads(f.read_text())
        if not verdict and revs:                        # e.g. the last round never reached review
            verdict = load(revs[-1] / "verdict.json")
        hp = ht = ""
        if a.clone and build and (build / "diff.patch").exists() and state and status == "ready":
            p, t = hidden(a.clone, a.python, state["base_sha"], build / "diff.patch", int(idx["issue"]))
            if t:
                hp, ht = p, t
        pr = (release or {}).get("pr", "") or idx.get("pr", "")
        rows.append({
            **{k: idx[k] for k in ("run_id", "experiment", "attempt", "issue", "variant", "reviewer_model", "mode")},
            "outcome": outcome, "rounds": rounds, "stopped_at_stage": (state or {}).get("stop_stage", ""),
            **{f"stage{i}": stage_status(state, i) for i in (1, 2, 3, 4)},
            "stage5_ci": ci, "stage6_review": review, "retries": " | ".join(retries),
            "failed_checks": " | ".join(f"stage {c['stage']}: {(c.get('reasons') or [''])[0][:80]}"
                                        for art in builds for c in (load(art / "run_state.json") or {}).get("checks", [])
                                        if not c.get("ok")),
            "agent_calls": " ".join(f"{u['role']}{u['attempt']}" for u in usage), "pr": pr,
            "review_findings": " ".join(f["severity"] for f in (verdict or {}).get("findings", [])),
            "reviewer_commands_ok": sum(1 for c in cmds if c.get("ok")) if revs else "",
            "hidden_passed": hp, "hidden_total": ht,
            "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
            "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
            "cache_read_tokens": sum(u.get("cache_read_input_tokens", 0) for u in usage),
            "cache_creation_tokens": sum(u.get("cache_creation_input_tokens", 0) for u in usage),
            "cost_usd_list_price": round(sum(u.get("cost_usd_list_price", 0) or 0 for u in usage), 4),
            "permission_denials": sum(u.get("permission_denials", 0) for u in usage),
            "duration_min": round(dur, 1), "run_url": info["url"],
            "pr_url": f"https://github.com/{REPO}/pull/{pr}" if pr else "",
            "review_url": review_url(pr, t0, t1) if pr and revs else "", "notes": idx["notes"],
        })
        print(f"{rid} {idx['experiment']:<8} #{idx['issue']} {outcome:<18} hidden {hp}/{ht}")
    with (RESULTS / "results.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    write_runs_md(rows)
    print(f"wrote {len(rows)} rows to results/results.csv and results/runs.md")
    return 0


def stage_rates(rows: list[dict]) -> str:
    """Pass rate per stage over the full runs of one group: passes / runs that reached the stage."""
    cells = []
    for key, label in [("stage1", "1 spec"), ("stage2", "2 design"), ("stage3", "3 build"), ("stage4", "4 tests"),
                       ("stage5_ci", "5 CI"), ("stage6_review", "6 review")]:
        reached = [r for r in rows if r[key]]
        good = [r for r in reached if r[key] in ("pass", "success", "approve")]
        cells.append(f"{label}: {len(good)}/{len(reached)}")
    return " · ".join(cells)


def write_runs_md(rows: list[dict]) -> None:
    out = ["# Runs", "",
           "Generated by `results/collect_results.py` from each run's artifacts. Every run is listed, including the "
           "failed ones. Evidence files are mirrored in `results/evidence/<run_id>/` because GitHub artifacts "
           "expire after 90 days.", ""]
    for group in ("smoke", "baseline", "E1", "E2", "after-fix", "injection"):
        g = [r for r in rows if r["experiment"] == group]
        if not g:
            continue
        full = [r for r in g if r["mode"] != "review-only"]
        out += [f"## {group}", ""]
        if full:
            out += [f"Stage pass rates over these runs (passed / reached): {stage_rates(full)}", ""]
        out += ["| run | attempt | issue | variant / reviewer | outcome | stages 1-4 | CI | review | hidden tests "
                "| output tokens | min | PR · review | notes |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in g:
            stages = " ".join(r[f"stage{i}"] or "-" for i in (1, 2, 3, 4))
            hid = f"{r['hidden_passed']}/{r['hidden_total']}" if r["hidden_total"] else "-"
            pr = f"[#{r['pr']}]({r['pr_url']})" if r["pr"] else "-"
            if r["review_url"]:
                pr += f" · [review]({r['review_url']})"
            out.append(f"| [{r['run_id']}]({r['run_url']}) | {r['attempt']} | #{r['issue']} | {r['variant']} / "
                       f"{r['reviewer_model']} | {r['outcome']} | {stages} | {r['stage5_ci'] or '-'} | "
                       f"{r['stage6_review'] or '-'} | {hid} | {r['output_tokens']} | {r['duration_min']} | {pr} | "
                       f"{r['notes']} |")
        out.append("")
    total = sum(int(r["output_tokens"]) for r in rows)
    cache = sum(int(r["cache_read_tokens"]) + int(r["cache_creation_tokens"]) for r in rows)
    fresh = sum(int(r["input_tokens"]) for r in rows)
    out += ["## Total token usage (all runs above)", "",
            f"- output tokens: {total:,}", f"- input tokens (uncached): {fresh:,}",
            f"- cached input tokens (read + creation): {cache:,}",
            f"- list-price equivalent: ${sum(float(r['cost_usd_list_price']) for r in rows):.2f} "
            "(the runs used a Claude Pro subscription, so this is usage, not money spent)", ""]
    (RESULTS / "runs.md").write_text("\n".join(out))


if __name__ == "__main__":
    raise SystemExit(main())
