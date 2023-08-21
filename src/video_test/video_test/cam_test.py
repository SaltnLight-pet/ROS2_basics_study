import rclpy as rp 
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np
import cv2
from cv_bridge import CvBridge
 
bridge = CvBridge() 
 
class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_sub')
        self.image_sub = self.create_subscription(
            Image,
            '/image_raw',
            self.image_callback,
            10
        )

    def canny_edge(self,low, high):
        src = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(src, low, high)
 
    def image_callback(self, data) :
        self.image = bridge.imgmsg_to_cv2(data, 'bgr8')
        canny_img = self.canny_edge(50, 100)
        cv2.imshow('canny', canny_img)
        cv2.imshow('img', self.image)
        cv2.waitKey(33)
 
def main(args=None) :
    rp.init(args=args)
    node = ImageSubscriber()
 
    try :
        rp.spin(node)
    except KeyboardInterrupt :
        node.get_logger().info('Stopped by Keyboard')
    finally :
        node.destroy_node()
        rp.shutdown()
 
 
if __name__ == '__main__' :
    main()