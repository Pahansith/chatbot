import { createChatBotMessage } from 'react-chatbot-kit';
import Avatar from './Avatar';
import './Avatar.css'


const config = {
  initialMessages: [createChatBotMessage(`Hi! I'm Toby. How may I help you today`)],
  botName:"Toby",
  customComponents: {
    botAvatar: (props) => <Avatar {...props} />,
  }
};

export default config;