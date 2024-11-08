
# Flox: Rethinking How We Build & Collab

Hi friends!  
In this session, we'll introduce you to [Flox](https://flox.dev).

Flox is an open-source (GPL2) tool for simple and powerful system dependency mangement,
per-project, and decoupled from your machine.  
Underneath, we are using [Nix](https://nixos.org) which gives us access to 
[over 100,000 packages](https://search.nixos.org/packages).  
Many of these packages are cross-platform and built natively for your machine
whether you are using a Macbook or a Linux server in Google Cloud.

Flox is designed to be simple to teach to your teammates so you can immediately
be productive together without taking much time to learn Nix concepts.

We'll start with the basics and try some Local AI development.

---

## Session Overview

**Instructor:** Ron Efroni & Tom Bereknyei

**Duration:** 30 minutes

**Objective:**  
- Set up a default environment (optionally auto-activated by your shell)
- Learn to initialize environment, search for dependencies, and activate your environment
- Use reproducible software from the public Nix Packages cache
- Activate multiple environments
- Clone and activate another project
- Start Services
- Start a Local AI stack for Retreival Augmented Generation

Through this session, you'll learn to leverage Flox as a collaborative and practical
way to use Nix in software and infrastructure projects.

---

## Prerequisites

- A MacOS, Linux, or (Windows Subsystem for Linux 2) machine to do the exercises.
  (Nix on Windows is not ready for public use, but WSL2 works)
- Internet access for pulling packages
- Basic familiarity with package managers such as `brew`/`apt`/`yum`, perhaps `npm`.
- Basic familiarity with `git`

---

## Agenda

1. **Introduction**  
   - Reproducible Software and Packaging Discipline -- Why Nix?
   - Evolving the Software Builder's Workflow
   
2. **Hands-on Activities**  
   - "Activating" the `default` environment
   - Cloning a project and using services
   - Trying your own workflow

3. **Q&A and Discussion**  
   - onboarding pain joining a new team or learning new tech
   - new possibilties with declarative and collaborative packaging
   - questions about Flox or Nix

---

## Setup

### Step 1: Install Flox
We have downloadable installers for many platforms.  
Some examples are MacOS, debian/Ubuntu systems, CentOS, NixOS, etc.
Find an option that works for you at https://flox.dev/docs/install-flox

If you have brew on MacOS, you can `brew install flox`  
The .deb package will also add sources to apt for autoupdates.

Installing Flox will install Nix for you.  
If you already have Nix or NixOS, there are instructions for that as well.


### Step 2: Run `flox --help`
Using a terminal session, run the `flox --help` command to see what sub-commands
are available!


## Challenges 🏆

### 1. The `default` environment
#### discovery
Let's create our very first Flox environment.
```bash
cd ~
flox init
```
We can list and see we currently have no packages installed here.
```bash
flox list
```
Let's search for something to install
```bash
flox search htop
```
And get some info about the package + the versions that are available
```bash
flox show htop
```
Nothing radical here -- it is nice to have a package manager support multiple versions!
#### activation
```bash
flox install htop
```
Now let's look that we have it...
```bash
which htop
```
You might notice that htop you don't have htop on your path, or it's coming
from some existing place on your system.  
Let's fix that:
```bash
flox activate
```
Now when we run `which htop` we'll see it's coming from our new flox environment.
```bash
which htop
```
We're in a sub-shell now with all of our packages and library paths configured.
When we leave our environment, it's will go back to how it was before.
```bash
exit
which htop
```
Activating "in-place" without creating a sub-shell is also an option:
```bash
source <(flox activate)
```
#### auto-activation (optional)
if you'd like to auto-activate your default environment every time you open a new
shell, add the following to your `~/.bashrc`, `~/.zshrc`, or `~/.config/fish/config.fish`:
```bash
command -v flox >/dev/null && eval "$(flox activate -d ~)"
```
Up until this point, we've been activating in our current directory, but we want to
specify the $HOME directory (~) here so that we can open shells in any folder and have
the same behavior :)

With this config, all of your new shells will have your new environment active.

This environment does not technically need to be created in `~`.  
You can pass any directory to `-d` and name it anything.  
However, this is the canonical place to put the default env.

If you skip this step, just run `flox activate -d ~` in all of your new terminals.

#### manifesting teamwork
Let's install a few more packages.  
Notably, we are installing the `micro` text editor: 
```bash
flox install git curl tree bat micro
```
Until now, we've been doing normal package manager type things.  
Notice how we had to run `flox init`?  
That's because flox makes a `.flox/` folder for us with a declarative manifest.
```bash
tree .flox
```
We've been modifying our environment imperatively using "install" commands.  
Let's edit our environment declaratively using `micro`:
```bash
export EDITOR="micro"

flox edit
```
This file format is toml, a readable markup language similar to JSON or INI files.  
You'll see in the comments, that flox environments contain many things you can declare:
- packages
- environment variables
- shell hooks
- services

For instance, if you'd like to always use the `micro` text editor, you can set the
`EDITOR` var in the `[vars]` section:
```
[vars]
EDITOR = "micro"
```
Hit `Ctrl+S` and `Ctrl+Q` to save and quit the micro text editor :)

Flox will check if you have any syntax errors, and then try to rebuild your environment.
Since we added a variable, it will ask you to exit and either create a new terminal or
run `flox activate` again.

Because everything we do in the flox environment changes the manifest,
we can check this entire folder into a git repo, use it on another machine, or
share it with our teammates.

