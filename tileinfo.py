#!/usr/bin/env python
# -*- Coding: UTF-8 -*-
"""
Get Tile Info from Pipeline Data Base.
"""
from model import db

__AUTHOR = "E. S. Pereira"
__DATE = "10/10/2017"
__EMAIL = "pereira.somoza@gmail.com"


def get_pnames():
    '''
    Return all PName from t80tiles
    '''
    pname = db().select(db.t80tiles.PNAME)
    pname = [pn.pname for pn in pname]
    return pname


def tile_info(tile):
    pass
