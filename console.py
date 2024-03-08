#!/usr/bin/python3
import cmd
from models import storage
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
        elif args in storage.Classes():
            instance = storage.Classes()[args]()
            instance.save()
            print(instance.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, args):
        """Prints the string representation of an instance based on the class name and id"""
        arg = args.split()
        if not arg:
            print("** class name is missing **")
        elif arg[0] not in storage.Classes():
            print("** class doesn't exist **")
        elif len(arg) < 2:
            print("** instance id missing **")
        else:
            storage.reload()
            all_objs = storage.all()
            instance = '.'.join(arg)
            try:
                print(all_objs[instance])
            except KeyError:
                print("** no instance found **")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id"""
        arg = args.split()
        if not arg:
            print("** class name is missing **")
        elif arg[0] not in storage.Classes():
            print("** class doesn't exist **")
        elif len(arg) < 2:
            print("** instance id missing **")
        else:
            storage.reload()
            all_objs = storage.all()
            instance = '.'.join(arg)
            try:
                del all_objs[instance]
                storage.save()
            except KeyError:
                print("** no instance found **")

    def do_all(self, args):
        """Prints all string representation of all instances based or not on the class name"""
        storage.reload()
        all_objs = storage.all()
        arg = args.split()
        if len(arg) == 1:
            lists = []
            for key in all_objs.keys():
                if key[:key.index('.')] == arg[0]:
                    lists.append(str(all_objs[key]))
            print(lists)
        else:
            lists = []
            for key in all_objs.keys():
                lists.append(str(all_objs[key]))
            print(lists)

    def precmd(self, args):
        # Modify the command or return it unchanged
        modified_line = args
        try:
            if args[:args.index('.')] in storage.Classes() and args[args.index('.'):] == ".all()":
                modified_line = f"all {args[:args.index('.')]}"
        except ValueError:
            pass
        return modified_line

    def do_update(self, args):
        """Updates an instance based on the class name and id by adding or updating attribute"""
        arg = args.split()
        if not arg:
            print("** class name is missing **")
        elif arg[0] not in storage.Classes():
            print("** class doesn't exist **")
        elif len(arg) < 2:
            print("** instance id missing **")
        elif len(arg) < 3:
            print("** attribute name missing **")
        elif len(arg) < 4:
            print("** value missing **")
        else:
            storage.reload()
            all_objs = storage.all()
            instance = f"{arg[0]}.{arg[1]}"
            try:
                for key, value in all_objs.items():
                    if instance == key:
                        types = type(value.to_dict()[arg[2]])
                        setattr(value, arg[2], types(arg[3][1:len(arg[3]) - 1]))
                        all_objs[instance].save()
            except KeyError:
                print("** no instance found **")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
