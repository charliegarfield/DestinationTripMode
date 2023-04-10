import pandas as pd
import readline


def main():
    # import data
    df: pd.DataFrame = pd.read_feather("OD_Annual_2021.feather")
    # get two user inputs for the two places to get trips between, including autocompletion from the data using readline
    readline.set_completer(lambda text, state: [x for x in df.origin_zone_name.unique() if x.startswith(text)][state])
    readline.set_completer_delims('\t')
    readline.parse_and_bind('tab: complete')
    place1: str = input("Enter the first place: ")
    place2: str = input("Enter the second place: ")

    # get all trips between two places as inputted by the user
    df = bidirectional_search(df, place1, place2)
    # do calculations from the data
    total_trips = df["annual_total_trips"].sum()
    rail_trips = df["mode_rail"].sum()
    air_trips = df["mode_air"].sum()
    atf_trips = df["mode_atf"].sum()
    vehicle_trips = df["mode_vehicle"].sum()
    # print results
    print("Total trips: " + "{:,}".format(total_trips))
    print("Vehicle share: " + "{:.2%}".format(vehicle_trips/total_trips))
    print("Rail share: " + "{:.2%}".format(rail_trips/total_trips))
    print("Air share: " + "{:.2%}".format(air_trips/total_trips))
    print("ATF share: " + "{:.2%}".format(atf_trips/total_trips))


def bidirectional_search(df: pd.DataFrame, place1: str, place2: str) -> pd.DataFrame:
    return df[((df.origin_zone_name == place1) & (df.destination_zone_name == place2)) | ((df.origin_zone_name == place2) & (df.destination_zone_name == place1))]


if __name__ == "__main__":
    main()
