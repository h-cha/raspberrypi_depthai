import logging
from datetime import datetime, timedelta
from arg_manager import parseArgs
import cv2

log = logging.getLogger(__name__)

def compare_past_distance(now, past, compareDistance):
    if past - now > compareDistance:
    # if now - past > 1:
    # if now < past :
        return True
    else:
        return False


class DistanceGuardian:

    def __init__(self):
        self.tracking = {}
        self.time_difference = timedelta(seconds=1)
        self.id_time = []
        self.result_id = []
        self.args = parseArgs()
        self.max_distance = self.args.dangerous_distance

    def parse_frame(self, frame, detections):
        results = []
        color = (255, 255, 255)
        close = False
        for i, detection in enumerate(detections):
            now = detection['time']
            tracking_id = str(detection['id']) + '_' + str(now.strftime('%Y年%m月%d日 %H:%M:%S'))
            if detection['depth_z'] != 0.0:
                now_distance = detection['depth_z']
                
                past_time = now - self.time_difference
                past_tracking_id = str(detection['id']) + '_' + str(past_time.strftime('%Y年%m月%d日 %H:%M:%S'))
                past_distance = 0.0
                dangerous = now_distance < self.max_distance

                if tracking_id not in self.id_time and detection['status'] != 'REMOVED':
                    if dangerous == True and past_tracking_id in self.tracking and now_distance != 0.0:
                    # もし　past_time　in tracking なら　past_distance と　now_distance を比較
                        past_distance = self.tracking[past_tracking_id]
                        close = compare_past_distance(now_distance, past_distance, self.args.compare_distance)




                    self.tracking[tracking_id] = now_distance

                    # 同じ時間に　1つのみ   result_id はtime
                    
                    results.append({
                        'id': tracking_id,
                        'dangerous': now_distance < self.max_distance,
                        'close': close,
                        'time': datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'),
                        'status': detection['status'],
                        'past_distance': past_distance,
                        'now_distance': now_distance,
                    })
                    cv2.putText(frame, str(close), (detection['x_min'] + 10, detection['y_min'] + 30), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)

                    # 同じIDはself.trackingに追加しない
                    self.id_time.append(tracking_id)
                # log.info("DG: {}".format(self.tracking))
                # if len(results) != 0:
                    # log.info("results: {}".format(results))
        return results