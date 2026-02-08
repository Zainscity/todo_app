import React, { useState } from 'react';
import taskApi from '../services/taskApi';

const TaskItem = ({ task, onTaskUpdated, onTaskDeleted }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({
    title: task.title,
    description: task.description || ''
  });
  const [error, setError] = useState('');

  const handleEditChange = (e) => {
    setEditForm({
      ...editForm,
      [e.target.name]: e.target.value
    });
  };

  const handleSaveEdit = async (e) => {
    e.preventDefault();

    try {
      const response = await taskApi.updateTask(task.user_id, task.id, editForm);
      onTaskUpdated(response);
      setIsEditing(false);
    } catch (err) {
      const errorMessage = err.response?.data?.detail ||
                          err.response?.data?.msg ||
                          err.response?.data?.message ||
                          err.message ||
                          'Failed to update task';
      setError(errorMessage);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await taskApi.deleteTask(task.user_id, task.id);
        onTaskDeleted(task.id);
      } catch (err) {
        const errorMessage = err.response?.data?.detail ||
                            err.response?.data?.msg ||
                            err.response?.data?.message ||
                            err.message ||
                            'Failed to delete task';
        setError(errorMessage);
      }
    }
  };

  const handleToggleComplete = async () => {
    try {
      const response = await taskApi.toggleTaskCompletion(task.user_id, task.id, !task.completed);
      onTaskUpdated(response);
    } catch (err) {
      const errorMessage = err.response?.data?.detail ||
                          err.response?.data?.msg ||
                          err.response?.data?.message ||
                          err.message ||
                          'Failed to update task completion status';
      setError(errorMessage);
    }
  };

  return (
    <div className={`task-item border-l-4 rounded-lg p-5 shadow-card bg-white hover:shadow-md transition-all duration-300 ${task.completed ? 'bg-green-50 border-l-green-500' : 'bg-white border-l-blue-500'} card-hover`}>
      {isEditing ? (
        <form onSubmit={handleSaveEdit} className="space-y-4 animate-fade-in">
          {error && (
            <div className="notification error rounded-lg p-3 text-sm">
              {error}
            </div>
          )}
          <input
            type="text"
            name="title"
            value={editForm.title}
            onChange={handleEditChange}
            className="form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors duration-200 text-gray-900"
            required
            placeholder="Task title..."
          />
          <textarea
            name="description"
            value={editForm.description}
            onChange={handleEditChange}
            className="form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors duration-200 text-gray-900"
            rows="2"
            placeholder="Task description (optional)..."
          />
          <div className="flex space-x-3 pt-2">
            <button
              type="submit"
              className="btn-primary px-4 py-2 text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors duration-200"
            >
              <span className="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="mr-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Save
              </span>
            </button>
            <button
              type="button"
              onClick={() => setIsEditing(false)}
              className="btn-secondary px-4 py-2 text-sm font-medium rounded-lg hover:bg-gray-700 transition-colors duration-200"
            >
              Cancel
            </button>
          </div>
        </form>
      ) : (
        <div className="flex items-start">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleComplete}
            className="mt-1 h-5 w-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer transition-transform duration-150 hover:scale-110"
          />
          <div className="ml-4 flex-1 min-w-0">
            <h3 className={`text-base font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`text-sm mt-1 ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                {task.description}
              </p>
            )}
            <div className="flex items-center justify-between mt-3">
              <div className="flex items-center space-x-2">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {task.completed ? 'Completed' : 'Pending'}
                </span>
                <span className="text-xs text-gray-500">
                  {new Date(task.created_at).toLocaleDateString()}
                </span>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={() => setIsEditing(true)}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center transition-colors duration-200"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="mr-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  Edit
                </button>
                <button
                  onClick={handleDelete}
                  className="text-red-600 hover:text-red-800 text-sm font-medium flex items-center transition-colors duration-200"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="mr-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskItem;