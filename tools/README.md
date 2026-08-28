# Tools

이 디렉터리는 논문 핵심 실행 로직이 아닌 시각화·분석·환경검증·포맷변환용
utility를 관리합니다.

```text
tools/
├── visualization/   # trajectory, intervention timeline, debug image/video
├── analysis/        # 결과 집계, 통계검정, 논문 표·그림 생성
├── validation/      # dependency, asset, config, paired-run 일관성 검사
└── conversion/      # CARLA/Leaderboard 로그를 연구 포맷으로 변환
```

전환 라벨, safety metric, paired protocol처럼 논문 결과를 정의하는 코드는
`tools/`가 아니라 `src/e2e_carla_paper/evaluation/`에 둡니다. Tools는 그 코드를
호출하는 얇은 command-line wrapper여야 합니다.

