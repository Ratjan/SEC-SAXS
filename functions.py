import numpy as np
import os
import pandas as pd


def merge_frames(DataFolder, filesuffix, start_frame, end_frame):
    merged_I = None
    merged_err2 = None
    q_values = None
    count = 0

    for scan in range(start_frame, end_frame):
        data = np.genfromtxt(f'{DataFolder}/shot_{scan:04d}_{filesuffix}.dat', skip_header=1)

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



def save_stitched(df_stitched, file_eiger, scan):
    # Save stitched data to .dat file

    os.makedirs(f'stitched_output/{scan}_stitched', exist_ok=True)

    #save data from mantid workspace to .dat file
    outfile_name = os.path.basename(file_eiger).split('_eiger')[0]
    df_stitched.to_csv(f'stitched_output/{scan}_stitched/{outfile_name}_stitched.dat', sep='\t', columns=['Q', 'I', 'IError'], index=False, header=True)
    #print(f'Saved: {outfile_name}')

def save_rebin(df_rebinned, file_eiger, scan):
    # Save rebinned data to .dat file

    os.makedirs(f'rebinned_output/{scan}_rebinned', exist_ok=True)

    #save data from mantid workspace to .dat file
    outfile_name = os.path.basename(file_eiger).split('_stitched')[0]
    df_rebinned.to_csv(f'rebinned_output/{scan}_rebinned/{outfile_name}_rebinned.dat', sep='\t', columns=['Q', 'I', 'IError'], index=False, header=True)
    #print(f'Saved: {outfile_name}')


def stitch_data(EigdataFolder, PildataFolder, file_eiger, file_pilatus):

    data_eiger = np.loadtxt(f'{EigdataFolder}/{file_eiger}')

    # Remove rows with zero values in any column
    data_eiger = data_eiger[~np.any(data_eiger == 0, axis=1)]

    # Optionally, handle rows with special characters (e.g., NaN or Inf)
    data_eiger = data_eiger[~np.isnan(data_eiger).any(axis=1)]  # Remove rows with NaN
    data_eiger = data_eiger[~np.isinf(data_eiger).any(axis=1)]  # Remove rows with Inf

    q_values = data_eiger[:, 0]
    intensity_eiger = data_eiger[:, 1]
    I_error_eiger = data_eiger[:, 2]

    # Filter data to include only q values below 0.095, which is around the cutoff where eiger data becomes noisy
    #mask = q_values < 0.1
    
    #q_values = q_values[mask]
    #intensity_eiger = intensity_eiger[mask]
    #I_error_eiger = I_error_eiger[mask]

    df_eig = pd.DataFrame({'Q':q_values,'I': intensity_eiger,'IError': I_error_eiger})

    data_pilatus = np.loadtxt(f'{PildataFolder}/{file_pilatus}')

    # Remove rows with zero values in any column
    data_pilatus = data_pilatus[~np.any(data_pilatus == 0, axis=1)]

    # Optionally, handle rows with special characters (e.g., NaN or Inf)
    data_pilatus = data_pilatus[~np.isnan(data_pilatus).any(axis=1)]  # Remove rows with NaN
    data_pilatus = data_pilatus[~np.isinf(data_pilatus).any(axis=1)]  # Remove rows with Inf
    
    q_values_pilatus = data_pilatus[:, 0]
    intensity_pilatus = data_pilatus[:, 1]
    I_error_pilatus = data_pilatus[:, 2]

    df_pil = pd.DataFrame({'Q':q_values_pilatus,'I': intensity_pilatus,'IError': I_error_pilatus})

    df_stitched = pd.concat([df_eig, df_pil], ignore_index=True)
    df_stitched = df_stitched.sort_values(by='Q').reset_index(drop=True)   
    return df_stitched
        

    

