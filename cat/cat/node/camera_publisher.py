import rclpy 
from rclpy.node import Node # Node 클래스
from rclpy.qos import QoSProfile # 퍼블리셔의 QoS 설정
from std_msgs.msg import String,Image # 퍼블리시하는 메시지 타입 - String 메시지 인터페이스
import cv2
import picamera

# Node 클래스 상속
class CameraPublisher(Node): 

    def __init__(self):
        super().__init__('camera_publisher') # 노드 이름 설정
        qos_profile = QoSProfile(depth=10) 
        self.camera_publisher = self.create_publisher(Image, 'camera', qos_profile)
        self.timer = self.create_timer(1, self.timer_callback)
        self.count = 0
        self.camera = picamera.PiCamera()
        self.br = CvBridge()

    def publish_helloworld_msg(self):
        msg = String()
        msg.data = 'Hello World: {0}'.format(self.count)
        self.helloworld_publisher.publish(msg) 	# 퍼블리시
        self.get_logger().info('Published message: {0}'.format(msg.data))
        self.count += 1

    def timer_callback(self):
        image = self.camera.capture()
        self.camera_publisher.publish(self.br.cv2_to_imgmsg(image)) 
    
    # def take_pictures(self):
    #     # Take compressed images and put into the queue.
    #     # 'jpeg', 'rgb'
    #     try:
    #         for capture in self.camera.capture_continuous(self.write_capture(self), format='jpeg'):
    #             if self.capture_event.is_set():
    #                 break
    #             # The exit flag could have been set while in the sleep
    #             if self.capture_event.is_set():
    #                 break
    #     except:
    #         self.get_logger().error('CAM: exiting take_pictures because of exception')


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