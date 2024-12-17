from cmd import Cmd
from traceback import print_exc
import requests

class BaseCommands(Cmd):
    """Base class for all commands"""
    
    def onecmd(self, line):
        """Override Cmd.onecmd to handle exceptions and expand help"""
        try:
            stripped_line = line.strip()
            if not stripped_line:
                return super().onecmd(line)

            # Possible help suffixes
            help_suffixes = ('help', '/?', ' -h', '?')
            matched_suffix = None

            # Find which suffix matches
            for suffix in help_suffixes:
                if stripped_line.lower().endswith(suffix):
                    matched_suffix = suffix
                    break

            if matched_suffix:
                # Remove the matched suffix from the line
                command_part = stripped_line[:-len(matched_suffix)].strip()
                if not command_part:
                    return super().onecmd(line)
                
                # Get the docstring for the command requested
                parts = command_part.split()
                command = parts[0]
                method_name = f"do_{command}"
                method = getattr(self, method_name, None)

                if method and method.__doc__:
                    print(method.__doc__)
                else:
                    print(f"No help available for '{command}'.")
                return False  # Indicate that the command was handled

            else:
                return super().onecmd(line)

        except ValueError as e:
            print(f"Invalid value: {str(e)}")
        except KeyError as e:
            print(f"Not found: {str(e)}")
        except requests.RequestException as e:
            print(f"Request error: {str(e)}")
        except Exception:
            print_exc()  # Print the full traceback as last resort
        return False

    def emptyline(self):
        """Override Cmd.emptyline to do nothing"""
        pass
        
    def default(self, line):
        """Override Cmd.default to handle unknown commands"""
        if line.startswith(("!", "#")):
            return
        print(f"Unknown command: {line}")

    def do_exit(self, arg):
        """Go back a level"""
        return True