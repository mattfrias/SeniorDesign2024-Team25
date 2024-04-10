<h1 align="center">
  <br>
  <a href="https://www.cse.uconn.edu/"><img src="./assets/coe.png" alt="UConn School of Computing" width="100"></a>
  <a href="https://www.sonalysts.com/"><img src="./assets/sonalysts.png" alt="Sonalysts" width="100"></a>
  <br>
    CSE Senior Design - Team 25
		<p align="center"><small>Kubernetes Cloud Orchestration Simulation</small></p>
</h1>

<p align="center">
  <a href="#decision-analysis-report">Decision Analysis Report</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#download">Download</a> •
  <a href="#credits">Credits</a> •
  <a href="#acknowledgements">Acknowledgements</a>
</p>

## Project Goals

## Evaluation Criteria

## Decision Analysis Report

![DAR Table](./assets/dar-table.png)

## Key Features

- Manage Kubernetes Resources: Deploy, manage, and delete Kubernetes resources using a command-line interface
- Cluster Management: Create and delete Kubernetes clusters for simulation purposes
- Flexible Resource Application: Apply resource configurations from files with the option to deploy multiple instances
- Resource Deletion: Delete specific Kubernetes resources by type and name
- Resource Retrieval: Retrieve information about Kubernetes resources by type
- Insightful Pod Characteristics: View detailed characteristics of pods, including CPU and memory requests and limits
- Node Resource Allocation: Understand resource allocation on nodes within the Kubernetes cluster
- Seamless Integration: Interact with the Kubernetes cluster using familiar tools like `kubectl` and `kwokctl`
- Versatile Tool: Suitable for experimentation, testing, and development of Kubernetes-related solutions within a simulated environment

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com), [KWOK](https://kwok.sigs.k8s.io/docs/user/installation/) and [Python](https://www.python.org/) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/mattfrias/SeniorDesign2024-Team25.git

# Go into the repository
$ cd SeniorDesign2024-Team25

# Run the help section of the Python script to view available commands
$ python simulation.py --help

# Add configuration files to the 'resources' folder
```

> **Note**
> If you're using Linux Bash for Windows, [see this guide](https://www.howtogeek.com/261575/how-to-run-graphical-linux-desktop-applications-from-windows-10s-bash-shell/) or use `node` from the command prompt.

## Credits

This project uses the following software:

- [Kubernetes WithOut Kubelet (KWOK)](https://kwok.sigs.k8s.io/)
- [Python](https://www.python.org/)

## Acknowledgements

Our team would like to thank Professor Yufeng Wu, our Sonalysts advisor Matthew Ferrier, and the University of Connecticut’s College of Engineering for their support on this CSE design project.


