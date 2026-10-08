#!/usr/bin/env python3
"""머신봇 상세 메이커 mini 검증·패키징.

사용법: python scripts/build.py [--release]
  --release  강의 링크 자리표시가 남아 있으면 실패한다.
"""
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER = "COURSE_URL_TODO"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
SKILL_REF_RE = re.compile(r"\$(machinebot-[a-z0-9-]+)")

errors: list[str] = []
warnings: list[str] = []


def err(msg):
    errors.append(msg)


def check_skill(skill_dir: Path):
    md = skill_dir / "SKILL.md"
    if not md.is_file():
        err(f"{skill_dir}: SKILL.md 없음")
        return
    text = md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        err(f"{md}: frontmatter 형식 오류")
        return
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    extra = set(fields) - {"name", "description", "license", "allowed-tools", "metadata"}
    if extra:
        err(f"{md}: 허용되지 않은 frontmatter 키 {sorted(extra)}")
    name = fields.get("name", "")
    desc = fields.get("description", "")
    if name != skill_dir.name:
        err(f"{md}: name({name})이 폴더명({skill_dir.name})과 다름")
    if not NAME_RE.match(name) or len(name) > 64:
        err(f"{md}: name 형식 오류")
    if not desc or len(desc) > 1024 or "<" in desc or ">" in desc:
        err(f"{md}: description 누락·1024자 초과·꺾쇠 포함 ({len(desc)}자)")


def check_links(base: Path, warn: bool = True):
    for md in base.rglob("*.md"):
        if any(p in md.parts for p in ("dist", ".build-check")) and base == ROOT:
            continue
        for target in LINK_RE.findall(md.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            if target == PLACEHOLDER:
                if warn:
                    warnings.append(f"강의 링크 자리표시: {md.relative_to(base)}")
                continue
            if not (md.parent / target.split("#")[0]).exists():
                err(f"{md.relative_to(base)}: 깨진 링크 {target}")


def check_plugin(plugin_dir: Path) -> dict:
    manifest_path = plugin_dir / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for key in ("name", "version", "description"):
        if not manifest.get(key):
            err(f"plugin.json: {key} 누락")
    if not NAME_RE.match(manifest.get("name", "")):
        err("plugin.json: name은 kebab-case")
    if not re.match(r"^\d+\.\d+\.\d+$", manifest.get("version", "")):
        err("plugin.json: version은 semver")
    ui = manifest.get("extensions", {}).get("com.openai", {}).get("interface", {})
    for key in ("displayName", "shortDescription", "developerName", "category"):
        if not ui.get(key):
            err(f"plugin.json interface: {key} 누락")
    for key in ("composerIcon", "logo"):
        path = ui.get(key)
        if path and (not path.startswith("./") or not (plugin_dir / path).is_file()):
            err(f"plugin.json interface: {key} 경로 오류 {path}")
    skills = [d for d in (plugin_dir / "skills").iterdir() if d.is_dir()]
    if not skills:
        err("skills/ 안에 스킬 없음")
    for d in skills:
        check_skill(d)
    names = {d.name for d in skills}
    for f in plugin_dir.rglob("*"):
        if f.suffix in (".md", ".yaml") and f.is_file():
            for ref in SKILL_REF_RE.findall(f.read_text(encoding="utf-8")):
                if ref not in names:
                    err(f"{f.relative_to(plugin_dir)}: 없는 스킬 참조 ${ref}")
    onboarding = manifest.get("extensions", {}).get("com.openai", {}).get("onboardingSkill")
    if onboarding and not (plugin_dir / onboarding).is_file():
        err(f"plugin.json onboardingSkill 경로 오류 {onboarding}")
    return manifest


def write_compat(plugin_dir: Path, manifest: dict):
    keys = ("name", "version", "description", "author", "homepage", "repository", "license", "keywords")
    compat = {k: manifest[k] for k in keys if k in manifest}
    compat["skills"] = "./skills/"
    compat["interface"] = manifest["extensions"]["com.openai"]["interface"]
    onboarding = manifest["extensions"]["com.openai"].get("onboardingSkill")
    if onboarding:
        compat["extensions"] = {"com.openai": {"onboardingSkill": onboarding}}
    out = plugin_dir / ".codex-plugin" / "plugin.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(compat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check_marketplace():
    mp = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    for entry in mp.get("plugins", []):
        for key in ("policy", "category"):
            if key not in entry:
                err(f"marketplace.json {entry.get('name')}: {key} 누락")
        path = entry["source"]["path"]
        target = ROOT / path
        if not path.startswith("./") or not (target / "plugin.json").is_file():
            err(f"marketplace.json: {path} 에 plugin.json 없음")
            continue
        name = json.loads((target / "plugin.json").read_text(encoding="utf-8"))["name"]
        if name != entry["name"]:
            err(f"marketplace.json: 항목 이름 {entry['name']} != plugin.json {name}")


def main():
    release = "--release" in sys.argv
    mp = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    plugin_dir = ROOT / mp["plugins"][0]["source"]["path"]
    manifest = check_plugin(plugin_dir)
    check_marketplace()
    check_links(ROOT)
    if errors:
        print("\n".join("오류: " + e for e in errors))
        sys.exit(1)

    write_compat(plugin_dir, manifest)
    name, version = manifest["name"], manifest["version"]
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    zip_path = dist / f"{name}-{version}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(plugin_dir.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                z.write(f, Path(name) / f.relative_to(plugin_dir))
    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    (dist / f"{zip_path.name}.sha256").write_text(f"{digest}  {zip_path.name}\n", encoding="utf-8")

    check_dir = ROOT / ".build-check"
    shutil.rmtree(check_dir, ignore_errors=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(check_dir)
    check_plugin(check_dir / name)
    check_links(check_dir / name, warn=False)
    shutil.rmtree(check_dir, ignore_errors=True)
    if errors:
        print("\n".join("압축 해제본 오류: " + e for e in errors))
        sys.exit(1)

    for w in sorted(set(warnings)):
        print("경고: " + w)
    print(f"통과: {zip_path.relative_to(ROOT)} ({zip_path.stat().st_size // 1024}KB)")
    print(f"SHA-256: {digest}")
    if release and warnings:
        print("릴리스 실패: 강의 링크 자리표시를 실제 주소로 바꾸세요.")
        sys.exit(1)


if __name__ == "__main__":
    main()
