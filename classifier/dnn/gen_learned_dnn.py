from osog.classifier.dnn.cnn import create

pathes = [
    '../../datasets/G/',  # class 0
    '../../datasets/beetle/',  # class 1
    '../../datasets/cricket/',  # class 2
    '../../datasets/stagbeetle/']  # class 3

create(name='modelX', dataset_pathes=pathes)