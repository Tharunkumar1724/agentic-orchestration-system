import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaComments, FaPaperPlane, FaRobot, FaUser, FaTrash, FaPlus, FaProjectDiagram } from 'react-icons/fa';
import axios from 'axios';
import WorkflowCommunicationGraph from './WorkflowCommunicationGraph';

const API_BASE_URL = 'http://localhost:8000';

const Message = ({ message, isUser }) => {
  const isWorkflowMessage = message.type === 'workflow' || message.workflowExecution;
  const isAgentMessage = message.type === 'agent';
  const isSystemMessage = message.type === 'system';
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex gap-3 ${isUser ? 'flex-row-reverse' : ''}`}
    >
      <div className={`p-3 rounded-full flex-shrink-0 ${
        isUser 
          ? 'bg-gradient-to-br from-agent-primary to-agent-secondary' 
          : isAgentMessage 
          ? 'bg-gradient-to-br from-blue-600 to-blue-700'
          : isSystemMessage
          ? 'bg-gradient-to-br from-gray-600 to-gray-700'
          : 'bg-gradient-to-br from-purple-500 to-pink-500'
      }`}>
        {isUser ? <FaUser className="text-xl" /> : <FaRobot className="text-xl" />}
      </div>
      <div className={`max-w-[70%] ${isUser ? 'text-right' : ''}`}>
        {isAgentMessage && message.agent && (
          <div className="mb-1 px-2">
            <span className="text-xs font-bold text-blue-400">{message.agent}</span>
          </div>
        )}
        <div className={`p-4 rounded-2xl ${
          isUser 
            ? 'bg-agent-primary bg-opacity-20 border border-agent-primary' 
            : isAgentMessage
            ? 'bg-gray-800 border border-blue-700'
            : isSystemMessage
            ? 'bg-gray-800/50 border border-gray-700'
            : 'bg-dark-card border border-dark-border'
        }`}>
          <p className="whitespace-pre-wrap text-gray-200">{message.content}</p>
          
          {/* Show tools used if available */}
          {message.tools && message.tools.length > 0 && (
            <div className="flex gap-1 mt-2 flex-wrap">
              {message.tools.map((tool, idx) => (
                <span key={idx} className="text-xs px-2 py-0.5 rounded-full bg-blue-600/30 text-blue-300 border border-blue-500/30">
                  {tool}
                </span>
              ))}
            </div>
          )}
          
          {/* Show tool results if available */}
          {message.toolResults && Object.keys(message.toolResults).length > 0 && (
            <div className="mt-2 p-2 bg-gray-900/50 rounded border border-gray-700">
              <p className="text-xs text-gray-400 mb-1">Tool Results:</p>
              {Object.entries(message.toolResults).map(([tool, result], idx) => (
                <div key={idx} className="text-xs text-green-400 font-mono truncate">
                  {tool}: {typeof result === 'string' ? result.substring(0, 60) : JSON.stringify(result).substring(0, 60)}...
                </div>
              ))}
            </div>
          )}
        </div>
        <p className="text-xs text-gray-500 mt-1 px-2">
          {new Date(message.timestamp).toLocaleTimeString()}
        </p>
      </div>
    </motion.div>
  );
};

const SessionCard = ({ session, isActive, onClick, onDelete }) => {
  const sessionName = session.name || session.metadata?.name || session.session_id;
  
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className={`p-4 rounded-lg cursor-pointer transition-all ${
        isActive 
          ? 'bg-gradient-to-r from-purple-500 to-pink-500 shadow-lg' 
          : 'bg-dark-card hover:bg-dark-hover border border-dark-border'
      }`}
      onClick={onClick}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <h4 className="font-semibold truncate">{sessionName}</h4>
          <p className="text-xs text-gray-400 mt-1">
            {session.messages?.length || 0} messages
          </p>
        </div>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onDelete(session.session_id);
          }}
          className="p-2 rounded-lg hover:bg-red-500 hover:bg-opacity-20 transition-colors"
        >
          <FaTrash className="text-sm" />
        </button>
      </div>
    </motion.div>
  );
};

const Chat = () => {
  const [sessions, setSessions] = useState([]);
  const [activeSession, setActiveSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [workflows, setWorkflows] = useState([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);
  const [agents, setAgents] = useState([]);
  const [communicationLog, setCommunicationLog] = useState([]);
  const [showWorkflowViz, setShowWorkflowViz] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetchSessions();
    fetchWorkflows();
    fetchAgents();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchSessions = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/chat/sessions`);
      setSessions(response.data);
      if (response.data.length > 0 && !activeSession) {
        loadSession(response.data[0].session_id);
      }
    } catch (error) {
      console.error('Error fetching sessions:', error);
    }
  };

  const fetchWorkflows = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/workflows`);
      setWorkflows(response.data);
    } catch (error) {
      console.error('Error fetching workflows:', error);
    }
  };

  const fetchAgents = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/agents`);
      setAgents(response.data);
    } catch (error) {
      console.error('Error fetching agents:', error);
    }
  };

  const loadSession = async (sessionId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/chat/sessions/${sessionId}`);
      setActiveSession(sessionId);
      setMessages(response.data.messages || []);
    } catch (error) {
      console.error('Error loading session:', error);
    }
  };

  const createNewSession = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/chat/sessions`, {
        name: `Chat ${new Date().toLocaleString()}`,
      });
      const newSessionId = response.data.session_id;
      await fetchSessions();
      // Load the new session
      setActiveSession(newSessionId);
      setMessages([]);
      setSelectedWorkflow(null);
      setCommunicationLog([]);
      setShowWorkflowViz(false);
    } catch (error) {
      console.error('Error creating session:', error);
      alert('Failed to create new chat session. Please check if the backend is running.');
    }
  };

  const deleteSession = async (sessionId) => {
    if (window.confirm('Are you sure you want to delete this chat session?')) {
      try {
        await axios.delete(`${API_BASE_URL}/chat/sessions/${sessionId}`);
        if (activeSession === sessionId) {
          setActiveSession(null);
          setMessages([]);
        }
        await fetchSessions();
      } catch (error) {
        console.error('Error deleting session:', error);
      }
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || !activeSession) return;

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const query = inputMessage;
    setInputMessage('');
    setLoading(true);

    try {
      // If workflow is selected, run workflow execution with message
      if (selectedWorkflow) {
        // Add system message for each execution
        const systemMsg = {
          type: 'system',
          content: `🚀 Executing workflow: ${selectedWorkflow.name}`,
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, systemMsg]);
        
        // Reset communication log for this new execution
        const currentCommLog = [];
        
        // Execute workflow
        const response = await axios.post(`${API_BASE_URL}/workflows/${selectedWorkflow.id}/run`, {
          query: query,
        });
        
        console.log('Workflow execution response:', response.data);
        
        // Extract communication log for visualization
        const commLog = response.data?.meta?.communication_log || [];
        
        // Update communication log (append to existing for continuous view)
        setCommunicationLog((prev) => [...prev, ...commLog]);
        setShowWorkflowViz(true);
        
        // Process communication log to show agent messages
        if (commLog.length > 0) {
          for (let i = 0; i < commLog.length; i++) {
            const logEntry = commLog[i];
            
            // Wait a bit between messages for visual effect
            await new Promise(resolve => setTimeout(resolve, 400));
            
            // Extract content safely
            let messageContent = '';
            if (logEntry.content) {
              if (typeof logEntry.content === 'object' && logEntry.content.llm_response) {
                messageContent = logEntry.content.llm_response;
              } else if (typeof logEntry.content === 'object') {
                messageContent = JSON.stringify(logEntry.content, null, 2);
              } else {
                messageContent = logEntry.content;
              }
            } else {
              messageContent = 'Processing...';
            }
            
            const agentMsg = {
              type: 'agent',
              agent: logEntry.agent || logEntry.sender || 'Agent',
              content: messageContent,
              tools: logEntry.content?.tools_used || logEntry.tools_used || [],
              toolResults: logEntry.content?.tool_results || logEntry.tool_results || {},
              timestamp: new Date().toISOString(),
            };
            
            setMessages((prev) => [...prev, agentMsg]);
          }
        }
        
        // Add final result if available
        const finalOutput = response.data?.result?.final_output || 
                           response.data?.final_output;
        
        if (finalOutput && typeof finalOutput === 'string') {
          await new Promise(resolve => setTimeout(resolve, 500));
          const finalMsg = {
            type: 'result',
            content: `✅ Workflow Complete!\n\n${finalOutput}`,
            timestamp: new Date().toISOString(),
          };
          setMessages((prev) => [...prev, finalMsg]);
        } else {
          // If no final output, show summary
          const resultSummary = `✅ Workflow "${selectedWorkflow.name}" completed successfully!\n\nProcessed ${commLog.length} agent steps.`;
          const summaryMsg = {
            type: 'result',
            content: resultSummary,
            timestamp: new Date().toISOString(),
          };
          setMessages((prev) => [...prev, summaryMsg]);
        }
        
      } else {
        // Regular chat message
        const response = await axios.post(`${API_BASE_URL}/chat/sessions/${activeSession}/message`, {
          message: query,
        });

        const assistantMessage = {
          role: 'assistant',
          content: response.data.response,
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      let errorMsg = 'Sorry, I encountered an error processing your message.';
      
      if (error.response?.data?.detail) {
        errorMsg = `Error: ${error.response.data.detail}`;
      } else if (error.message.includes('Network Error')) {
        errorMsg = 'Network error. Please check your connection and ensure the backend server is running.';
      } else if (error.code === 'ECONNREFUSED') {
        errorMsg = 'Cannot connect to the backend server. Please make sure it is running on port 8000.';
      }
      
      const errorMessage = {
        role: 'assistant',
        content: errorMsg,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-full gap-6">
      {/* Sidebar - Sessions */}
      <div className="w-80 flex flex-col gap-4">
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold flex items-center gap-2">
              <FaComments className="text-purple-500" />
              Chat Sessions
            </h2>
            <button
              onClick={createNewSession}
              className="p-2 rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 hover:shadow-lg transition-all"
            >
              <FaPlus />
            </button>
          </div>

          <div className="space-y-2 max-h-[calc(100vh-300px)] overflow-y-auto">
            {sessions.map((session) => (
              <SessionCard
                key={session.session_id}
                session={session}
                isActive={activeSession === session.session_id}
                onClick={() => loadSession(session.session_id)}
                onDelete={deleteSession}
              />
            ))}
          </div>

          {sessions.length === 0 && (
            <div className="text-center py-8 text-gray-400">
              <p className="mb-4">No chat sessions yet</p>
              <button
                onClick={createNewSession}
                className="btn-primary bg-gradient-to-r from-purple-500 to-pink-500"
              >
                <FaPlus className="inline mr-2" />
                Start New Chat
              </button>
            </div>
          )}
        </div>

        {/* Workflow Selector */}
        <div className="card p-4">
          <h3 className="text-sm font-bold flex items-center gap-2 mb-3">
            <FaProjectDiagram className="text-blue-500" />
            Select Workflow
          </h3>
          <select
            value={selectedWorkflow?.id || ''}
            onChange={(e) => {
              const wf = workflows.find(w => w.id === e.target.value);
              setSelectedWorkflow(wf || null);
              setCommunicationLog([]);
              setShowWorkflowViz(!!wf);
            }}
            className="w-full px-3 py-2 bg-dark-bg border border-dark-border rounded-lg text-sm focus:border-purple-500 focus:outline-none"
          >
            <option value="">💬 Normal Chat (No Workflow)</option>
            {workflows.map((wf) => (
              <option key={wf.id} value={wf.id}>
                🔄 {wf.name} ({wf.nodes?.length || 0} agents)
              </option>
            ))}
          </select>
          {selectedWorkflow && (
            <div className="mt-3 p-3 bg-blue-600/10 rounded-lg border border-blue-500/30">
              <p className="text-xs font-semibold text-blue-400 mb-1">Active Workflow</p>
              <p className="text-xs text-gray-300">{selectedWorkflow.name}</p>
              <p className="text-xs text-gray-400 mt-1">
                {selectedWorkflow.nodes?.length || 0} agents • {selectedWorkflow.type || 'sequence'} type
              </p>
              {selectedWorkflow.description && (
                <p className="text-xs text-gray-500 mt-2">{selectedWorkflow.description}</p>
              )}
              <button
                onClick={() => {
                  setSelectedWorkflow(null);
                  setCommunicationLog([]);
                  setShowWorkflowViz(false);
                }}
                className="mt-2 w-full px-2 py-1 text-xs bg-red-600/20 hover:bg-red-600/30 rounded border border-red-500/30 text-red-400 transition-colors"
              >
                Clear Workflow
              </button>
            </div>
          )}
          {!selectedWorkflow && (
            <div className="mt-3 p-3 bg-gray-800/50 rounded-lg border border-gray-700">
              <p className="text-xs text-gray-400">
                💬 Normal chat mode - Select a workflow above to enable workflow execution
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 card flex flex-col">
        {activeSession ? (
          <>
            {/* Header */}
            <div className="p-6 border-b border-dark-border flex items-center justify-between">
              <div className="flex-1">
                <h2 className="text-2xl font-bold">Chat</h2>
                <p className="text-sm text-gray-400">
                  {selectedWorkflow 
                    ? `🔄 Workflow Mode: ${selectedWorkflow.name} - Send messages to execute` 
                    : '💬 Normal Chat - Ask questions and get AI responses'}
                </p>
              </div>
              {selectedWorkflow && (
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setShowWorkflowViz(!showWorkflowViz)}
                    className={`px-4 py-2 rounded-lg transition-all flex items-center gap-2 text-sm font-semibold ${
                      showWorkflowViz 
                        ? 'bg-blue-600 hover:bg-blue-700' 
                        : 'bg-gray-700 hover:bg-gray-600'
                    }`}
                  >
                    <FaProjectDiagram />
                    {showWorkflowViz ? 'Hide Graph' : 'Show Graph'}
                  </button>
                  {communicationLog.length > 0 && (
                    <div className="px-3 py-2 bg-green-600/20 rounded-lg border border-green-500/30">
                      <span className="text-xs font-semibold text-green-400">
                        {communicationLog.length} steps executed
                      </span>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Chat Content - Split view when workflow is active */}
            <div className="flex-1 flex overflow-hidden">
              {/* Messages Area */}
              <div className={`${showWorkflowViz && selectedWorkflow ? 'w-1/2' : 'w-full'} flex flex-col`}>
                <div className="flex-1 overflow-y-auto p-6 space-y-6">
                  {messages.length === 0 && !loading && (
                    <div className="flex flex-col items-center justify-center h-full text-center">
                      <FaComments className="text-6xl text-purple-500 mb-4 opacity-50" />
                      <h3 className="text-xl font-bold text-gray-400 mb-2">
                        {selectedWorkflow ? 'Workflow Chat Ready' : 'Start a Conversation'}
                      </h3>
                      <p className="text-gray-500 max-w-md">
                        {selectedWorkflow 
                          ? `Type a message below to execute the "${selectedWorkflow.name}" workflow and see the results.`
                          : 'Type a message below to start chatting. You can also select a workflow to execute it with your queries.'}
                      </p>
                    </div>
                  )}
                  
                  <AnimatePresence>
                    {messages.map((message, index) => (
                      <Message
                        key={index}
                        message={message}
                        isUser={message.role === 'user'}
                      />
                    ))}
                  </AnimatePresence>

                  {loading && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="flex gap-3"
                    >
                      <div className="p-3 rounded-full bg-gradient-to-br from-purple-500 to-pink-500">
                        <FaRobot className="text-xl" />
                      </div>
                      <div className="bg-dark-card border border-dark-border p-4 rounded-2xl">
                        <div className="flex gap-2">
                          <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                          <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                        </div>
                      </div>
                    </motion.div>
                  )}

                  <div ref={messagesEndRef} />
                </div>

                {/* Input */}
                <form onSubmit={sendMessage} className="p-6 border-t border-dark-border">
                  {selectedWorkflow && messages.length > 0 && (
                    <div className="mb-3 flex items-center justify-between">
                      <p className="text-xs text-gray-400">
                        💡 Tip: Each message executes the workflow again with your new query
                      </p>
                      <button
                        type="button"
                        onClick={() => {
                          setCommunicationLog([]);
                          setMessages([]);
                        }}
                        className="px-3 py-1 text-xs bg-gray-700 hover:bg-gray-600 rounded transition-colors"
                      >
                        Clear History
                      </button>
                    </div>
                  )}
                  <div className="flex gap-4">
                    <input
                      type="text"
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      placeholder={selectedWorkflow ? `Send query to ${selectedWorkflow.name}...` : "Type your message..."}
                      className="flex-1 input-field"
                      disabled={loading}
                    />
                    <button
                      type="submit"
                      disabled={loading || !inputMessage.trim()}
                      className="px-6 py-3 rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                    >
                      <FaPaperPlane />
                      {selectedWorkflow ? 'Execute' : 'Send'}
                    </button>
                  </div>
                  {selectedWorkflow && (
                    <p className="text-xs text-gray-500 mt-2 text-center">
                      🔄 Workflow will run for each message • Results stack in chat
                    </p>
                  )}
                </form>
              </div>

              {/* Workflow Visualization Panel */}
              {showWorkflowViz && selectedWorkflow && communicationLog.length > 0 && (
                <div className="w-1/2 border-l border-dark-border bg-dark-bg">
                  <div className="p-3 bg-gray-900 border-b border-dark-border">
                    <div className="flex items-center justify-between">
                      <h3 className="text-sm font-bold text-gray-300">Workflow Execution Graph</h3>
                      <div className="text-xs text-gray-400">
                        Live visualization
                      </div>
                    </div>
                  </div>
                  <div className="h-full">
                    <WorkflowCommunicationGraph
                      workflow={selectedWorkflow}
                      agents={agents}
                      communicationLog={communicationLog}
                      isExecuting={loading}
                    />
                  </div>
                </div>
              )}
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-gray-400">
            <div className="text-center">
              <FaComments className="text-6xl mx-auto mb-4 text-gray-600" />
              <p className="text-xl mb-2">No chat session selected</p>
              <p className="text-sm">Create a new session or select an existing one to start chatting</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Chat;
