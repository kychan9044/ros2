import rclpy 
from rclpy.node import Node 
from rclpy.qos import QoSProfile 
from std_msgs.msg import String
import cv2
# import picamera
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import time
# import queue
import os

class CameraPublisher(Node): 

    def __init__(self):
        super().__init__('camera_publisher') 
        self.get_logger().info('********init************')
        qos_profile = QoSProfile(depth=10) 
        self.camera_publisher = self.create_publisher(Image, 'camera', qos_profile)
        self.count = 0

        self.cam = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
        if self.cam.isOpened():
            self.get_logger().info("Camera open failed!")
            raise Exception("Camera open failed!")
        self.br = CvBridge()
        self.publish_timer = self.create_timer(1, self.publish_images)
    
    def publish_images(self):
        # while True:
        self.get_logger().info('***********Published message***********')
        # try:
        #     msg = self.capture_queue.get(block=True, timeout=2)
        # except queue.Empty:
        #     msg = None
        # if msg != None:
        #     self.get_logger().debug('CAM: sending frame. frame=%s'
        #                         % (msg.header.frame_id) )
        #     self.publisher.publish(msg)
        # img = cv2.imread('camera.jpg')
        ret, frame = self.cam.read()
        if not ret:
            self.get_logger().info('Image read failed!')
        else:
            print((type(frame),frame))
            self.camera_publisher.publish(self.br.cv2_to_imgmsg(frame, encoding="bgr8"))

def main(args=None):
    rclpy.init(args=args)
    node = CameraPublisher()
    try:
        rclpy.spin(node) # 생성한 노드를 spin시켜 지정된 콜백함수가 실행
    except KeyboardInterrupt: 
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()