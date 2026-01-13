#!/usr/bin/env python3
"""
PROJECT PREDATOR - 24 Hour Stability Test
Runs periodic tests to ensure system stability over 24 hours.
"""
import time
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Test configuration
TEST_DURATION_HOURS = 24
TEST_INTERVAL_MINUTES = 30  # Run tests every 30 minutes
LOG_FILE = "stability_test.log"

def log(message: str):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")

def run_test(test_name: str, command: list) -> bool:
    """Run a test and return True if successful"""
    try:
        log(f"Running {test_name}...")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout per test
            cwd=Path(__file__).parent
        )
        if result.returncode == 0:
            log(f"✓ {test_name} PASSED")
            return True
        else:
            log(f"✗ {test_name} FAILED")
            log(f"  stdout: {result.stdout[:500]}")
            log(f"  stderr: {result.stderr[:500]}")
            return False
    except subprocess.TimeoutExpired:
        log(f"✗ {test_name} TIMEOUT (>5 minutes)")
        return False
    except Exception as e:
        log(f"✗ {test_name} ERROR: {e}")
        return False

def run_all_tests() -> dict:
    """Run all stability tests"""
    results = {
        "basic": False,
        "phase1": False,
        "phase2": False,
        "phase3": False,
        "demo": False,
    }
    
    # Test 1: Basic tests
    results["basic"] = run_test(
        "Basic Tests",
        [sys.executable, "-m", "pytest", "tests/test_basic.py", "-v", "--tb=short"]
    )
    
    # Test 2: Phase 1 tests
    results["phase1"] = run_test(
        "Phase 1 Tests",
        [sys.executable, "-m", "pytest", "tests/test_blueprint_faz1.py", "-v", "--tb=short"]
    )
    
    # Test 3: Phase 2 tests
    results["phase2"] = run_test(
        "Phase 2 Tests",
        [sys.executable, "-m", "pytest", "tests/test_blueprint_faz2.py", "-v", "--tb=short"]
    )
    
    # Test 4: Phase 3 tests (T1-T5)
    results["phase3"] = run_test(
        "Phase 3 Tests (T1-T5)",
        [sys.executable, "-m", "pytest", "tests/test_phase3_simulation.py", "-v", "-k", "test_t1 or test_t2 or test_t3 or test_t4 or test_t5", "--tb=short"]
    )
    
    # Test 5: Demo run (smoke test)
    results["demo"] = run_test(
        "Demo Smoke Test",
        [sys.executable, "demo.py"]
    )
    
    return results

def main():
    """Main stability test runner"""
    log("=" * 80)
    log("PROJECT PREDATOR - 24 Hour Stability Test")
    log("=" * 80)
    log(f"Test Duration: {TEST_DURATION_HOURS} hours")
    log(f"Test Interval: {TEST_INTERVAL_MINUTES} minutes")
    log(f"Log File: {LOG_FILE}")
    log("=" * 80)
    
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=TEST_DURATION_HOURS)
    test_count = 0
    success_count = 0
    failure_count = 0
    
    log(f"Test started at: {start_time}")
    log(f"Test will end at: {end_time}")
    log("")
    
    try:
        while datetime.now() < end_time:
            test_count += 1
            remaining = end_time - datetime.now()
            log(f"\n--- Test Run #{test_count} (Time remaining: {remaining}) ---")
            
            results = run_all_tests()
            
            # Count successes
            all_passed = all(results.values())
            if all_passed:
                success_count += 1
                log(f"✓ All tests passed in run #{test_count}")
            else:
                failure_count += 1
                failed_tests = [k for k, v in results.items() if not v]
                log(f"✗ Some tests failed in run #{test_count}: {failed_tests}")
            
            # Summary
            log(f"\nRun #{test_count} Summary:")
            log(f"  Total runs: {test_count}")
            log(f"  Successful runs: {success_count}")
            log(f"  Failed runs: {failure_count}")
            log(f"  Success rate: {(success_count/test_count)*100:.1f}%")
            
            # Wait for next interval
            if datetime.now() < end_time:
                wait_seconds = TEST_INTERVAL_MINUTES * 60
                log(f"\nWaiting {TEST_INTERVAL_MINUTES} minutes until next test run...")
                time.sleep(wait_seconds)
    
    except KeyboardInterrupt:
        log("\n\nStability test interrupted by user")
    
    # Final summary
    total_time = datetime.now() - start_time
    log("\n" + "=" * 80)
    log("STABILITY TEST FINAL SUMMARY")
    log("=" * 80)
    log(f"Total Duration: {total_time}")
    log(f"Total Test Runs: {test_count}")
    log(f"Successful Runs: {success_count}")
    log(f"Failed Runs: {failure_count}")
    log(f"Success Rate: {(success_count/test_count)*100:.1f}%")
    log("=" * 80)
    
    if failure_count == 0:
        log("✓ STABILITY TEST PASSED - All runs successful!")
        return 0
    else:
        log("✗ STABILITY TEST FAILED - Some runs had failures")
        return 1

if __name__ == "__main__":
    sys.exit(main())
