#!/usr/bin/python3
import cmd
from models.base_model import BaseModel 


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_EOF(self, args):
        """Used to exit the program"""
        return True
    def do_quit(self, args):
        """Used to exit the program"""
        return True
    def do_create(self, args):
        """Creates a new instance of BaseModel"""
        if not args:
            print("** class name missing **")
        elif args == "BestModel":
            instance = BaseModel()
            instance.save()
            print(instance.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, args):
        """Prints the string representation of an instance based on the class name and id"""
        lists = [arg for arg in args.split()]
        if not lists[0]:
            print("** class name is missing **")
        elif lists[0] == "BestModel" and lists[1]:
            ...
            print(args)





if __name__ == '__main__':
    HBNBCommand().cmdloop()
