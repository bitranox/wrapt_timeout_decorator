import pytest
from typing import List

collect_ignore: List[str] = []


def pytest_load_initial_conftests(early_config: pytest.Config, parser: pytest.Parser, args: List[str]) -> None:
    # PizzaCutter Template can add here additional pytest args
    additional_pytest_args: List[str] = []
    args[:] = list(set(args + additional_pytest_args))
