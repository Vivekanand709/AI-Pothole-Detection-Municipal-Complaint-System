import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import { potholeService } from '../api/potholes';
import L from 'leaflet';

// Fix for default marker icons in Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const PotholeMap = () => {
  const [potholes, setPotholes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterSeverity, setFilterSeverity] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [filterArea, setFilterArea] = useState('');

  useEffect(() => {
    loadPotholes();
  }, [filterSeverity, filterStatus, filterArea]);

  const loadPotholes = async () => {
    try {
      setLoading(true);
      const data = await potholeService.getPotholesForMap({
        severity: filterSeverity || undefined,
        status: filterStatus || undefined,
        area: filterArea || undefined
      });
      setPotholes(data);
    } catch (error) {
      console.error('Error loading potholes:', error);
    } finally {
      setLoading(false);
    }
  };

  const getMarkerColor = (severity) => {
    const colors = {
      'Low': 'green',
      'Medium': 'yellow',
      'High': 'orange',
      'Critical': 'red'
    };
    return colors[severity] || 'blue';
  };

  const createCustomIcon = (severity) => {
    const color = getMarkerColor(severity);
    return L.divIcon({
      className: 'custom-marker',
      html: `<div style="background-color: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
      iconSize: [20, 20],
      iconAnchor: [10, 10]
    });
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Pothole Map</h1>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Severity
            </label>
            <select
              value={filterSeverity}
              onChange={(e) => setFilterSeverity(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Severities</option>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
              <option value="Critical">Critical</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Status
            </label>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Statuses</option>
              <option value="detected">Detected</option>
              <option value="reported">Reported</option>
              <option value="resolved">Resolved</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Area
            </label>
            <input
              type="text"
              value={filterArea}
              onChange={(e) => setFilterArea(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="Filter by area"
            />
          </div>
        </div>
      </div>

      {/* Map */}
      <div className="bg-white rounded-lg shadow-md p-6">
        {loading ? (
          <div className="flex items-center justify-center h-96">
            <div className="text-gray-600">Loading map data...</div>
          </div>
        ) : (
          <div className="h-96 rounded-lg overflow-hidden">
            <MapContainer
              center={[40.7128, -74.0060]}
              zoom={13}
              style={{ height: '100%', width: '100%' }}
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              />
              {potholes.map((pothole) => (
                <Marker
                  key={pothole.id}
                  position={[pothole.latitude, pothole.longitude]}
                  icon={createCustomIcon(pothole.severity)}
                >
                  <Popup>
                    <div className="p-2">
                      <h3 className="font-bold text-lg">Pothole #{pothole.id}</h3>
                      <div className="mt-2 space-y-1 text-sm">
                        <p><strong>Severity:</strong> {pothole.severity}</p>
                        <p><strong>Confidence:</strong> {(pothole.confidence * 100).toFixed(1)}%</p>
                        <p><strong>Status:</strong> {pothole.status}</p>
                        <p><strong>Coordinates:</strong> {pothole.latitude.toFixed(4)}, {pothole.longitude.toFixed(4)}</p>
                        {pothole.ticket_id && (
                          <p><strong>Ticket:</strong> {pothole.ticket_id}</p>
                        )}
                        {pothole.detection_time && (
                          <p><strong>Detected:</strong> {new Date(pothole.detection_time).toLocaleDateString()}</p>
                        )}
                      </div>
                    </div>
                  </Popup>
                </Marker>
              ))}
            </MapContainer>
          </div>
        )}

        <div className="mt-4 flex items-center justify-between">
          <div className="text-sm text-gray-600">
            Showing {potholes.length} potholes
          </div>
          <div className="flex items-center space-x-4 text-sm">
            <div className="flex items-center">
              <div className="w-4 h-4 rounded-full bg-green-500 mr-2"></div>
              <span>Low</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 rounded-full bg-yellow-500 mr-2"></div>
              <span>Medium</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 rounded-full bg-orange-500 mr-2"></div>
              <span>High</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 rounded-full bg-red-500 mr-2"></div>
              <span>Critical</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PotholeMap;
