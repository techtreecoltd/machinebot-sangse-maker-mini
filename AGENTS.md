# AGENTS.md

## 이 저장소

머신봇 상세 메이커 mini, 즉 정식 버전 머신봇 상세 메이커의 공개 버전 플러그인이다. 정식 버전이 원본이고 mini는 정식 버전에서 노하우 층을 덜어낸 파생본이다.

## 원칙

- 기능은 모두 열어 두고, 품질을 끌어올리는 세부 기획(소구 맵, 장면 설계, CG 판단, 구매 결정형 FAQ 설계, 세트 검수)은 넣지 않는다.
- 지침은 "이렇게 만든다"는 긍정형으로 짧게 쓴다. 금지 목록은 넣지 않는다.
- 정식 버전 안내 문구는 `references/upgrade.md` 한 곳에서만 관리한다.

## 수정할 때

| 바꾸는 것 | 함께 고칠 곳 |
|---|---|
| 플러그인 정보·버전 | `plugins/.../plugin.json`, `CHANGELOG.md` |
| 작업 흐름 | `SKILL.md`, 관련 `references/`, README의 "설치 후 1분 점검" 표 |
| 스킬 추가·이름 변경 | 해당 `SKILL.md`, 허브의 입구 표, `always-on-block.md`, `validation/trigger-cases.json`, README의 연결 표 |
| 스킬 description | 수정 후 `scripts/trigger_eval.py`를 다시 돌려 결과를 갱신 |
| 결과물 기본값 | `references/branches.md`, README 요청 표 |
| 강의 링크 | `README.md`, 플러그인 `README.md`, `references/upgrade.md`의 준비 중 안내를 실제 주소로 교체 |

`.codex-plugin/plugin.json`은 직접 고치지 않는다. `scripts/build.py`가 `plugin.json`에서 만든다.

## 검증과 배포

```powershell
$env:PYTHONUTF8 = "1"
python scripts/build.py
```

스크립트는 다음 순서로 진행한다.

1. 매니페스트, 스킬, 마켓플레이스, 문서 링크를 검사한다.
2. 호환 매니페스트를 생성한다.
3. `dist/`에 ZIP과 SHA-256을 만든다.
4. 압축 해제본을 다시 검사한다.

깨진 강의 링크 자리표시가 남아 있으면 경고하고, `--release`에서는 실패한다. 현재는 주소가 지정되지 않아 링크 없는 준비 중 안내로 배포한다. 버전을 올릴 때는 `dist/`에 새 파일을 만든다. 공개 저장소에 정식판 이력·백업·배포 ZIP을 추가하지 않는다.

## 호출 구조

- 요청 종류마다 전용 입구 스킬이 있다. 공통 절차와 기본값은 허브(`machinebot-sangse-maker-mini`)의 `references/` 한 곳에 둔다.
- 상시 연결은 `machinebot-mini-setup`이 사용자 동의 후 전역 AGENTS.md에 `<!-- machinebot-mini:start -->` 블록을 넣는 방식이다.
- `python scripts/trigger_eval.py`로 실제 호출률을 측정한다. 이 PC처럼 문서 폴더에서 Python 쓰기가 막히면 저장소를 임시 폴더로 복사해서 실행한다.
