import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from cat.node.detect_gesture import detect_gesture

class CameraSubscriber(Node):

    def __init__(self):
        super().__init__('Camera_subscrixber')
        qos_profile = QoSProfile(depth=10)
        self.camera_subscriber = self.create_subscription(
            Image,
            'camera',
            self.listener_callback,
            qos_profile)
        self.br = CvBridge()
        self.count = 0

    def listener_callback(self, data):
        self.get_logger().info('Received message')
        self.count+=1
        # Convert ROS Image message to OpenCV image 
        current_frame = self.br.imgmsg_to_cv2(data)
        detect_gesture(current_frame)
        # Display image 
        cv2.imwrite("img"+self.count+".jpg", current_frame)
        # cv2.imshow("img",current_frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

def main(args=None):
    rclpy.init(args=args)
    node = CameraSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()