import numpy as np


class Channel:

    def __init__(self, channel_name, txData, _system, EbN0dBs):
        self.channel_name = channel_name
        self.txData = txData
        self.EbN0dBs = EbN0dBs
        ber_len = len(EbN0dBs)
        simulatedBer = np.zeros(ber_len)
        if channel_name == "AWGN":
            for j, EbN0dB in enumerate(EbN0dBs):
                noiseGamma = 10 ** (EbN0dB / 10)
                avgPower = np.mean(np.abs(txData) ** 2)
                #     avgPower = sum(abs(txData) ** 2) / len(txData)
                linear_noisePower = avgPower / noiseGamma
                #
                noise_vector = np.sqrt(
                    linear_noisePower / 2
                ) * np.random.standard_normal(txData.shape)
                # Add Noice to the tx data
                noisy_signal = txData + noise_vector
                rxData = noisy_signal >= 0
                rxData = rxData.astype(int)
                sourceData = (txData >= 0).astype(
                    int
                )  # convert the data back to 0 and 1

                simulatedBer[j] = np.sum(rxData != sourceData) / len(txData)
            self.rxData = rxData
            self.simulatedBER = simulatedBer

    def get_rxData(self):
        return self.rxData

    def get_simulatedBer(self):
        return self.simulatedBER
