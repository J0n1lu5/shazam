import uuid
import numpy as np
import settings
from pydub import AudioSegment
from scipy.signal import spectrogram
from scipy.ndimage import maximum_filter


class AudioFingerprinter:
    def __init__(self):
        pass

    def _my_spectrogram(self, audio):
        nperseg = int(settings.SAMPLE_RATE * settings.FFT_WINDOW_SIZE)
        return spectrogram(audio, settings.SAMPLE_RATE, nperseg=nperseg)
    
    def _find_peaks(self, Sxx):
        """Finds peaks in a spectrogram."""
        data_max = maximum_filter(Sxx, size=settings.PEAK_BOX_SIZE, mode='constant', cval=0.0)
        peak_goodmask = (Sxx == data_max)  # good pixels are True
        y_peaks, x_peaks = peak_goodmask.nonzero()
        peak_values = Sxx[y_peaks, x_peaks]
        i = peak_values.argsort()[::-1]
        # get co-ordinates into arr
        j = [(y_peaks[idx], x_peaks[idx]) for idx in i]
        total = Sxx.shape[0] * Sxx.shape[1]
        # in a square with a perfectly spaced grid, we could fit area / PEAK_BOX_SIZE^2 points
        # use point efficiency to reduce this, since it won't be perfectly spaced
        # accuracy vs speed tradeoff
        peak_target = int((total / (settings.PEAK_BOX_SIZE**2)) * settings.POINT_EFFICIENCY)
        return j[:peak_target]

    def _idxs_to_tf_pairs(self, idxs, t, f):
        """Helper function to convert time/frequency indices into values."""
        return np.array([(f[i[0]], t[i[1]]) for i in idxs])

    def _hash_point_pair(self, p1, p2):
        """Helper function to generate a hash from two time/frequency points."""
        return hash((p1[0], p2[0], p2[1]-p2[1]))

    def _target_zone(self, anchor, points, width, height, t):
        """Generates a target zone as described in the Shazam paper."""
        x_min = anchor[1] + t
        x_max = x_min + width
        y_min = anchor[0] - (height*0.5)
        y_max = y_min + height
        for point in points:
            if point[0] < y_min or point[0] > y_max:
                continue
            if point[1] < x_min or point[1] > x_max:
                continue
            yield point

    def _hash_points(self, points, filename):
        """Generates all hashes for a list of peaks."""
        hashes = []
        song_id = uuid.uuid5(uuid.NAMESPACE_OID, filename).int
        for anchor in points:
            for target in self._target_zone(
                anchor, points, settings.TARGET_T, settings.TARGET_F, settings.TARGET_START
            ):
                hashes.append((
                    # hash
                    self._hash_point_pair(anchor, target),
                    # time offset
                    anchor[1],
                    # filename
                    str(song_id)
                ))
        return hashes

    def fingerprint_file(self, filename):
        """Generate hashes for a file."""
        f, t, Sxx = self._file_to_spectrogram(filename)
        peaks = self._find_peaks(Sxx)
        peaks = self._idxs_to_tf_pairs(peaks, t, f)
        return self._hash_points(peaks, filename)

    def fingerprint_audio(self, frames):
        """Generate hashes for a series of audio frames."""
        f, t, Sxx = self._my_spectrogram(frames)
        peaks = self._find_peaks(Sxx)
        peaks = self._idxs_to_tf_pairs(peaks, t, f)
        return self._hash_points(peaks, "recorded")

    def _file_to_spectrogram(self, filename):
        """Calculates the spectrogram of a file."""
        a = AudioSegment.from_file(filename).set_channels(1).set_frame_rate(settings.SAMPLE_RATE)
        audio = np.frombuffer(a.raw_data, np.int16)
        return self._my_spectrogram(audio)