import matplotlib.pyplot as plt
import warnings
import numpy as np
import seaborn as sns
import pandas as pd

plt.style.use('seaborn')
plt.rcParams['figure.figsize'] = [16, 9]
plt.rcParams['figure.dpi'] = 200
warnings.simplefilter(action='ignore', category=FutureWarning)


"""
# Data generated as follows

if __name__ == "__main__":

    Params.NUM_TIMESTEPS = 175
    Settings.RANDOM_SEED = None
    Settings.DRAW_GRAPH = False

    deaths_with = []
    deaths_without = []
    peak_isolation_timestep_with = []
    peak_isolation_timestep_without = []

    for _ in range(1):
        Params.PRODUCT_IN_USE = True
        m = run()
        deaths_with.append(m.data_handler.get_death_data()[-1])
        iso_data = m.data_handler.get_isolated_data()
        peak_isolation_timestep_with.append(
            iso_data.index(max(iso_data))
        )

        Params.PRODUCT_IN_USE = False
        m = run()
        deaths_without.append(m.data_handler.get_death_data()[-1])
        iso_data = m.data_handler.get_isolated_data()
        peak_isolation_timestep_without.append(
            iso_data.index(max(iso_data))
        )

    print("Deaths with:", deaths_with)
    print("Deaths without:", deaths_without)

    print("Peak isolation time with:", peak_isolation_timestep_with)
    print("Peak isolation time without:", peak_isolation_timestep_without)

    '''
    Deaths with:
    [2256, 2321, 2255, 2311, 2309, 2354, 2401, 2312, 2354, 2371, 2266, 2353, 2352, 2322, 2289, 2332, 2398, 2311, 2288, 2302, 2318, 2384, 2282, 2273, 2283, 2315, 2383, 2314, 2331, 2273, 2298, 2328, 2297, 2296, 2313, 2318, 2303, 2277, 2321, 2270, 2326, 2298, 2307, 2405, 2252, 2345, 2324, 2361, 2320, 2361]
    Deaths without:
    [2660, 2542, 2508, 2609, 2563, 2530, 2546, 2535, 2544, 2551, 2574, 2612, 2560, 2566, 2495, 2612, 2554, 2629, 2623, 2589, 2586, 2508, 2563, 2536, 2487, 2583, 2590, 2609, 2583, 2557, 2666, 2586, 2511, 2599, 2597, 2517, 2610, 2574, 2626, 2640, 2572, 2626, 2546, 2651, 2527, 2520, 2593, 2561, 2605, 2620]
    Peak isolation time with:
    [60, 62, 56, 64, 62, 64, 60, 58, 63, 62, 54, 65, 62, 74, 64, 54, 68, 59, 59, 61, 74, 61, 58, 77, 61, 64, 66, 66, 62, 65, 69, 65, 67, 56, 60, 64, 58, 63, 56, 63, 60, 10, 58, 58, 59, 59, 60, 65, 57, 54]
    Peak isolation time without:
    [66, 73, 59, 78, 59, 60, 64, 80, 62, 61, 61, 66, 62, 66, 72, 61, 69, 66, 72, 60, 73, 63, 61, 59, 63, 59, 63, 87, 59, 69, 73, 69, 63, 65, 62, 60, 60, 69, 65, 72, 61, 59, 69, 62, 59, 60, 59, 60, 71, 62]
    '''
"""



def deaths_comparison(with_product, without_product):
    fig, ax = plt.subplots(2, 1, sharex=True)
    fig.suptitle("Violin plot comparing the number of deaths with and without the product in use")
    plt.xlabel('Number of deaths')

    sns.violinplot(with_product, ax=ax[0])
    ax[0].set_title('With product')

    sns.violinplot(without_product, ax=ax[1])
    ax[1].set_title('Without product')

    plt.show()


with_product = np.array([2256, 2321, 2255, 2311, 2309, 2354, 2401, 2312, 2354, 2371, 2266, 2353, 2352, 2322, 2289, 2332, 2398, 2311, 2288, 2302, 2318, 2384, 2282, 2273, 2283, 2315, 2383, 2314, 2331, 2273, 2298, 2328, 2297, 2296, 2313, 2318, 2303, 2277, 2321, 2270, 2326, 2298, 2307, 2405, 2252, 2345, 2324, 2361, 2320, 2361])
without_product = np.array([2660, 2542, 2508, 2609, 2563, 2530, 2546, 2535, 2544, 2551, 2574, 2612, 2560, 2566, 2495, 2612, 2554, 2629, 2623, 2589, 2586, 2508, 2563, 2536, 2487, 2583, 2590, 2609, 2583, 2557, 2666, 2586, 2511, 2599, 2597, 2517, 2610, 2574, 2626, 2640, 2572, 2626, 2546, 2651, 2527, 2520, 2593, 2561, 2605, 2620])
deaths_comparison(with_product, without_product)
