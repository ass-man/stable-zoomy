# i have no idea what im doings

#%%
import librosa
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
# %%
y, sr = librosa.load(r"C:\Users\santt\Videos\Kemuri.mp3")
hop_length = 512

frame_length = 512
framerate = 15
# %%
onset_env = librosa.onset.onset_strength(y=y, sr=sr,
                                         aggregate=np.median)
tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env,
                                       sr=sr)
fig, ax = plt.subplots(nrows=2, sharex=True)
times = librosa.times_like(onset_env, sr=sr, hop_length=hop_length)

M = librosa.feature.melspectrogram(y=y, sr=sr, hop_length=hop_length)
librosa.display.specshow(librosa.power_to_db(M, ref=np.max),
                         y_axis='mel', x_axis='time', hop_length=hop_length,
                         ax=ax[0])
ax[0].label_outer()
ax[0].set(title='Mel spectrogram')
ax[1].plot(times, librosa.util.normalize(onset_env),
         label='Onset strength')
ax[1].vlines(times[beats], 0, 1, alpha=0.5, color='r',
           linestyle='--', label='Beats')
ax[1].legend()



# %%

onset_strength = librosa.util.normalize(onset_env)

key_frames = []
diffs = []

def getOnset(index):
    return onset_strength[index]


for i in beats:
    cur_keyframe = np.floor(framerate * times[i])
    key_frames.append([cur_keyframe,times[i],getOnset(i)])

for i in range(1,len(key_frames)):
    diffs.append(key_frames[i][0] - key_frames[i-1][0])

avg_diff = np.floor(np.average(diffs))
zoom_keyframe_length = np.floor(avg_diff / 2)
print("tempo", tempo)
print(avg_diff,zoom_keyframe_length)

frame_offset = 0 
frame_extra_len = 1
zoom_str = 1.13
dezoom_str = 1

def getFrames(key_frames):
    zoom_frames = []
    for frame in key_frames:
        zoom_start_frame = int(frame[0] - frame_offset)
        zoom_end_frame = int(zoom_start_frame + zoom_keyframe_length + frame_extra_len)
        if(zoom_start_frame > 0):
            zoom_frames.append([zoom_start_frame,zoom_end_frame])
    return zoom_frames

def getZoomString(key_frames):

    output = ""
    for i,frame in enumerate(getFrames(key_frames)):
        zs = round(1 +  (0.2 * key_frames[i][2]),2)
        dzs = round(1 -  (0.1 * key_frames[i][2] / 3),2)
        output += f"{frame[0]}:({zs}),"
        output += f"{frame[1]}:({dzs}),"
    output = output.strip(',')
    return output


def getZ_translationString(key_frames):

    output = ""
    for i,frame in enumerate(getFrames(key_frames)):
        zs = round(3 +  (2 * key_frames[i][2]),2)
        dzs = round(-1 -  (1 * key_frames[i][2]),2)
        output += f"{frame[0]}:({zs}),"
        output += f"{frame[1]}:({dzs}),"
    output = output.strip(',')
    return output

def getX_tranlationString(key_frames):
    output = ""
    do_nothing = 0
    x_left = -2
    x_right = 2
    for i,frame in enumerate(getFrames(key_frames)):
        output += f"{frame[0]}:({do_nothing}),"
        if(i%2 == 0):
            val = round(1 + (x_right * key_frames[i][2]),2)
            output += f"{frame[1]}:({val}),"
        else:
            val = round(-1 + (x_left * key_frames[i][2]),2)
            output += f"{frame[1]}:({val}),"
    output = output.strip(',')
    return output

def getY_tranlationString(key_frames):
    output = ""
    do_nothing = 0
    z_back = -1
    z_front = 2
    for i,frame in enumerate(getFrames(key_frames)):
        output += f"{frame[0]}:({do_nothing}),"
        if(i%2 != 0):
            val = round(z_front + (z_front * key_frames[i][2]),2)
            output += f"{frame[1]}:({val}),"
        else:
            val = round(z_back + (z_back * key_frames[i][2]),2)
            output += f"{frame[1]}:({val}),"
    output = output.strip(',')
    return output


print(getZoomString(key_frames),"\n")
print(getX_tranlationString(key_frames),"\n")

print(getY_tranlationString(key_frames),"\n")
print(getZ_translationString(key_frames),"\n")




# %%
