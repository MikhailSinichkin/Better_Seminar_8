import ui


def read_file(file_num):
    with open(f"db/data{file_num}.txt", "r", encoding="utf-8") as file_object:
        data = file_object.readlines()
    return data


def write_file(file_num, data_list):
    with open(f"db/data{file_num}.txt", "w", encoding="utf-8") as file_object:
        for i in range(len(data_list)):
            line_separator = data_list[i][-1]
            file_object.write(
                line_separator.join(
                    data_list[i][j] for j in range(len(data_list[i]) - 1)
                )
                + "\n"
            )


def get_separator(line):
    separators = [".", ";", ",", "-"]

    for separator in separators:
        if separator in line:
            return separator

    return None


def get_data_list(data):
    data_list = list()
    for line in data:
        separator = get_separator(line)
        if separator is not None:
            line_list = line.rstrip("\n").split(separator)
            line_list.append(separator)
            data_list.append(line_list)
        else:
            data_list.append(line)
    return data_list


def delete_line(file_num, line):
    data = read_file(file_num)
    data_list = get_data_list(data)

    del data_list[line - 1]

    for i in range(line - 1, len(data_list)):
        data_list[i][0] = str(i + 1)

    write_file(file_num, data_list)


def add_to_file(file_num, parameters):
    data = read_file(file_num)
    data_list = get_data_list(data)

    position = "1"
    if data:
        position = str(int(data_list[-1][0]) + 1)

    parameters.insert(0, position)
    data_list.append(parameters)
    write_file(file_num, data_list)


def change_line(file_num, line, parameters):
    data = read_file(file_num)
    data_list = get_data_list(data)

    for i in range(len(parameters)):
        if parameters[i] != "":
            data_list[line - 1][i + 1] = parameters[i]

    write_file(file_num, data_list)


def clear_file(file_num):
    open(f"db/data{file_num}.txt", "w").close()


def clear_all_files():
    for i in range(1, 4):
        clear_file(i)


def print_data():
    for i in range(3):
        print(
            ui.output["underscores"],
            ui.output["print_msg"].format(file_num=i+1),
            sep="\n",
        )
        data = read_file(i + 1)
        if len(data) == 0:
            print(ui.output["empty_file"])
        else:
            data_list = get_data_list(data)
            max_strlen = 0

            for line in data_list:
                for field in line:
                    if len(field) > max_strlen:
                        max_strlen = len(field)

            fields = ui.output["fields"]
            for field in fields:
                print(f"{field:{max_strlen}}", end=" ")
            print("\n" + "=" * max_strlen * len(fields))

            for line in data_list:
                for element in line[:-1]:
                    print(f"{element:{max_strlen}}", end=" ")
                print()
            print("\n")
        ui.loading()
