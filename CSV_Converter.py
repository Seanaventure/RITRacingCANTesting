import csv

#MAKE A CASE FOR THE LAST THING IN THE ARRAY AFTER THE SPLIT SINCE IT HAS \N.


def main():
    csv_file = input('Enter the name of your input file: ')
    txt_file = input('Enter the name of your output file: ')



    with open(txt_file, "w") as fileOutput:
        fileOutput.write("<send>\n")
        with open(csv_file, "r") as fileInput:
            for line in fileInput:
                data1 = line.split(",")
                if(data1[0] == "ECU_IDprim"):
                    data2 = next(fileInput).split(",")
                    oilP = convert_filtered_hex(data1[4], 100)
                    batt = convert_filtered_hex(data2[1], 1000)
                    oilT = convert_filtered_hex(data1[2], 1)
                    waterT = convert_filtered_hex(data1[3], 1)
                    RPM = convert_filtered_hex(data1[1], 1)
                    gear = convert_filtered_hex(data1[5], 1)
                    gear = '0' + gear
                    fileOutput.write("\tSND 090 " + RPM+oilT+waterT+oilP+gear+batt + "\n")
                else:
                #it is a wait statement
                    fileOutput.write("\tdelay=" + data1[1] + "\n")
        fileOutput.write("</send>")
def convert_filtered_hex(data, multi):
    temp = int(float(data)*multi)
    return hex(temp)[2:].upper()

main()