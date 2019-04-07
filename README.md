# animenotanime

This repository contains a web application that classifies images as anime or not anime, which was inspired by
[this YouTube video](https://www.youtube.com/watch?v=xIx2dAmKtms).

This was designed to be a whimsical website for my friends; it is NOT optimized or suitable for large-scale deployment.

## Heroku

This project is designed to run the web server (under `src`) on Heroku out-of-the-box.

## Sub-projects

This repository contains two sub-projects: one for training a deep neural network (`pytorch`), and one for deploying the
web server (`src`).

The two sub-projects have their own `requirements.txt` files because the server is designed to run on Heroku. In
particular, `src` has minimal dependencies and loads a PyTorch wheel that only supports the CPU. The two sub-projects
have different versions of PyTorch and thus, their environments are generally incompatible.