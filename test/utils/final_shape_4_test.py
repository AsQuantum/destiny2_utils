import random

from src.utils.final_shape_4 import find_min_swaps_path


def generate_random_states(m, n, unique_chars):
    chars = [chr(i) for i in range(65, 65 + unique_chars)]  # Generate A, B, C, etc.
    initial_state = [random.choices(chars, k=n) for _ in range(m)]

    # Flatten the list to shuffle characters
    flat_list = [char for sublist in initial_state for char in sublist]
    random.shuffle(flat_list)

    # Create final_state from shuffled flat_list
    final_state = []
    index = 0
    for _ in range(m):
        final_state.append(flat_list[index:index + n])
        index += n

    return initial_state, final_state


if __name__ == '__main__':
    # Find the minimum swaps path
    # Parameters for random generation
    m = 3  # Number of subarrays
    n = 2  # Length of each subarray
    unique_chars = 5  # Number of unique characters to choose from

    # Generate random initial and final states
    initial_array, final_array = generate_random_states(m, n, unique_chars)
    min_swaps_path = find_min_swaps_path(initial_array, final_array)
    print(f'{initial_array=}, {final_array=}')
    # Print the minimum swaps path
    print("\nshortest path: ")
    if min_swaps_path:
        for step in min_swaps_path:
            print(f"swapping idx={step[0]} chr={step[1]} with idx={step[2]} chr={step[3]}")
    else:
        print('No path found or No need to swap')
