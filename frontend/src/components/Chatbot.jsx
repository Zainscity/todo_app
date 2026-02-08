import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const Chatbot = () => {
    const { user } = useAuth();
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const handleSend = async () => {
        if (input.trim() === '') return;

        const newMessages = [...messages, { text: input, sender: 'user' }];
        setMessages(newMessages);
        setInput('');

        // Send message to backend
        const response = await fetch('http://localhost:8000/api/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ message: input, user_id: user.id }),
        });

        const data = await response.json();
        setMessages([...newMessages, { text: data.response, sender: 'bot' }]);
    };

    return (
        <div className="flex flex-col w-full max-w-lg mx-auto min-h-[500px] bg-white shadow-lg rounded-lg">
            <div className="flex-1 overflow-y-auto p-4">
                {messages.map((message, index) => (
                    <div key={index} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} mb-2`}>
                        <div className={`p-2 rounded-xl ${message.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'}`}>
                            {message.text}
                        </div>
                    </div>
                ))}
            </div>
            <div className="p-4">
                <div className="flex">
                                            <input
                                            type="text"
                                            className="flex-1 border-gray-300 rounded-l-xl p-2 text-gray-900"
                                            value={input}                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    />
                    <button className="bg-blue-500 text-white rounded-r-xl px-4 py-2" onClick={handleSend}>
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Chatbot;

