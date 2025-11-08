import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaRobot, FaTools, FaProjectDiagram, FaLightbulb, FaArrowRight, FaChartLine } from 'react-icons/fa';
import { agentsAPI, toolsAPI, workflowsAPI, solutionsAPI } from '../services/api';

const StatCard = ({ title, count, color, icon: Icon, loading, onNavigate }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.05, y: -5 }}
      className="stat-card group cursor-pointer"
      onClick={onNavigate}
    >
      {/* Background gradient effect */}
      <div className={`absolute inset-0 bg-gradient-to-br ${color} opacity-10 rounded-xl transition-opacity group-hover:opacity-20`}></div>
      
      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <div className={`p-4 rounded-2xl bg-gradient-to-br ${color} shadow-xl transform group-hover:scale-110 transition-transform`}>
            <Icon className="text-3xl text-white" />
          </div>
          <FaArrowRight className="text-2xl text-gray-600 group-hover:text-gray-400 transform group-hover:translate-x-2 transition-all" />
        </div>
        
        <div>
          <h3 className="text-gray-400 text-sm font-medium uppercase tracking-wider mb-2">{title}</h3>
          {loading ? (
            <div className="h-10 w-20 bg-dark-bg animate-pulse rounded"></div>
          ) : (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="text-4xl font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent"
            >
              {count}
            </motion.div>
          )}
        </div>
      </div>

      {/* Hover effect */}
      <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-white to-transparent opacity-0 group-hover:opacity-50 transition-opacity"></div>
    </motion.div>
  );
};

const RecentActivity = ({ activities, loading }) => {
  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold flex items-center gap-2">
          <FaChartLine className="text-agent-primary" />
          Recent Activity
        </h2>
      </div>

      {loading ? (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-16 bg-dark-bg animate-pulse rounded-lg"></div>
          ))}
        </div>
      ) : activities && activities.length > 0 ? (
        <div className="space-y-3">
          {activities.slice(0, 5).map((activity, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="flex items-center gap-4 p-4 bg-dark-bg rounded-lg hover:bg-dark-hover transition-colors cursor-pointer"
            >
              <div className={`p-3 rounded-lg ${
                activity.type === 'workflow' ? 'bg-workflow-primary bg-opacity-20 text-workflow-primary' :
                activity.type === 'agent' ? 'bg-agent-primary bg-opacity-20 text-agent-primary' :
                'bg-tool-primary bg-opacity-20 text-tool-primary'
              }`}>
                {activity.type === 'workflow' ? <FaProjectDiagram /> : 
                 activity.type === 'agent' ? <FaRobot /> : <FaTools />}
              </div>
              <div className="flex-1">
                <p className="font-medium">{activity.title}</p>
                <p className="text-sm text-gray-400">{activity.timestamp}</p>
              </div>
              <div className="text-sm text-gray-400">{activity.status}</div>
            </motion.div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-gray-400">
          <p>No recent activity</p>
        </div>
      )}
    </div>
  );
};

const QuickActions = ({ onNavigate }) => {
  const actions = [
    {
      id: 'create-agent',
      title: 'Create Agent',
      description: 'Add a new AI agent',
      icon: FaRobot,
      color: 'from-agent-primary to-agent-secondary',
      action: () => onNavigate('agents'),
    },
    {
      id: 'create-tool',
      title: 'Create Tool',
      description: 'Add a new tool',
      icon: FaTools,
      color: 'from-tool-primary to-tool-secondary',
      action: () => onNavigate('tools'),
    },
    {
      id: 'create-workflow',
      title: 'Design Workflow',
      description: 'Build a workflow',
      icon: FaProjectDiagram,
      color: 'from-workflow-primary to-workflow-secondary',
      action: () => onNavigate('workflows'),
    },
  ];

  return (
    <div className="card p-6">
      <h2 className="text-2xl font-bold mb-6">Quick Actions</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {actions.map((action, index) => (
          <motion.button
            key={action.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={action.action}
            className={`p-6 rounded-xl bg-gradient-to-br ${action.color} hover:shadow-2xl transition-all text-left`}
          >
            <action.icon className="text-4xl mb-4" />
            <h3 className="text-lg font-bold mb-2">{action.title}</h3>
            <p className="text-sm opacity-90">{action.description}</p>
          </motion.button>
        ))}
      </div>
    </div>
  );
};

const Dashboard = ({ onNavigate }) => {
  const [stats, setStats] = useState({
    agents: 0,
    tools: 0,
    workflows: 0,
    solutions: 0,
  });
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [agentsRes, toolsRes, workflowsRes, solutionsRes] = await Promise.all([
        agentsAPI.getAll().catch(() => ({ data: [] })),
        toolsAPI.getAll().catch(() => ({ data: [] })),
        workflowsAPI.getAll().catch(() => ({ data: [] })),
        solutionsAPI.getAll().catch(() => ({ data: [] })),
      ]);

      setStats({
        agents: agentsRes.data.length,
        tools: toolsRes.data.length,
        workflows: workflowsRes.data.length,
        solutions: solutionsRes.data.length,
      });

      // Generate recent activities from solutions/runs
      const recentActivities = solutionsRes.data.slice(0, 5).map((solution) => ({
        type: 'workflow',
        title: `Workflow executed: ${solution.workflow_id || 'Unknown'}`,
        timestamp: new Date(solution.created_at || Date.now()).toLocaleString(),
        status: solution.status || 'completed',
      }));

      setActivities(recentActivities);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-5xl font-bold mb-2 bg-gradient-to-r from-white via-agent-primary to-workflow-primary bg-clip-text text-transparent">
          Agentic AI Dashboard
        </h1>
        <p className="text-gray-400 text-lg">
          Orchestrate intelligent AI workflows with ease
        </p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Agents"
          count={stats.agents}
          color="from-agent-primary to-agent-secondary"
          icon={FaRobot}
          loading={loading}
          onNavigate={() => onNavigate('agents')}
        />
        <StatCard
          title="Tools"
          count={stats.tools}
          color="from-tool-primary to-tool-secondary"
          icon={FaTools}
          loading={loading}
          onNavigate={() => onNavigate('tools')}
        />
        <StatCard
          title="Workflows"
          count={stats.workflows}
          color="from-workflow-primary to-workflow-secondary"
          icon={FaProjectDiagram}
          loading={loading}
          onNavigate={() => onNavigate('workflows')}
        />
        <StatCard
          title="Solutions"
          count={stats.solutions}
          color="from-solution-primary to-solution-secondary"
          icon={FaLightbulb}
          loading={loading}
          onNavigate={() => onNavigate('solutions')}
        />
      </div>

      {/* Quick Actions */}
      <QuickActions onNavigate={onNavigate} />

      {/* Recent Activity */}
      <RecentActivity activities={activities} loading={loading} />
    </div>
  );
};

export default Dashboard;
