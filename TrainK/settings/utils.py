import os
from enum import IntEnum
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.abspath(__file__)
for _ in range(3):
	BASE_DIR = os.path.dirname(BASE_DIR)

class Mode(IntEnum):
	Develop = 0
	Testing = 1
	Production = 2
