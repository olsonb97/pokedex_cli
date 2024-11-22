from cmd import Cmd
import pyreadline3

class BaseCommands(Cmd):
    """Base class for all commands"""
    
    def onecmd(self, line):
        """Override Cmd.onecmd to handle exceptions and provide help"""
        try:
            stripped_line = line.strip()
            if not stripped_line:
                return super().onecmd(line)

            if stripped_line.endswith(('?', 'help', '/?')):
                parts = stripped_line[:-1].strip().split()
                if not parts:
                    return super().onecmd(line)
                command = parts[0]
                method_name = f"do_{command}"
                method = getattr(self, method_name, None)

                if method and method.__doc__:
                    print(method.__doc__)
                else:
                    print(f"No help available for '{command}'.")
                return False
            else:
                return super().onecmd(line)
            
        except ValueError as e:
            print(f"Invalid value: {str(e)}")
        except KeyError as e:
            print(f"Not found: {str(e)}")
        except Exception as e:
            print(e)
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