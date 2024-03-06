#!/usr/bin/python3
import cmd


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_EOF(self, args):
        """Used to exit the program"""
        return True
    def do_quit(self, args):
        """Used to exit the program"""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
