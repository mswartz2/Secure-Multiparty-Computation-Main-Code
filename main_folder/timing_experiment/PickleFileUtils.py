import pickle
import os
import bz2
from dataclasses import dataclass, field

# from ecgPreprocessedData import Data


def write_to_pickle_file(data, filename):
    # make directory two levels higher
    if not os.path.exists(os.path.dirname(os.path.dirname(filename))):
        os.makedirs(os.path.dirname(os.path.dirname(filename)))

    # make directory one level higher
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    pickle_file = bz2.BZ2File(filename, "wb")
    pickle.dump(data, pickle_file)
    pickle_file.close()


def read_in_pickle_file(filename):
    with bz2.BZ2File(filename, "rb") as myfile:
        data_loaded = pickle.load(myfile)

    return data_loaded


@dataclass
class SignalDataset:
    # data: list = field(default_factory=list)
    # labels: list = field(default_factory=list)
    # patient_ids: list = field(default_factory=list)

    def __init__(self, data, labels, patient_ids):
        self.data = data
        self.labels = labels
        self.patient_ids = patient_ids

    def __add__(self, otherSignalDataset):
        combined_data = self.data + otherSignalDataset.data
        combined_labels = self.labels + otherSignalDataset.labels
        combined_patient_ids = self.patient_ids + otherSignalDataset.patient_ids
        return SignalDataset(combined_data, combined_labels, combined_patient_ids)

    def __len__(self):
        return len(self.patient_ids)

    def getRecord(self, id):
        return self.data[id], self.labels[id], self.patient_ids[id]
