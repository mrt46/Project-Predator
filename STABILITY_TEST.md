# PROJECT PREDATOR - Stability Test Guide

## Overview

The stability test validates that FAZ 3 remains stable over a 24-hour period by running periodic test suites.

## Running the Stability Test

### Full 24-Hour Test
```bash
python stability_test.py
```

This will:
- Run tests every 30 minutes for 24 hours
- Test all phases (FAZ 1, 2, 3)
- Run demo smoke tests
- Log all results to `stability_test.log`

### Custom Duration
Edit `stability_test.py`:
```python
TEST_DURATION_HOURS = 24  # Change to desired hours
TEST_INTERVAL_MINUTES = 30  # Change to desired interval
```

### Quick Test (for development)
```bash
# Run a single test cycle
python -c "from stability_test import run_all_tests; run_all_tests()"
```

## What Gets Tested

1. **Basic Tests** (`test_basic.py`)
   - Core platform functionality
   - EventBus, Registry, Scheduler

2. **Phase 1 Tests** (`test_blueprint_faz1.py`)
   - CoreEngine validation
   - PolicyGuard checks

3. **Phase 2 Tests** (`test_blueprint_faz2.py`)
   - Agent registration
   - Event subscriptions

4. **Phase 3 Tests** (`test_phase3_simulation.py`)
   - T1: 1-day replay
   - T2: 1-year backtest
   - T3: Strategy switching
   - T4: Accelerated time
   - T5: Deterministic replay

5. **Demo Smoke Test** (`demo.py`)
   - Full system startup/shutdown
   - 10-second runtime validation

## Monitoring

### Log File
All test results are logged to `stability_test.log`:
```bash
tail -f stability_test.log
```

### Success Criteria
- **Pass**: All test runs successful (100% success rate)
- **Fail**: Any test run fails (success rate < 100%)

## Phase 4 Gate

To proceed to Phase 4, the stability test must:
- [ ] Complete 24 hours without failures
- [ ] Maintain 100% success rate
- [ ] All test suites passing consistently

## Troubleshooting

### Test Timeout
If tests timeout (>5 minutes), check:
- System resources (CPU, memory)
- Test data size
- Network connectivity (if applicable)

### Intermittent Failures
If failures occur:
1. Check `stability_test.log` for error details
2. Review test output for specific failures
3. Verify system state hasn't changed
4. Check for resource leaks

### Manual Verification
If automated test fails, manually verify:
```bash
# Run all tests manually
python -m pytest tests/ -v

# Run demo
python demo.py

# Check system health
python -m backend.main &
curl http://localhost:8000/health
```

## Next Steps

After successful 24-hour stability test:
1. Update `PhaseStatus.md` - mark stability test complete
2. Proceed to Phase 4 planning
3. Review Phase 4 design documents
4. Begin Phase 4 implementation
