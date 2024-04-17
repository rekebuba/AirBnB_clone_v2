#!/usr/bin/python3
"""A module that contains the entry point of the command interpreter"""

import cmd
import re
from checker import Checker
from models import storage
from models.base_model import BaseModel
from datetime import datetime
import uuid


class HBNBCommand(cmd.Cmd):
    """Command line program"""
    prompt = '(hbnb) '

    def do_EOF(self, args):
        """Used to exit the program"""
        print()
        return True

    def do_quit(self, args):
        """Used to exit the program"""
        return True

    def emptyline(self):
        """emptyline should not execute anything"""
        pass

    def do_create(self, args):
        """Creates a new instance of BaseModel"""
        matches = re.findall(r"^(\S*) ?|([^=]*)=\"?([^(\" )]*)\"? ?", args)
        kwargs = {}
        args = matches[0][0]
        if len(matches) > 1:
            for i, _ in enumerate(matches):
                if i != 0:
                    att = Checker().attributes()[args][matches[i][1]]
                    kwargs[matches[i][1]] = att(matches[i][2].replace('_', ' '))
        if not args:
            print("** class name missing **")
        elif args not in Checker().classes():
            print("** class doesn't exist **")
        else:
            instance = Checker().classes()[args](**kwargs)
            instance.save()
            print(instance.id)

    def do_show(self, args):
        """Prints the string representation of an instance
        based on the class name and id"""
        arg = args.split()
        if args == "" or args is None:
            print("** class name missing **")
        elif arg[0] not in Checker().classes():
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
            print("** class name missing **")
        elif arg[0] not in Checker().classes():
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
        if args and args not in Checker().classes():
            print("** class doesn't exist **")
        elif args:
            for key, value in all_objs.items():
                if key[:key.index('.')] == args:
                    try:
                        del value.__dict__['_sa_instance_state']
                    except KeyError:
                        pass
                    lists.append(str(all_objs[key]))
            print(lists)
        else:
            for key, value in all_objs.items():
                try:
                    del value.__dict__['_sa_instance_state']
                except KeyError:
                    pass
                lists.append(str(all_objs[key]))
            print(lists)

    def default(self, line):
        """default value if nothing matches"""
        self._precmd(line)

    def _precmd(self, line):
        """Modify the command or return it unchanged"""
        new_line = line
        try:
            match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
            clas_name = match.group(1)
            method = match.group(2)
            args = match.group(3)
            char = '"'
            if method in ["all", "count"]:
                new_line = f"{method} {clas_name}"
            elif method in ["show", "destroy"]:
                new_line = f"{method} {clas_name} {args.replace(char, '')}"
            elif method == "update":
                arg = re.search(r"^\"?([^\"]*)\"?,? ?(\"\w*\
                    \")?(?:, ([^\{].*))?(.*)?$", args)
                if clas_name == '' or clas_name is None:
                    new_line = f"{method} {clas_name}"
                else:
                    id = arg.group(1)
                    attribute = arg.group(2)
                    value = arg.group(3)
                    dicts = arg.group(4)
                    if dicts != '' and dicts is not None:
                        new_line = f"{method} {clas_name} {id} {dicts}"
                    else:
                        new_line = f"{method} {clas_name} {id} {attribute} \
                            {value}"
        except Exception:
            return line
        self.onecmd(new_line)
        return new_line

    def do_count(self, args):
        """prints the number of instances of a class"""
        count = 0
        storage.reload()
        all_obj = storage.all()
        if args == "":
            print("** class name missing **")
        elif args not in Checker().classes():
            print("** class doesn't exist **")
        else:
            for key in all_obj.keys():
                if key[:key.index('.')] == args:
                    count += 1
            print(count)

    def do_update(self, line):
        """Updates an instance based on the class name and id by
        adding or updating attribute"""
        if line == "" or line is None:
            print("** class name missing **")
            return
        match = re.search(r"^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:\"[^\"]*\
                        \")|(?:(\S)+)))?)?)?", line)
        clas_name = match.group(1)
        id = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        try:
            value = eval(value)
        except (TypeError, NameError):
            pass
        if clas_name is None:
            print("** class name missing **")
        elif clas_name not in Checker().classes():
            print("** class doesn't exist **")
        elif id is None:
            print("** instance id missing **")
        elif id:
            key = f"{clas_name}.{id}"
            if key not in storage.all():
                print("** no instance found **")
            elif type(value) is dict:
                clas_key = f"{clas_name}.{id}"
                for k, v in value.items():
                    self.set_attribute(clas_name, clas_key, k, v)
            elif attribute == "None" or attribute is None:
                print("** attribute name missing **")
            elif value == "None" or value is None:
                print("** value missing **")
            else:
                clas_key = f"{clas_name}.{id}"
                self.set_attribute(clas_name, clas_key, attribute, value)

    def set_attribute(self, class_name, id, key, value):
        """set or update an attribute for the given class
        with the key and the value"""
        try:
            storage.reload()
            all_objs = storage.all()
            setattr(all_objs[id], key, value)
            all_objs[id].save()
        except KeyError:
            print("** no instance found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
