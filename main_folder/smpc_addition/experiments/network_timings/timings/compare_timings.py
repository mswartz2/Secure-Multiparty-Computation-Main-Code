import pandas as pd


def run():
    folder = "main_folder//smpc_addition//experiments//network_timings//timings//"
    df_traditional = pd.read_csv(f"{folder}timing_results_traditional.csv")
    df_secure = pd.read_csv(f"{folder}timing_results_secure.csv")

    df_traditional_results = pd.DataFrame()
    df_secure_results = pd.DataFrame()

    # get traditional results stats
    df_traditional_results["client_setup_time"] = (
        df_traditional["initial_network_connection_finished"]
        - df_traditional["start_time"]
    )
    df_traditional_results["client_to_server_networking"] = (
        df_traditional["server_computation_start_time"]
        - df_traditional["initial_network_connection_finished"]
    )
    df_traditional_results["server_comp_time"] = (
        df_traditional["server_computation_end_time"]
        - df_traditional["server_computation_start_time"]
    )
    df_traditional_results["server_to_client_networking"] = (
        df_traditional["client_received_time"] - df_traditional["server_sent_data_time"]
    )
    df_traditional_results["client_comp_time"] = 0
    df_traditional_results["total_time"] = (
        df_traditional["client_received_time"] - df_traditional["start_time"]
    )

    # get secure results stats
    df_secure_results["client_setup_time"] = (
        df_secure["initial_network_connection_finished"] - df_secure["start_time"]
    )
    df_secure_results["client_to_server_networking"] = (
        df_secure["server_computation_start_time"]
        - df_secure["client_setup_finished_time"]
    )
    df_secure_results["server_comp_time"] = (
        df_secure["server_computation_end_time"]
        - df_secure["server_computation_start_time"]
    )
    df_secure_results["server_to_client_networking"] = (
        df_secure["client_received_time"] - df_secure["server_sent_data_time"]
    )
    df_secure_results["client_comp_time"] = (
        df_secure["client_computation_finish_time"] - df_secure["client_received_time"]
    )
    df_secure_results["total_time"] = (
        df_secure["client_computation_finish_time"] - df_secure["start_time"]
    )

    # get time in ms
    df_traditional_results = df_traditional_results.mean() * 1000
    df_secure_results = df_secure_results.mean() * 1000

    print("\nTraditional")
    print(df_traditional_results)
    print("\nSecure")
    print(df_secure_results)


run()
