# Emotion Visualizer

## Overview

Patients who are going through emotional crisis need to visualize their emotional state. When user write their emotion with text, this model create a visualized image.

After suggesting an image, user is able to write down more detail description for the image, which is created based on their invisible states. CLIP model calculate the similarities between user input text and generaated image. If the similarities increase, it means that user becomes more obective and expression-able about what they feel. This 'visualizing' whole process will help patients to get better.

## Features

- Text-to-Image: Converts text input of emotions into visual representations.
- Similarities: with CLIP

## Setup Instructions

### Prerequisites

- Python 3.10+
- pip
- Docker (optional, for containerization)
