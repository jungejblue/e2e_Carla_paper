# Analysis tools

다음 wrapper를 배치합니다.

- paired event 결과 집계
- intervention precision/recall과 비유효 개입률 계산
- bootstrap confidence interval
- calibration/test split 비교
- 논문 표·그림 생성

Metric 정의와 계산 함수는 `src/e2e_carla_paper/evaluation/metrics.py`에 구현하고,
이 디렉터리는 여러 run을 읽어 해당 함수를 호출하는 역할만 담당합니다.

