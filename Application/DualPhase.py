import math
import statistics
import time


class DualPhase:

    @staticmethod
    def dual_phase_decomposition(gui, strings=None, string_for_xy=None):
        a = 0
        while len(gui.acquired_data_Y) == 0:
            time.sleep(0.2)
            a = a + 1
            gui.text_to_update = 'no data ' + str(a)
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

        gui.dut = [d * (3.30 / 4095) for d in gui.acquired_data_YY]
        gui.ref = [r * (3.30 / 4095) for r in gui.acquired_data_XX]
        gui.ref90 = [rd * (3.30 / 4095) for rd in gui.acquired_data_ZZ]

        aa = gui.crossings_nonzero_pos2neg(gui.ref)
        if len(aa) < 2 * int(len(gui.ref) / gui.sample_per_period):
            ba = gui.crossings_nonzero_neg2pos(gui.ref)
            min_removed_end = min(aa[0], ba[0])
            del gui.ref[0:min_removed_end]
            del gui.ref90[0:min_removed_end]
            del gui.dut[0:min_removed_end]

            a = gui.crossings_nonzero_pos2neg(gui.ref)
            b = gui.crossings_nonzero_neg2pos(gui.ref)

            length_of_calculation = 0
            if len(gui.dut) > len(gui.ref):
                length_of_calculation = len(gui.ref)
            if len(gui.dut) < len(gui.ref):
                length_of_calculation = len(gui.dut)
            length_of_ref = length_of_calculation
            if aa[0] == min_removed_end:
                length_of_ref = a[-1]
            if ba[0] == min_removed_end:
                length_of_ref = b[-1]

            del gui.ref[length_of_ref:-1]
            del gui.ref90[length_of_ref:-1]
            del gui.dut[length_of_ref:-1]

        gui.ref_norm = [r ** 2 for r in gui.ref]
        mrs_norm_ref = math.sqrt(statistics.mean(gui.ref_norm))
        gui.ref_norm = [r / mrs_norm_ref for r in gui.ref]

        gui.ref90n = [r ** 2 for r in gui.ref90]
        mrs_norm_ref_90 = math.sqrt(statistics.mean(gui.ref90n))
        gui.ref90n = [r / mrs_norm_ref_90 for r in gui.ref90]

        del gui.ref[-1]
        del gui.ref90[-1]
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
            gui.Yn.append(gui.dut[i] * gui.ref90n[i])
        mean_x_norm = 0
        mean_y_norm = 0
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
        sa = -(180 * (math.atan2(mean_y, mean_x) / math.pi))
        dist = math.sqrt(mean_x ** 2 + mean_y ** 2)
        dist_norm = math.sqrt(mean_x_norm ** 2 + mean_y_norm ** 2)
        input_gain = 1
        if dist > 0:
            if len(gui.ref) > 0:
                input_gain = math.sqrt(statistics.mean([r ** 2 for r in gui.ref]))
            else:
                input_gain = 1
            sb = 20 * math.log10((dist_norm / input_gain))
            dists = int(abs(math.log10(abs(dist_norm)))) + 4
            string = "{:." + str(dists) + "f}"
            sas = int(abs(math.log10(abs(sa)))) + 4
            strings = "{:." + str(sas) + "f}"
            sbs = int(abs(math.log10(abs(sb)))) + 4
            string_bs = "{:." + str(sbs) + "f}"
            sxs = int(abs(math.log10(abs(mean_x)))) + 4
            string_for_xy = "{:." + str(sxs) + "f}"
            dist4 = int(abs(math.log10(abs(gui.time_sample)))) + 4
            string3 = "{:." + str(dist4) + "f}"
            time_duration_string = string3.format(gui.time_sample)
            gui.text_to_update = "Phase = " + strings.format(sa) + "° and  gain = " + string_bs.format(
                sb) + " dB,\nX: " + string_for_xy.format(mean_x) + " Y: " + string_for_xy.format(
                mean_y) + " U\N{SUBSCRIPT TWO} = " + string.format(
                dist) + " V" + " U\N{SUBSCRIPT TWO} / U\N{SUBSCRIPT ONE} = " + string.format(
                (dist_norm / input_gain)) + " " + "\nTime duration = {0} s".format(time_duration_string)
            gui.Gain.append(sb)
        else:
            gui.text_to_update = "Phase = " + strings.format(sa) + "° and  gain = -Inf " + \
                                  " dB X: " + string_for_xy.format(mean_x) + " Y: " + string_for_xy.format(mean_y)
            gui.Gain.append(-99)

        gui.Phase.append(sa)
        gui.reader.calculated = True
