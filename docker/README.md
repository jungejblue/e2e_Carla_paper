# Docker development environment

## Design

CARLA 0.9.15 server는 Ubuntu host에서 실행하고, Docker container는 다음만
담당합니다.

- frozen TransFuser++ inference
- CARLA Python client
- safety monitor와 fallback controller
- paired closed-loop evaluation
- 결과 분석과 headless visualization

CARLA package와 CARLA Garage 원본은 image에 복사하지 않고 read-only bind mount로
연결합니다. 따라서 image 크기와 Git 저장소 크기를 줄이고 외부 commit을 독립적으로
고정할 수 있습니다.

## Dependency basis

- Base image: CUDA 11.7.1 / cuDNN 8 / Ubuntu 20.04
- Python: 3.10.15
- CARLA Garage: `leaderboard_2` commit recorded in `third_party/manifest.yaml`
- CARLA Garage packages: `requirements-carla-garage.txt`
- Project tools: `requirements-project.txt`

Base image와 Python 버전은 CARLA Garage의 공식 environment와 Dockerfile에 맞춘
것입니다. 호스트 CUDA toolkit은 image에 전달하지 않으며, 호스트에는 호환 가능한
NVIDIA driver와 NVIDIA Container Toolkit이 필요합니다.

## Host prerequisites

1. Docker Engine과 Docker Compose v2
2. NVIDIA driver
3. NVIDIA Container Toolkit
4. CARLA 0.9.15 package
5. CARLA Garage `leaderboard_2` checkout
6. TransFuser++ checkpoint

GPU 전달을 먼저 확인합니다.

```bash
docker run --rm --gpus all nvidia/cuda:11.7.1-base-ubuntu20.04 nvidia-smi
```

## Configuration

```bash
cp docker/compose.env.example docker/.env
```

`docker/.env`의 경로를 수정합니다. 모든 경로는 `~`가 아닌 절대경로여야 합니다.

```dotenv
CARLA_ROOT_HOST_PATH=/home/jungejblue/e2e_carla_ws
CARLA_GARAGE_HOST_PATH=/home/jungejblue/carla_garage
TRANSFUSERPP_CHECKPOINT_HOST_PATH=/home/jungejblue/e2e_checkpoints/model_0030_0.pth
EXPERIMENT_OUTPUT_HOST_PATH=/home/jungejblue/e2e_experiment_outputs
```

현재 사용자 ID를 확인해 `RESEARCH_UID`, `RESEARCH_GID`도 맞춥니다.

```bash
id -u
id -g
```

## Build

```bash
docker compose --env-file docker/.env -f docker/compose.yaml build research
```

Compose 설정만 먼저 검사하려면 다음을 사용합니다.

```bash
docker compose --env-file docker/.env -f docker/compose.yaml config
```

## Run

먼저 host에서 CARLA server를 실행합니다.

```bash
cd ~/e2e_carla_ws
./CarlaUE4.sh -quality-level=Low
```

다른 terminal에서 연구 container를 실행합니다.

```bash
cd ~/e2e_Carla_paper
docker compose --env-file docker/.env -f docker/compose.yaml run --rm research
```

Container 내부 검증:

```bash
python tools/validation/check_container.py --strict
python -m e2e_carla_paper.cli check-env
pytest
```

## Important limitations

- `network_mode: host`는 현재 연구 host인 Linux/Ubuntu를 전제로 합니다.
- Docker build 성공은 CARLA server 연결이나 checkpoint 정상 추론을 보장하지 않습니다.
- `requirements-carla-garage.txt`를 임의로 upgrade하면 baseline 자체가 바뀔 수 있습니다.
- CARLA server까지 container에 넣는 방식은 custom package와 렌더링 검증이 완료된
  뒤 별도 compose service로 추가하는 것이 안전합니다.

