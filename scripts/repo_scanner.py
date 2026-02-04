#!/usr/bin/env python3
"""
REALM FORGE â€” SOVEREIGN BACKEND COMPARATOR v60.6

- Scans the repo
- Compares against canonical backend schema
- Lists ALL missing files (e.g., 110) for creation
- Lists extra files, but DOES NOT treat src/agents/* as extra
"""

import json
from pathlib import Path

# ---------------------------------------------------------
# 1. CANONICAL BACKEND SCHEMA (exactly your structure)
# ---------------------------------------------------------
CANONICAL_SCHEMA = [
    "README.md",
    "LICENSE",
    "pyproject.toml",
    "requirements.txt",
    ".env.example",
    ".gitignore",

    "src/main.py",
    "src/app.py",

    "src/config/settings.py",
    "src/config/secrets_manager.py",
    "src/config/logging_config.py",
    "src/config/environment.py",

    "src/api/routes/missions.py",
    "src/api/routes/agents.py",
    "src/api/routes/tools.py",
    "src/api/routes/billing.py",
    "src/api/routes/auth.py",
    "src/api/routes/health.py",

    "src/api/middleware/auth_middleware.py",
    "src/api/middleware/rate_limit.py",
    "src/api/middleware/request_logger.py",

    "src/api/schemas/mission_schema.py",
    "src/api/schemas/agent_schema.py",
    "src/api/schemas/tool_schema.py",
    "src/api/schemas/billing_schema.py",
    "src/api/schemas/auth_schema.py",

    "src/agents/base_agent.py",
    "src/agents/agent_registry.py",
    "src/agents/guardian_agent.py",
    "src/agents/planner_agent.py",
    "src/agents/executor_agent.py",
    "src/agents/researcher_agent.py",
    "src/agents/writer_agent.py",
    "src/agents/analyst_agent.py",
    "src/agents/accountant_agent.py",
    "src/agents/hr_agent.py",

    "src/tools/base_tool.py",
    "src/tools/tool_registry.py",
    "src/tools/web_search.py",
    "src/tools/browser_automation.py",
    "src/tools/file_manager.py",
    "src/tools/vector_store.py",
    "src/tools/embeddings.py",
    "src/tools/crm_client.py",
    "src/tools/stripe_client.py",
    "src/tools/shopify_client.py",
    "src/tools/github_client.py",
    "src/tools/email_sender.py",

    "src/missions/mission_engine.py",
    "src/missions/mission_registry.py",

    "src/missions/mission_plans/research_plan.yaml",
    "src/missions/mission_plans/content_plan.yaml",
    "src/missions/mission_plans/automation_plan.yaml",
    "src/missions/mission_plans/crm_sync_plan.yaml",
    "src/missions/mission_plans/billing_plan.yaml",

    "src/missions/mission_templates/grant_discovery.yaml",
    "src/missions/mission_templates/seo_campaign.yaml",
    "src/missions/mission_templates/outreach_pipeline.yaml",
    "src/missions/mission_templates/product_launch.yaml",
    "src/missions/mission_templates/data_cleanup.yaml",

    "src/orchestration/router.py",
    "src/orchestration/planner.py",
    "src/orchestration/executor.py",
    "src/orchestration/validator.py",
    "src/orchestration/sandbox.py",
    "src/orchestration/context_builder.py",
    "src/orchestration/event_bus.py",

    "src/billing/ledger.py",
    "src/billing/invoice_generator.py",
    "src/billing/cost_model.py",
    "src/billing/agent_compensation.py",
    "src/billing/usage_tracker.py",
    "src/billing/audit_trail.py",

    "src/auth/jwt_manager.py",
    "src/auth/api_keys.py",
    "src/auth/oauth_providers.py",
    "src/auth/permissions.py",

    "src/data/logs/system.log",
    "src/data/logs/missions.log",
    "src/data/logs/billing.log",
    "src/data/logs/errors.log",

    "src/data/ledger/mission_history.csv",
    "src/data/ledger/billing_history.csv",
    "src/data/ledger/agent_earnings.csv",

    "src/data/vector_store/",
    "src/data/cache/",

    "src/utils/hashing.py",
    "src/utils/time_utils.py",
    "src/utils/id_generator.py",
    "src/utils/retry.py",
    "src/utils/file_utils.py",
    "src/utils/text_cleaner.py",

    "src/ui/static/",
    "src/ui/templates/",
    "src/ui/components/",
    "src/ui/dashboard/mission_view.py",
    "src/ui/dashboard/agent_view.py",
    "src/ui/dashboard/billing_view.py",
    "src/ui/dashboard/logs_view.py",

    "tests/test_agents.py",
    "tests/test_tools.py",
    "tests/test_missions.py",
    "tests/test_billing.py",
    "tests/test_api.py",
    "tests/test_auth.py",

    "docs/architecture.md",
    "docs/agents.md",
    "docs/tools.md",
    "docs/missions.md",
    "docs/billing.md",
    "docs/api_reference.md",
    "docs/deployment.md",
    "docs/security.md"
]

IGNORE_DIRS = {
    "node_modules", ".next", "__pycache__", ".git",
    "dist", "build", "venv", ".idea", ".vscode"
}

def scan_repo(root: Path):
    discovered = []
    for path in root.rglob("*"):
        if path.is_dir():
            if path.name in IGNORE_DIRS:
                continue
            continue
        rel = str(path.relative_to(root)).replace("\\", "/")
        discovered.append(rel)
    return discovered

def compare(discovered, canonical):
    discovered_set = set(discovered)
    canonical_set = set(canonical)

    missing = sorted(list(canonical_set - discovered_set))

    # Extra files, but ignore anything under src/agents/*
    raw_extra = discovered_set - canonical_set
    extra = sorted([
        p for p in raw_extra
        if not p.startswith("src/agents/")
    ])

    # Moved files (same filename, different path)
    moved = []
    canonical_names = {Path(p).name: p for p in canonical}
    discovered_names = {Path(p).name: p for p in discovered}

    for name, canonical_path in canonical_names.items():
        if name in discovered_names and discovered_names[name] != canonical_path:
            moved.append({
                "file": name,
                "expected": canonical_path,
                "found": discovered_names[name]
            })

    return {
        "missing_files": missing,
        "extra_files": extra,
        "moved_files": moved
    }

def main():
    root = Path(".").resolve()
    discovered = scan_repo(root)
    report = compare(discovered, CANONICAL_SCHEMA)

    with open("sovereign_backend_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("\n=== BACKEND SOVEREIGN SCAN COMPLETE ===")
    print(f"Missing files: {len(report['missing_files'])}")
    print(f"Extra files (excluding src/agents/*): {len(report['extra_files'])}")
    print(f"Moved files: {len(report['moved_files'])}")
    print("Report saved to sovereign_backend_report.json\n")

    # Optional: print all missing files to console for quick creation
    print("---- MISSING FILES (for creation) ----")
    for path in report["missing_files"]:
        print(path)

if __name__ == "__main__":
    main()
