class SquareCalculation:

    @staticmethod
    def square_calculation(gui):
        a = 0
        while len(gui.acquired_data_Y) == 0:
            time.sleep(0.2)
            a = a + 1
            gui.text_to_update = 'no data ' + str(a)

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
        ref_length = len(gui.ref)
        gui.time_sample = ref_length / gui.sf
        mx = statistics.mean(gui.ref)
        a = 0
        for i in gui.ref:
            if i > mx:
                gui.ref[a] = 1
            if i < mx:
                gui.ref[a] = -1
            a = a + 1

            # vaclav.grim@fel.cvut.cz

        gui.X = []
        gui.Y = []
        for i in range(0, len(gui.dut)):
            gui.X.append(gui.dut[i] * gui.ref[i])
        string3 = ""
        string1 = ""
        string = ""
        std_x = 0
        if len(gui.X) > 0:
            mean_x = statistics.mean(gui.X)
            std_x = statistics.stdev(gui.X)
            dist = int(abs(math.log10(abs(std_x)))) + 4
            dist2 = int(abs(math.log10(abs(mean_x)))) + 4
            dist3 = int(abs(math.log10(abs(mean_x / std_x))))
            dist = max(dist, dist2)
            string = "{:." + str(dist) + "f}"
            string1 = "{:." + str(dist3) + "f}"
            dist4 = int(abs(math.log10(abs(gui.time_sample)))) + 4
            string3 = "{:." + str(dist4) + "f}"

        else:
            mean_x = 1
        gui.acquired_data = []
        gui.acquired_data_X = []
        gui.acquired_data_Y = []
        string_for_time_sample = string3.format(gui.time_sample)
        try:
            gui.text_to_update = "U\N{SUBSCRIPT TWO} = " + string.format(
                mean_x) + " V," + " sigma =" + " " + string.format(
                std_x) + " V, " + "U\N{SUBSCRIPT TWO}/sigma= " + string1.format(
                20 * math.log10(mean_x / std_x)) + " dB\n" + "Time duration = {0} s".format(string_for_time_sample)
        except ValueError:
            gui.text_to_update = "U\N{SUBSCRIPT TWO} = " + string.format(
                mean_x) + " V," + " sigma =" + " " + string.format(
                std_x) + " V \n" + "Time duration = {0} s".format(string_for_time_sample)
        gui.Gain.append(string.format(mean_x))
        # self.Phase.append(string_for_time_sample)
        gui.reader.calculated = True