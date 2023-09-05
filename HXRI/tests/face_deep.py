from deepface import DeepFace

import time

# get the start time
st = time.time()

DeepFace.stream(source=0, time_threshold=1, frame_threshold=1)

et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
print (obj)