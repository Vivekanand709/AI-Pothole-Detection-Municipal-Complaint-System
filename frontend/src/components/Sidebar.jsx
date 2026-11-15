import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { authService } from '../api/auth';

const Sidebar = () => {
  const location = useLocation();
  const [user, setUser] = React.useState(null);

  React.useEffect(() => {
    setUser(authService.getUser());
  }, []);

  const handleLogout = () => {
    authService.logout();
    window.location.href = '/login';
  };

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/citizen-report', label: 'Citizen Report Portal', icon: '📝' },
    { path: '/map', label: 'Live Road Map', icon: '�️' },
    { path: '/upload', label: 'Pothole Detection', icon: '�' },
    { path: '/inspections', label: 'Inspections', icon: '�' },
    { path: '/tickets', label: 'Maintenance Tickets', icon: '🎫' },
    { path: '/potholes', label: 'Road Analytics', icon: '�' },
    { path: '/settings', label: 'Settings', icon: '⚙️' },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <div className="w-64 bg-gradient-to-b from-slate-900 to-slate-800 text-white flex flex-col shadow-xl">
      {/* Logo Section */}
      <div className="p-6 border-b border-slate-700">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-700 rounded-lg flex items-center justify-center">
            <span className="text-white text-xl">🛣️</span>
          </div>
          <div>
            <h1 className="text-lg font-bold">RoadGuard AI</h1>
            <p className="text-xs text-slate-400">Municipal Intelligence</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`flex items-center px-4 py-3 rounded-lg transition-all duration-200 ${
              isActive(item.path)
                ? 'bg-blue-600 text-white shadow-lg'
                : 'text-slate-300 hover:bg-slate-700 hover:text-white'
            }`}
          >
            <span className="mr-3 text-lg">{item.icon}</span>
            <span className="text-sm font-medium">{item.label}</span>
          </Link>
        ))}
      </nav>

      {/* User Section */}
      <div className="p-4 border-t border-slate-700 bg-slate-900">
        <div className="mb-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-medium">
              {user?.name?.charAt(0) || 'A'}
            </div>
            <div>
              <p className="text-sm font-medium">{user?.name || 'Admin User'}</p>
              <p className="text-xs text-slate-400">{user?.role || 'Municipal Officer'}</p>
            </div>
          </div>
        </div>
        <button
          onClick={handleLogout}
          className="w-full bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg transition-colors text-sm font-medium"
        >
          Logout
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
