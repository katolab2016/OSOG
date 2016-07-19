from osog.classifier.dnn.cnn import create

pathes = [
    '../datasets/toy/',
    '../datasets/g/',  # class 0
    '../datasets/beetle/',
    '../datasets/cricket/',
    '../datasets/stagbeetle/',
    '../datasets/hand/'
]

create(name='6class', dataset_pathes=pathes)