# Research protocol

## Primary question

관측 가능한 불안정 징후로 계산 지연 상황의 전환 필요성과 유효성을 온라인에서
판정하고, 필요한 전환의 recall을 유지하면서 비유효한 개입을 줄일 수 있는가?

## Fixed scope

- One frozen E2E model: TransFuser++
- One representative perturbation: FIFO action latency
- One reference fallback: lane-recovery controller
- No E2E fine-tuning
- No full modular perception-planning stack
- No multi-sensor fault suite

## Paired protocol

각 candidate event에 대해 intervention 이전 조건이 허용 오차 내에서 같은 두 개의
폐루프 실행을 비교합니다.

1. `e2e_continue`: E2E 제어를 유지
2. `forced_fallback`: 동일 후보 시점에 fallback을 강제 적용

단순히 seed가 같다는 이유만으로 counterfactual equivalence를 주장하지 않습니다.
위치, 속도, heading, 주변 actor 상태 등 pre-intervention consistency를 확인하고,
허용 오차를 넘은 pair는 분석에서 제외하거나 별도로 보고합니다.

## Intervention truth table

| E2E continue | Forced fallback | Label |
| --- | --- | --- |
| unsafe | safe | `NECESSARY_EFFECTIVE` |
| safe | safe | `UNNECESSARY` |
| unsafe | unsafe | `INEFFECTIVE` |
| safe | unsafe | `HARMFUL` |

`safe`의 연산적 정의는 실험 전에 collision, lane departure, TTLC 기준으로 고정해야
합니다. Calibration split에서 monitor threshold를 고정한 뒤 test split에는 변경 없이
적용합니다.

