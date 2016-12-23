import numpy as np
import wave
import struct

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

############################## Initialize ##################################


# Some Useful Variables
window_size = 2205    # Size of window to be used for detecting silence
beta = 1   # Silence detection parameter
max_notes = 100    # Maximum number of notes in file, for efficiency
sampling_freq = 44100	# Sampling frequency of audio signal
threshold = 600
array = [1046.50, 1174.66, 1318.51, 1396.91, 1567.98, 1760.00, 1975.53,
         2093.00, 2349.32, 2637.02, 2793.83, 3135.96, 3520.00, 3951.07,
         4186.01, 4698.63, 5274.04, 5587.65, 6271.93, 7040.00, 7902.13]

notes = ['C6', 'D6', 'E6', 'F6', 'G6', 'A6', 'B6',
         'C7', 'D7', 'E7', 'F7', 'G7', 'A7', 'B7',
         'C8', 'D8', 'E8', 'F8', 'G8', 'A8', 'B8']
Identified_Notes = []

############################## Read Audio File #############################
print ('\n\nReading Audio File...')

sound_file = wave.open('Audio_1.wav', 'r')
file_length = sound_file.getnframes()

sound = np.zeros(file_length)
mean_square = []
sound_square = np.zeros(file_length)
for i in range(file_length):
    data = sound_file.readframes(1)
    data = struct.unpack("<h", data)
    sound[i] = int(data[0])
    
sound = np.divide(sound, float(2**15))	# Normalize data in range -1 to 1


######################### DETECTING SCILENCE ##################################

sound_square = np.square(sound)
frequency = []
dft = []
i = 0
j = 0
k = 0    
# traversing sound_square array with a fixed window_size
while(i<=len(sound_square)-window_size):
	s = 0.0
	j = 0
	while(j<=window_size):
		s = s + sound_square[i+j]
		j = j + 1	
# detecting the silence waves
	if s < threshold:
		if(i-k>window_size*4):
			dft = np.array(dft) # applying fourier transform function
			dft = np.fft.fft(sound[k:i])
			dft=np.argsort(dft)

			if(dft[0]>dft[-1] and dft[1]>dft[-1]):
				i_max = dft[-1]
			elif(dft[1]>dft[0] and dft[-1]>dft[0]):
				i_max = dft[0]
			else :	
				i_max = dft[1]
# claculating frequency				
			frequency.append((i_max*sampling_freq)/(i-k))
			dft = []
			k = i+1
	i = i + window_size

print('length',len(frequency))
print("frequency")   

for i in frequency :
	print(i)
	idx = (np.abs(array-i)).argmin()
	Identified_Notes.append(notes[idx])
print(Identified_Notes)






