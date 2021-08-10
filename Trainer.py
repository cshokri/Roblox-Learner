from fastai.vision.all import *

path = "C:\\Users\\cshok\\OneDrive\\Desktop\\Projects\\RobloxLearner"
games = ["speed_race_data", "speed_run_data"]
data_path = os.path.join(path, games[1])
fnames = get_image_files(data_path)
print(len(fnames))


def label_func(image):
    name = image.parent.name
    return name[:name.index("_")]


def main():
    dls = ImageDataLoaders.from_path_func(
        data_path, fnames, label_func, num_workers=0, bs=64)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(torch.cuda.get_device_name(0))
    torch.cuda.empty_cache()

    trainer = cnn_learner(dls, resnet34, metrics=accuracy)
    trainer.to(device)

    trainer.fine_tune(4, base_lr=1.0e-02)

    interpreter = ClassificationInterpretation.from_learner(trainer)
    interpreter.plot_confusion_matrix()

    trainer.export()


if __name__ == "__main__":
    main()
