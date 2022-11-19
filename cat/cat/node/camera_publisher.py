import rclpy 
from rclpy.node import Node 
from rclpy.qos import QoSProfile 
from std_msgs.msg import String
import cv2
import picamera
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import time
import queue

class CameraPublisher(Node): 

    def __init__(self):
        super().__init__('camera_publisher') 
        qos_profile = QoSProfile(depth=10) 
        self.camera_publisher = self.create_publisher(Image, 'camera', qos_profile)
        self.count = 0
        self.camera = picamera.PiCamera()
        self.br = CvBridge()
        self.timer = self.create_timer(1, self.take_pictures)
        self.timer = self.create_timer(1, self.publish_images)

    def timer_callback(self):
        self.get_logger().info('Published message')
        image = self.camera.capture()
        self.camera_publisher.publish(self.br.cv2_to_imgmsg(image)) 

    def take_pictures(self):
        # Take compressed images and put into the queue.
        # 'jpeg', 'rgb'
        try:
            for capture in self.camera.capture_continuous(self.write_capture(self), format='jpeg'):
                if self.capture_event.is_set():
                    break
                time.sleep(0.5)
                # The exit flag could have been set while in the sleep
                if self.capture_event.is_set():
                    break
        except:
            self.get_logger().error('CAM: exiting take_pictures because of exception')
    
    def publish_images(self):
        # Loop reading from capture queue and send to ROS topic
        while True:
            if self.publisher_event.is_set():
                break
            try:
                msg = self.capture_queue.get(block=True, timeout=2)
            except queue.Empty:
                msg = None
            if self.publisher_event.is_set():
                break
            if msg != None:
                self.get_logger().debug('CAM: sending frame. frame=%s'
                                    % (msg.header.frame_id) )
                self.publisher.publish(msg)


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