# e2e_Carla_paper

CARLA 폐루프 환경에서 E2E 자율주행기의 **전환 필요성·유효성**을 평가하고,
필요한 전환의 재현율을 유지하면서 불필요하거나 비유효한 개입을 줄이기 위한
연구 코드 저장소입니다.

## 구조

```text
e2e_Carla_paper/
├── configs/                 # 실행·agent·safety·실험 설정
├── src/e2e_carla_paper/
│   ├── runtime/             # CARLA 연결과 episode 실행
│   ├── agent/               # TransFuser++ adapter와 FIFO latency
│   ├── safety/              # monitor, fallback, takeover manager
│   └── evaluation/          # paired run, 라벨, 지표
├── scenarios/               # route/seed/조건 manifest
├── scripts/                 # 실험 실행 진입점
├── tests/                   # CARLA 없이 가능한 단위시험
├── docs/                    # 연구·실험 프로토콜
├── third_party/             # 외부 의존성 버전 기록
└── paper_results/           # 논문용 소용량 요약·표·그림
```

## 외부 디렉터리 권장 배치

```text
~/e2e_carla_ws/                 # CARLA 0.9.15
~/carla_garage/                 # CARLA Garage leaderboard_2
~/e2e_Carla_paper/              # 이 저장소
~/e2e_checkpoints/              # TransFuser++ checkpoint
~/e2e_experiment_outputs/       # 로그·영상·recorder 파일
```

## 설치

CARLA Garage와 TransFuser++가 동작하는 Python 3.10 환경에서 이 저장소를
editable package로 설치합니다.

```bash
git clone https://github.com/jungejblue/e2e_Carla_paper.git
cd e2e_Carla_paper
python -m pip install -e '.[dev]'
```

`.env` 값을 로컬 경로에 맞게 수정한 다음 셸에 로드합니다.

```bash
set -a
source .env
set +a
python -m e2e_carla_paper.cli check-env
```

