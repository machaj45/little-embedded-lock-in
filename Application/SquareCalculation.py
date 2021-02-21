import math
import statistics
import time


class SquareCalculation:

    @staticmethod
    def start_rect(gui):
        a = 0
        while len(gui.acquired_data_Y) == 0:
            time.sleep(0.2)
            a = a + 1
            gui.text_to_update_3.put('no data ' + str(a))

        my = statistics.mean(gui.acquired_data_Y)
        mx = 0

        gui.acquired_data_XX = []
        gui.acquired_data_YY = []

        for i in range(0, len(gui.acquired_data_Y)):
            gui.acquired_data_YY.append(gui.acquired_data_Y[i] - my)
        for i in range(0, len(gui.acquired_data_X)):
            gui.acquired_data_XX.append(gui.acquired_data_X[i] - mx)

        del gui.acquired_data_XX[0:int(gui.sample_per_period / 4)]
        del gui.acquired_data_YY[0:int(gui.sample_per_period / 4)]
        del gui.acquired_data_XX[len(gui.acquired_data_XX) - gui.sample_per_period:-1]
        del gui.acquired_data_YY[len(gui.acquired_data_YY) - gui.sample_per_period:-1]

        gui.ref = [r * (3.30 / 4095.0) for r in gui.acquired_data_XX]
        gui.dut = [d * (3.30 / 4095.0) for d in gui.acquired_data_YY]

        del gui.ref[-1]
        del gui.dut[-1]

        ref_length = len(gui.ref)
        gui.time_sample = ref_length / gui.sf
        mx = statistics.mean(gui.ref)
        gui.ref_norm = []
        for i in gui.ref:
            if i > mx:
                gui.ref_norm.append(1)
            if i < mx:
                gui.ref_norm.append(-1)
        gui.number_of_used_samples = len(gui.ref_norm)

    @staticmethod
    def square_calculation(gui):

        SquareCalculation.start_rect(gui)

        gui.X = []

        for i in range(0, len(gui.dut)):
            gui.X.append(gui.dut[i] * gui.ref_norm[i])

        string_for_mean_div_std = ""
        string_for_std = ""
        std_x = 0
        if len(gui.X) > 0:
            mean_x = statistics.mean(gui.X)
            std_x = statistics.stdev(gui.X)
            number_of_digits_for_std = int(abs(math.log10(abs(std_x)))) + 4
            number_of_digits_for_mean = int(abs(math.log10(abs(mean_x)))) + 4
            number_of_digits_for_mean_div_std = int(abs(math.log10(abs(mean_x / std_x))))
            number_of_digits_for_std = max(number_of_digits_for_std, number_of_digits_for_mean)
            number_of_digit_for_ts = int(abs(math.log10(abs(gui.time_sample)))) + 4
            string_for_std = "{:." + str(number_of_digits_for_std) + "f}"
            string_for_mean_div_std = "{:." + str(number_of_digits_for_mean_div_std) + "f}"
            string_for_ts = "{:." + str(number_of_digit_for_ts) + "f}"
            string_for_time_sample = string_for_ts.format(gui.time_sample)
        else:
            mean_x = 1

        gui.acquired_data = []
        gui.acquired_data_X = []
        gui.acquired_data_Y = []

        try:
            gui.text_to_update = "U\N{SUBSCRIPT TWO} = " + string_for_std.format(
                mean_x) + " V," + " sigma =" + " " + string_for_std.format(
                std_x) + " V, " + "U\N{SUBSCRIPT TWO}/sigma= " + string_for_mean_div_std.format(
                20 * math.log10(mean_x / std_x)) + " dB\n" + "Time duration = {0} s, Number of samples = {1}".format(
                string_for_time_sample, gui.number_of_used_samples)
        except ValueError:
            gui.text_to_update = "U\N{SUBSCRIPT TWO} = " + string_for_std.format(
                mean_x) + " V," + " sigma =" + " " + string_for_std.format(
                std_x) + " V \n" + "Time duration = {0} s, Number of samples = {1}".format(string_for_time_sample,
                                                                                           gui.number_of_used_samples)
        gui.Gain.append(string_for_std.format(mean_x))
        # self.Phase.append(string_for_time_sample)
        gui.reader.calculated = True
