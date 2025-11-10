import React, { useState, useEffect, useRef } from 'react';
import { FaPlay, FaStop, FaCheckCircle, FaSpinner, FaArrowRight, FaBrain, FaNetworkWired } from 'react-icons/fa';
import MetricsDisplay from './MetricsDisplay';

function SolutionExecutionView({ solution, onClose }) {
  const [ws, setWs] = useState(null);
  const [executing, setExecuting] = useState(false);
  const [workflowStates, setWorkflowStates] = useState({});
  const [handoffs, setHandoffs] = useState([]);
  const [summary, setSummary] = useState(null);
  const [overallMetrics, setOverallMetrics] = useState(null);  // Add overall metrics state
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    console.log('🔌 Connecting to WebSocket for solution:', solution.id);
    const websocket = new WebSocket(`ws://localhost:8000/solutions/ws/${solution.id}`);
    
    websocket.onopen = () => {
      console.log('✅ Solution WebSocket connected!');
      setWs(websocket);
    };
    
    websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('📨 Received WebSocket message:', data);
        handleWebSocketMessage(data);
      } catch (e) {
        console.error('❌ WebSocket message error:', e);
      }
    };
    
    websocket.onerror = (error) => {
      console.error('❌ WebSocket error:', error);
      setError('WebSocket connection error');
    };
    
    websocket.onclose = () => {
      console.log('🔌 Solution WebSocket disconnected');
      setWs(null);
    };
    
    return () => {
      console.log('🧹 Cleaning up WebSocket');
      if (websocket.readyState === WebSocket.OPEN) {
        websocket.close();
      }
    };
  }, [solution.id]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [workflowStates, handoffs]);

  function handleWebSocketMessage(message) {
    console.log('📥 Processing message type:', message.type, message);

    switch (message.type) {
      case 'execution_started':
        console.log('▶️ Execution started!');
        setExecuting(true);
        setWorkflowStates({});
        setHandoffs([]);
        setSummary(null);
        setError(null);
        break;

      case 'workflow_started':
        console.log('🔄 Workflow started:', message.workflow_name);
        setWorkflowStates(prev => ({
          ...prev,
          [message.workflow_id]: {
            name: message.workflow_name,
            status: 'running',
            position: message.position,
            total: message.total
          }
        }));
        break;

      case 'handoff_prepared':
        console.log('🤝 Handoff prepared:', message.from_workflow, '→', message.to_workflow);
        setHandoffs(prev => [...prev, {
          from: message.from_workflow,
          to: message.to_workflow,
          data: message.handoff_data,
          timestamp: new Date().toISOString()
        }]);
        break;

      case 'workflow_completed':
        console.log('✅ Workflow completed:', message.workflow_id);
        setWorkflowStates(prev => ({
          ...prev,
          [message.workflow_id]: {
            ...prev[message.workflow_id],
            status: 'completed',
            kag: message.kag_analysis,
            output: message.output,
            metrics: message.metrics  // Capture metrics from WebSocket message
          }
        }));
        break;

      case 'execution_completed':
        console.log('🎉 Execution completed!');
        setExecuting(false);
        setSummary(message.summary);
        setOverallMetrics(message.overall_metrics);  // Capture overall metrics
        break;

      case 'error':
        console.error('❌ Error:', message.message);
        setError(message.message);
        setExecuting(false);
        break;

      default:
        console.log('❓ Unknown message type:', message.type);
    }
  }

  function startExecution() {
    console.log('🚀 Starting execution, ws state:', ws?.readyState);
    if (ws && ws.readyState === WebSocket.OPEN) {
      console.log('📤 Sending execute command for solution:', solution.id);
      ws.send(JSON.stringify({ action: 'execute' }));
    } else {
      console.error('❌ WebSocket not ready:', ws?.readyState);
      setError('WebSocket not connected. Readiness: ' + (ws?.readyState || 'null'));
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-lg shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col border border-purple-500/30">
        {/* Header */}
        <div className="p-6 border-b border-gray-800 flex justify-between items-center bg-gradient-to-r from-purple-900/20 to-blue-900/20">
          <div>
            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
              <FaBrain className="text-purple-400" />
              {solution.name}
            </h2>
            <p className="text-gray-400 mt-1">{solution.description}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white text-2xl transition-colors"
          >
            ×
          </button>
        </div>

        {/* Control Panel */}
        <div className="p-4 border-b border-gray-800 bg-gray-900/50">
          <div className="flex gap-4 items-center">
            <button
              onClick={startExecution}
              disabled={executing || !ws}
              className="px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {executing ? (
                <>
                  <FaSpinner className="animate-spin" />
                  Executing...
                </>
              ) : (
                <>
                  <FaPlay />
                  Start Execution
                </>
              )}
            </button>

            {!ws && (
              <span className="text-yellow-400 text-sm">Connecting...</span>
            )}

            {executing && (
              <span className="text-green-400 text-sm flex items-center gap-2">
                <FaSpinner className="animate-spin" />
                AI is orchestrating workflows...
              </span>
            )}
          </div>
        </div>

        {/* Execution View */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {error && (
            <div className="bg-red-900/20 border border-red-500 text-red-300 p-4 rounded-lg">
              {error}
            </div>
          )}

          {/* Visual Workflow Chain */}
          {Object.keys(workflowStates).length > 0 && (
            <div className="space-y-6">
              <h3 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
                <FaNetworkWired className="text-purple-400" />
                Live Workflow Communication Chain
              </h3>
              
              <div className="flex flex-col items-center space-y-6">
                {Object.entries(workflowStates).map(([workflowId, state], index) => (
                  <div key={workflowId} className="w-full max-w-4xl">
                    {/* Workflow Node */}
                    <div className={`relative border-2 rounded-xl p-6 transition-all transform ${
                      state.status === 'running' 
                        ? 'border-blue-500 bg-gradient-to-br from-blue-900/30 to-blue-800/20 shadow-lg shadow-blue-500/50 scale-105' 
                        : state.status === 'completed' 
                        ? 'border-green-500 bg-gradient-to-br from-green-900/20 to-green-800/10 shadow-lg shadow-green-500/30' 
                        : 'border-gray-700 bg-gray-800/50'
                    }`}>
                      {/* Status Badge */}
                      <div className="absolute -top-3 -right-3">
                        {state.status === 'running' && (
                          <div className="bg-blue-600 text-white px-4 py-2 rounded-full flex items-center gap-2 shadow-lg animate-pulse">
                            <FaSpinner className="animate-spin" />
                            <span className="font-semibold">Running</span>
                          </div>
                        )}
                        {state.status === 'completed' && (
                          <div className="bg-green-600 text-white px-4 py-2 rounded-full flex items-center gap-2 shadow-lg">
                            <FaCheckCircle />
                            <span className="font-semibold">Complete</span>
                          </div>
                        )}
                      </div>

                      {/* Workflow Header */}
                      <div className="mb-4">
                        <div className="flex items-center gap-3 mb-2">
                          <div className="w-10 h-10 rounded-full bg-purple-600 flex items-center justify-center text-white font-bold text-lg">
                            {state.position}
                          </div>
                          <div>
                            <h4 className="text-xl font-bold text-white">{state.name}</h4>
                            <p className="text-sm text-gray-400">
                              Workflow {state.position} of {state.total}
                            </p>
                          </div>
                        </div>
                      </div>

                      {/* AI Analysis Results */}
                      {state.kag && (
                        <div className="space-y-4 bg-purple-900/20 border border-purple-500/30 rounded-lg p-5">
                          <div className="flex items-center gap-2 text-purple-300 font-semibold text-lg border-b border-purple-500/30 pb-2">
                            <FaBrain className="text-xl" />
                            Gemini AI Analysis
                          </div>
                          
                          {/* Summary */}
                          <div className="bg-black/30 rounded-lg p-4">
                            <p className="text-xs text-gray-400 font-semibold mb-2 uppercase">Summary</p>
                            <p className="text-white leading-relaxed">{state.kag.summary}</p>
                          </div>

                          {/* Facts Grid */}
                          {state.kag.facts && state.kag.facts.length > 0 && (
                            <div className="bg-black/30 rounded-lg p-4">
                              <p className="text-xs text-gray-400 font-semibold mb-3 uppercase">
                                Extracted Facts ({state.kag.facts.length})
                              </p>
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                                {state.kag.facts.map((fact, i) => (
                                  <div key={i} className="bg-green-900/20 border border-green-500/30 rounded px-3 py-2 flex items-start gap-2">
                                    <span className="text-green-400 mt-0.5 text-sm">✓</span>
                                    <span className="text-green-100 text-sm">{fact}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Reasoning */}
                          {state.kag.reasoning && (
                            <div className="bg-black/30 rounded-lg p-4">
                              <p className="text-xs text-gray-400 font-semibold mb-2 uppercase">AI Reasoning</p>
                              <p className="text-blue-200 text-sm leading-relaxed italic">{state.kag.reasoning}</p>
                            </div>
                          )}
                        </div>
                      )}

                      {/* Workflow Metrics */}
                      {state.metrics && (
                        <div className="mt-6">
                          <MetricsDisplay 
                            metrics={state.metrics} 
                            title={`${state.name} - Performance Metrics`}
                          />
                        </div>
                      )}
                    </div>

                    {/* Communication Arrow & Handoff */}
                    {index < Object.keys(workflowStates).length - 1 && (
                      <div className="flex flex-col items-center my-6 relative">
                        {/* Animated Arrow */}
                        <div className="relative h-16 w-1 bg-gradient-to-b from-purple-500 to-yellow-500 rounded-full">
                          <div className="absolute top-0 w-1 h-8 bg-white animate-pulse rounded-full"></div>
                        </div>
                        <div className="text-yellow-400 text-3xl -mt-2">
                          ▼
                        </div>

                        {/* Handoff Data Card */}
                        {handoffs[index] && (
                          <div className="w-full max-w-2xl bg-gradient-to-r from-yellow-900/30 to-orange-900/30 border-2 border-yellow-500/50 rounded-lg p-5 mt-4 relative overflow-hidden">
                            {/* Glow Effect */}
                            <div className="absolute inset-0 bg-yellow-400/5 animate-pulse"></div>
                            
                            <div className="relative z-10">
                              <div className="flex items-center gap-3 mb-4">
                                <FaArrowRight className="text-yellow-400 text-2xl animate-bounce" />
                                <div>
                                  <span className="text-yellow-300 font-bold text-lg">AI-Powered Handoff</span>
                                  <p className="text-yellow-200/70 text-xs">Context transfer from Workflow {index + 1} → {index + 2}</p>
                                </div>
                              </div>
                              
                              <div className="space-y-3 bg-black/40 rounded-lg p-4">
                                {handoffs[index].data?.handoff_data && (
                                  <div>
                                    <span className="text-gray-300 text-sm font-semibold block mb-1">📦 Data Passed:</span>
                                    <div className="bg-yellow-900/30 border border-yellow-600/30 rounded p-3 text-white text-sm">
                                      {typeof handoffs[index].data.handoff_data === 'string' 
                                        ? handoffs[index].data.handoff_data 
                                        : JSON.stringify(handoffs[index].data.handoff_data, null, 2)
                                      }
                                    </div>
                                  </div>
                                )}
                                {handoffs[index].data?.relevance && (
                                  <div>
                                    <span className="text-gray-300 text-sm font-semibold block mb-1">🎯 Relevance:</span>
                                    <p className="text-yellow-100 text-sm">{handoffs[index].data.relevance}</p>
                                  </div>
                                )}
                                {handoffs[index].data?.context && (
                                  <div>
                                    <span className="text-gray-300 text-sm font-semibold block mb-1">💡 Context:</span>
                                    <p className="text-orange-100 text-sm">{handoffs[index].data.context}</p>
                                  </div>
                                )}
                                {handoffs[index].data?.facts && handoffs[index].data.facts.length > 0 && (
                                  <div>
                                    <span className="text-gray-300 text-sm font-semibold block mb-1">📌 Key Facts ({handoffs[index].data.facts.length}):</span>
                                    <ul className="space-y-1">
                                      {handoffs[index].data.facts.map((fact, i) => (
                                        <li key={i} className="text-green-300 text-xs flex items-start gap-2">
                                          <span className="text-green-500">•</span>
                                          <span>{fact}</span>
                                        </li>
                                      ))}
                                    </ul>
                                  </div>
                                )}
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Workflow Progress - OLD VERSION REMOVED */}
          {Object.keys(workflowStates).length === 0 && !error && (
            <div className="text-center text-gray-500 py-20">
              <FaNetworkWired className="text-6xl mx-auto mb-4 opacity-30" />
              <p className="text-lg">Click "Start Execution" to begin workflow orchestration</p>
              <p className="text-sm mt-2">Watch AI analyze and pass context between workflows in real-time</p>
            </div>
          )}

          {/* Final Summary */}
          {summary && (
            <div className="space-y-6 mt-6">
              {/* Overall Solution Metrics */}
              {overallMetrics && (
                <MetricsDisplay 
                  metrics={overallMetrics} 
                  title="Overall Solution Performance"
                />
              )}

              {/* AI Summary */}
              <div className="bg-gradient-to-br from-purple-900/30 to-blue-900/30 border border-purple-500/50 rounded-lg p-6">
                <h3 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                  <FaCheckCircle className="text-green-400" />
                  Solution Complete - AI Summary
                </h3>
                
                <div className="space-y-4">
                  <div>
                    <p className="text-gray-400 text-sm mb-1">Total Workflows:</p>
                    <p className="text-white text-lg font-semibold">{summary.total_workflows}</p>
                  </div>

                  {summary.overall_context && (
                    <div>
                      <p className="text-gray-400 text-sm mb-1">Overall Context:</p>
                      <p className="text-white">{summary.overall_context}</p>
                    </div>
                  )}

                  {summary.combined_facts && summary.combined_facts.length > 0 && (
                    <div>
                      <p className="text-gray-400 text-sm mb-2">All Facts Collected:</p>
                      <div className="bg-black/30 rounded p-4 max-h-48 overflow-y-auto">
                        <ul className="space-y-1">
                          {summary.combined_facts.map((fact, i) => (
                            <li key={i} className="text-green-300 text-sm flex items-start gap-2">
                              <span className="text-green-500">•</span>
                              <span>{fact}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>
    </div>
  );
}

export default SolutionExecutionView;
