import React, { useState } from 'react';
import Dashboard from './components/Dashboard';
import Agents from './components/Agents';
import Tools from './components/Tools';
import Workflows from './components/Workflows';
import Solutions from './components/Solutions';
import SolutionsManagement from './components/SolutionsManagement';
import Chat from './components/Chat';
import Sidebar from './components/Sidebar';

function App() {
  const [view, setView] = useState('dashboard');
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);
  const [selectedSolution, setSelectedSolution] = useState(null);

  const handleViewSolution = (workflow, result) => {
    setSelectedWorkflow(workflow);
    setSelectedSolution(result);
    setView('solutions');
  };

  return (
    <div className="flex h-screen bg-dark-bg">
      <Sidebar onNavigate={setView} active={view} />
      <main className="flex-1 overflow-auto p-8">
        {view === 'dashboard' && <Dashboard onNavigate={setView} />}
        {view === 'agents' && <Agents />}
        {view === 'tools' && <Tools />}
        {view === 'workflows' && <Workflows onViewSolution={handleViewSolution} />}
        {view === 'solutions' && <SolutionsManagement />}
        {view === 'runs' && <Solutions />}
        {view === 'chat' && <Chat />}
      </main>
    </div>
  );
}

export default App;

