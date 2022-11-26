import rclpy 
from rclpy.node import Node # Node 클래스.
from rclpy.qos import QoSProfile # 퍼블리셔의 QoS 설정
from std_msgs.msg import String # 퍼블리시하는 메시지 타입 - String 메시지 인터페이스

# Node 클래스 상속
class HelloworldPublisher(Node): 

    def __init__(self):
        super().__init__('helloworld_publisher') # 노드 이름 설정
        qos_profile = QoSProfile(depth=10) 
        self.helloworld_publisher = self.create_publisher(String, 'helloworld', qos_profile)
        self.timer = self.create_timer(1, self.publish_helloworld_msg)
        self.count = 0

    def publish_helloworld_msg(self):
        msg = String()
        msg.data = 'Hello World: {0}'.format(self.count)
        self.helloworld_publisher.publish(msg) 	# 퍼블리시
        self.get_logger().info('Published message: {0}'.format(msg.data))
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = HelloworldPublisher()
    try:
        rclpy.spin(node) 
    except KeyboardInterrupt: 
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()