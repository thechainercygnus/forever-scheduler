"""The pre-commit hooks: the push hooks run the Semgrep CI runs."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def hook_block(hook_id: str) -> str:
    """One hook's lines in .pre-commit-config.yaml, from its `- id:` to the next."""
    pattern = rf"- id: {re.escape(hook_id)}\n(.*?)(?=\n\s*- id: |\Z)"
    match = re.search(pattern, read(".pre-commit-config.yaml"), re.S)
    assert match, f"no {hook_id} hook"
    return match[1]


def test_the_push_hooks_run_the_semgrep_ci_runs() -> None:
    pinned = re.search(r"SEMGREP: (semgrep==[\d.]+)", read(".github/workflows/semgrep.yml"))
    assert pinned, "semgrep.yml pins SEMGREP"
    for hook_id in ("semgrep-rules", "semgrep-rule-tests"):
        block = hook_block(hook_id)
        assert f"--from {pinned[1]} " in block, f"{hook_id}: bump it with semgrep.yml"
        assert "stages: [pre-push]" in block


def test_the_other_hooks_stay_at_commit() -> None:
    config = read(".pre-commit-config.yaml")
    assert "default_stages: [pre-commit]" in config
    assert "default_install_hook_types: [pre-commit, pre-push]" in config
