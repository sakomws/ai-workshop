# Session Title: Generating Interactive Environments: 

This session will give an overview of world models and then look at a few recent papers and implementations to discuss why they're important for gaming and creating generalist agents.

---

## Session Overview

**Instructor:** Luke Hollis

**Duration:** 30 minutes

**Objective:**  
- Understand world models and their importance in gaming and generalist agents
- Play Atari with Diamond: Run a diffusion world model implementation on your local machine
- Reproducing Genie: Follow along with steps to reproduce concepts from the Genie paper from the Google DeepMind team, creating a foundation world model, and learn how generalizable actions can be learned from unlabeled videos
- Play Minecraft in Oasis: See how one startup is using world models to generate Minecraft levels
  
By the end of this session, you will have a deeper understanding of world models and their practical applications in gaming and interactive environments.

---

## Prerequisites

- Basic knowledge of Python and ML concepts
- Familiarity with PyTorch
- A computer with GPU access (recommended but not required)

---

## Agenda

1. **Introduction to World Models**  
   - Overview of world models and their importance
   - Some recent papers: Genie, Diamond, GameNGen, Oasis
   - Key architectural components and considerations

2. **Hands-on Activities**  
   - Challenge 1: Running a diffusion world model to simulate Atari games with Diamond
   - Challenge 2: Follow along with Genie reproducibility steps, training a foundation world model to generalize actions from unlabeled videos
   - Challenge 3: Explore a Minecraft world model on Oasis 

3. **Q&A and Discussion**  
   - Discussion on world model architectures and how they can be used in the future
   - Other questions

---

## Slides

