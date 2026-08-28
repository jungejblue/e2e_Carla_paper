# e2e_Carla_paper

CARLA 폐루프 환경에서 E2E 자율주행기의 **전환 필요성·유효성**을 평가하고,
필요한 전환의 재현율을 유지하면서 불필요하거나 비유효한 개입을 줄이기 위한
연구 코드 저장소입니다.

## 연구 범위

- Simulator: CARLA 0.9.15 / Unreal Engine 4.26
- E2E baseline: frozen TransFuser++ checkpoint from CARLA Garage
- Ego vehicle: `vehicle.lincoln.mkz_2020`
- Verified maps: Town01–Town07, Town10HD–Town12
- Perturbation: FIFO action latency
- Safety controller: fixed lane-recovery fallback controller
- Evaluation: paired closed-loop runs
  - `e2e_continue`
  - `forced_fallback`
- Intervention labels:
  - `NECESSARY_EFFECTIVE`
  - `UNNECESSARY`
  - `INEFFECTIVE`
  - `HARMFUL`

Town13과 Town15는 현재 실험 범위에서 제외합니다. TransFuser++는 추가학습하지
않으며 CARLA, CARLA Garage, 모델 checkpoint와 원시 실험 결과는 이 저장소에
포함하지 않습니다.

## 구조

```text
e2e_Carla_paper/
├── configs/                 # 실행·agent·safety·실험 설정
├── docker/                  # GPU 개발 container와 고정 dependency
├── src/e2e_carla_paper/
│   ├── runtime/             # CARLA 연결과 episode 실행
│   ├── agent/               # TransFuser++ adapter와 FIFO latency
│   ├── safety/              # monitor, fallback, takeover manager
│   └── evaluation/          # paired run, 라벨, 지표
├── scenarios/               # route/seed/조건 manifest
├── scripts/                 # 실험 실행 진입점
├── tools/                   # 시각화·분석·검증·포맷변환 utility
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
git clone <REPOSITORY_URL> e2e_Carla_paper
cd e2e_Carla_paper
python -m pip install -e '.[dev]'
cp .env.example .env
```

`.env` 값을 로컬 경로에 맞게 수정한 다음 셸에 로드합니다.

```bash
set -a
source .env
set +a
python -m e2e_carla_paper.cli check-env
```

분석 및 시각화 의존성까지 로컬에 설치하려면 다음을 사용합니다.

```bash
python -m pip install -e '.[dev,analysis]'
```

## Docker 개발환경

권장 구조는 CARLA 0.9.15 server를 Ubuntu host에서 실행하고, Docker container에서
TransFuser++와 연구 코드를 실행하는 방식입니다. CARLA와 CARLA Garage 원본은
image에 복사하지 않고 read-only bind mount로 연결합니다.

```bash
cp docker/compose.env.example docker/.env
docker compose --env-file docker/.env -f docker/compose.yaml build research
docker compose --env-file docker/.env -f docker/compose.yaml run --rm research
```

세부 설정과 host 준비사항은 [`docker/README.md`](docker/README.md)를 참고합니다.
의존성 선정 근거와 고정 정책은 [`docs/dependencies.md`](docs/dependencies.md)에
정리되어 있습니다.

## Tools

`tools/`에는 다음과 같은 논문 보조 코드를 둡니다.

- `visualization/`: trajectory, risk score, takeover timeline, debug 영상
- `analysis/`: 결과 집계, 통계검정, 논문 표·그림 생성
- `validation/`: dependency, CARLA asset, config, paired consistency 검사
- `conversion/`: Leaderboard/CARLA 로그를 연구 포맷으로 변환

전환 라벨과 safety metric처럼 논문 결과를 정의하는 구현은 `tools/`에 두지 않고
반드시 `src/e2e_carla_paper/evaluation/`에 유지합니다.

## 현재 실행 순서

1. `check-env`: CARLA, CARLA Garage, checkpoint, output 경로 검사
2. Town01 단일 route smoke test
3. frozen TransFuser++ clean run
4. FIFO latency가 적용된 `e2e_continue` run
5. 동일 후보 이벤트의 `forced_fallback` paired run
6. intervention label 생성 및 monitor threshold calibration
7. 고정 threshold로 test set 평가

## 테스트

```bash
pytest
```

CARLA가 필요한 integration test는 로컬 장비에서만 실행하고, GitHub Actions에는
단위시험과 설정 검증만 포함합니다.

Docker 내부 dependency와 GPU mount는 다음으로 확인합니다.

```bash
python tools/validation/check_container.py --strict
```

## 결과 저장 원칙

원시 결과는 `${EXPERIMENT_OUTPUT_ROOT}`에 저장합니다. Git에는 설정, scenario
manifest, 외부 의존성 commit, 집계된 CSV/JSON, 최종 표와 그림만 커밋합니다.

## 주의

현재 맵 범위는 전체 Bench2Drive route 집합과 동일하지 않습니다. 따라서 정식
Bench2Drive 전체 벤치마크 결과가 아닌 경우 README와 논문에서 `custom CARLA
closed-loop evaluation` 또는 `Bench2Drive route subset`으로 명시해야 합니다.
