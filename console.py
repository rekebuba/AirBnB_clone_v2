#!/usr/bin/python3
"""A module that contains the entry point of the command interpreter"""
import cmd
from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_EOF(self, args):
        """Used to exit the program"""
        print()
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
        """Prints the string representation of an instance
        based on the class name and id"""
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
        """Prints all string representation of all instances
        based or not on the class name"""
        storage.reload()
        all_objs = storage.all()
        lists = []
        if args and args not in storage.Classes():
            print("** class doesn't exist **")
        elif args:
            for key in all_objs.keys():
                if key[:key.index('.')] == args:
                    lists.append(str(all_objs[key]))
            print(lists)
        else:
            for key in all_objs.keys():
                lists.append(str(all_objs[key]))
            print(lists)

    def precmd(self, args):
        """Modify the command or return it unchanged"""
        new_line = args
        try:
            if args[args.index('.'):] == ".all()":
                new_line = f"all {args[:args.index('.')]}"
            elif args[args.index('.'):] == ".count()":
                new_line = f"count {args[:args.index('.')]}"
            elif args[args.index('.'):args.index('(') + 1] == ".show(":
                char = '"'
                A = args.index('.')
                B = args.index(char)
                new_line = f"show {args[:A]} {args[B + 1:-2]}"
            elif args[args.index('.'):args.index('(') + 1] == ".destroy(":
                char = '"'
                A = args.index('.')
                B = args.index(char)
                new_line = f"destroy {args[:A]} {args[B + 1:-2]}"
            elif args[args.index('.'):args.index('(') + 1] == ".update(":
                char = '"'
                A = args.index('.')
                B = args.index('{')
                C = args.index(')')
                tokens = args[args.index(char):-1].replace(char, '').split(',')
                if '{' in args:
                    new_line = f"update {args[:A]} {tokens[0]} {args[B:C]}"
                else:
                    new_line = f"update {args[:A]} {tokens[0]} {tokens[1]} \"{tokens[2].strip()}\""
        except ValueError:
            pass
        return new_line

    def do_count(self, args):
        """prints the number of instances of a class"""
        count = 0
        storage.reload()
        all_obj = storage.all()
        if args not in storage.Classes():
            print("** class doesn't exist **")
        else:
            for key in all_obj.keys():
                if key[:key.index('.')] == args:
                    count += 1
            print(count)

    def do_update(self, args):
        """Updates an instance based on the class name and id by
        adding or updating attribute"""
        arg = args.split()
        storage.reload()
        all_objs = storage.all()
        if not arg:
            print("** class name is missing **")
        elif arg[0] not in storage.Classes():
            print("** class doesn't exist **")
        elif len(arg) < 2:
            print("** instance id missing **")
        elif '{' in args:
            instance = f"{arg[0]}.{arg[1]}"
            args_dict = eval(args[args.index('{'):args.index('}') + 1])
            try:
                for key, value in args_dict.items():
                    obj = all_objs[instance]
                    setattr(obj, key, value)
                all_objs[instance].save()
            except KeyError:
                print("** no instance found **")
            pass
        elif len(arg) < 3:
            print("** attribute name missing **")
        elif len(arg) < 4:
            print("** value missing **")
        else:
            instance = f"{arg[0]}.{arg[1]}"
            try:
                value = all_objs[instance]
                types = type(value.to_dict()[arg[2]])
                setattr(value, arg[2], types(arg[3].replace('"', '')))
                all_objs[instance].save()
            except KeyError:
                print("** no instance found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