### 2. Cloning a project and using services
Let's start a RAG stack to do some Local AI.  
Make sure your `default` flox environment is already active -- this is gonna be cool.
```bash
git clone https://github.com/stealthybox/verba-with-flox
cd verba-with-flox
```
Let's go
```bash
flox activate --start-services
  # the shorter flag is -s
```
#### layers 🥞
Notice what just happenned in your prompt.  
Both the `verba-with-flox` environment and your `default` are active.  
We are layering! You can do with with as many environments as you want.  
The use-cases are endless:
- have multiple `$HOME/toolbox/*` envs
- create environments to hold variables and secrets for `dev`,`stage`,`production`
- juggle in 3 programming languages in one git repository
This is fun.  
No volume mounts or VM's or containers -- we can simply compose toolboxes of native binaries
directly on our actual laptop.

#### services
Now let's look at the services:
```bash
flox services status
```
You should have:
- a running ollama daemon
- a weaviate vector db
- verba, a UI service for RAG workflows
- a "models" service

> note: If the weaviate or verba services say "Completed", they aren't running
>       This is not good -- something else on your machine is probably using port 8000 or 8080
>       Stop those processes and run `flox services start` again.

The models service should be attempting to pull the needed pre-trained models
for our RAG stack:
```bash
flox services logs models --follow
```
hit `Ctrl+C` or open a new tab.  
One of these is around 5 GB, so if you don't have disk space, you can run:
```bash
flox services stop models
```
This may take a few minutes to download...  
Let's see how this environment is defined:
```bash
export EDITOR="micro"
flox edit
```
You'll see in here, we've
- defined a python virtual environment
- pre-installed the `goldenverba` python package for you
- setup options and environment variables
- defined services for inference, vectors, and the web UI
- implemented some janky waiting code (we need to expose a better API for service health and dependencies)

`Ctrl+Q` will let you exit the `micro` editor without saving.

Once our models have pulled (`flox services logs models --follow`), we should be able
to prep our RAG application.

- visit https://localhost:8000 in your browser

#### RAG
You should see Verba.  
Click Custom and then continue to the UI.  

Click Config.

We need to:
- configure our **Embedder** to
  - Ollama
  - `mxbai-embed-large:latest`
- configure our **Generator** to
  - Ollama
  - `llama3:latest`

Now lets add the blog posts to Verba so that we can chunk and embed them into the
Weaviate vector DB.  
You should see these files in the `blog_posts/` folder of this repo.

Click "Import Data" on the top.  
Click "Directory" > "Default" on the middle-left.  
Click "Import All"

Once this process is finished,  
Cluck "Chat"  
We should be able to ask questions like:
- "How does flox change my team workflow?"
- "What companies use Nix?"
- "How can I bring Nix to work?"

We've spun up a Local AI app with a `git clone` and a `flox activate`.

This is a moderately ambitious demo.  
There are so many different types of hardware, that not everything will perform well
or be capable of running these models.  
You may need to close some applications and stop Docker Desktop.  
(This demo does work on a base M1 mac)  
If it's not fully working on your machine, find a buddy :)

#### saving battery 🔋
One more thing...
```bash
exit
```
Now check https://localhost:8000

When we close the last shell that is using a flox environment, Flox will shut down
all of the services automatically.  
We can just close our shells and send an email or close our laptops without wasting any more battery.


### 3. Your workflow 💻

#### forking with `pull --copy`
We run a service called [FloxHub](https://hub.flox.dev).  
This is a great place to get [example environments](https://github.com/flox/floxenvs).

For instance, say you want to start hacking on a postgres database.  
You could make a new folder:
```bash
cd ~
mkdir pg-hack
```
And then just pull a sample env:
```bash
flox pull --copy flox/postgres
```
We've basically forked an example.  
Now activate and `--start-services`/`-s`:

The environment will make sure a database is created.

Now we can install a programming language:
```bash
flox install go
```
And now you're ready to write a go app against a postgres db running natively on
your machine.

#### Your own quest
Flox is simple nix, presented to the builder in you.  
What do you want to build?  
Make a folder and run `flox init`, or copy an [example environment](https://github.com/flox/floxenvs).  
Then hack on it and make it your own!  

To push it to FloxHub, run:
```
flox push
```
You can authenticate with your GitHub account :)

We want to help you and your teammates build whatever you want without the friction
of installing the wrong tools and dependencies.

Whatever you push to FloxHub, consider it good enough for an entry to our giveaway:
https://go.flox.dev/pushtowin

It's a great way to leave us feedback too!
We hope `flox` can help you bring the Nix value of reproducible, reliable tools to
your $HOME workflow, your team, and your projects -- thanks!

### Side quests: 🏹
- Look around https://search.nixos.org/, find a package and click on its OS-architecture
  combinations (`aarch-darwin` is for Apple Silicon Macs / `x86_64-linux` is a typical Linux Server)
  You'll be presented with build jobs from Hydra, the public Nixpkgs build system.
- Visit https://github.com/nixos/nixpkgs. This is the central git repo where over
  5,000 contributors have made 700,000 commits to define every package over 2 decades.
- Check your default environment `~/.flox` into a git repo.
- Create an environment on your machine. Clone it on another machine using a different
  operating system or CPU architecture.
- Push your environment to GitHub or FloxHub and share it with someone!

---

## Additional Resources 📚

- **Documentation:**  
  - https://flox.dev/docs
  - https://nixos.org/guides/how-nix-works/

- **Demo Repo**:
  - https://github.com/stealthybox/verba-with-flox

- **Further Reading:**  
  - https://flox.dev/blog
  - https://flox.dev/blog/get-a-portable-turn-key-rag-stack-with-verba-and-flox/ 
  - https://flox.dev/blog/onboarding-made-easy-with-github-and-flox/

---

## Join Slack! 🎉
https://floxcommunitygroup.slack.com

## File an Issue 📄
https://github.com/flox/flox/issues
