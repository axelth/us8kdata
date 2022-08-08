from pathlib import Path
import pandas as pd
import numpy as np
from typing import List, Generator, Union
from scipy.io import wavfile


class UrbanSound8K:
    """
    Dataloader for the cleaned UrbanSound8K dataset
    init params: data_dir - root directory of cleaned data
    attributes:
        data_root: absolute path to data_dir
        metadata: dataset metadata DataFrame
        sample_rate: sample rate of audio files
    """

    def __init__(self, data_dir):
        self.data_root = Path(data_dir).absolute()
        self.metadata = pd.read_csv(self.data_root / "metadata/urbansound8K.csv")
        first_file = self.metadata.query("fold == 1").slice_file_name.iloc[0]
        self.sample_rate = wavfile.read(self.data_root / f"fold1/{first_file}")[0]

    def get_folds(self) -> List[int]:
        """return a list of the folds contained in the dataset"""
        return self.metadata.fold.sort_values().unique().tolist()

    def samples_from_file(self, path: Union[Path, str]) -> np.ndarray:
        """
        Read samples and return them as float32
        params: path - path of wavfile
        returns:
            sr: sample rate
            samples: array of samples as float32 normalized to [-1.0 1.0]
        """
        sr, samples = wavfile.read(path)
        # convert int16 samples to float32 normalized to
        # between -1.0 .. 1.0, to match the values returned
        # by librosa.load.
        # We don't use librosa.load itself because it was
        # 4x slower than wavfile.read
        samples = samples.astype(np.float32) / (np.iinfo(np.int16).max - 1)
        return sr, samples

    def fold_audio_generator(
        self, fold: Union[int, List], classID: Union[int, List] = None
    ) -> Generator:
        """
        Generator function that yields the sample array
        for each audio file in one or more folds
        params:
            fold: fold ID or list of fold IDs
            classID: classID or list of classIDs
        yields: array of float32 samples
        """
        df = self.filter_metadata(fold, classID)
        for _, foldnr, fname in df[['fold', 'slice_file_name']].itertuples():
            path = self.data_root / f"fold{foldnr}/{fname}"
            sr, samples = self.samples_from_file(path)
            yield samples

    def get_fold_classIDs(self, fold, classID=None) -> pd.Series:
        """return classIDs for fold or folds as a Series"""
        return self.filter_metadata(fold, classID).classID

    def get_fold_class_names(self, fold, classID=None) -> pd.Series:
        """return class names for fold or folds as a Series"""
        return self.filter_metadata(fold, classID)["class"]

    def filter_metadata(self, fold, classID=None) -> pd.DataFrame:
        """
        filter metadata on fold and classID
        params:
            fold: fold ID or list of fold IDs
            classID: classID or list of classIDs
        returns: DataFrame
        """
        df = self.metadata
        if not hasattr(fold, "__iter__"):
            fold = [fold]
        if classID is not None:
            if not hasattr(classID, "__iter__"):
                classID = [classID]
            return df[(df["fold"].isin(fold)) & (df["classID"].isin(classID))]
        else:
            return df[df["fold"].isin(fold)]
