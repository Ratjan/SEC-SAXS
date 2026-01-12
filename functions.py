import numpy as np
import os

def merge_frames(DataFolder, start_frame, end_frame):
    merged_I = None
    merged_err2 = None
    q_values = None
    count = 0

    for scan in range(start_frame, end_frame):
        data = np.loadtxt(f'{DataFolder}/shot_{scan:04d}_eiger.dat')

        q = data[:, 0]
        I = data[:, 1]
        err = data[:, 2]

        if merged_I is None:
            q_values = q
            merged_I = np.zeros_like(I)
            merged_err2 = np.zeros_like(err)

        merged_I += I
        merged_err2 += err**2
        count += 1

    merged_I /= count
    merged_err = np.sqrt(merged_err2) / count

    return q_values, merged_I, merged_err, count


def save_data (scan, item_name, start_frame, end_frame, q_values, intensity_values, propagated_err):
    # Save the mean intensity and propagated error to a file


    # Ensure the directory exists
    os.makedirs(f'Output', exist_ok=True)
    try:
        np.savetxt(
            f'Output/{scan}_{item_name}_{start_frame:04d}_{end_frame:04d}.dat',
            np.column_stack((q_values, intensity_values, propagated_err)),
            header="q intensity propagated_error"
        )
        print(f"Data saved for {item_name} at shots {start_frame:04d} to {end_frame:04d} at Output/{scan}_{item_name}_{start_frame:04d}_{end_frame:04d}.dat")
    except Exception as e:
        print(f"Error saving file for {item_name} at shots {start_frame:04d} to {end_frame:04d}: {e}")