import argparse
import glob
import os

from _libg96 import G96Mol
from _libstate import StateMol


def _parse_args():
    # prepare argument parser
    parser = argparse.ArgumentParser(
        prog="state2g96",
        description="Convert OpenMM state xml to g96 format.",
    )

    # options to sepcify input file
    parser.add_argument(
        "-f",
        type=str,
        help="OpenMM state xml",
        required=True,
    )

    parser.add_argument(
        "-o",
        type=str,
        help="Output g96 file",
        required=False,
        default="state.g96",
    )

    args = parser.parse_args()

    return args


def _check_args(args):
    # check input OpenMM state xml
    if not os.path.exists(args.f):
        raise FileNotFoundError(
            f"Input OpenMM state xml file {args.f} not found."
        )


def _auto_backup(
    file: str,
) -> None:
    if not os.path.exists(file):
        return

    file_dir = os.path.dirname(file)
    file_name = os.path.basename(file)

    old_file_pattern = f"#{file_name}.*#"
    old_files = sorted(glob.glob(os.path.join(
        file_dir,
        old_file_pattern,
    )))

    num_old_files = len(old_files)

    new_backup_file_name = f"#{file_name}.{num_old_files + 1}#"
    new_backup_file = os.path.join(file_dir, new_backup_file_name)

    os.rename(file, new_backup_file)


if __name__ == "__main__":
    # parse args
    args = _parse_args()

    # check args
    _check_args(args)

    # convert
    state = StateMol.from_file(args.f)
    g96_mol = G96Mol(
        title="",
        timestep=state.timestep,
        position=state.position,
        velocity=state.velocity,
        box_vectors=state.box_vectors,
    )

    _auto_backup(args.o)

    with open(args.o, "w") as f:
        f.writelines(f"{str(g96_mol)}\n")
