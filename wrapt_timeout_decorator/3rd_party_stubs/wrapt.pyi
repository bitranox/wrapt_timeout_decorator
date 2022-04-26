from typing import Any, TypeVar, Callable, Optional

F = TypeVar('F', bound=Callable[..., Any])
A = TypeVar('A', bound=Callable[..., Any])

def decorator(wrapper: F, enabled: Optional[bool] = None, adapter: Optional[A] = None) -> F: ...
