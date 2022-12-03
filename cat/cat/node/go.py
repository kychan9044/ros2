import sys
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
import time


class Go(Node):
    
    def __init__(self):
        super().__init__("go")
        """
        self.status = 0
        self.target_linear_vel   = 0.0
        self.target_angular_vel  = 0.0
        self.control_linear_vel  = 0.0
        self.control_angular_vel = 0.0
        """
        self.get_logger().info('********init************')
        qos_profile = QoSProfile(depth=10) 
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.camera_subscriber = self.create_subscription(
            String,
            'gesture',
            self.move,
            qos_profile)
    
    def move(self,data):
        self.get_logger().info('********Receive Gesture************')
        twist = Twist()
            
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        
        if data.data == "palm": # 우회전
            twist.linear.x = 0.2
            twist.angular.z = 0.3
            self.pub.publish(twist)
            
            time.sleep(5)
            
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.pub.publish(twist)
            

        elif data.data == "punch": # 직진
            twist.linear.x = 0.2
            twist.angular.z = 0.0
            self.pub.publish(twist)

            time.sleep(5)
            
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.pub.publish(twist)



        elif data.data == "one": # 좌회전
            twist.linear.x = 0.2
            twist.angular.z = -0.3
            self.pub.publish(twist)

            time.sleep(5)
            
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    goto_goal = Go()
    try:  
        rclpy.spin(goto_goal)
    except KeyboardInterrupt: 
        goto_goal.get_logger().info('Error')
    finally:
        goto_goal.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