Intro to World Models and Challenges:
[Slides](https://docs.google.com/presentation/d/1dmGuaffiLb1isMf9k1OLFX-5T6w_VzU8gWPzDB3zRgU/edit?usp=sharing)  

## Challenge 1: Running a diffusion world model to simulate Atari games with Diamond

### Step 1: Clone the Diamond Repository 
```bash
git clone git@github.com:eloialonso/diamond.git
```

### Step 2: Set Up Environment with Conda
```bash
cd diamond
conda create -n diamond python=3.10
conda activate diamond
pip install -r requirements.txt
```

### Step 3: Play the pre-trained model with Atari

```bash
python src/play.py --pretrained
```

### BONUS: Play the pre-trained model with CSGO
```bash
git checkout csgo
python src/play.py
```

If this doesn't work, you can also play CSGO with Diamond on FAL: 

[Play CSGO with Diamond on FAL](https://fal.ai/demos/csgo)


## Challenge 2: Follow along with Genie reproducibility steps, training a model to generalize actions from unlabeled videos


### Step 1: Clone an implementation of Genie following the paper 
```bash
git clone git@github.com:lukehollis/genie-bottle.git
```

### Step 2: Set Up Environment with Conda
```bash
cd genie-bottle
conda create -n genie python=3.10 pytorch=2.3.0 cudatoolkit=12.1 -c pytorch -c nvidia
conda activate genie 
pip install -r requirements.txt
```

### Note: if you don't have a GPU, you can skip to the last step by downloading the example data in [data.zip](https://drive.google.com/file/d/1a2F0SzFTUrsv0Ow7T3WTvBIP-m3yBMqP/view?usp=drive_link). 
Unzip the file and move it into the `genie-bottle` directory, so that the file structure looks like this:
```
genie-bottle/
├── config
├── data
│   ├── log 
│   ├── train
│   ├── val
│   └── test
├── res
├── genie.py
├── ... 
```

### Step 3: Generate training data for the `VideoTokenizer`
First, to generate a very small set of training data for the `VideoTokenizer` one can use the `sample.py` script and then split it into train/val/test sets with the `split.py` script:

```bash
python sample.py --env_name Coinrun --num_envs 10 --timeout 1000 --root ./data
python split.py --env_name Coinrun --root ./data
```

In the actual reproducability study, the authors recommended generating 10,000 videos.

### Step 4: Train the `VideoTokenizer`
To train the `VideoTokenizer`, one should run the following command, where `<path_to_conf_file>` is the path to the configuration file for the tokenizer. You can copy the `config/tokenize.yaml` file to `config/tokenize.local.yaml` and modify the paths to point to your data--or leave it as is to use the default paths.

```bash
python tokenizer.py fit -c <path_to_conf_file>
```

### Step 5: Train the `Genie` model
Then to train in parallel both the `LatentAction` and `Dynamics` model (leveraging a fully-trained `VideoTokenizer`), one can again simply run the following command, where `<path_to_conf_file>` is the path to the configuration file for the `Genie` model. You can copy the `config/genie.yaml` file to `config/genie.local.yaml`. *Be sure to modify the `tokenizer_ckpt_path` to point to the checkpoint of the trained `VideoTokenizer`*.

```bash
python genie.py fit -config <path_to_conf_file>
```

### Step 6: Generate videos from the trained models
Finally, to generate videos from the trained models one can use the `play.py` script:

```bash
python play.py --checkpoint <path_to_checkpoint> --tokenizer_checkpoint <path_to_tokenizer_checkpoint> --image <path_to_image> --output <path_to_output>
```

We provide example configuration files in the `📂 config` folder. There's also an example image in the `📂 res` folder to test video generation--and a plaintext copy of the paper so that you can interactively ask questions of this repo and described implementation.


## Challenge 3: Explore a Minecraft world model on Oasis

Last week, two startups released a [world model](https://oasis-model.github.io/) for simulating experience playing Minecraft with a similar strategy to Diamond, Genie, and Dreamer V3. 

Explore a foundation world model for playing Minecraft on Oasis:

[Play Minecraft on Oasis](https://oasis.decart.ai/welcome)

Per the paper, their addition is using fast transformer inference to generate real-time interactive video. 

> We believe fast transformer inference is the missing link to making generative video a reality. Using Decart's inference engine, we show that real-time video is possible. When Etched's transformer ASIC, Sohu, is released, we can run models like Oasis in 4K. Today, we're releasing Oasis's code, the weights of a 500M parameter model you can run locally, and a live playable demo of a larger checkpoint.

### Step 1: Clone the Oasis Repository 
```bash
git clone git@github.com/etched-ai/open-oasis.git
```

Questions for discussion:
- How does the Oasis model compare to the other models we've seen today?
- What are the tradeoffs of the Oasis model architecture?
- What are the implications of this approach for the future of world models?

---

## Citations and Additional Resources

```bibtex
@incollection{ha2018worldmodels,
  title = {Recurrent World Models Facilitate Policy Evolution},
  author = {Ha, David and Schmidhuber, J{\"u}rgen},
  booktitle = {Advances in Neural Information Processing Systems 31},
  pages = {2451--2463},
  year = {2018},
  publisher = {Curran Associates, Inc.},
  url = {https://papers.nips.cc/paper/7512-recurrent-world-models-facilitate-policy-evolution},
  note = "\url{https://worldmodels.github.io}",
}
```

```bibtex
@article{bruce2024genie,
  title={Genie: Generative Interactive Environments},
  author={Bruce, Jake and Dennis, Michael and Edwards, Ashley and Parker-Holder, Jack and Shi, Yuge and Hughes, Edward and Lai, Matthew and Mavalankar, Aditi and Steigerwald, Richie and Apps, Chris and others},
  journal={arXiv preprint arXiv:2402.15391},
  year={2024}
}
```

```bibtex
@inproceedings{alonso2024diffusionworldmodelingvisual,
      title={Diffusion for World Modeling: Visual Details Matter in Atari},
      author={Eloi Alonso and Adam Jelley and Vincent Micheli and Anssi Kanervisto and Amos Storkey and Tim Pearce and François Fleuret},
      booktitle={Thirty-eighth Conference on Neural Information Processing Systems}}
      year={2024},
      url={https://arxiv.org/abs/2405.12399},
}
```

```bibtex
@article{oasis2024,
  author    = {Decart and Julian Quevedo, Quinn McIntyre, Spruce Campbell, Xinlei Chen, Robert Wachen},
  title     = {Oasis: A Universe in a Transformer},
  year      = {2024},
  url       = {https://oasis-model.github.io/}
}
```

```bibtex
@misc{valevski2024diffusionmodelsrealtimegame,
        title={Diffusion Models Are Real-Time Game Engines}, 
        author={Dani Valevski and Yaniv Leviathan and Moab Arar and Shlomi Fruchter},
        year={2024},
        eprint={2408.14837},
        archivePrefix={arXiv},
        primaryClass={cs.LG},
        url={https://arxiv.org/abs/2408.14837}, 
  }
```

```bibtex
@article{hafner2023dreamerv3,
  title={Mastering Diverse Domains through World Models},
  author={Hafner, Danijar and Pasukonis, Jurgis and Ba, Jimmy and Lillicrap, Timothy},
  journal={arXiv preprint arXiv:2301.04104},
  year={2023}
}
```

```bibtex
@article{yu2023language,
  title={Language Model Beats Diffusion--Tokenizer is Key to Visual Generation},
  author={Yu, Lijun and Lezama, Jos{\'e} and Gundavarapu, Nitesh B and Versari, Luca and Sohn, Kihyuk and Minnen, David and Cheng, Yong and Gupta, Agrim and Gu, Xiuye and Hauptmann, Alexander G and others},
  journal={arXiv preprint arXiv:2310.05737},
  year={2023}
}
```

```bibtex
@inproceedings{chang2022maskgit,
  title={Maskgit: Masked generative image transformer},
  author={Chang, Huiwen and Zhang, Han and Jiang, Lu and Liu, Ce and Freeman, William T},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages={11315--11325},
  year={2022}
}
```

---

## Contact

If you have questions during the workshop, please reach out to **[@lukehollis](https://x.com/lukehollis)** / luke@mused.com or open an issue in the repository.

