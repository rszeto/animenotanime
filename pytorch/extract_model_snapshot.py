import torch


def main():
    model_checkpoint = torch.load('model_best.pth.tar', map_location={'cuda:0': 'cpu'})['state_dict']
    torch.save(model_checkpoint, 'model_best_small.pth.tar')


if __name__ == '__main__':
    main()