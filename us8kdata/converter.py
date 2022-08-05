import subprocess
import pandas as pd
from pathlib import Path
from argparse import ArgumentParser
from shutil import which
"""
Convert UrbanSound8K audio clips stored in RAW_AUDIO_ROOT
into 16kHz (default) or 8kHz 16bit mono wave files, and output them to  OUT_ROOT.

The files are divided into fold directories for reproducible cross validation,
and this folder structure is kept.

Also, the UrbanSound8K metadata is pruned and output to OUT_ROOT as well.
"""

# RAW_DATA_ROOT = Path(__file__).absolute() / '../raw_data'

# RAW_AUDIO_ROOT = RAW_DATA_ROOT / 'audio'

# METADATA_PATH = RAW_DATA_ROOT / 'metadata/UrbanSound8K.csv'

# OUT_ROOT = Path(__file__).absolute().parent() / 'data'

parser = ArgumentParser()
parser.add_argument(
    "raw_data_root",
    type=Path,
    help='The directory that holds UrbanSounds8K "audio/" and "metadata/"',
)
parser.add_argument(
    "out_root", type=Path, help="The output directory for the converted data"
)
parser.add_argument(
    "--eight-k",
    action="store_true",
    help="if set, convert raw data to 8kHz sample rate",
)


def convert_audio(raw_data_root, out_root, eight_k=False):
    # get a list of all wave files in the raw_data directory
    raw_audio_root = raw_data_root / "audio"

    # OUT_ROOT = Path(__file__).absolute().parent() / 'data'
    all_files = list(raw_audio_root.glob("*/*.wav"))
    if not all_files:
        raise UserWarning(f"ERROR:: Can't find wave files under {raw_audio_root}")
    print(f"Converting {len(all_files)} files.")
    # Iterate over the files and convert each one using ffmpeg
    # We use ffmpeg rather than converting with python because
    # some of the files have tricky formats
    for idx, path in enumerate(all_files):
        if idx % 500 == 0:
            print(f"{idx} files done. Converting {path}")
        outpath = out_root / Path(*path.parts[-2:])

        if not outpath.parent.exists():
            outpath.parent.mkdir(parents=True)
        if not outpath.exists():
            sample_rate, codec = 16000, "pcm_s16le"
            if eight_k:
                sample_rate, codec = 8000, "pcm_s8le"
            cmd_str = f"ffmpeg -i {path.as_posix()} -ar {sample_rate} -ac 1 -c:a {codec} {outpath.as_posix()}"  # noqa
            subprocess.run(
                cmd_str, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            )


def convert_metadata(metadata_path, out_root):
    outpath = out_root / Path(*metadata_path.parts[-2:])
    df = pd.read_csv(metadata_path)
    if not outpath.parent.exists():
        outpath.parent.mkdir()
    df[["slice_file_name", "salience", "fold", "classID", "class"]].to_csv(
        outpath, index=False
    )


if __name__ == "__main__":
    if which("ffmpeg") is None:
        raise UserWarning("ERROR: Can't find ffmpeg on PATH\n\tInstall ffmpeg and try again\n\t(eg 'brew install ffmpeg')")
    args = parser.parse_args()
    convert_audio(args.raw_data_root, args.out_root, eight_k=args.eight_k)
    metadata_path = args.raw_data_root / "metadata/UrbanSound8K.csv"
    convert_metadata(metadata_path, args.out_root)
