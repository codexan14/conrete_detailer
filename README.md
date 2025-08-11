# My Git Projects

This repository serves as a centralized collection of various personal and professional projects developed using Git for version control. Each sub-directory within this repository represents a distinct project, complete with its own codebase, documentation, and relevant files.

## Table of Contents

- [About](#about)
- [Projects](#projects)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About

This repository is a showcase of my work, demonstrating my skills in various programming languages, frameworks, and tools. It includes a diverse range of projects, from small scripts and command-line tools to more complex applications and web services. The primary goal is to maintain a well-organized and accessible portfolio of my coding endeavors.

## Projects

Below is a list of the projects currently hosted in this repository. Click on the links to navigate to each project's dedicated directory for more details.

*   **[Project 1: Name of Project 1](project1/)**
    *   *Description:* A brief overview of Project 1 and its main purpose.
    *   *Technologies Used:* Python, Flask, HTML, CSS
*   **[Project 2: Name of Project 2](project2/)**
    *   *Description:* A brief overview of Project 2 and its main purpose.
    *   *Technologies Used:* JavaScript, React, Node.js
*   **[Project 3: Name of Project 3](project3/)**
    *   *Description:* A brief overview of Project 3 and its main purpose.
    *   *Technologies Used:* Java, Spring Boot, MySQL
*   **[Project 4: Name of Project 4](project4/)**
    *   *Description:* A brief overview of Project 4 and its main purpose.
    *   *Technologies Used:* C++, OpenGL
*   **[Project 5: Name of Project 5](project5/)**
    *   *Description:* A brief overview of Project 5 and its main purpose.
    *   *Technologies Used:* Go, Docker, Kubernetes

*(Add more projects as you create them, following the same format)*

## Build the project: 

pyinstaller --noconsole --onefile gui/main.py --add-data "gui/img;gui/img" --add-data "core;core" --add-data "gui/tabs;gui/tabs" --hidden-import numpy --hidden-import pandas --hidden-import tkinter.filedialog --hidden-import PIL --hidden-import PIL.ImageFile  