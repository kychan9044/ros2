import rclpy 
from rclpy.node import Node 
from rclpy.qos import QoSProfile 
from std_msgs.msg import String
import cv2
import picamera
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class CameraPublisher(Node): 

    def __init__(self):
        super().__init__('camera_publisher') # 노드 이름 설정
        qos_profile = QoSProfile(depth=10) 
        self.camera_publisher = self.create_publisher(Image, 'camera', qos_profile)
        self.timer = self.create_timer(1, self.timer_callback)
        self.count = 0
        self.camera = picamera.PiCamera()
        self.br = CvBridge()

    def timer_callback(self):
        self.get_logger().info('Published message')
        image = self.camera.capture()
        self.camera_publisher.publish(self.br.cv2_to_imgmsg(image)) 


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