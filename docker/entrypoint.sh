#!/usr/bin/env bash
set -euo pipefail

if [[ -d "${CARLA_GARAGE_ROOT:-}" ]]; then
    export SCENARIO_RUNNER_ROOT="${SCENARIO_RUNNER_ROOT:-${CARLA_GARAGE_ROOT}/scenario_runner}"
    export LEADERBOARD_ROOT="${LEADERBOARD_ROOT:-${CARLA_GARAGE_ROOT}/leaderboard}"
    export TEAM_CODE_ROOT="${TEAM_CODE_ROOT:-${CARLA_GARAGE_ROOT}/team_code}"
    export PYTHONPATH="${CARLA_ROOT:-/external/CARLA}/PythonAPI/carla:${SCENARIO_RUNNER_ROOT}:${LEADERBOARD_ROOT}:${TEAM_CODE_ROOT}:/workspace/e2e_Carla_paper/src:${PYTHONPATH:-}"
fi

exec "$@"

