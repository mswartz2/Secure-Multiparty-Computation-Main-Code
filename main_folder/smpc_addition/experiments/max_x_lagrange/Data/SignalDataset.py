from dataclasses import dataclass, field


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