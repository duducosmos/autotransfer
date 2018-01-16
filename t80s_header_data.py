#!/usr/bin/env python
# -*- Coding: UTF-8 -*-
"""
Add info in header of image of T80S from Pipeline Data Base.
"""

from astropy.io import fits

from config import JYPE_VERSION, PATH_ROOT, TILES_VERSION, FILTERS
from tileinfo import tile_info, get_zp, get_depth2fwhm5s, get_depth3arc5s
from tileinfo import get_deptharcsec2, get_mjd_for_tiling


__AUTHOR = "E. S. Pereira"
__DATE = "10/10/2017"
__EMAIL = "pereira.somoza@gmail.com"


def t80s_header_data(pname, filetype="fz", hdr_pos=0):
    tile_path = "{0}/{1}/tiles/{2}/{3}".format(PATH_ROOT,
                                               JYPE_VERSION,
                                               TILES_VERSION,
                                               pname)

    for filt in FILTERS:
        img_path = "{0}/{1}/{2}_{1}_swp.{3}".format(tile_path,
                                                    filt,
                                                    pname,
                                                    filetype
                                                    )
        print("Processing data for img: {0}.".format(img_path))
        print("For filter: {0}.".format(filt))
        id_tilesinfo, ref_image_id, fwhm_min, fwhm_max, filter_id, \
            moffatbeta_mean, noise = tile_info(pname, filt)
        zpt, err_zp, calib_procedure = get_zp(id_tilesinfo)
        depth2fwhm5s = get_depth2fwhm5s(pname, filt)
        depth3arc5s = get_depth3arc5s(pname, filt)
        deptharcsec2 = get_deptharcsec2(pname, filt)

        mjds = get_mjd_for_tiling(pname, filt)

        if len(mjds) > 3:
            mjd1_exp, mjd2_exp, mjd3_exp = mjds[:3]
        elif len(mjds) == 3:
            mjd1_exp, mjd2_exp, mjd3_exp = mjds

        data, hdr = fits.getdata(img_path, header=True)

        hdr['PNAME'] = pname
        hdr['IMAGE_ID'] = id_tilesinfo
        hdr['REF_IMAGE_ID'] = ref_image_id
        hdr['ZPT'] = zpt
        hdr['ERRZPT'] = err_zp
        hdr['CALIB_PROCEDURE'] = calib_procedure
        hdr['MJD1'] = mjd1_exp[0]
        hdr['EXPTIME1'] = mjd1_exp[1]
        hdr['MJD2'] = mjd2_exp[0]
        hdr['EXPTIME2'] = mjd2_exp[1]
        hdr['MJD3'] = mjd3_exp[0]
        hdr['EXPTIME3'] = mjd3_exp[1]
        hdr['FWHM_MIN'] = fwhm_min
        hdr['FWHM_MAX'] = fwhm_max
        hdr['MOFFATBETA_MEAN'] = moffatbeta_mean
        hdr['DEPTH2FWHM5S'] = depth2fwhm5s
        hdr['DEPTH3ARC5S'] = depth3arc5s
        hdr['DEPTHARCSEC2'] = deptharcsec2

        fits.writeto(img_path, data, hdr, overwrite=True)


if __name__ == "__main__":
    import argparse
    import sys
    DESCRIPTION = '''
    Update Header of combined images for a given Tile.
    '''
    PARSER = argparse.ArgumentParser(
        description=DESCRIPTION)

    PARSER.add_argument("-p",
                        help="PNAME: Name of tile",
                        type=str,
                        default=None)

    PARSER.add_argument("-t",
                        help="Extesion of fits file (fits or fz)",
                        type=str,
                        default='fz')

    PARSER.add_argument("-l",
                        help="Position of header in fits. default 0",
                        type=int,
                        default=0)

    ARGS = PARSER.parse_args()

    if ARGS.p is None:
        print("Name of tile (PNAME), not passed")
        sys.exit(0)

    if ARGS.t not in ['fits', 'fz']:
        print("No valid fits image format: {}".format(ARGS.t))
        sys.exit(0)

    t80s_header_data(ARGS.p, ARGS.t, ARGS.l)
