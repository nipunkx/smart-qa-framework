"""
Pytest Plugin: Automatic AI-Powered Failure Analysis
Hooks into pytest to automatically analyze test failures
"""
import pytest
import os
from typing import Optional
from utils.ai.ai_failure_analyzer import AIFailureAnalyzer


# Global analyzer instance
_analyzer: Optional[AIFailureAnalyzer] = None


def pytest_configure(config):
    """Initialize AI analyzer when pytest starts"""
    global _analyzer
    
    # Check if AI analysis is enabled
    ai_enabled = os.getenv("ENABLE_AI_ANALYSIS", "true").lower() == "true"
    
    if ai_enabled:
        # Try to get Ollama host from config, fall back to env var, then default
        try:
            from utils.config_reader import ConfigReader
            config_reader = ConfigReader()
            ai_config = config_reader.config.get('ai', {})
            ollama_host = ai_config.get('ollama_host', 'http://192.168.50.105:11434')
        except:
            ollama_host = os.getenv("OLLAMA_HOST", "http://192.168.50.105:11434")
        
        _analyzer = AIFailureAnalyzer(ollama_host=ollama_host)
        print(f"\n🤖 AI Failure Analysis ENABLED (Ollama: {ollama_host})")
    else:
        print("\n🤖 AI Failure Analysis DISABLED")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook that runs after each test
    Captures failures and triggers AI analysis
    """
    outcome = yield
    report = outcome.get_result()
    
    # Only analyze test failures (not setup/teardown failures)
    if report.when == "call" and report.failed and _analyzer:
        try:
            # Extract failure information
            test_name = item.nodeid
            error_type = report.longrepr.reprcrash.message.split(':')[0] if hasattr(report.longrepr, 'reprcrash') else "Exception"
            error_message = str(report.longrepr.reprcrash.message) if hasattr(report.longrepr, 'reprcrash') else str(report.longrepr)
            traceback_text = str(report.longrepr) if report.longrepr else None
            
            # Analyze the failure
            print(f"\n🤖 Analyzing failure for: {test_name}")
            analysis = _analyzer.analyze_failure(
                test_name=test_name,
                error_message=error_message,
                error_type=error_type,
                traceback_text=traceback_text
            )
            
            # Store analysis in test report
            if not hasattr(report, 'ai_analysis'):
                report.ai_analysis = analysis
            
            # Print analysis to console
            print(f"\n{'='*70}")
            print("🤖 AI FAILURE ANALYSIS")
            print(f"{'='*70}")
            print(f"Test: {test_name}")
            print(f"Error: {error_type}")
            print("-" * 70)
            print(analysis.get('analysis', 'No analysis available'))
            print(f"{'='*70}\n")
            
        except Exception as e:
            print(f"\n⚠️ AI analysis failed: {str(e)}")


@pytest.fixture(scope="function", autouse=True)
def ai_failure_context(request):
    """
    Fixture that adds AI analysis context to test reports
    This runs for every test automatically
    """
    yield
    
    # After test completes, check if it failed and has AI analysis
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        if hasattr(request.node.rep_call, 'ai_analysis'):
            # AI analysis is already attached to the report
            pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """Store test reports for later access"""
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """Store call phase report"""
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item):
    """Store teardown report"""
    yield


def pytest_runtest_logreport(report):
    """Store reports in test item for later access"""
    if hasattr(report, 'item'):  # Only if item attribute exists
        if report.when == 'setup':
            report.item.rep_setup = report
        elif report.when == 'call':
            report.item.rep_call = report
        elif report.when == 'teardown':
            report.item.rep_teardown = report
