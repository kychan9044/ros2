import rclpy 
from rclpy.node import Node 
from rclpy.qos import QoSProfile 
from std_msgs.msg import String
import cv2
# import picamera
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import time
import os


class CameraPicture(Node): 

    def __init__(self):
        super().__init__('camera_picture') 
        self.get_logger().info('********init************')

        # self.camera = picamera.PiCamera()
        self.br = CvBridge()
        self.picture_timer = self.create_timer(1, self.take_pictures_with_shell)

    def take_pictures(self):
        self.get_logger().info('Take picture')
        try:
            for capture in self.camera.capture_continuous(self.write_capture(self), format='jpeg'):
                time.sleep(0.5)
        except:
            self.get_logger().error('CAM: exiting take_pictures because of exception')
    
    def take_pictures_with_shell(self):
        while True:
            self.get_logger().info('******************Take picture******************')
            os.system("raspistill -v -o camera.jpg")
            time.sleep(3)

def main(args=None):
    rclpy.init(args=args)
    node = CameraPicture()
    try:
        rclpy.spin(node) # 생성한 노드를 spin시켜 지정된 콜백함수가 실행
    except KeyboardInterrupt: 
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()