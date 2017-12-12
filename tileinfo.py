#!/usr/bin/env python
# -*- Coding: UTF-8 -*-
"""
Get Tile Info from Pipeline Data Base.
"""
from model import db
from astropy.time import Time

__AUTHOR = "E. S. Pereira"
__DATE = "10/10/2017"
__EMAIL = "pereira.somoza@gmail.com"


def get_mjd_for_tiling(pname, filt_name):
    '''
    Return a list of MJD and Exposure time of image used to produce a tile.
    INPUT: PNAme
           Fileter
    '''

    query = db((db.t80tiles.PName == pname)
               &
               (db.filter.Name == filt_name)
               )

    tile_info = query.select(db.t80tiles.id, db.t80tiles.RA, db.t80tiles.DEC,
                             db.t80tiles.PIXEL_SCALE, db.t80tiles.IMAGE_SIZE
                             ).first()

    query = db(db.t80tileImgs.Tile_ID == tile_info.id)
    rcid = query.select(db.t80tileImgs.RC_ID)
    proc_images = [db(db.rc.id == rcidi.RC_ID).select(db.rc.ori_id).first()
                   for rcidi in rcid
                   ]

    images = [db(db.t80oa.id == primg.ori_id).select(db.t80oa.Date,
                                                     db.t80oa.Time,
                                                     db.t80oa.ExpTime
                                                     ).first()
              for primg in proc_images
              ]

    image_date_time = ["{0}T{1}".format(img.Date.strftime("%Y-%m-%d"),
                                        img.Time.strftime("%H:%M:%S"))
                       for img in images
                       ]
    mjd = Time(image_date_time).mjd

    return [[mjd[i], float(images[i].ExpTime)] for i in range(len(images))]


def get_pnames():
    '''
    Return all PName from t80tiles
    '''
    pname = db().select(db.t80tiles.PName)
    pname = [pn.PName for pn in pname]
    return pname


def get_zp(id_tilesinfo):
    '''
    Return zp info:
    Input: ID of tilesinfo
    '''
    query = db(db.calib_zp_tiles.id_tilesinfo == id_tilesinfo)
    zp_info = query.select(db.calib_zp_tiles.zp,
                           db.calib_zp_tiles.err_zp,
                           db.calib_zp_tiles.calib_procedure,
                           ).first()
    return [zp_info.zp, zp_info.err_zp, zp_info.calib_procedure]


def tile_info(pname, filt_name):
    '''
    Return Tile Info.
    Input: PNAME
           filt_name
    '''
    query = db((db.t80tiles.PName == pname)
               &
               (db.filter.Name == filt_name)
               )
    tile_info = query.select(db.t80tilesinfo.id,
                             db.t80tilesinfo.RefImage_ID,
                             db.t80tilesinfo.FWHM_Min,
                             db.t80tilesinfo.FWHM_Max,
                             db.t80tilesinfo.Filter_ID,
                             db.t80tilesinfo.MoffatBeta_Mean
                             ).first()

    return [tile_info.id, tile_info.RefImage_ID, tile_info.FWHM_Min,
            tile_info.FWHM_Max, tile_info.Filter_ID, tile_info.MoffatBeta_Mean]


if __name__ == "__main__":
    # print(get_pnames())
    tile_images = get_mjd_for_tiling('HYDRA_0049', 'R')
    # print(tile_images)
    print(tile_images)
    print(tile_info('HYDRA_0049', 'R'))
