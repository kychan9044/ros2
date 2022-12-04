from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
import cv2

class Gesture():
    def __init__(self):
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        cfg.DATASETS.TRAIN = ("mdata1_train",)
        # cfg.DATASETS.TEST = ("mdata1_val",)
        # self.test_metadata = MetadataCatalog.get("mdata1_val").set(thing_classes=["palm", "punch", "one","two"])
        self.metadata_train = MetadataCatalog.get("mdata1_train").set(thing_classes=["palm", "punch", "one", "two"])
        cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")  # Let training initialize from model zoo

        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 4
        cfg.MODEL.DEVICE='cpu'
        cfg.MODEL.WEIGHTS = "model_final.pth"  # path to the model we just trained
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set a custom testing threshold
        self.predictor = DefaultPredictor(cfg)
        print("=================Finish Init========================")

    def detect_gesture(self,img,id):
        outputs = self.predictor(img)
        v = Visualizer(img[:,:,::-1], metadata=self.metadata_train, scale=1.2)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        cv2.imwrite("outcome"+str(id)+".jpg", out.get_image()[:, :, ::-1])
        # cv2.imshow("image", out.get_image()[:, :, ::-1])
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        print('==========',id,'============')
        print(outputs["instances"].pred_classes)
        print(outputs["instances"].pred_boxes)

        class_index = None
        class_name = None

        for idx, coordinates in enumerate(outputs["instances"].pred_boxes):
            class_index = outputs["instances"].pred_classes[idx]
            class_name = self.metadata_train.thing_classes[class_index]
        return (class_name, class_index)

        # return outputs["instances"].pred_classes
