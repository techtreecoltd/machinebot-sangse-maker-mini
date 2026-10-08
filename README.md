# 머신봇 상세 메이커 mini

제품 사진을 올리면 쿠팡·스마트스토어에 바로 쓸 썸네일, 누끼컷, 연출컷, 기능 설명 컷, 상세페이지까지 만들어 주는 ChatGPT · Codex 플러그인입니다. 머신봇 상세 메이커의 공개 버전이에요.

> **정식 버전 머신봇 상세 메이커**는 고객이 살 이유를 먼저 설계하고, 장면 구성과 구매 결정 FAQ까지 맞춰서 만듭니다. 정식 버전은 강의 수강생에게 제공됩니다. mini는 지금 무료로 사용할 수 있어요. → [격차 · 이커머스의 정석 — 김머신](https://www.gykcha.com/html/class_detail.php?it_id=1673617370)

## 이렇게 요청하면 이렇게 만들어요

| 요청 | 결과 |
|---|---|
| "이 사진으로 메인 썸네일 만들어 줘" | 흰 배경 제품 썸네일 1장, 바로 생성 |
| "썸네일 세트 만들어 줘" | 메인 1장 + 서브 5장 |
| "누끼 따 줘" | 흰 배경 스튜디오 제품컷 1장 |
| "사용하는 장면 만들어 줘" | 연출·실사용컷 4장 |
| "이 기능을 그림으로 보여줘" | 기능 설명 컷 3장 |
| "상세페이지 만들어 줘" | 6장 구성표를 먼저 보여주고, 확인 후 1080×2160px 6장 생성 |
| "FAQ 이미지 한 장" | 질문 3~5개짜리 FAQ 1장 |
| "이 중국어 상세페이지를 한국어로" | 제품만 살려 한국어 상세페이지 6장으로 새로 생성 |
| "전부 다 만들어 줘" | 누끼·썸네일·연출·기능·상세를 순서대로 |

수량, 비율, 배경, 문구를 직접 말하면 그대로 따릅니다.

## 설치

플러그인을 지원하는 ChatGPT 데스크톱 앱의 로컬 작업 환경과 Codex에서 설치합니다. 아래 방법 중 하나를 사용하세요. [공식 플러그인 설치 문서](https://developers.openai.com/plugins/build/plugins)를 기준으로 구성했습니다.

### 방법 1. 명령어 한 줄 (Codex CLI가 있을 때)

```bash
codex plugin marketplace add techtreecoltd/machinebot-sangse-maker-mini
```

1. 위 명령어를 실행합니다.
2. ChatGPT 데스크톱 앱을 완전히 종료했다가 다시 엽니다.
3. 플러그인 디렉터리에서 **머신봇** 마켓플레이스를 고르고 **머신봇 상세 메이커 mini**를 설치합니다.

### 방법 2. 직접 복사 (명령어 없이)

1. 이 저장소를 ZIP으로 내려받아 압축을 풉니다.
2. `plugins/machinebot-sangse-maker-mini` 폴더를 아래 위치에 복사합니다.
   - Windows: `C:\Users\내이름\.codex\plugins\machinebot-sangse-maker-mini`
   - macOS: `~/.codex/plugins/machinebot-sangse-maker-mini`
3. 홈 폴더의 `.agents/plugins/marketplace.json` 파일을 만들고 아래 내용을 넣습니다. 이미 파일이 있으면 `plugins` 목록에 항목만 추가합니다.

```json
{
  "name": "machinebot-public",
  "interface": { "displayName": "머신봇" },
  "plugins": [
    {
      "name": "machinebot-sangse-maker-mini",
      "source": { "source": "local", "path": "./.codex/plugins/machinebot-sangse-maker-mini" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Productivity"
    }
  ]
}
```

4. ChatGPT 데스크톱 앱을 다시 열고 플러그인 디렉터리에서 설치합니다.

## 사용하기

**ChatGPT:** 새 채팅에서 `@`를 입력하고 **머신봇 상세 메이커 mini**를 고른 뒤, 제품 사진과 함께 요청합니다.

```text
@머신봇 상세 메이커 mini 이 사진으로 메인 썸네일 한 장 만들어 줘
```

**Codex:** 스킬 이름으로 부릅니다.

```text
$machinebot-sangse-maker-mini 이 제품으로 상세페이지 6장 만들어 줘
```

제품 정면 사진, 제품명, 꼭 넣고 싶은 특징이나 문구를 함께 주면 결과가 좋아집니다.

## 늘 발동하는 구조

스킬 이름을 몰라도 평소 말투로 요청할 때 알맞은 스킬이 선택되도록 구성했습니다. 요청 종류마다 전용 입구가 있어요. 자동 선택은 호스트·모델과 다른 지침의 영향을 받으므로, 빠졌을 때는 `@` 또는 `$`로 직접 호출하세요.

| 이런 요청이 오면 | 연결되는 스킬 |
|---|---|
| 상세페이지, 상페, FAQ 이미지, 중국어 상세 번역 | `machinebot-mini-detail-page` |
| 썸네일, 대표이미지, 서브 이미지 | `machinebot-mini-thumbnail` |
| 누끼, 배경 제거, 연출컷, 실사용컷, 기능 설명 컷 | `machinebot-mini-product-shots` |
| 뭐부터 만들지 모름, 전체 패키지, 사용법, 정식 버전 문의 | `machinebot-sangse-maker-mini` |
| 설치 후 설정, 상시 연결 켜기·끄기 | `machinebot-mini-setup` |

### 상시 연결 (권장)

설정을 지원하는 호스트에서는 설치 후 안내를 따르거나, `$machinebot-mini-setup 상시 연결 켜 줘`라고 요청하세요. 동의 후 Codex 전역 지침 파일(기본 `~/.codex/AGENTS.md`, `AGENTS.override.md`가 있으면 그 파일)에 짧은 연결 블록을 추가합니다. 적용되는 로컬 작업 환경의 새 대화에서 사용하며, ChatGPT 웹·모바일 전체에 적용되는 설정은 아닙니다. 끄려면 "상시 연결 해제"라고 요청하세요.

### 호출률 점검

실제 Codex에 요청 문장 12개를 넣고, 모델이 어떤 스킬을 열었는지로 자동 호출 여부를 판정합니다. 결과는 [validation/trigger-eval-latest.md](validation/trigger-eval-latest.md)에 저장됩니다.

```bash
python scripts/trigger_eval.py
```

최근 결과는 스킬만 설치한 상태와 상시 연결을 켠 상태 모두 12/12입니다. 상세페이지·썸네일·제품컷 요청이 각자 맞는 스킬로 연결됐고, 코딩 질문과 유튜브 썸네일 요청에서는 발동하지 않았습니다.

## 설치 후 1분 점검

설치가 제대로 됐는지 아래 순서로 확인하세요.

| 해 볼 말 | 정상이라면 |
|---|---|
| "어떻게 써?" | 만들 수 있는 것과 요청 예시를 알려 줌. 이미지는 만들지 않음 |
| 스킬 이름 없이 "상페 6장 뽑아 줘" | 상세페이지 스킬이 바로 연결되고, 구성표나 사진 요청으로 시작 |
| 제품 사진 + "메인 썸네일 만들어 줘" | 질문 없이 1장을 만들어 보여 주고, 끝에 정식 버전 안내가 한 줄 붙음 |
| 같은 대화에서 "누끼도 따 줘" | 1장을 만들어 줌. 정식 버전 안내는 다시 붙지 않음 |
| "상세페이지 만들어 줘" | 6장 구성표를 먼저 보여 주고, 확인하면 생성 |

목록에 플러그인이 안 보이면 ChatGPT 데스크톱 앱을 완전히 종료했다가 다시 여세요. 이미지가 만들어지지 않는 환경에서는 프롬프트와 구성표까지만 제공합니다.

## mini와 정식 버전

| | mini | 정식 버전 |
|---|---|---|
| 썸네일 | 흰 배경 기본, 요청한 스타일 반영 | 구매 이유에 맞춰 모델컷·장점 시각화·정보성 문구를 골라 조합 |
| 누끼 | 1장 | 여러 각도 마스터컷, 이후 제작에 이어 쓰기 |
| 연출·기능 컷 | 요청한 장면 생성 | 장면마다 다른 구매 정보 배정, CG 표현 판단 |
| 상세페이지 | 6장 기본 구성 | 구매 이유 설계 → 장면 설계 → 6·8·10장 구성 |
| FAQ | 질문 3~5개 | 구매 직전 망설임을 뽑은 정보 중심 레이아웃 |
| 외국어 재제작 | 한국어로 새로 생성 | 원문 분석, 브랜드 보존, 잔존 문구 검수 |
| 제공 방식 | 누구나 무료 | 강의 수강생에게 별도 설치 주소로 제공 |

→ [격차 · 이커머스의 정석 강의 보기](https://www.gykcha.com/html/class_detail.php?it_id=1673617370)

정식판 설치에는 운영자가 제공하는 별도 설치 자료 또는 비공개 저장소 접근 권한이 필요합니다.

## 공개 배포 상태

mini 1.0.1은 정리된 공개 파일만 담은 독립 저장소입니다. 정식판 프롬프트·이전 커밋·백업 파일은 포함하지 않습니다. 패키지 검증과 Codex 호출 평가를 수행했으며, ChatGPT 데스크톱 UI에서의 최종 실사용 검증은 아직 하지 않았습니다. 격차 강의 페이지로 연결하며, 이메일 수집과 수강생 자동 인증은 아직 연동하지 않았습니다.

## 업데이트와 삭제

```bash
codex plugin marketplace upgrade machinebot-public
codex plugin marketplace remove machinebot-public
```

직접 복사한 경우에는 폴더를 새 버전으로 바꾸고 앱을 다시 엽니다.

## 폴더 구조

```text
.
├─ .agents/plugins/marketplace.json   # 설치용 마켓플레이스
├─ plugins/machinebot-sangse-maker-mini/
│  ├─ plugin.json                     # 플러그인 정보
│  ├─ .codex-plugin/plugin.json       # 이전 버전 앱 호환용 (자동 생성)
│  ├─ assets/logo.png
│  └─ skills/
│     ├─ machinebot-sangse-maker-mini/   # 시작 창구 + 공통 참고 문서(references/)
│     ├─ machinebot-mini-detail-page/    # 상세페이지·FAQ·외국어 재제작 입구
│     ├─ machinebot-mini-thumbnail/      # 썸네일 입구
│     ├─ machinebot-mini-product-shots/  # 누끼·연출·기능 컷 입구
│     └─ machinebot-mini-setup/          # 설치 직후 설정, 상시 연결
├─ scripts/
│  ├─ build.py                        # 검증과 ZIP 생성
│  └─ trigger_eval.py                 # 스킬 호출률 평가
├─ validation/                        # 평가 문장과 최근 결과
└─ dist/                              # 배포 ZIP
```
