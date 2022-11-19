import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String,Image
import cv2

class CameraSubscriber(Node):

    def __init__(self):
        super().__init__('Camera_subscriber')
        qos_profile = QoSProfile(depth=10)
        self.camera_subscriber = self.create_subscription(
            Image,
            'camera',
            self.listener_callback,
            qos_profile)
        self.br = CvBridge()

    def listener_callback(self, data):
        # Convert ROS Image message to OpenCV image 
        current_frame = self.br.imgmsg_to_cv2(data)
        # Display image 
        cv2.imshow("camera", current_frame) 
        cv2.waitKey(1)
        cv2.imwrite("img.jpg", current_frame)

    def subscribe_topic_message(self, msg):
        self.get_logger().info('Received message: {0}'.format(msg.data))


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