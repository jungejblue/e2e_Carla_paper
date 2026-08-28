# Visualization tools

다음 코드를 배치합니다.

- ego/fallback trajectory overlay
- risk score와 takeover 시점 timeline
- action age, lateral error, TTLC plot
- debug camera 영상에 control mode와 metric 표시
- 논문용 failure-case figure 생성

대화형 시각화보다 재현 가능한 PNG/PDF/MP4 생성을 기본으로 합니다. 출력 파일은
원시 실험 폴더 또는 `paper_results/figures/`에 저장하고 source CSV의 run ID를 함께
기록해야 합니다.

