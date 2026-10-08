#!/usr/bin/env python3
"""머신봇 상세 메이커 mini 스킬 호출률 평가.

실제 Codex에 요청 문장을 넣고, 모델이 어떤 스킬 파일(SKILL.md)을 열었는지로
자동 호출 여부를 판정한다. 로그인된 Codex CLI가 필요하고, 요청마다 모델 사용량이 든다.

사용법:
  python scripts/trigger_eval.py                 # 두 조건 모두
  python scripts/trigger_eval.py --mode skills   # 스킬만 설치한 상태
  python scripts/trigger_eval.py --mode always-on  # 상시 연결 블록을 켠 상태
옵션: --jobs 4  --timeout 240  --out validation/trigger-eval-latest.md
"""
import argparse
import concurrent.futures as cf
import datetime
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "machinebot-sangse-maker-mini"
BLOCK = PLUGIN / "skills" / "machinebot-mini-setup" / "assets" / "always-on-block.md"
CASES = ROOT / "validation" / "trigger-cases.json"
SKILL_READ_RE = re.compile(r"skills[\\/]+([A-Za-z0-9_.-]+)[\\/]+SKILL\.md")
MODES = {"skills": "스킬만 설치", "always-on": "상시 연결 켬"}


def codex_bin() -> str:
    found = os.environ.get("CODEX_BIN") or shutil.which("codex.exe") or shutil.which("codex")
    if not found:
        raise SystemExit("Codex CLI를 찾을 수 없습니다. CODEX_BIN 환경 변수로 경로를 지정하세요.")
    return found


def make_workspace(mode: str) -> Path:
    ws = Path(tempfile.mkdtemp(prefix=f"mbmini-eval-{mode}-"))
    shutil.copytree(PLUGIN / "skills", ws / ".agents" / "skills")
    if mode == "always-on":
        (ws / "AGENTS.md").write_text(BLOCK.read_text(encoding="utf-8"), encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=ws, check=False)
    return ws


def skills_read(stdout: str) -> list[str]:
    found: list[str] = []
    for line in stdout.splitlines():
        try:
            item = json.loads(line).get("item") or {}
        except (json.JSONDecodeError, AttributeError):
            continue
        if item.get("type") in ("agent_message", "reasoning"):
            continue
        probe = {k: v for k, v in item.items() if k != "aggregated_output"}
        for name in SKILL_READ_RE.findall(json.dumps(probe, ensure_ascii=False)):
            if name not in found:
                found.append(name)
    return found


def run_case(binary: str, ws: Path, case: dict, timeout: int) -> dict:
    cmd = [binary, "exec", "--json", "--skip-git-repo-check", "-s", "read-only", "-"]
    try:
        proc = subprocess.run(cmd, input=case["prompt"], cwd=ws, capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=timeout)
        error = None if proc.returncode == 0 else f"exit {proc.returncode}"
        read = skills_read(proc.stdout)
    except subprocess.TimeoutExpired:
        error, read = "timeout", []
    ours = [s for s in read if s.startswith("machinebot-")]
    expect = case["expect"]
    passed = (not ours) if expect == "none" else (expect in ours)
    return {"read": read, "ours": ours, "passed": passed and error is None, "error": error}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["skills", "always-on", "both"], default="both")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--out", default=str(ROOT / "validation" / "trigger-eval-latest.md"))
    args = ap.parse_args()

    cases = json.loads(CASES.read_text(encoding="utf-8"))
    modes = ["skills", "always-on"] if args.mode == "both" else [args.mode]
    binary = codex_bin()
    version = subprocess.run([binary, "--version"], capture_output=True, text=True).stdout.strip()

    results: dict[tuple[str, str], dict] = {}
    with cf.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {}
        for mode in modes:
            ws = make_workspace(mode)
            for case in cases:
                futures[pool.submit(run_case, binary, ws, case, args.timeout)] = (mode, case["id"])
        for fut in cf.as_completed(futures):
            mode, cid = futures[fut]
            results[(mode, cid)] = fut.result()
            r = results[(mode, cid)]
            print(f"[{MODES[mode]}] {cid}: {'통과' if r['passed'] else '실패'} {r['ours'] or '-'} {r['error'] or ''}")

    lines = [
        "# 스킬 호출률 평가",
        "",
        f"- 실행: {datetime.datetime.now():%Y-%m-%d %H:%M}",
        f"- Codex: {version}",
        "- 판정: 기대한 머신봇 스킬의 SKILL.md를 실제로 열었으면 통과. 기대값 none은 머신봇 스킬을 하나도 열지 않아야 통과.",
        "- 환경: 실행한 PC의 전역 스킬과 전역 AGENTS.md가 함께 로드된다. 다른 스킬 열람도 기록한다.",
        "",
        "## 요약",
        "",
        "| 조건 | 통과 |",
        "|---|---|",
    ]
    for mode in modes:
        ok = sum(results[(mode, c["id"])]["passed"] for c in cases)
        lines.append(f"| {MODES[mode]} | {ok}/{len(cases)} |")
    lines += ["", "## 상세", "", "| ID | 요청 | 기대 | " + " | ".join(MODES[m] for m in modes) + " |",
              "|---|---|---|" + "---|" * len(modes)]
    for case in cases:
        cells = []
        for mode in modes:
            r = results[(mode, case["id"])]
            mark = "통과" if r["passed"] else "실패"
            others = [s for s in r["read"] if s not in r["ours"]]
            detail = ", ".join(r["ours"]) or "없음"
            if others:
                detail += f" (기타: {', '.join(others)})"
            if r["error"]:
                detail += f" [{r['error']}]"
            cells.append(f"{mark}: {detail}")
        lines.append(f"| {case['id']} | {case['prompt']} | {case['expect']} | " + " | ".join(cells) + " |")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"결과: {out}")


if __name__ == "__main__":
    main()
