import pytest


def pytest_addoption(parser):
    parser.addoption(
        '-B',
        '--run-benchmarks',
        action='store_true',
        default=False,
        help='run benchmarks',
    )

def pytest_runtest_setup(item):
    """
    Skip test marked benchmark unless --run-benchmark is given to pytest
    """
    run_benchmarks = item.config.getoption('--run-benchmarks')

    is_benchmark = any(item.iter_markers(name="benchmark"))

    if is_benchmark:
        if run_benchmarks:
            return

        pytest.Skip(
            'need --run-benchmarks to run benchmark'
        )

def pytest_collection_modifyitens(items):
    """
    Add the "benchmark" mark to test that start with "benchmark_".
    """
    for item in items:
        test_class_name = item.cls.__name__
        if test_class_name.startswith("benchmark_"):
            item.add_marker(pytest.mark.benchmark)