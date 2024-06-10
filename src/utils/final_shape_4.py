import re
import copy
import bisect
from colorama import Fore
from collections import deque

def calculate_diff(initial_shape, final_shape):
    diff_state = [dict() for _ in range(len(initial_shape))]
    final_state = [dict() for _ in range(len(initial_shape))]
    for x, direction in enumerate(initial_shape):
        for y, shape in enumerate(direction):
            final_state[x][final_shape[x][y]] = final_state[x].get(final_shape[x][y], 0) + 1
            diff_state[x][shape] = diff_state[x].get(shape, 0) + 1
            diff_state[x][final_shape[x][y]] = diff_state[x].get(final_shape[x][y], 0) - 1
    return diff_state, final_state


def is_diff_equilibrium(diff_state):
    for diff in diff_state:
        if diff.values() and not min(diff.values()) == max(diff.values()) == 0:
            return False
    return True


def find_min_swaps_path(initial_state, final_state):
    # Initialize the BFS queue
    start_diff_state, final_state = calculate_diff(initial_state, final_state)
    queue = deque([([], 0, start_diff_state)])
    visited = set()
    m = len(initial_state)
    n = len(initial_state[0])
    while queue:
        path, old_idx, diff_state = queue.popleft()
        # print('[GET]', path, old_idx, diff_state)
        if is_diff_equilibrium(diff_state):
            return path

        for i in range(old_idx, m):
            i_shape_list = list(diff_state[i].keys())
            i_shape_list.sort(key=lambda shape: diff_state[i][shape])
            i_shape_idx_s = bisect.bisect_left(i_shape_list, 0, key=lambda shape: diff_state[i][shape])
            i_shape_idx_l = bisect.bisect_right(i_shape_list, 0, key=lambda shape: diff_state[i][shape])
            for i_shape in reversed(i_shape_list[i_shape_idx_l:]):
                for j in range(i + 1, m):
                    j_shape_list = list(diff_state[j].keys())
                    j_shape_list.sort(key=lambda shape: diff_state[j][shape])
                    j_shape_idx_s = bisect.bisect_left(j_shape_list, 0, key=lambda shape: diff_state[j][shape])
                    # j_shape_idx_l = bisect.bisect_right(j_shape_list, 0, key=lambda shape: diff_state[j][shape])
                    for j_shape in reversed(j_shape_list[j_shape_idx_s:]):
                        if j_shape not in i_shape_list[:i_shape_idx_s]:
                            continue
                        if diff_state[j][j_shape] + final_state[j].get(j_shape, 0) <= 0:
                            continue
                        new_diff_state = copy.deepcopy(diff_state)
                        new_diff_state[i][i_shape] -= 1
                        new_diff_state[j][j_shape] -= 1
                        new_diff_state[i][j_shape] = new_diff_state[i].get(j_shape, 0) + 1
                        new_diff_state[j][i_shape] = new_diff_state[j].get(i_shape, 0) + 1
                        new_path = path + [(i, i_shape, j, j_shape)]
                        # print('[ADD]', new_path, i, new_diff_state)
                        queue.append((new_path, i, new_diff_state))

    return []


