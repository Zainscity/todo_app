import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import TaskItem from './TaskItem';
import TaskForm from './TaskForm';
import taskApi from '../services/taskApi';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);

  const { user } = useAuth();

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      if (!user || !user.id) {
        setError('User not authenticated');
        return;
      }
      const response = await taskApi.getTasks(user.id);
      // Ensure response is an array before setting tasks
      if (Array.isArray(response)) {
        setTasks(response);
      } else {
        console.error('Unexpected response format:', response);
        setError('Failed to load tasks - unexpected response format');
      }
    } catch (err) {
      const errorMessage = err.response?.data?.detail ||
                          err.response?.data?.msg ||
                          err.response?.data?.message ||
                          err.message ||
                          'Failed to load tasks';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskCreated = (newTask) => {
    setTasks([...tasks, newTask]);
    setShowForm(false);
  };

  const handleTaskUpdated = (updatedTask) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (taskId) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  const handleToggleComplete = async (task) => {
    try {
      if (!user || !user.id) {
        setError('User not authenticated');
        return;
      }
      const response = await taskApi.toggleTaskCompletion(user.id, task.id, !task.completed);
      setTasks(tasks.map(t => t.id === task.id ? response : t));
    } catch (err) {
      const errorMessage = err.response?.data?.detail ||
                          err.response?.data?.msg ||
                          err.response?.data?.message ||
                          err.message ||
                          'Failed to update task status';
      setError(errorMessage);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-8 animate-fade-in">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
        <p className="text-gray-600">Loading your tasks...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8 animate-fade-in">
        <div className="inline-block rounded-full h-12 w-12 bg-red-100 text-red-600 mb-4 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p className="text-red-500 font-medium">{error}</p>
        <button
          onClick={fetchTasks}
          className="mt-4 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 animate-fade-in">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Your Tasks</h2>
          <p className="text-sm text-gray-600 mt-1">{tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-6 py-3 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-md hover:shadow-lg transition-all duration-200 transform hover:-translate-y-0.5 btn-hover"
        >
          <span className="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            {showForm ? 'Cancel' : 'Add Task'}
          </span>
        </button>
      </div>

      {showForm && (
        <div className="mb-8 animate-slide-up">
          <TaskForm onTaskCreated={handleTaskCreated} />
        </div>
      )}

      {tasks.length === 0 ? (
        <div className="text-center py-12 animate-fade-in">
          <div className="mx-auto h-24 w-24 bg-gray-100 rounded-full flex items-center justify-center mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No tasks yet</h3>
          <p className="text-gray-500 mb-6">Get started by creating your first task!</p>
          <button
            onClick={() => setShowForm(true)}
            className="px-6 py-3 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-md hover:shadow-lg transition-all duration-200 transform hover:-translate-y-0.5"
          >
            Create Your First Task
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {tasks.map((task, index) => (
            <div key={task.id} className="animate-slide-up" style={{ animationDelay: `${index * 0.05}s` }}>
              <TaskItem
                task={task}
                onTaskUpdated={handleTaskUpdated}
                onTaskDeleted={handleTaskDeleted}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;