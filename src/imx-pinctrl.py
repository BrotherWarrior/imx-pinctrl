#!/bin/env python3
import argparse
import enum


class ImxCommonConfig(enum.Flag):
    PAD_CTL_HYS = (1 << 16)
    PAD_CTL_PUE = (1 << 13)
    PAD_CTL_PKE = (1 << 12)
    PAD_CTL_ODE = (1 << 11)


class ImxPUSConfig(enum.Flag):
    PAD_CTL_PUS_100K_DOWN = (0 << 14)
    PAD_CTL_PUS_47K_UP = (1 << 14)
    PAD_CTL_PUS_100K_UP = (2 << 14)
    PAD_CTL_PUS_22K_UP = (3 << 14)


class ImxSPEEDConfig(enum.Flag):
    PAD_CTL_SPEED_LOW = (0 << 6)
    PAD_CTL_SPEED_MED = (1 << 6)
    PAD_CTL_SPEED_UNK = (2 << 6)
    PAD_CTL_SPEED_HIGH = (3 << 6)


class ImxDSEConfig(enum.Flag):
    PAD_CTL_DSE_DISABLE = (0 << 3)
    PAD_CTL_DSE_260ohm = (1 << 3)
    PAD_CTL_DSE_130ohm = (2 << 3)
    PAD_CTL_DSE_87ohm = (3 << 3)
    PAD_CTL_DSE_65ohm = (4 << 3)
    PAD_CTL_DSE_52ohm = (5 << 3)
    PAD_CTL_DSE_43ohm = (6 << 3)
    PAD_CTL_DSE_37ohm = (7 << 3)


class ImxSREConfig(enum.Flag):
    PAD_CTL_SRE_FAST = (1 << 0)
    PAD_CTL_SRE_SLOW = (0 << 0)


class ImxODTConfig(enum.Flag):
    PAD_CTL_ODT_off = (0 << 8)
    PAD_CTL_ODT_120_Ohm = (1 << 8)
    PAD_CTL_ODT_60_Ohm = (2 << 8)
    PAD_CTL_ODT_40_Ohm = (3 << 8)
    PAD_CTL_ODT_30_Ohm = (4 << 8)
    PAD_CTL_ODT_24_Ohm = (5 << 8)
    PAD_CTL_ODT_20_Ohm = (6 << 8)
    PAD_CTL_ODT_17_Ohm = (7 << 8)


def ImxConfigFromString(arg):
    if arg in ImxCommonConfig._member_names_:
        return ImxCommonConfig[arg]

    if arg in ImxDSEConfig._member_names_:
        return ImxDSEConfig[arg]

    if arg in ImxODTConfig._member_names_:
        return ImxODTConfig[arg]

    if arg in ImxPUSConfig._member_names_:
        return ImxPUSConfig[arg]

    if arg in ImxSREConfig._member_names_:
        return ImxSREConfig[arg]

    if arg in ImxSPEEDConfig._member_names_:
        return ImxSPEEDConfig[arg]

    msg = "'%s' is not a valid PAD_CTL_* value" % arg
    raise argparse.ArgumentTypeError(msg)

def encode(args):
    v = 0
    for a in args.flags:
        v |= a.value

    print(hex(v))


def int_parser(arg):
    return int(arg, 0)


def decode(args):
    b = args.value
    bits = []
    bits.extend([bit.name for bit in ImxCommonConfig
                 if b & bit.value == bit.value])

    # if b & ImxCommonConfig.PAD_CTL_PUE.value:
    bits.extend([bit.name for bit in ImxPUSConfig
                 if b & (3 << 14) == bit.value])

    bits.extend([bit.name for bit in ImxODTConfig
                 if b & (7 << 8) == bit.value])
    bits.extend([bit.name for bit in ImxSPEEDConfig
                 if b & (3 << 6) == bit.value])
    bits.extend([bit.name for bit in ImxDSEConfig
                 if b & (7 << 3) == bit.value])
    bits.extend([bit.name for bit in ImxSREConfig
                 if b & (3) == bit.value])

    print(' | '.join(bits))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(help='command')

    sub_decode = sub_parsers.add_parser('decode', help='Decode pinctrl')
    sub_decode.add_argument('value', type=int_parser, help='Value to decode')
    sub_decode.set_defaults(func=decode)

    sub_encode = sub_parsers.add_parser('encode', help='Encode pinctrl')
    sub_encode.add_argument('flags', nargs='+',
                            type=ImxConfigFromString)
    sub_encode.set_defaults(func=encode)

    args = parser.parse_args()

    args.func(args)
