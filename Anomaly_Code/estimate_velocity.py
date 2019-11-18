def velocity_car(frame1, frame2, road = 850):
    '''Input: frame1: index of the first frame
              frame2: index of the second frame
              road: the actual width of the road in the video
       Output: the speed of one car
    '''
    fps = 30
    time = (frame2 - frame1) / fps
    speed = road / time
    return speed

def velocity(anomaly_frames, size):
    '''Input: anomaly_frame: index of the anomaly frames for each tile
              size: tile size
       Output: speed of the car
    '''
    tile1 = anomaly_frames[0]
    tile2 = anomaly_frames[-1]
    fps = 30
    speed = []
    while tile1 != [] and tile2 != []:
        frame1 = tile1[0]
        frame2 = tile2[0]
        speed_ips = velocity_car(frame1, frame2)
        speed_mph = speed_ips * 0.0568
        speed.append([frame2,speed_mph])
        frame_box = ((100 / size + 1) * 22.1) / speed_ips * fps
        tile1 = [i for i in tile1 if i > frame_box + frame1 + 10]
        tile2 = [i for i in tile2 if i > frame_box + frame2 + 10]
    return speed
# suv: 221 inches 9 boxes with width 10 pixels
