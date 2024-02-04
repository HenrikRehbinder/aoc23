import sys
sys.path.append('..')
from utils.imports import *
file = 'input.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]

