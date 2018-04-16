import utils


def reparse_file(path):

    file = open(path,"r")
    write = open("../datas/video_graph/ssim_v.txt", "w+")

    lines = file.readlines()
    for line in lines:
        split = line.split(" ")
        v_num1 = utils.get_video_brand(split[0],1)
        v_num2 = utils.get_video_brand(split[1],1)
        weigth = line.find("{")

        """
        # find weigth value
        pos = line[weigth:].find(" ")
        weigth_value = line[weigth+pos+1:weigth+pos+4]
        print(weigth_value)

        newline = v_num1 + " " + v_num2 + " " + line[weigth:]
        if float(weigth_value) > 0.8:
            write.write(newline)
        """
        newline = v_num1 + " " + v_num2 + " " + line[weigth:]
        write.write(newline)


    write.close()