def main():
    print('=' * 75)
    print(
        f'{Fore.LIGHTGREEN_EX}◇ 请输入形状（圆=0，方=4，三角=3）：不带空格，按左中右顺序，内场为3个数字，外场为6个数字{Fore.RESET}')
    interior_shape = input('- 内场雕像（终焉之形）：').strip()
    exterior_shape = input('- 外场雕像（始焉之形）：').strip()
    while re.match(r'^[034]{3,3}$', interior_shape) is None or re.match(r'^[034]{6,6}$', exterior_shape) is None:
        print(
            f'{Fore.LIGHTRED_EX}◇ 输入有误，请重新输入（圆=0，方=4，三角=3）：不带空格，内场为3个数字，外场为6个数字{Fore.RESET}')
        interior_shape = input('- 内场雕像（终焉之形）：').strip()
        exterior_shape = input('- 外场雕像（始焉之形）：').strip()

    all_shape = set('043')
    final_shape = [sorted(list(all_shape - set(ip))) for ip in interior_shape.strip()]
    initial_shape = [sorted(list(exterior_shape[2 * i:2 * (i + 1)])) for i in range(len(exterior_shape) // 2)]

    idx_dir_map = {0: '左', 1: '中', 2: '右'}
    str_shape_map = {'0': '●', '3': '▲', '4': '■'}
    list_3d_shape_map = {'●●': '球', '●▲': '圆锥', '●■': '圆柱', '▲▲': '三棱锥', '▲■': '四棱锥', '■■': '正方体'}
    print(f'{Fore.LIGHTGREEN_EX}◇ 输入图案结果{Fore.RESET}')

    def pattern_converter(any_shape):
        pattern_output_map = map(
            lambda idx: f'{"".join(map(lambda shape: str_shape_map.get(shape, shape), any_shape[idx]))}',
            range(len(any_shape)))
        return pattern_output_map

    print('- 面向方向：\t', '\t'.join(['左', '中', '右']))
    exterior_name = ','.join(map(lambda dir_shape: list_3d_shape_map.get(dir_shape[-2:], dir_shape[-2:]),
                                 pattern_converter(initial_shape)))
    print('- 外场雕像：\t',
          '\t'.join(pattern_converter(initial_shape)), f'\t({exterior_name})')
    print('- 内场玩家：\t', '\t'.join(pattern_converter(final_shape)))

    display_shape = copy.deepcopy(initial_shape)
    # Find the minimum swaps path
    min_swaps_path = find_min_swaps_path(initial_shape, final_shape)

    def display_mode(display_shape, step):
        index_left = display_shape[step[0]].index(step[1])
        index_right = display_shape[step[2]].index(step[3])
        display_shape_mode = copy.deepcopy(display_shape)
        display_shape_mode_res = list(pattern_converter(display_shape_mode))
        display_shape_mode_res[step[0]] = list(display_shape_mode_res[step[0]])
        display_shape_mode_res[step[0]][
            index_left] = f'{Fore.LIGHTBLUE_EX}{display_shape_mode_res[step[0]][index_left]}{Fore.RESET}'
        display_shape_mode_res[step[0]] = ''.join(display_shape_mode_res[step[0]])
        display_shape_mode_res[step[2]] = list(display_shape_mode_res[step[2]])
        display_shape_mode_res[step[2]][
            index_left] = f'{Fore.LIGHTBLUE_EX}{display_shape_mode_res[step[2]][index_left]}{Fore.RESET}'
        display_shape_mode_res[step[2]] = ''.join(display_shape_mode_res[step[2]])
        display_shape[step[0]][index_left] = step[3]
        display_shape[step[2]][index_right] = step[1]
        return display_shape_mode_res

    # Print the minimum swaps path
    print(f"{Fore.LIGHTGREEN_EX}◇ 最短交换步骤{Fore.RESET}")
    print('- P:\t', '\t'.join(list('左中右')))
    print(f'- I:\t{Fore.LIGHTBLACK_EX}', '\t'.join(pattern_converter(initial_shape)), Fore.RESET)
    if min_swaps_path:
        for i, step in enumerate(min_swaps_path):
            print(f'- {Fore.LIGHTRED_EX}{i}{Fore.RESET}:\t', '\t'.join(display_mode(display_shape, step)),
                  f"\t({idx_dir_map[step[0]]}{Fore.LIGHTBLUE_EX}{str_shape_map[step[1]]}{Fore.RESET}"
                  f"{idx_dir_map[step[2]]}{Fore.LIGHTBLUE_EX}{str_shape_map[step[3]]}{Fore.RESET})")
    else:
        print('- E:\t', "找不到路径或无需交换形状。")
    print(f'- F:\t{Fore.LIGHTBLACK_EX}', '\t'.join(pattern_converter(final_shape)), Fore.RESET)


if __name__ == '__main__':
    print('=' * 75)
    print(f'{Fore.LIGHTGREEN_EX}◇ 救赎边缘遭遇战4图案计算最短路径 - By AsQuantum{Fore.RESET}')
    while True:
        main()
