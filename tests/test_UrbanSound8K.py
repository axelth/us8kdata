import os
from us8kdata.loader import UrbanSound8K
from pandas import DataFrame
from pathlib import Path
import numpy as np

DATADIR = os.getenv('DATADIR', 'us8kdata/data')


class TestUrbanSound8K:
    def test_init(self):
        loader = UrbanSound8K(DATADIR)
        assert (hasattr(loader, 'data_root'))
        assert isinstance(loader.data_root,  Path)
        assert (hasattr(loader, 'metadata'))
        assert isinstance(loader.metadata,  DataFrame)
        assert (hasattr(loader, 'sample_rate'))
        assert isinstance(loader.sample_rate,  int)

    def test_filter_metadata_one_fold_all_classes(self):
        loader = UrbanSound8K(DATADIR)
        # pass int
        one_fold_all_classes = loader.filter_metadata(1)
        assert (one_fold_all_classes
                .fold
                .isin([1])
                .all())
        assert (one_fold_all_classes
                .classID
                .nunique() == 10)
        # pass list with one int
        one_fold_all_classes = loader.filter_metadata([1])
        assert (one_fold_all_classes
                .fold
                .isin([1])
                .all())
        assert (one_fold_all_classes
                .classID
                .nunique() == 10)

    def test_filter_metadata_two_folds_one_class(self):
        loader = UrbanSound8K(DATADIR)
        two_folds_all_classes = loader.filter_metadata([1, 2])
        assert (two_folds_all_classes
                .fold
                .isin([1, 2])
                .all())
        assert (two_folds_all_classes
                .classID
                .nunique() == 10)

    def test_filter_metadata_all_folds_one_class(self):
        loader = UrbanSound8K(DATADIR)
        # pass int
        all_folds_one_class = loader.filter_metadata(
            range(1, 11),
            classID=1
        )
        assert (all_folds_one_class
                .fold
                .nunique() == 10)
        assert (all_folds_one_class
                .classID
               .isin([1])
                .all())

        # pass list with one int
        all_folds_one_class = loader.filter_metadata(
            range(1, 11),
            classID=[1]
        )
        assert (all_folds_one_class
                .fold
                .nunique() == 10)
        assert (all_folds_one_class
                .classID
                .isin([1])
                .all())

    def test_filter_metadata_all_folds_two_classes(self):
        loader = UrbanSound8K(DATADIR)
        # pass int
        all_folds_two_classes = loader.filter_metadata(
            range(1, 11),
            classID=[1, 2]
        )
        assert (all_folds_two_classes
                .fold
                .nunique() == 10)
        assert (all_folds_two_classes
                .classID
               .isin([1, 2])
                .all())

    def test_samples_from_file(self):
        loader = UrbanSound8K(DATADIR)
        fname, fold = loader.metadata.iloc[0, [0, 2]]
        path = loader.data_root / f'fold{fold}' / fname
        sr, samples = loader.samples_from_file(path)
        assert sr == loader.sample_rate
        assert isinstance(samples, np.ndarray)
