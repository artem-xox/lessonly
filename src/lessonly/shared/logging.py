import logging
import sys
from functools import wraps
from typing import Any, Callable, Optional, Protocol, Union

_configured: bool = False


def _configure_root_logger(level: int = logging.INFO) -> None:
    global _configured
    if _configured:
        return

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Avoid adding multiple handlers if something configured logging elsewhere
    if not root_logger.handlers:
        handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        handler.setLevel(level)
        root_logger.addHandler(handler)

    _configured = True


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a module-specific logger with pretty stdout formatting.

    The first call configures the root logger once. Subsequent calls reuse it.
    """
    _configure_root_logger()
    return logging.getLogger(name if name else __name__)


class _BeforeMessageBuilder(Protocol):
    def __call__(self, *args: Any, **kwargs: Any) -> str: ...


class _AfterMessageBuilder(Protocol):
    def __call__(self, result: Any, *args: Any, **kwargs: Any) -> str: ...


MessageBuilder = Union[str, _BeforeMessageBuilder]
AfterMessageBuilder = Union[str, _AfterMessageBuilder]


def log_calls(
    *,
    before: Optional[MessageBuilder] = None,
    after: Optional[AfterMessageBuilder] = None,
    logger_attr: str = "logger",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator to log before and after a function/method call.

    - If used on instance methods, it will prefer `self.<logger_attr>` when present.
    - `before` and `after` can be static strings or callables building messages.
      For `after` callables, the first argument is the function result.
    """

    def _resolve_logger(args: tuple[Any, ...]) -> logging.Logger:
        if args and hasattr(args[0], logger_attr):
            candidate = getattr(args[0], logger_attr)
            if isinstance(candidate, logging.Logger):
                return candidate
        # Fallback to module logger
        return get_logger(__name__)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = _resolve_logger(args)

            if before is not None:
                message = before(*args, **kwargs) if callable(before) else before
                logger.info(message)

            result = func(*args, **kwargs)

            if after is not None:
                if callable(after):
                    message_after = after(result, *args, **kwargs)
                else:
                    message_after = after
                logger.info(message_after)

            return result

        return wrapper

    return decorator
