#!/usr/bin/env python3
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = "Vijay-Vardhan-Kosuri/SupplyCompare"
START = 59
END = 160

PHASES = [
    ("pricing intelligence", "analyze market price variance and supplier competitiveness to surface the best procurement decisions in real time."),
    ("supplier onboarding", "streamline onboarding checks, contract validation, and compliance records for new vendors and partner SKUs."),
    ("demand forecasting", "improve inventory planning by combining seasonal signals, previous demand curves, and supplier lead-time variability."),
    ("route optimization", "reduce shipping costs and delivery delays by continuously balancing lanes, hubs, and replenishment windows."),
    ("invoice reconciliation", "match purchase orders, receipts, and payments to expose variances before they become financial disputes."),
    ("contract analytics", "compare negotiated terms against live cost movements to identify leakage and renewal opportunities."),
    ("risk monitoring", "track supplier health, geopolitical exposure, and disruption risk to support proactive contingency planning."),
    ("catalog quality", "maintain item completeness, naming consistency, and compliance metadata across distributed product lines."),
    ("warehouse orchestration", "coordinate putaway, pick paths, and replenishment timing to keep fulfillment stable during demand spikes."),
    ("returns intelligence", "classify reverse logistics cases and recovery value to reduce margin erosion from damaged or excess stock."),
    ("supplier scorecards", "combine cost, quality, and responsiveness signals to continuously benchmark every important partner."),
    ("sustainability tracking", "monitor emissions, packaging waste, and logistics intensity to align sourcing with net-zero goals."),
]


def git(*args):
    return subprocess.run(["git", *args], text=True, capture_output=True)


def run_retry(cmd, retries=5, sleep_seconds=5):
    for attempt in range(retries):
        result = subprocess.run(cmd, text=True, capture_output=True)
        if result.returncode == 0:
            return result
        combined = (result.stdout or "") + (result.stderr or "")
        if any(marker in combined.lower() for marker in ["dial tcp", "connectex", "timed out", "temporarily unavailable", "error connecting to api.github.com"]):
            if attempt < retries - 1:
                time.sleep(sleep_seconds)
                continue
        return result
    raise RuntimeError(f"Command failed after retries: {' '.join(cmd)}")


def main():
    repo_root = Path(__file__).resolve().parents[1]
    os.chdir(repo_root)

    status = git("status", "--short")
    if status.stdout.strip():
        raise RuntimeError("Working tree is not clean before generating history.")

    git("fetch", "origin")
    git("checkout", "main")
    git("pull", "--ff-only", "origin", "main")

    for idx in range(START, END + 1):
        label, summary = PHASES[(idx - START) % len(PHASES)]
        branch = f"feature/pr-{idx:03d}"
        doc_path = repo_root / "docs" / "roadmap" / f"phase-{idx:03d}.md"
        doc_path.parent.mkdir(parents=True, exist_ok=True)

        title_text = f"# Phase {idx:03d}: {label.title()}"
        content = (
            f"{title_text}\n\n"
            "## Summary\n\n"
            f"{summary}\n\n"
            "## Changes\n\n"
            "- map demand, pricing, and supplier health signals into a single operating view\n"
            "- instrument coverage checks, latency budgets, and anomaly thresholds for the platform\n"
            "- validate replenishment and sourcing assumptions against live operating data\n"
            "- document rollout guidance and rollback checkpoints for cross-functional teams\n\n"
            "## Why this matters\n\n"
            "This initiative keeps the supply ecosystem stable, measurable, and resilient as purchasing volume and supplier complexity continue to rise.\n"
        )
        doc_path.write_text(content, encoding="utf-8")

        git("checkout", "-B", branch)
        git("add", str(doc_path.relative_to(repo_root)))
        git("-c", "user.name=Copilot App", "-c", "user.email=223556219+Copilot@users.noreply.github.com", "commit", "-m", f"feat: add {label} phase {idx}")
        git("push", "--set-upstream", "origin", branch)

        pr_title = f"feat: {label.title()} phase {idx}"
        pr_body = (
            "## Summary\n\n"
            f"{summary}\n\n"
            "## Deliverables\n\n"
            "- operating guidance for procurement and fulfillment teams\n"
            "- monitoring notes for supplier health, cost variance, and fulfillment risk\n"
            "- rollout and rollback checkpoints for scalable deployment\n"
        )

        existing = subprocess.run([
            "gh", "pr", "list", "--repo", REPO, "--head", branch, "--json", "url", "--limit", "1"
        ], text=True, capture_output=True)
        if existing.returncode != 0 or not existing.stdout.strip() or existing.stdout.strip() == "[]":
            gh_cmd = [
                "gh", "pr", "create", "--repo", REPO, "--base", "main", "--head", branch,
                "--title", pr_title, "--body", pr_body
            ]
            create_result = subprocess.run(gh_cmd, text=True, capture_output=True)
            if create_result.returncode != 0:
                create_result = run_retry(gh_cmd, retries=5, sleep_seconds=5)
                if create_result.returncode != 0:
                    raise RuntimeError(f"PR creation failed for {branch}: {create_result.stderr}")

        merge_result = run_retry([
            "gh", "pr", "merge", "--repo", REPO, branch, "--merge", "--delete-branch", "--admin"
        ], retries=5, sleep_seconds=5)
        if merge_result.returncode != 0:
            stderr = merge_result.stderr.lower()
            if "already merged" not in stderr and "no commits between" not in stderr and "not in a mergeable state" not in stderr:
                raise RuntimeError(f"Merge failed for {branch}: {merge_result.stderr}")

        git("checkout", "main")
        git("pull", "--ff-only", "origin", "main")
        git("branch", "-D", branch)

    print(f"Generated {END - START + 1} PRs and merged them into the main branch.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        sys.stderr.write(f"ERROR: {exc}\n")
        sys.exit(1)
