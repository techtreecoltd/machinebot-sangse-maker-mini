# 스킬 호출률 평가

- 실행: 2026-10-08 16:40
- Codex: codex-cli 0.160.0
- 판정: 기대한 머신봇 스킬의 SKILL.md를 실제로 열었으면 통과. 기대값 none은 머신봇 스킬을 하나도 열지 않아야 통과.
- 환경: 실행한 PC의 전역 스킬과 전역 AGENTS.md가 함께 로드된다. 다른 스킬 열람도 기록한다.

## 요약

| 조건 | 통과 |
|---|---|
| 스킬만 설치 | 12/12 |
| 상시 연결 켬 | 12/12 |

## 상세

| ID | 요청 | 기대 | 스킬만 설치 | 상시 연결 켬 |
|---|---|---|---|---|
| D1 | 이 텀블러 상세페이지 만들어줘. 사진은 아직 없어. | machinebot-mini-detail-page | 통과: machinebot-mini-detail-page, machinebot-sangse-maker-mini | 통과: machinebot-mini-detail-page |
| D2 | 쿠팡에 올릴 접이식 캠핑의자 상페 6장 뽑아줘 | machinebot-mini-detail-page | 통과: machinebot-mini-detail-page | 통과: machinebot-mini-detail-page, machinebot-sangse-maker-mini |
| D3 | 타오바오에서 가져온 중국어 상세 이미지를 한국어로 바꿔서 다시 만들어줘 | machinebot-mini-detail-page | 통과: machinebot-mini-detail-page, machinebot-sangse-maker-mini | 통과: machinebot-mini-detail-page, machinebot-sangse-maker-mini |
| D4 | 전기 요가매트 구매 전에 많이 묻는 질문으로 FAQ 이미지 한 장 만들어줘 | machinebot-mini-detail-page | 통과: machinebot-mini-detail-page | 통과: machinebot-mini-detail-page |
| T1 | 스마트스토어 대표이미지 하나 만들어줘. 제품은 무선 가습기야 | machinebot-mini-thumbnail | 통과: machinebot-mini-thumbnail | 통과: machinebot-mini-thumbnail |
| T2 | 블루투스 스피커 상품 썸네일 세트 필요해 | machinebot-mini-thumbnail | 통과: machinebot-mini-thumbnail | 통과: machinebot-mini-thumbnail, machinebot-sangse-maker-mini |
| P1 | 제품 사진 배경 지우고 흰 배경 누끼로 만들어줘 | machinebot-mini-product-shots | 통과: machinebot-mini-product-shots | 통과: machinebot-mini-product-shots |
| P2 | 이 쿠션을 거실에서 쓰는 연출컷 4장 만들어줘 | machinebot-mini-product-shots | 통과: machinebot-mini-product-shots | 통과: machinebot-mini-product-shots |
| H1 | 손목보호대를 온라인에서 팔려는데 판매 이미지를 뭐부터 만들어야 할지 모르겠어 | machinebot-sangse-maker-mini | 통과: machinebot-sangse-maker-mini | 통과: machinebot-sangse-maker-mini |
| H2 | 머신봇 상세 메이커 정식 버전은 어떻게 받아? | machinebot-sangse-maker-mini | 통과: machinebot-sangse-maker-mini | 통과: machinebot-sangse-maker-mini |
| N1 | 파이썬으로 CSV 파일 두 개 합치는 코드 짜줘 | none | 통과: 없음 | 통과: 없음 |
| N2 | 내 유튜브 영상 썸네일에 넣을 문구 아이디어 5개만 줘 | none | 통과: 없음 | 통과: 없음 |
