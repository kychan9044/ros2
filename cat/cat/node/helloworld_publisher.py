import rclpy 
from rclpy.node import Node # Node 클래스
from rclpy.qos import QoSProfile # 퍼블리셔의 QoS 설정
from std_msgs.msg import String # 퍼블리시하는 메시지 타입 - String 메시지 인터페이스
from sensor_msgs.msg import LaserScan
import math

# Node 클래스 상속
class HelloworldPublisher(Node): 

    def __init__(self):
        super().__init__('helloworld_publisher') # 노드 이름 설정
        qos_profile = QoSProfile(depth=10) 
        self.helloworld_publisher = self.create_publisher(String, 'helloworld', qos_profile)
        self.timer = self.create_timer(1, self.publish_helloworld_msg)
        self.count = 0

    def publish_helloworld_msg(self):
        # msg = String()
        # msg.data = 'Hello World: {0}'.format(self.count)
        # self.helloworld_publisher.publish(msg) 	# 퍼블리시
        # self.get_logger().info('Published message: {0}'.format(msg.data))
        # self.count += 1
        scan = rclpy.wait_for_message('scan', LaserScan)
        scan_filter = []
       
        samples = len(scan.ranges)  # The number of samples is defined in 
                                    # turtlebot3_<model>.gazebo.xacro file,
                                    # the default is 360.
        samples_view = 1            # 1 <= samples_view <= samples
        
        if samples_view > samples:
            samples_view = samples

        if samples_view is 1:
            scan_filter.append(scan.ranges[0])

        else:
            left_lidar_samples_ranges = -(samples_view//2 + samples_view % 2)
            right_lidar_samples_ranges = samples_view//2
            
            left_lidar_samples = scan.ranges[left_lidar_samples_ranges:]
            right_lidar_samples = scan.ranges[:right_lidar_samples_ranges]
            scan_filter.extend(left_lidar_samples + right_lidar_samples)

        for i in range(samples_view):
            if scan_filter[i] == float('Inf'):
                scan_filter[i] = 3.5
            elif math.isnan(scan_filter[i]):
                scan_filter[i] = 0
        print(scan_filter)
        return scan_filter


def main(args=None):
    rclpy.init(args=args)
    node = HelloworldPublisher()
    try:
        rclpy.spin(node) # 생성한 노드를 spin시켜 지정된 콜백함수가 실행
    except KeyboardInterrupt: 
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()