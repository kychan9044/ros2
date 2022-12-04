import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String, Bool
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from cat.node.detect_gesture import Gesture

class CameraSubscriber(Node):

    def __init__(self):
        super().__init__('Camera_subscrixber')
        qos_profile = QoSProfile(depth=10)
        self.camera_subscriber = self.create_subscription(
            Image,
            'camera_data',
            self.listener_callback,
            qos_profile)
        self.camera_flag_publisher = self.create_publisher(String, 'camera_flag', qos_profile)
        self.br = CvBridge()
        self.count = 0
        self.gesture = Gesture()
        self.gesture_publisher = self.create_publisher(String, 'gesture', qos_profile)

    def listener_callback(self, data):
        msg = String()
        msg.data = "Disable"
        self.camera_flag_publisher.publish(msg)
        self.get_logger().info('Received message')
        self.count+=1
        # Convert ROS Image message to OpenCV image 
        current_frame = self.br.imgmsg_to_cv2(data)
        result = self.gesture.detect_gesture(current_frame,self.count)
        # Display image 
        print('**************Finish detect****************')
        cv2.imwrite("img"+str(self.count)+".jpg", current_frame)
        msg.data = result[0]
        self.gesture_publisher.publish(msg)
        # cv2.imshow("img"+str(self.count),current_frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        msg.data = "Enable"
        self.camera_flag_publisher.publish(msg)

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