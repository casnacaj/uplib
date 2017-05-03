# Function which can be used to push data to phant webserver
# (data.sparkfun.com or similar).
#
# Copyright (c) 2017 Jan A. Humpl <jan.a.humpl@centrum.cz>
#
# Distributed under terms of the MIT license.

from netut import wget
from phant_config import HOST
from phant_config import PUB_KEY
from phant_config import PRI_KEY

PATH = 'input/' + PUB_KEY + '?private_key=' + PRI_KEY

def update(string):
    path = PATH + string
    wget(HOST, path)
