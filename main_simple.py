#!/usr/bin/env python3
"""
Simple main file for testing CI pipeline
"""

import sys
import os


def test_imports():
    """Test all imports"""
    try:
        from core.config import get_settings

        print("✅ Core config imported successfully")
    except Exception as e:
        print(f"❌ Core config import failed: {e}")
        return False

    try:
        from core.metrics import SystemMetrics

        print("✅ Core metrics imported successfully")
    except Exception as e:
        print(f"❌ Core metrics import failed: {e}")
        return False

    try:
        from core.langfuse_client import LangfuseClient

        print("✅ Langfuse client imported successfully")
    except Exception as e:
        print(f"❌ Langfuse client import failed: {e}")
        return False

    return True


def test_basic_functionality():
    """Test basic functionality"""
    try:
        from core.metrics import SystemMetrics

        metrics = SystemMetrics()
        metrics.record_task_completion(True, 1000.0)

        assert metrics.metrics["total_tasks_processed"] == 1
        assert metrics.metrics["success_rate"] == 1.0

        print("✅ Basic functionality test passed")
        return True

    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Testing Python Trading Control Platform")

    success = True
    success &= test_imports()
    success &= test_basic_functionality()

    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
