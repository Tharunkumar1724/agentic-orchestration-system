import React, { useState } from 'react';
import { FaHome, FaRobot, FaTools, FaProjectDiagram, FaLightbulb, FaComments, FaBars, FaTimes } from 'react-icons/fa';

const Sidebar = ({ onNavigate, active }) => {
  const [collapsed, setCollapsed] = useState(false);

  const menuItems = [
    { id: 'dashboard', icon: FaHome, label: 'Dashboard', color: 'text-gray-400' },
    { id: 'agents', icon: FaRobot, label: 'Agents', color: 'text-agent-primary' },
    { id: 'tools', icon: FaTools, label: 'Tools', color: 'text-tool-primary' },
    { id: 'workflows', icon: FaProjectDiagram, label: 'Workflows', color: 'text-workflow-primary' },
    { id: 'solutions', icon: FaLightbulb, label: 'Solutions', color: 'text-solution-primary' },
    { id: 'chat', icon: FaComments, label: 'Chat', color: 'text-purple-500' },
  ];

  return (
    <div className={`${collapsed ? 'w-20' : 'w-64'} bg-dark-card border-r border-dark-border transition-all duration-300 flex flex-col`}>
      {/* Header */}
      <div className="p-6 border-b border-dark-border flex items-center justify-between">
        {!collapsed && <h1 className="text-xl font-bold">Agentic AI</h1>}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-2 rounded-lg hover:bg-dark-hover transition-colors"
        >
          {collapsed ? <FaBars /> : <FaTimes />}
        </button>
      </div>

      {/* Menu Items */}
      <nav className="flex-1 py-6">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onNavigate(item.id)}
            className={`w-full flex items-center gap-4 px-6 py-4 transition-all ${
              active === item.id
                ? 'bg-dark-hover border-l-4 border-agent-primary'
                : 'hover:bg-dark-hover border-l-4 border-transparent'
            }`}
          >
            <item.icon className={`text-2xl ${active === item.id ? item.color : 'text-gray-400'}`} />
            {!collapsed && (
              <span className={`font-medium ${active === item.id ? 'text-white' : 'text-gray-400'}`}>
                {item.label}
              </span>
            )}
          </button>
        ))}
      </nav>

      {/* Footer */}
      {!collapsed && (
        <div className="p-6 border-t border-dark-border">
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
            <span>API Connected</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default Sidebar;
