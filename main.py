#!/usr/bin/python3
from models.base_model import BaseModel
import re


b = BaseModel()
rex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
res = rex.match(str(b))
