from fastai.vision.all import *
from fastai.callback.tracker import EarlyStoppingCallback

def create_model(dls):
    learn = vision_learner(dls, resnet34, metrics=[error_rate, accuracy, F1Score()], ps=0.5)
    lrs = learn.lr_find(suggest_funcs=(minimum, steep, valley, slide))
    lr_max = (lrs.minimum + lrs.steep) / 2
    learn.fit_one_cycle(10, lr_max=lr_max, cbs=[EarlyStoppingCallback()])
    return learn

def label_function(data):
    return "Label de l'objet"
