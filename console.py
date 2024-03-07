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
    def do_create(self, args):
        """Creates a new instance of BaseModel"""
        if not args:
            print("** class name missing **")
        elif args == "BestModel":
            from models.base_model import BaseModel
            instance = BaseModel()
            instance.save()
            print(instance.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, args):
        """Prints the string representation of an instance based on the class name and id"""
        arg = args.split()
        if not arg:
            print("** class name is missing **")
        elif arg[0] != "BaseModel":
            print("** class doesn't exist **")
        elif len(arg) < 2:
            print("** instance id missing **")
        else:
            from models.engine.file_storage import FileStorage
            storage = FileStorage()
            storage.reload()
            all_objs = storage.all()
            instance = '.'.join(arg)
            try:
                print(all_objs[instance])
            except KeyError:
                print("** instance id not found **")






if __name__ == '__main__':
    HBNBCommand().cmdloop()
