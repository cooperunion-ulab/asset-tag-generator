#!/usr/bin/env python3
#
#  Cooper Union uLab Asset Tag Generator
#  Copyright (C) 2024 Gary Kim <gary@garykim.dev>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import pathlib

from PIL import Image, ImageDraw, ImageFont

import qrcode


def _generate_asset_qr(asset_id: str) -> Image:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=30,
        border=0,
    )

    qr.add_data(asset_id)
    qr.make(fit=True)
    return qr.make_image(fill_color='black', back_color='white')


def _main():
    parser = argparse.ArgumentParser(
        prog='asset-tag-generator',
        description='Cooper Union microLab Asset Tag Generator',
    )
    parser.add_argument(
        '-f', '--tags-from', type=int, default='0'
    )
    parser.add_argument(
        '-t', '--tags-to', type=int, default='1'
    )
    parser.add_argument(
        '-s', '--save', type=pathlib.Path, default=pathlib.Path('.')
    )
    args = parser.parse_args()

    # Some basic checks
    if args.tags_to > 99999:
        raise Exception('Cannot handle asset tag numbers above 99999')

    if args.tags_to < 0 or args.tags_from < 0:
        raise Exception('Cannot handle negative asset tag numbers')

    if not args.save.is_dir():
        raise Exception('Given path does not seem to be a directory')

    unicode_font = ImageFont.truetype('LiberationSans-Regular.ttf', 227)
    size = (35 * 96, 10 * 96)

    for i in range(args.tags_from, args.tags_to + 1):
        number = f'{i:05}'
        im = Image.new('1', size, (1,))

        d = ImageDraw.Draw(im)

        d.text((7 * 96, 150), 'μLab Asset', font=unicode_font, fill=(0,))
        d.text((7 * 96, 550), number, font=unicode_font, fill=(0,))
        qr = _generate_asset_qr(number)
        im.paste(qr, (2000, 150))

        im.save(args.save / f'{i}.png')


if __name__ == '__main__':
    _main()
