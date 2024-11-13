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
        """Exit the Pokedex"""
        print("Bye bye!")
        return True

    def do_help(self, arg):
        """List available commands with 'help'"""
        if arg:
            super().do_help(arg)
        else:
            print("\nPokedex Commands:")
            print("=" * 50)
            
            for category, commands in self.categories.items():
                print(f"{category}:")
                for cmd in commands:
                    doc = getattr(self, f"do_{cmd}").__doc__ or ""
                    print(f"    {cmd:<10} - {doc.split(":")[0]}")
            
            print("\nFor detailed help on a command, type: help <command>")
