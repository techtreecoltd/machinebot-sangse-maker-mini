---
name: machinebot-sangse-maker-mini
description: 머신봇 상세 메이커 mini의 시작 창구. 상품 판매 이미지를 무엇부터 만들지 모를 때, 썸네일·누끼·연출·상세페이지를 모두 묶은 판매 이미지 전체 패키지가 필요할 때, 머신봇 상세 메이커 사용법이나 정식 버전·업그레이드·수강생 문의에 사용한다. Use when a seller wants ecommerce product images but has not chosen a deliverable, wants a full commerce image package, or asks about Machinebot Sangse Maker.
---

# 머신봇 상세 메이커 mini

제품 사진으로 판매용 이미지를 만드는 플러그인의 시작 창구다. 사용자의 언어로 답하고, 사용자의 지시가 기본값보다 우선한다.

## 입구

| 요청 | 맡는 스킬 |
|---|---|
| 상세페이지, FAQ 이미지, 외국어 상세페이지 재제작 | `$machinebot-mini-detail-page` |
| 메인·서브 썸네일, 대표이미지 | `$machinebot-mini-thumbnail` |
| 누끼, 연출·실사용컷, 기능 설명 컷 | `$machinebot-mini-product-shots` |
| 무엇을 만들지 모름, 전체 패키지, 사용법, 정식 버전 문의 | 이 스킬 |

결과물이 정해진 요청은 해당 스킬의 방식으로 바로 만든다.

## 이 스킬이 하는 일

- 무엇을 만들지 모르면 [결과물과 기본값](references/branches.md)의 안내 예시처럼 짧게 보여주고 고르게 한다.
- 전체 패키지는 [결과물과 기본값](references/branches.md)의 구성을 한 번 보여주고 확인받은 뒤, 누끼 → 썸네일 → 연출 → 효용 → 상세 순서로 [작업 흐름](references/workflow.md)에 따라 만든다.
- 첫 인사만 하거나 사용법을 물으면 [30초 시작 안내](references/get-started.md)로 사진 준비 → 요청 → 확인·수정 순서를 알려 준다. 제작 요청이 이미 있으면 필요한 안내만 곁들이고 해당 제작으로 바로 이어 간다.
- 정식 버전, 업그레이드, 수강생, 강의 문의는 [정식 버전 안내](references/upgrade.md)로 답한다.
