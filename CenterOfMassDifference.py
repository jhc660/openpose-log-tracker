import math

def com_difference(current, previous, threshold):
    cur_cor = [0,0]
    prev_cor = [0,0]
    count = 0

    current_x_values = current[0::3]
    current_y_values = current[1::3]
    current_c_values = current[2::3]

    previous_x_values = previous[0::3]
    previous_y_values = previous[1::3]
    previous_c_values = previous[2::3]

    for x in range(math.floor(len(current)/3)):
        count += current_c_values[x]*previous_c_values[x]
        cur_cor[0] += current_x_values[x] * current_c_values[x] *previous_c_values[x]
        prev_cor[0] += previous_x_values[x] * current_c_values[x] *previous_c_values[x]
        cur_cor[1] += current_y_values[x] * current_c_values[x] *previous_c_values[x]
        prev_cor[1] += previous_y_values[x] * current_c_values[x] *previous_c_values[x]

    if count == 0:
        return threshold
    else:
        cur_cor[0] /= count
        cur_cor[1] /= count
        prev_cor[0] /= count
        prev_cor[1] /= count
        return math.sqrt(math.pow((cur_cor[0]-prev_cor[0]),2)+math.pow((cur_cor[1]-prev_cor[1]),2)) + (threshold*(18-count)/36)  
