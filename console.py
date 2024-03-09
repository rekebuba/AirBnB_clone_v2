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
            char = '"'
            A = args.index('.')
            B = args.index('(')
            C = args.index(')')
            if args[A:] == ".all()":
                new_line = f"all {args[:A]}"
            elif args[A:] == ".count()":
                new_line = f"count {args[:A]}"
            elif args[A:B] == ".show":
                args = args.replace(char, '')
                new_line = f"show {args[:A]} {args[B + 1:C]}"
            elif args[A:B] == ".destroy":
                args = args.replace(char, '')
                new_line = f"destroy {args[:A]} {args[B + 1:C]}"
            elif args[A:B] == ".update":
                tokens = args[args.index(char):C].replace(char, '').split(',')
                if '{' in args:
                    B = args.index('{')
                    new_line = f"update {args[:A]} {tokens[0]} {args[B:C]}"
                elif '[' in args:
                    D = args.index('[')
                    new_line = f"update {args[:A]} {tokens[0]} {tokens[1]} {args[D:C]}"
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
        if not arg:
            print("** class name is missing **")
        elif arg[0] not in storage.Classes():
            print("** class doesn't exist **")
        elif len(arg) < 2:
            print("** instance id missing **")
        elif '{' in args:
            clas_key = f"{arg[0]}.{arg[1]}"
            A = args.index('{')
            B = args.index('}')
            args_dict = eval(args[A:B + 1])
            for key, value in args_dict.items():
                self.set_attribute(arg[0], clas_key, key, value)
        elif len(arg) < 3:
            print("** attribute name missing **")
        elif len(arg) < 4:
            print("** value missing **")
        elif '[' in args:
            clas_key = f"{arg[0]}.{arg[1]}"
            A = args.index('[')
            B = args.index(']')
            args_dict = eval(args[A:B + 1])
            self.set_attribute(arg[0], clas_key, arg[2], args_dict)
        else:
            clas_key = f"{arg[0]}.{arg[1]}"
            self.set_attribute(arg[0], clas_key, arg[2], arg[3].replace('"', ''))

    def set_attribute(self, class_name, id, key, value):
        """set or update an attribute for the given class
        with the key and the value"""
        try:
            storage.reload()
            all_objs = storage.all()
            types = storage.Types()[class_name][key]
            setattr(all_objs[id], key, types(value))
            all_objs[id].save()
        except KeyError:
            print("** no instance found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
