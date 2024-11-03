"""
Author : Arun CS
Date : 2024-11-03
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erfc

import channels
import data_processing
import modulations

FREQUENCY = 200
NO_OF_SYMBOLS = 10e5
AMPLITUDE = 1
MODULATION_SCHEME = "all-compare"  # bpsk,qpsk,all-compare
CHANEL_CODING = "none"
CHANNEL = "AWGN"
NUMBER_OF_SAMPLES = 100


# def comapre(_qpsk,_bspk):
def plot_Q_I(txData, x_axis):
    plt.plot(x_axis, np.real(txData[: len(x_axis)]), label="In-Phase Component")
    plt.plot(x_axis, np.imag(txData[: len(x_axis)]), label="Quadrature Component")
    plt.legend()
    plt.title("QPSK Modulated Signal")
    plt.show()


def compare_ber(CHANNEL, EbN0dBs, newSystem):
    bpsk_txData, bpsk_constellations = modulations.bpsk(newSystem)
    qpsk_txData, qpsk_constellations = modulations.qpsk(newSystem)
    newSystem.modulation_scheme = "bpsk"
    newAWGNChannel = channels.Channel(
        CHANNEL, bpsk_txData, _system=newSystem, EbN0dBs=EbN0dBs
    )

    bpsk_rxData = newAWGNChannel.get_rxData()
    bpsk_simulatedBER = newAWGNChannel.get_simulatedBer()
    newSystem.modulation_scheme = "qpsk"
    newAWGNChannel = channels.Channel(
        CHANNEL, qpsk_txData, _system=newSystem, EbN0dBs=EbN0dBs
    )
    qpsk_rxData = newAWGNChannel.get_rxData()
    qpsk_simulatedBER = newAWGNChannel.get_simulatedBer()
    print(bpsk_simulatedBER)
    print(qpsk_simulatedBER)
    plt.semilogy(EbN0dBs, bpsk_simulatedBER, "o-", label="Simulated BER BPSK")
    plt.semilogy(EbN0dBs, qpsk_simulatedBER, "o-", label="Simulated BER QPSK")
    plt.legend(loc="upper right")
    plt.show()


def plot_ber(EbN0dBs, simulatedBER, theoreticalBER, scheme):

    fig, ax = plt.subplots(1, 1)
    ax.semilogy(EbN0dBs, simulatedBER, "o-", label="Simulated BER")
    ax.semilogy(EbN0dBs, theoreticalBER, "o-", label="Theoretical BER")
    ax.set_xlabel("$E_b/N_0(dB)$")
    ax.set_ylabel("BER ($P_b$)")
    ax.set_title(f"Probability of Bit Error for {scheme} over AWGN channel")
    ax.set_xlim(-5, 13)
    ax.grid(True)
    ax.legend()
    plt.show()


if __name__ == "__main__":
    # Set properties like frequency, number of symbols and amplitude
    properties = data_processing.Properties(
        FREQUENCY, NO_OF_SYMBOLS, amplitude=AMPLITUDE
    )

    # Define x_axis

    x_axis = np.linspace(0, 2 * np.pi, NUMBER_OF_SAMPLES)

    # Eb/N0 range in dB for simulation
    EbN0dBs = np.arange(start=-4, stop=13, step=2)

    # Create a new System
    newSystem = data_processing.Communication_System(
        properties, modulation_scheme=MODULATION_SCHEME
    )

    ## Transmission
    if newSystem.get_modulation_scheme() == "bpsk":
        # BPSK Modulated Data
        txData, constellations = modulations.bpsk(newSystem)
        plt.plot(
            x_axis, txData[: len(x_axis)]
        )  # last arg is to match the ploting lengths

        #####  Channel
        # Variable to store EbN0dB

        newAWGNChannel = channels.Channel(
            CHANNEL, txData, _system=newSystem, EbN0dBs=EbN0dBs
        )

        #####  Reciever
        rxData = newAWGNChannel.get_rxData()

        simulatedBER = newAWGNChannel.get_simulatedBer()

        theoreticalBER = 0.5 * erfc(np.sqrt(10 ** (EbN0dBs / 10)))

        plot_ber(EbN0dBs, simulatedBER, theoreticalBER, newSystem.modulation_scheme)
    if newSystem.get_modulation_scheme() == "qpsk":
        txData, constellations = modulations.qpsk(newSystem)

        plot_Q_I(txData, x_axis)

        ##### Channel
        newAWGNChannel = channels.Channel(
            CHANNEL, txData, _system=newSystem, EbN0dBs=EbN0dBs
        )

        ##### Receiver
        rxData = newAWGNChannel.get_rxData()
        simulatedBER = newAWGNChannel.get_simulatedBer()

        # Theoretical BER for QPSK
        theoreticalBER = erfc(np.sqrt(10 ** (EbN0dBs / 10))) * 0.5

        plot_ber(EbN0dBs, simulatedBER, theoreticalBER, newSystem.modulation_scheme)
    if newSystem.get_modulation_scheme() == "all-compare":
        compare_ber(CHANNEL, EbN0dBs, newSystem)
