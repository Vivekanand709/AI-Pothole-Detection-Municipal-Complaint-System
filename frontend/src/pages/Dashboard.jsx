import React, { useState, useEffect } from 'react';
import { dashboardService } from '../api/dashboard';
import { potholeService } from '../api/potholes';
import { ticketService } from '../api/tickets';
import { inspectionService } from '../api/inspections';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';

// Fix for default marker icons in Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const COLORS = {
  Critical: '#dc2626',
  High: '#f97316',
  Medium: '#eab308',
  Low: '#22c55e',
  Open: '#3b82f6',
  'In Progress': '#f59e0b',
  Resolved: '#10b981',
  Closed: '#6b7280'
};

const SEVERITY_COLORS = ['#dc2626', '#f97316', '#eab308', '#22c55e'];
const STATUS_COLORS = ['#3b82f6', '#f59e0b', '#10b981', '#6b7280'];

const KPICard = ({ title, value, icon, trend, color }) => {
  const colorClasses = {
    red: 'bg-red-50 border-red-200 text-red-700',
    orange: 'bg-orange-50 border-orange-200 text-orange-700',
    yellow: 'bg-yellow-50 border-yellow-200 text-yellow-700',
    green: 'bg-green-50 border-green-200 text-green-700',
    blue: 'bg-blue-50 border-blue-200 text-blue-700',
    purple: 'bg-purple-50 border-purple-200 text-purple-700'
  };

  return (
    <div className={`border-l-4 ${colorClasses[color] || colorClasses.blue} bg-white p-4 shadow-sm`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider opacity-70">{title}</p>
          <p className="text-3xl font-bold mt-1">{value}</p>
          {trend && (
            <p className={`text-xs mt-1 ${trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
              {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}% from last week
            </p>
          )}
        </div>
        <div className="text-4xl opacity-20">{icon}</div>
      </div>
    </div>
  );
};

const IntelligencePanel = ({ potholes, tickets }) => {
  const criticalPotholes = potholes.filter(p => p.severity === 'Critical').slice(0, 5);
  const openTickets = tickets.filter(t => t.status === 'Open').slice(0, 5);

  return (
    <div className="bg-white border border-gray-200 shadow-sm">
      <div className="px-4 py-3 border-b border-gray-200 bg-gray-50">
        <h3 className="font-semibold text-sm uppercase tracking-wider text-gray-700">Road Intelligence</h3>
      </div>
      <div className="divide-y divide-gray-100">
        <div className="p-4">
          <h4 className="text-xs font-semibold text-red-600 uppercase mb-3">Critical Potholes</h4>
          {criticalPotholes.length === 0 ? (
            <p className="text-xs text-gray-500">No critical potholes</p>
          ) : (
            <div className="space-y-2">
              {criticalPotholes.map(pothole => (
                <div key={pothole.id} className="flex items-center justify-between text-xs">
                  <div>
                    <p className="font-medium">{pothole.road_name || 'Unknown Road'}</p>
                    <p className="text-gray-500">{pothole.area || 'Unknown Area'}</p>
                  </div>
                  <span className="px-2 py-1 bg-red-100 text-red-700 rounded text-xs font-medium">
                    {pothole.severity}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
        <div className="p-4">
          <h4 className="text-xs font-semibold text-blue-600 uppercase mb-3">Open Work Orders</h4>
          {openTickets.length === 0 ? (
            <p className="text-xs text-gray-500">No open work orders</p>
          ) : (
            <div className="space-y-2">
              {openTickets.map(ticket => (
                <div key={ticket.id} className="flex items-center justify-between text-xs">
                  <div>
                    <p className="font-medium">TKT-{ticket.ticket_id?.slice(-6) || ticket.id}</p>
                    <p className="text-gray-500">{ticket.priority} Priority</p>
                  </div>
                  <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-medium">
                    Open
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const MapComponent = ({ potholes, filterSeverity, setFilterSeverity }) => {
  const [map, setMap] = useState(null);

  const getMarkerColor = (severity) => {
    return COLORS[severity] || '#3b82f6';
  };

  const createCustomIcon = (severity) => {
    const color = getMarkerColor(severity);
    return L.divIcon({
      className: 'custom-marker',
      html: `<div style="background-color: ${color}; width: 24px; height: 24px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>`,
      iconSize: [24, 24],
      iconAnchor: [12, 12]
    });
  };

  useEffect(() => {
    if (map) {
      map.setView([30.9, 75.85], 12);
    }
  }, [map]);

  const filteredPotholes = filterSeverity === 'All' 
    ? potholes 
    : potholes.filter(p => p.severity === filterSeverity);

  return (
    <div className="relative h-full">
      <div className="absolute top-4 left-4 z-[1000] bg-white p-2 rounded shadow-md border border-gray-200">
        <div className="flex gap-2">
          {['All', 'Critical', 'High', 'Medium', 'Low'].map(severity => (
            <button
              key={severity}
              onClick={() => setFilterSeverity(severity)}
              className={`px-3 py-1 text-xs font-medium rounded ${
                filterSeverity === severity
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {severity}
            </button>
          ))}
        </div>
      </div>
      <MapContainer
        center={[30.9, 75.85]}
        zoom={12}
        style={{ height: '100%', width: '100%' }}
        whenCreated={setMap}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap contributors'
        />
        {filteredPotholes.map(pothole => (
          <Marker
            key={pothole.id}
            position={[pothole.latitude, pothole.longitude]}
            icon={createCustomIcon(pothole.severity)}
          >
            <Popup>
              <div className="text-xs">
                <p className="font-bold">{pothole.road_name || 'Unknown Road'}</p>
                <p>Severity: {pothole.severity}</p>
                <p>Confidence: {(pothole.confidence * 100).toFixed(1)}%</p>
                <p>Status: {pothole.status}</p>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [potholes, setPotholes] = useState([]);
  const [tickets, setTickets] = useState([]);
  const [inspections, setInspections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterSeverity, setFilterSeverity] = useState('All');
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    loadDashboardData();
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const loadDashboardData = async () => {
    try {
      const [statsData, potholesData, ticketsData, inspectionsData] = await Promise.all([
        dashboardService.getStats(),
        potholeService.getPotholes(),
        ticketService.getTickets(),
        inspectionService.getInspections()
      ]);
      setStats(statsData);
      setPotholes(potholesData);
      setTickets(ticketsData);
      setInspections(inspectionsData);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading Road Intelligence...</p>
        </div>
      </div>
    );
  }

  if (!stats) {
    return <div className="text-red-600 p-8">Error loading dashboard data</div>;
  }

  const severityData = Object.entries(stats.potholes_by_severity).map(([severity, count]) => ({
    name: severity,
    value: count
  }));

  const statusData = Object.entries(stats.tickets_by_status).map(([status, count]) => ({
    name: status,
    value: count
  }));

  const areaData = Object.entries(stats.potholes_by_area).map(([area, count]) => ({
    name: area || 'Unknown',
    value: count
  }));

  const trendData = stats.potholes_over_time || [];

  return (
    <div className="bg-gray-100 min-h-screen">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center">
                <span className="text-white text-xl">🛣️</span>
              </div>
              <div className="ml-3">
                <h1 className="text-xl font-bold text-gray-900">RoadGuard AI</h1>
                <p className="text-xs text-gray-500">Municipal Road Intelligence Platform</p>
              </div>
            </div>
          </div>
          <div className="flex items-center space-x-6">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900">
                {currentTime.toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short' })}
              </p>
              <p className="text-xs text-gray-500">
                {currentTime.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}
              </p>
            </div>
            <div className="relative">
              <button className="p-2 text-gray-600 hover:text-gray-900">
                <span className="text-xl">🔔</span>
              </button>
              <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                AD
              </div>
              <div className="text-sm">
                <p className="font-medium text-gray-900">Admin</p>
                <p className="text-xs text-gray-500">Municipal Corporation</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-6">
        {/* Section Title */}
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Road Intelligence Overview</h2>
          <p className="text-sm text-gray-600">Real-time municipal road monitoring and pothole detection analytics</p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-6 gap-4 mb-6">
          <KPICard title="Total Potholes" value={stats.total_potholes} icon="🕳️" color="blue" />
          <KPICard title="Critical" value={stats.critical_potholes} icon="⚠️" color="red" />
          <KPICard title="High" value={stats.high_severity_potholes} icon="🔴" color="orange" />
          <KPICard title="Medium" value={stats.potholes_by_severity?.Medium || 0} icon="🟡" color="yellow" />
          <KPICard title="Low" value={stats.potholes_by_severity?.Low || 0} icon="🟢" color="green" />
          <KPICard title="Open Work Orders" value={stats.open_tickets} icon="📋" color="purple" />
        </div>

        {/* Map and Intelligence Panel */}
        <div className="grid grid-cols-4 gap-6 mb-6">
          <div className="col-span-3 bg-white border border-gray-200 shadow-sm" style={{ height: '500px' }}>
            <div className="px-4 py-3 border-b border-gray-200 bg-gray-50 flex items-center justify-between">
              <h3 className="font-semibold text-sm uppercase tracking-wider text-gray-700">Live Road Map</h3>
              <div className="flex items-center space-x-2 text-xs text-gray-500">
                <span>📍 Punjab, India</span>
                <span>|</span>
                <span>{potholes.length} Markers</span>
              </div>
            </div>
            <div className="h-[calc(100%-48px)]">
              <MapComponent potholes={potholes} filterSeverity={filterSeverity} setFilterSeverity={setFilterSeverity} />
            </div>
          </div>
          <div className="col-span-1">
            <IntelligencePanel potholes={potholes} tickets={tickets} />
          </div>
        </div>

        {/* Analytics Section */}
        <div className="grid grid-cols-4 gap-6 mb-6">
          <div className="bg-white border border-gray-200 shadow-sm p-4">
            <h3 className="font-semibold text-sm uppercase tracking-wider text-gray-700 mb-4">Potholes by Severity</h3>
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={severityData}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={70}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {severityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={SEVERITY_COLORS[index % SEVERITY_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="bg-white border border-gray-200 shadow-sm p-4">
            <h3 className="font-semibold text-sm uppercase tracking-wider text-gray-700 mb-4">Work Order Status</h3>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={statusData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 10 }} />
                <Tooltip />
                <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="bg-white border border-gray-200 shadow-sm p-4">
            <h3 className="font-semibold text-sm uppercase tracking-wider text-gray-700 mb-4">Potholes by Area</h3>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={areaData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 10 }} />
                <Tooltip />
                <Bar dataKey="value" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="bg-white border border-gray-200 shadow-sm p-4">
            <h3 className="font-semibold text-sm uppercase tracking-wider text-gray-700 mb-4">Detection Trend</h3>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 10 }} />
                <Tooltip />
                <Line type="monotone" dataKey="count" stroke="#8b5cf6" strokeWidth={2} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Tables Section */}
        <div className="grid grid-cols-2 gap-6">
          {/* Recent Inspections */}
          <div className="bg-white border border-gray-200 shadow-sm">
            <div className="px-4 py-3 border-b border-gray-200 bg-gray-50">
              <h3 className="font-semibold text-sm uppercase tracking-wider text-gray-700">Recent Inspections</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-xs">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left font-semibold text-gray-700">ID</th>
                    <th className="px-4 py-2 text-left font-semibold text-gray-700">Road</th>
                    <th className="px-4 py-2 text-left font-semibold text-gray-700">City</th>
                    <th className="px-4 py-2 text-left font-semibold text-gray-700">Date</th>
                    <th className="px-4 py-2 text-left font-semibold text-gray-700">Potholes</th>
                    <th className="px-4 py-2 text-left font-semibold text-gray-700">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {inspections.slice(0, 5).map(inspection => (
                    <tr key={inspection.id} className="hover:bg-gray-50">
                      <td className="px-4 py-2 font-medium">INS-{inspection.id}</td>
                      <td className="px-4 py-2">{inspection.road_name || 'Unknown'}</td>
                      <td className="px-4 py-2">{inspection.area || 'Unknown'}</td>
                      <td className="px-4 py-2">{new Date(inspection.upload_date).toLocaleDateString('en-IN')}</td>
                      <td className="px-4 py-2">
                        {potholes.filter(p => p.inspection_id === inspection.id).length}
                      </td>
                      <td className="px-4 py-2">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          inspection.status === 'completed' ? 'bg-green-100 text-green-700' :
                          inspection.status === 'processing' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-gray-100 text-gray-700'
                        }`}>
                          {inspection.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Maintenance Work Orders */}
          <div className="bg-white border border-gray-200 shadow-sm">
            <div className="px-4 py-3 border-b border-gray-200 bg-gray-50">
              <h3 className="font-semibold text-sm uppercase tracking-wider text-gray-700">Maintenance Work Orders</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-xs">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left font-semibold text-gray-700">Ticket ID</th>
                    <th className="px-4 py-2 text-left font-semibold text-gray-700">Road</th>
                    <th className="px-4 py-2 text-left font-semibold text-gray-700">Ward</th>
                    <th className="px-4 py-2 text-left font-semibold text-gray-700">Severity</th>
                    <th className="px-4 py-2 text-left font-semibold text-gray-700">Team</th>
                    <th className="px-4 py-2 text-left font-semibold text-gray-700">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {tickets.slice(0, 5).map(ticket => {
                    const pothole = potholes.find(p => p.id === ticket.pothole_id);
                    return (
                      <tr key={ticket.id} className="hover:bg-gray-50">
                        <td className="px-4 py-2 font-medium">TKT-{ticket.ticket_id?.slice(-6) || ticket.id}</td>
                        <td className="px-4 py-2">{pothole?.road_name || 'Unknown'}</td>
                        <td className="px-4 py-2">{pothole?.area || 'Unknown'}</td>
                        <td className="px-4 py-2">
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            ticket.priority === 'Critical' ? 'bg-red-100 text-red-700' :
                            ticket.priority === 'High' ? 'bg-orange-100 text-orange-700' :
                            ticket.priority === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                            'bg-green-100 text-green-700'
                          }`}>
                            {ticket.priority}
                          </span>
                        </td>
                        <td className="px-4 py-2">{ticket.assigned_team || 'Unassigned'}</td>
                        <td className="px-4 py-2">
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            ticket.status === 'Open' ? 'bg-blue-100 text-blue-700' :
                            ticket.status === 'In Progress' ? 'bg-yellow-100 text-yellow-700' :
                            ticket.status === 'Resolved' ? 'bg-green-100 text-green-700' :
                            'bg-gray-100 text-gray-700'
                          }`}>
                            {ticket.status}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
