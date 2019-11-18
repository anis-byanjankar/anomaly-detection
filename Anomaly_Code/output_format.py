from estimate_velocity import *
from anomaly_treec import *

def output(tiles, imgs, t, n, size):
    '''Input: tiles: list with tile coordinates
              imgs: frames RGB values
              t: number of trees to fit
              n: subsamle size
              size: tile size
       Output: anomaly scores, anomaly frames and velocity
    '''
    scores = []
    anomaly = []
    for i in range(len(tiles)):
        tile = tiles[i]
        result = anomaly_frames(imgs,t,n,tile)
        index = []
        for j in range(len(result)):
            if result[j] > 0.75:
                index.append(j)
        scores.append(result)
        anomaly.append(index)
    scores = np.array(scores) > 0.75
    scores = list(zip(*scores))
    v1 = velocity(anomaly[0:(len(anomaly) // 2)], size)
    v2 = velocity(anomaly[(len(anomaly) // 2):len(anomaly)], size)
    v = sorted(v1 + v2)
    v.append([len(imgs), v[-1][1]])
    return (scores, anomaly, v)

def annotate(imgs, scores, tiles, v, fps, name):
    '''Input: imgs: frames RGB values
              scores: anomaly scores
              tiles: list with tile coordinates
              v: velocity for each object
              fps: fps of the video
              name: output video name
       Output: an annotated video with speed for each car
    '''
    for i in range(len(imgs)):
        for j in range(len(scores[0])):
            if scores[i][j]:
                cv2.rectangle(imgs[i], (tiles[j][0], tiles[j][1]), (tiles[j][2], tiles[j][3]), (0,255,0),1)
    for i in range(len(v)-1):
        curr_index = v[i][0]
        for j in range(v[i+1][0] - curr_index):
            cv2.putText(imgs[curr_index + j], 'Vehicle ' + str(i+1) + ": Last Speed: " + str(round(v[i][1],1)) + "mph",
            (40,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_name = '../Videos/{0}.mp4'.format(name)
    video=cv2.VideoWriter(video_name, fourcc, fps, (imgs[0].shape[1],imgs[0].shape[0]))
    for j in range(len(imgs)):
        video.write(imgs[j])
    cv2.destroyAllWindows()
    video.release()

def main(file, t, n, row1, row2, size, name):
    '''Input: file: the file name

       Output:
    '''
    tiles1 = tile_list(size, row1)
    tiles2 = tile_list(size, row2)
    tiles = tiles1 + tiles2
    file_data = read_file(file)
    imgs = file_data[0]
    fps = file_data[1]
    (scores, anomaly, v) = output(tiles, imgs, t, n, size)
    return annotate(imgs, scores, tiles, v, fps, name)

import time
start_time = time.time()
main('../Videos/traffic-short.mp4', 50, 256, 15, 55, 15, 'videooooo')
print('elapsed time{0}:'.format(time.time() - start_time))
