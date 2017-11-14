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


def tile_info(pname, filt_name):
    '''
    Return Tile Info.
    Input: PNAME
           filt_name
    '''
    query = db((db.t80tiles.pname == pname)
               &
               (db.filter.Name == filt_name)
               )
    tile_info = query.select(db.t80tilesinfo.id,
                             db.t80tilesinfo.RefImage_ID,
                             db.t80tilesinfo.FWHM_Min,
                             db.t80tilesinfo.FWHM_Max,
                             db.t80tilesinfo.Filter_ID).first()

    return [tile_info.id, tile_info.RefImage_ID, tile_info.FWHM_Min,
            tile_info.FWHM_Max, tile_info.id]
