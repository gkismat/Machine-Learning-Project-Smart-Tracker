from scipy.fft import rfft, rfftfreq
import numpy as np

class FourierTransformation:
    def find_fft_transformation(self, data):
        transformation = rfft(data)
        return np.abs(transformation)

    def abstract_frequency(self, data_table, cols, window_size, sampling_rate):
        freqs = rfftfreq(window_size, d=1/sampling_rate)
        print(f"Generated Frequency Bins: {freqs}")

        for col in cols:
            data_table[col + "_max_freq"] = np.nan
            data_table[col + "_freq_weighted"] = np.nan
            data_table[col + "_pse"] = np.nan

            for freq in freqs:
                if np.isclose(freq, 1.429, atol=0.01) or np.isclose(freq, 2.5, atol=0.01):
                    data_table[col + f"_freq_{freq:.3f}_Hz_ws_{window_size}"] = np.nan

        for i in range(window_size, len(data_table.index)):
            for col in cols:
                data = data_table[col].iloc[i - window_size: i].values
                if len(data) != window_size or np.any(np.isnan(data)) or np.any(np.isinf(data)):
                    continue

                real_ampl = self.find_fft_transformation(data)
                if len(real_ampl) > len(freqs):
                    real_ampl = real_ampl[:len(freqs)]

                for j, freq in enumerate(freqs):
                    if np.isclose(freq, 1.429, atol=0.01) or np.isclose(freq, 2.5, atol=0.01):
                        data_table.loc[i, col + f"_freq_{freq:.3f}_Hz_ws_{window_size}"] = real_ampl[j]

                data_table.loc[i, col + "_max_freq"] = freqs[np.argmax(real_ampl)]
                data_table.loc[i, col + "_freq_weighted"] = np.sum(freqs * real_ampl) / np.sum(real_ampl)
                PSD = np.square(real_ampl) / len(real_ampl)
                PSD_pdf = PSD / np.sum(PSD)
                PSD_pdf = PSD_pdf + 1e-12  # Avoid log(0)
                data_table.loc[i, col + "_pse"] = -np.sum(np.log(PSD_pdf) * PSD_pdf)

        return data_table
