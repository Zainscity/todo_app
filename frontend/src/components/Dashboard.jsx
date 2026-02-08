'use client';

import { useAuth } from '../context/AuthContext';
import TaskList from './TaskList';
import Chatbot from './Chatbot'; // Keep this import

export default function DashboardComponent() {
  const { user, logout, loading } = useAuth(); // Keep user, loading

  const handleLogout = () => {
    logout();
  };

  // Keep loading check
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Keep unauthenticated check
  if (!user) {
    // This should ideally not happen if routing is correct, but as a fallback
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-red-600">You are not authenticated. Redirecting to login...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-8 animate-fade-in">
          <div className="animate-slide-up">
            <h1 className="text-3xl font-bold text-gray-900 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Todo Dashboard
            </h1>
            <p className="mt-2 text-gray-600">Manage your tasks efficiently</p>
          </div>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm font-medium text-white bg-gradient-to-r from-red-600 to-red-700 rounded-lg hover:from-red-700 hover:to-red-800 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 shadow-md hover:shadow-lg transition-all duration-200 transform hover:-translate-y-0.5"
          >
            Logout
          </button>
        </div>

        {/* Keep grid layout with Chatbot */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-white shadow-xl rounded-xl p-6 border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
              <TaskList />
            </div>
            <div className="bg-white shadow-xl rounded-xl p-6 border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
                <Chatbot />
            </div>
        </div>
      </div>
    </div>
  );
}