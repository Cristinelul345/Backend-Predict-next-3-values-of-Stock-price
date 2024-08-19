import os
import glob
import csv
import random
import pandas as pd

# CSV file contains 106 values.
# We need to generate 9 more starting from the random choosen number for each file.
# Than we must estimate the next 3 values.
# Also in excel the numbering strats at 1
# eg: _lse_random_nr = 0  -------------------> it will show number in line 1

_nr_last_elements = 3

# input function to retrive the number of files accesed for each stock exchange


def read_input():
    while 1:
        try:
            input_lse_nr_files = int(
                input("Specify the number of files selected for LSE.(1 or 2): ")
            )
        except:
            print("An exception occurred")

        if input_lse_nr_files == 1:
            print("FLTR.csv file provided")
            break
        elif input_lse_nr_files == 2:
            print("FLTR.csv and GSK.csv are provided.")
            break
        else:
            print("Please select a value from the available options (1 or 2).")

    while 1:
        input_nasdaq_nr_files = int(
            input("Specify the number of files selected for NASDAQ.(1): ")
        )
        if input_nasdaq_nr_files == 1:
            print("TSLA.csv file provided")
            break
        else:
            print("Please select the available option (1).")

    while 1:
        input_nyse_nr_files = int(
            input("Specify the number of files selected for NYSE.(1 or 2): ")
        )
        if input_nyse_nr_files == 1:
            print("ASH.csv file provided")
            break
        elif input_nyse_nr_files == 2:
            print("ASH.csv and NMR.csv are provided.")
            break
        else:
            print("Please select a value from the available options (1 or 2).")

    return input_lse_nr_files, input_nasdaq_nr_files, input_nyse_nr_files


# Function to show 10 data values from the given path(stock->file)


def write_output(i_path, o_path, random_nr):
    output_list = [0] * 10
    aux = 0
    try:
        with open(i_path, "r") as source, open(o_path, "w", newline="") as target:
            reader = csv.reader(source)
            writer = csv.writer(target)

            for i, row in enumerate(reader):
                if random_nr <= i and i <= random_nr + 12:
                    writer.writerow(row)
                    if aux < 10:
                        number = float(row[2])
                        output_list[aux] = number
                        aux += 1

            elem_1, elem_2, elem_3 = estimate_value_3(output_list)

    except FileNotFoundError:
        print("\nError: File path not found.")
        return None
    return elem_1, elem_2, elem_3


def estimate_value_3(array_10):
    max0 = 0
    element_n1 = 0
    for i in array_10:
        if i > max0:
            temp = max0
            max0 = i
            element_n1 = temp
        if i > element_n1 and i != max0:
            element_n1 = i
            
    # Given Logic:
    
    element_n2 = float((array_10[-1] - element_n1) / 2)
    element_n3 = float((element_n1 - element_n2) / 4)
    return element_n1, element_n2, element_n3


def update_last_3_val(file_i_o, n, new_values):
    try:
        # Read the CSV file in DataFrame
        df = pd.read_csv(file_i_o)

        # Update from -3 to -1 the given cells
        # 2 -> we change values on the second column
        for i in range(-n, 0, 1):
            df.iloc[i, 2] = new_values[i]

        # Write the updated DataFrame back in the CSV file
        df.to_csv(file_i_o, index=False, header=False)

    except Exception as e:
        print(f" Error: {e}")


def calculate_array_10(nr_files_lse, nr_files_nyse):

    path_lse_1_input = ".\\stock_price_data_files\\LSE\\FLTR.csv"
    path_lse_1_output = ".\\output\\lse_1.csv"
    _lse1_random_nr = random.randint(0, 93)

    update_last_3_val(
        path_lse_1_output,
        _nr_last_elements,
        list(write_output(path_lse_1_input, path_lse_1_output, _lse1_random_nr)),
    )

    if nr_files_lse == 2:
        path_lse_2_input = ".\\stock_price_data_files\\LSE\\GSK.csv"
        path_lse_2_output = ".\\output\\lse_2.csv"
        _lse2_random_nr = random.randint(0, 93)

        update_last_3_val(
            path_lse_2_output,
            _nr_last_elements,
            list(write_output(path_lse_2_input, path_lse_2_output, _lse2_random_nr)),
        )

    path_nasdaq_input = ".\\stock_price_data_files\\NASDAQ\\TSLA.csv"
    path_nasdaq_output = ".\\output\\nasdaq.csv"
    _nasdaq_random_nr = random.randint(0, 93)

    update_last_3_val(
        path_nasdaq_output,
        _nr_last_elements,
        list(write_output(path_nasdaq_input, path_nasdaq_output, _nasdaq_random_nr)),
    )

    path_nyse_1_input = ".\\stock_price_data_files\\NYSE\\ASH.csv"
    path_nyse_1_output = ".\\output\\nyse_1.csv"
    _nyse1_random_nr = random.randint(0, 93)

    update_last_3_val(
        path_nyse_1_output,
        _nr_last_elements,
        list(write_output(path_nyse_1_input, path_nyse_1_output, _nyse1_random_nr)),
    )

    if nr_files_nyse == 2:
        path_nyse_2_input = ".\\stock_price_data_files\\NYSE\\NMR.csv"
        path_nyse_2_output = ".\\output\\nyse_2.csv"
        _nyse2_random_nr = random.randint(0, 93)

        update_last_3_val(
            path_nyse_2_output,
            _nr_last_elements,
            list(write_output(path_nyse_2_input, path_nyse_2_output, _nyse2_random_nr)),
        )


def cleanup():
    files = glob.glob('.\\output/*')
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print(f" Could not delete file: {f}")


def main():
    cleanup()
    i_lse, i_nasdaq, i_nyse = read_input()
    calculate_array_10(i_lse, i_nyse)
    print("Check the output directory.\n")


if __name__ == "__main__":
    main()