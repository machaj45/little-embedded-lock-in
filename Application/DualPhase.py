import math
import statistics
import time


class DualPhase:

    @staticmethod
    def start_pd(gui):
        a = 0
        while len(gui.acquired_data_Y) == 0:
            time.sleep(0.2)
            a = a + 1
            gui.text_to_update_3.put('no data ' + str(a))
        for i in range(0, len(gui.acquired_data_Y)):
            if abs(gui.acquired_data_Y[i]) >= 4096:
                gui.acquired_data_Y[i] = 0
        for i in range(0, len(gui.acquired_data_X)):
            if abs(gui.acquired_data_X[i]) >= 4096:
                gui.acquired_data_X[i] = 0

        my = statistics.mean(gui.acquired_data_Y)
        mx = statistics.mean(gui.acquired_data_X)

        gui.acquired_data_XX = []
        gui.acquired_data_YY = []
        gui.acquired_data_ZZ = []

        for i in range(0, len(gui.acquired_data_Y)):
            gui.acquired_data_YY.append(gui.acquired_data_Y[i] - my)
        for i in range(0, len(gui.acquired_data_X)):
            gui.acquired_data_XX.append(gui.acquired_data_X[i] - mx)
            gui.acquired_data_ZZ.append(gui.acquired_data_X[i] - mx)
        for i in range(0, int(gui.sample_per_period / 4)):
            gui.acquired_data_ZZ.insert(0, 0)

        # remove start for angle accuracy

        del gui.acquired_data_XX[0:int(gui.sample_per_period / 4)]
        del gui.acquired_data_YY[0:int(gui.sample_per_period / 4)]
        del gui.acquired_data_ZZ[0:int(gui.sample_per_period / 4)]
        del gui.acquired_data_XX[len(gui.acquired_data_XX) - gui.sample_per_period:-1]
        del gui.acquired_data_YY[len(gui.acquired_data_YY) - gui.sample_per_period:-1]
        del gui.acquired_data_ZZ[
            len(gui.acquired_data_ZZ) - int(gui.sample_per_period + gui.sample_per_period / 4):-1]

        gui.dut = [d * (3.301 / 4095) for d in gui.acquired_data_YY]
        gui.ref = [r * (3.30 / 4095) for r in gui.acquired_data_XX]
        gui.ref90 = [rd * (3.30 / 4095) for rd in gui.acquired_data_ZZ]

    @staticmethod
    def dual_phase_decomposition(gui, string_for_angle=None, string_for_xy=None):
        DualPhase.start_pd(gui)

        number_of_crossing_pos2neg = gui.crossings_nonzero_pos2neg(gui.ref)

        if len(number_of_crossing_pos2neg) < 2 * int(len(gui.ref) / gui.sample_per_period):
            number_of_crossing_neg2pos = gui.crossings_nonzero_neg2pos(gui.ref)
            min_removed_end = min(number_of_crossing_pos2neg[0], number_of_crossing_neg2pos[0])

            del gui.ref[0:min_removed_end]
            del gui.ref90[0:min_removed_end]
            del gui.dut[0:min_removed_end]

            number_of_crossing_trim_pos2neg = gui.crossings_nonzero_pos2neg(gui.ref)
            number_of_crossing_trim_neg2pos = gui.crossings_nonzero_neg2pos(gui.ref)

            length_of_calculation = 0
            if len(gui.dut) > len(gui.ref):
                length_of_calculation = len(gui.ref)
            if len(gui.dut) < len(gui.ref):
                length_of_calculation = len(gui.dut)
            length_of_ref = length_of_calculation
            if number_of_crossing_pos2neg[0] == min_removed_end:
                length_of_ref = number_of_crossing_trim_pos2neg[-1]
            if number_of_crossing_neg2pos[0] == min_removed_end:
                length_of_ref = number_of_crossing_trim_neg2pos[-1]

            del gui.ref[length_of_ref:-1]
            del gui.ref90[length_of_ref:-1]
            del gui.dut[length_of_ref:-1]

        gui.ref_norm = [r ** 2 for r in gui.ref]
        mrs_norm_ref = math.sqrt(statistics.mean(gui.ref_norm))
        gui.ref_norm = [r / mrs_norm_ref for r in gui.ref]
        gui.ref90_norm = [r ** 2 for r in gui.ref90]
        mrs_norm_ref_90 = math.sqrt(statistics.mean(gui.ref90_norm))
        gui.ref90_norm = [r / mrs_norm_ref_90 for r in gui.ref90]

        del gui.dut[-1]
        del gui.ref[-1]
        del gui.ref90[-1]
        del gui.ref_norm[-1]
        del gui.ref90_norm[-1]

        ref_length = len(gui.ref)
        gui.time_sample = ref_length / gui.sf

        gui.X = []
        gui.Y = []
        gui.Xn = []
        gui.Yn = []

        length_of_calculation = 0
        if len(gui.dut) >= len(gui.ref):
            length_of_calculation = len(gui.ref)
        if len(gui.dut) <= len(gui.ref):
            length_of_calculation = len(gui.dut)
        for i in range(0, length_of_calculation):
            gui.X.append(gui.dut[i] * gui.ref[i])
            gui.Xn.append(gui.dut[i] * gui.ref_norm[i])
        for i in range(0, length_of_calculation):
            gui.Y.append(gui.dut[i] * gui.ref90[i])
            gui.Yn.append(gui.dut[i] * gui.ref90_norm[i])
        mean_x_norm = 0
        mean_y_norm = 0
        gui.number_of_used_samples = length_of_calculation
        if len(gui.X) > 0:
            mean_x = statistics.mean(gui.X)
            mean_y = statistics.mean(gui.Y)
            mean_x_norm = statistics.mean(gui.Xn)
            mean_y_norm = statistics.mean(gui.Yn)
        else:
            mean_x, mean_y = 1, 0

        gui.acquired_data = []
        gui.acquired_data_X = []
        gui.acquired_data_Y = []

        phase_angle = -(180 * (math.atan2(mean_y, mean_x) / math.pi))
        norm_of_vector = math.sqrt(mean_x ** 2 + mean_y ** 2)
        normalized_norm_of_vector = math.sqrt(mean_x_norm ** 2 + mean_y_norm ** 2)

        if norm_of_vector > 0:
            if len(gui.ref) > 0:
                ref_rsm = math.sqrt(statistics.mean([r ** 2 for r in gui.ref]))
            else:
                ref_rsm = 1
            gain = 20 * math.log10((normalized_norm_of_vector / ref_rsm))

            number_of_digits_for_angle = int(abs(math.log10(abs(phase_angle)))) + 4
            string_for_angle = "{:." + str(number_of_digits_for_angle) + "f}"

            number_of_digits_for_gain = int(abs(math.log10(abs(gain)))) + 4
            string_for_gain = "{:." + str(number_of_digits_for_gain) + "f}"

            number_of_digits_for_u2 = int(abs(math.log10(abs(normalized_norm_of_vector)))) + 4
            string_for_u2 = "{:." + str(number_of_digits_for_u2) + "f}"

            number_of_digits_for_xy = int(abs(math.log10(abs(mean_x)))) + 4
            string_for_xy = "{:." + str(number_of_digits_for_xy) + "f}"

            number_of_digits_for_time_sample = int(abs(math.log10(abs(gui.time_sample)))) + 3
            string_for_time_sample = "{:." + str(number_of_digits_for_time_sample) + "f}"
            time_duration_string = string_for_time_sample.format(gui.time_sample)

            gui.text_to_update = "Phase = " + string_for_angle.format(phase_angle) +\
                                 "°,\t Gain = " + string_for_gain.format(gain) + " dB\n" \
                                 "X: " + string_for_xy.format(mean_x) + \
                                 ",\t Y: " + string_for_xy.format(mean_y) + \
                                 "\nU\N{SUBSCRIPT TWO} = " + string_for_u2.format(normalized_norm_of_vector) + " V" + \
                                 ",\t U\N{SUBSCRIPT TWO} / U\N{SUBSCRIPT ONE} = " +\
                                 string_for_u2.format((normalized_norm_of_vector / ref_rsm)) + \
                                 "\nTime duration = {0} s, Number of samples = {1}".format(time_duration_string,
                                                                                           gui.number_of_used_samples)
            gui.Gain.append(gain)
        else:
            gui.text_to_update = "Phase = " + string_for_angle.format(phase_angle) + "° and  gain = -Inf " + \
                                  " dB X: " + string_for_xy.format(mean_x) + " Y: " + string_for_xy.format(mean_y)
            gui.Gain.append(-99)

        gui.Phase.append(phase_angle)
        gui.reader.calculated = True
