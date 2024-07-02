# Chatbot Application

## Overview
This application is a simple chatbot developed using TensorFlow and an LSTM (Long Short-Term Memory) recurrent neural network model. It includes two modules: `chat-ui` and `chat-backend`.

### Modules

#### chat-ui
- **Description**: A simple React chat UI application that demonstrates the capabilities of the chat server.
- **Technology**: Developed using [react-chatbot-kit](https://www.npmjs.com/package/react-chatbot-kit).

#### chat-backend
- **Description**: The backend of the chat app, built using an LSTM RNN model and TensorFlow.

## Getting Started

### Prerequisites
- Docker Desktop or any compatible Docker Runtime

### Installation and Setup

1. **Clone the Repository**
   - Clone the project to your local machine using the following command:
     ```bash
     git clone https://github.com/Pahansith/chatbot.git
     ```

2. **Navigate to Project Directory**
   - Change to the project directory:
     ```bash
     cd Chatbot
     ```

3. **Build and Run the Application**
   - Use Docker Compose to build and run the application:
     ```bash
     docker-compose up --build
     ```
