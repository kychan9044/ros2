from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2 import model_zoo
import cv2
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

def detect_gesture():
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    # cfg.DATASETS.TRAIN = ("mdata1_train",)
    cfg.DATASETS.TEST = ("mdata1_val",)
    test_metadata = MetadataCatalog.get("mdata1_val").set(thing_classes=["palm", "punch", "one","two"])
    # cfg.DATALOADER.NUM_WORKERS = 2
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")  # Let training initialize from model zoo
    # cfg.SOLVER.IMS_PER_BATCH = 2
    # cfg.SOLVER.BASE_LR = 0.00025  # pick a good LR
    # cfg.SOLVER.MAX_ITER = 1000    # 300 iterations seems good enough for this toy dataset; you will need to train longer for a practical dataset
    # cfg.SOLVER.STEPS = []        # do not decay learning rate
    # cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128   # faster, and good enough for this toy dataset (default: 512)
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 4  # only has one class (mount).

    # os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    # trainer = DefaultTrainer(cfg) 
    # trainer.resume_or_load(resume=False)
    # trainer.train()
    # MetadataCatalog.get("mdata1_train").set(thing_classes=["palm", "punch", "one", "two"])

    cfg.MODEL.DEVICE='cpu'
    cfg.MODEL.WEIGHTS = "model_final.pth"  # path to the model we just trained
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set a custom testing threshold
    predictor = DefaultPredictor(cfg)

    im = cv2.imread('./images/outcome/outcome17.jpg')
    outputs = predictor(im)
    # v = Visualizer(im[:,:,::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    v = Visualizer(im[:,:,::-1], metadata=test_metadata, scale=1.2)
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    # cv2.imshow("image", out.get_image()[:, :, ::-1])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    print(outputs)
    print(outputs["instances"].pred_classes)
    print(outputs["instances"].pred_boxes)

detect_gesture()