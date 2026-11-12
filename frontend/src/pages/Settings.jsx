import React from 'react';
import { authService } from '../api/auth';

const Settings = () => {
  const [user, setUser] = React.useState(null);

  React.useEffect(() => {
    setUser(authService.getUser());
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Settings</h1>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">User Information</h2>
        <div className="space-y-3">
          <div>
            <span className="text-sm text-gray-600">Name:</span>
            <span className="ml-2 font-medium">{user?.name || 'Demo User'}</span>
          </div>
          <div>
            <span className="text-sm text-gray-600">Email:</span>
            <span className="ml-2 font-medium">{user?.email || 'demo@municipal.gov'}</span>
          </div>
          <div>
            <span className="text-sm text-gray-600">Role:</span>
            <span className="ml-2 font-medium">{user?.role || 'Municipal Officer'}</span>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">System Information</h2>
        <div className="space-y-3">
          <div>
            <span className="text-sm text-gray-600">Application:</span>
            <span className="ml-2 font-medium">Municipal Road Monitoring System</span>
          </div>
          <div>
            <span className="text-sm text-gray-600">Version:</span>
            <span className="ml-2 font-medium">1.0.0</span>
          </div>
          <div>
            <span className="text-sm text-gray-600">Mode:</span>
            <span className="ml-2 font-medium">Demo Mode</span>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Demo Mode Information</h2>
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h3 className="font-semibold text-yellow-800 mb-2">About Demo Mode</h3>
          <ul className="text-sm text-yellow-700 space-y-1">
            <li>• AI detections are simulated for demonstration purposes</li>
            <li>• GPS coordinates are approximate and randomly generated</li>
            <li>• All data is stored locally in SQLite database</li>
            <li>• This is a proof-of-concept implementation</li>
            <li>• For production use, integrate real AI models and GPS data</li>
          </ul>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">API Configuration</h2>
        <div className="space-y-3">
          <div>
            <span className="text-sm text-gray-600">Backend URL:</span>
            <span className="ml-2 font-medium">http://localhost:8000</span>
          </div>
          <div>
            <span className="text-sm text-gray-600">API Documentation:</span>
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="ml-2 text-blue-600 hover:text-blue-800"
            >
              View Swagger Docs
            </a>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Supported Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-center">
            <span className="text-green-500 mr-2">✓</span>
            <span className="text-sm">Video upload and processing</span>
          </div>
          <div className="flex items-center">
            <span className="text-green-500 mr-2">✓</span>
            <span className="text-sm">AI pothole detection (demo mode)</span>
          </div>
          <div className="flex items-center">
            <span className="text-green-500 mr-2">✓</span>
            <span className="text-sm">GPS coordinate association</span>
          </div>
          <div className="flex items-center">
            <span className="text-green-500 mr-2">✓</span>
            <span className="text-sm">Severity classification</span>
          </div>
          <div className="flex items-center">
            <span className="text-green-500 mr-2">✓</span>
            <span className="text-sm">Interactive map visualization</span>
          </div>
          <div className="flex items-center">
            <span className="text-green-500 mr-2">✓</span>
            <span className="text-sm">Maintenance ticket management</span>
          </div>
          <div className="flex items-center">
            <span className="text-green-500 mr-2">✓</span>
            <span className="text-sm">Dashboard analytics</span>
          </div>
          <div className="flex items-center">
            <span className="text-green-500 mr-2">✓</span>
            <span className="text-sm">User authentication and roles</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
