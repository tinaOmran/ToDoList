"""Main entry point for the Todo List application."""

from cli.console import run_cli


def main():
    """Main application entry point."""
    print("To_do_List Application")

    try:
        # start CLI
        run_cli()
    except KeyboardInterrupt:
        print("\n Application stopped by user")
    except Exception as e:
        print(f"Application error: {e}")
    finally:
        print("Application shutdown complete")


if __name__ == "__main__":
    main()