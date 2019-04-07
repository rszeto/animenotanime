# pytorch

This part of the code is used to train a deep neural network that classifies anime images. All commands should be run in
this directory (`pytorch`) unless otherwise specified.

## Preparing data

The following commands will download images to `data/images/anime` and `data/images/not_anime`.

```bash
python collect_images.py anime --num_pages 100
python collect_images.py notanime notanime <client_id> <client_secret> --num_pages 100
```

The following command will create training/validation splits in `data/train` and `data/val` by creating random symbolic
links to the downloaded images.

```bash
python create_train_val_symlinks.py
```

## Training a model

The following command will train the deep neural network and save a checkpoint to `pytorch/model_best.pth.tar`.

```bash
python train.py data --gpu 0 --pretrained
```

The training script is taken directly from the [official PyTorch example](https://github.com/pytorch/examples/blob/27a6244452c5fcc2269dc59e26a50a4599771081/imagenet/main.py).


## Extracting model weights and copying to the server

The following commands will extract just the neural network weights and copy them to the server.

```bash
python extract_model_snapshot.py
cp model_best_small.pth.tar ../src/model_best_small.pth.tar
```