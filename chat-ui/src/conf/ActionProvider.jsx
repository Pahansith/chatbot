import React from 'react';
import axios from 'axios';

const ActionProvider = ({ createChatBotMessage, setState, children }) => {
  const handleBackendCall = async (userMessage) => {
    const reply = await axios.post('http://localhost:5000/chat', {message: userMessage})
    console.log(reply)
    const botMessage = createChatBotMessage(reply.data.response);
    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));
  };



  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {handleBackendCall},
        });
      })}
    </div>
  );
};

export default ActionProvider;