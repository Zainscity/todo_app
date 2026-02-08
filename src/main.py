"""
Todo In-Memory Python Console App - Main Entry Point

This application provides a command-line interface for managing a to-do list.
All data is stored in memory and will be lost when the application exits.
"""
import sys
from cli.interface import CLIInterface


def main():
    """Main entry point for the application."""
    if len(sys.argv) > 1:
        # Command-line mode
        cli = CLIInterface()
        try:
            cli.handle_command_line_args(sys.argv[1:])
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
    else:
        # Interactive mode
        cli = CLIInterface()
        try:
            cli.run_interactive()
        except KeyboardInterrupt:
            print("\nGoodbye!")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()