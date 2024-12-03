"""
PIRK Protocol
--
Measurement specific functions.
"""

def get_pirk_slices_and_intensities (index, info, protocol_label = 'PIRK', pirk_led = 'PIRK'):

    """
    Return a list of intensities and start:stop indexes for subtraces during PIRK pulses, 
    i.e. where the PIRK intensity > 0.

    :param index: 
    :param info: 
    :param protocol_label: protocol label name (default: PIRK)
    :param pirk_led: pirk led label name (default: PIRK)
    :returns: PIRK_intensities, PIRK_slices
    :rtype: list[dict]
    """

    pulse_sequences = get_pulse_sequences(protocol_label, info)

    actinic_intensities = get_actinic_intensities(protocol_label, index, info)

    prev_intensity = 0 # should be the PAR in the pre_illumination

    # Set up arrays to hold the beginning and end of the PIRK subtraces
    PIRK_end_indexes = []
    PIRK_intensities = []
    for i, current_intensity in enumerate(actinic_intensities[pirk_led]):
        if (current_intensity == 0) and (prev_intensity > 0):
            PIRK_end_indexes.append(i)
            PIRK_intensities.append(prev_intensity)
        prev_intensity = current_intensity

    # Make a list of 
    PIRK_slices = [[pulse_sequences[2][i], pulse_sequences[2][i+1]] for i in PIRK_end_indexes]

    return PIRK_intensities, PIRK_slices

