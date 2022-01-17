import logging
from datetime import datetime, timedelta
log = logging.getLogger(__name__)

def compare_past_distance(now, past):
    if now - past > 0.1:
        return True
    else:
        return False


class DistanceGuardian:
    max_distance = 1

    def __init__(self):
        self.tracking = {}
        self.time_difference = timedelta(seconds=5)
        self.id_time = []
        self.result_id = []

    def parse_frame(self, frame, detections):
        results = []
        
        close = False
        for i, detection in enumerate(detections):
            now = detection['time']
            tracking_id = str(detection['id']) + '_' + str(now.strftime('%Y年%m月%d日 %H:%M:%S'))
            now_distance = detection['depth_z']
            
            past_time = now - self.time_difference
            past_tracking_id = str(detection['id']) + '_' + str(past_time.strftime('%Y年%m月%d日 %H:%M:%S'))
            dangerous = now_distance < self.max_distance

            if tracking_id not in self.id_time and detection['status'] != 'REMOVED':
                if dangerous == True and past_tracking_id in self.tracking:
                # もし　past_time　in tracking なら　past_distance と　now_distance を比較
                    past_distance = self.tracking[past_tracking_id]
                    close = compare_past_distance(now_distance, past_distance)


                self.tracking[tracking_id] = now_distance

                # 同じ時間に　1つのみ   result_id はtime
                if _id not in self.result_id:
                    results.append({
                        'id': tracking_id,
                        'dangerous': now_distance < self.max_distance,
                        'close': close,
                        'time': datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'),
                        'status': detection['status'],
                    })

                # 同じIDはself.trackingに追加しない
                self.id_time.append(tracking_id)
            # log.info("DG: {}".format(self.tracking))
            # log.info("results: {}".format(results))
        return resultss
