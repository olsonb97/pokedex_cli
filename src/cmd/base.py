from cmd import Cmd

class BaseCommands(Cmd):
    """Base class for all commands"""
    categories = {
            "Pokemon": ["search"],
            "System": ["exit"]
        }
    
    def onecmd(self, line):
        """Override Cmd.onecmd to handle exceptions"""
        try:
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