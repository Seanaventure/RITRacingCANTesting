import plotly
import plotly.graph_objs as go


class CANPlot:

    def hist(self, results_file):
        id_dict = {}
        msg_dict = {}
        with open(results_file) as file:
            can_msg_list = file.readlines()
        for msg in can_msg_list:
            msg_split = msg.split()
            if msg_split[0] in id_dict:
                x = id_dict.get(msg_split[0])
                x += 1
                id_dict[msg_split[0]] = x
            if msg_split[1] in msg_dict:
                y = id_dict.get(msg_split[1])
                y += 1
                id_dict[msg_split[1]] = y

    def func_plot(self):

        xMax = 50
        xMin = -50
        yMax = 50
        yMin = -50

        z = []
        for x in range(xMin, xMax):
            zx = []
            for y in range(yMin, yMax):
                zx.append(x*x - y*y)
            z.append(zx)
        trace = go.Surface(
            colorscale='Viridis',
            z=z)
        data = [trace]
        plotly.offline.plot(data)
        print("Done")