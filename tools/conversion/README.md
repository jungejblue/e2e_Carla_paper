# Conversion tools

다음 변환 코드를 배치합니다.

- CARLA Leaderboard result JSON → paired event summary
- frame-level CSV/JSON → Parquet
- CARLA recorder metadata → episode metadata
- route XML → project scenario manifest

원시 포맷, 좌표계, timestamp 단위와 schema version을 변환 결과에 반드시
기록합니다. 변환 코드 안에서 safety label이나 metric 정의를 다시 구현하면 안 됩니다.

