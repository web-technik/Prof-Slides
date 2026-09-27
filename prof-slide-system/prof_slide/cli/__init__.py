"""CLI entry point for prof-slide."""


def main():
    """Run the CLI without importing its module during package initialization."""
    from prof_slide.cli.main import main as _main

    return _main()


__all__ = ["main"]
