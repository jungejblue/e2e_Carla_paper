# Validation tools

다음 검증 코드를 배치합니다.

- Docker GPU와 Python dependency 확인
- CARLA client/server 버전 확인
- Lincoln MKZ 2020과 map asset 확인
- YAML schema와 외부 commit/checkpoint hash 확인
- paired run의 pre-intervention state consistency 확인

```bash
python tools/validation/check_container.py --strict
```

