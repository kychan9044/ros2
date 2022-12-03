import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.DATASETS.TRAIN = ("mdata4_train",)
cfg.DATASETS.TEST = ()
cfg.DATALOADER.NUM_WORKERS = 2
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")  # Let training initialize from model zoo
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.00025  # pick a good LR
cfg.SOLVER.MAX_ITER = 1000    # 300 iterations seems good enough for this toy dataset; you will need to train longer for a practical dataset
cfg.SOLVER.STEPS = []        # do not decay learning rate
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128   # faster, and good enough for this toy dataset (default: 512)
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3  # only has one class (mount).

cfg.MODEL.DEVICE='cpu'
cfg.MODEL.WEIGHTS = "./train/model_final.pth"  # path to the model we just trained
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set a custom testing threshold
predictor = DefaultPredictor(cfg)

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

    def listener_callback(self, data):
        self.get_logger().info('Received message')
        
        # Convert ROS Image message to OpenCV image 
        current_frame = self.br.imgmsg_to_cv2(data)
        detect_gesture(current_frame)
        # Display image 
        # cv2.imwrite("img.jpg", current_frame)
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

def detect_gesture(img):
    outputs = predictor(img)
    # v = Visualizer(im[:,:,::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    # out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    # cv2.imshow("image", out.get_image()[:, :, ::-1])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    print(outputs["instances"].pred_classes)
    print(outputs["instances"].pred_boxes)

if __name__ == '__main__':
    main()