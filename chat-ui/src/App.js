
import Chatbot from 'react-chatbot-kit';
import 'react-chatbot-kit/build/main.css';
import config from './conf/config';
import MessageParser from './conf/MessageParser';
import ActionProvider from './conf/ActionProvider';
import './App.css'

function App() {
  return (
    <div className="App"> 
    <Chatbot
        config={config}
        messageParser={MessageParser}
        actionProvider={ActionProvider}
      />
      
    </div>
  );
}

export default App;
