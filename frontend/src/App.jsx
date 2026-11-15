import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import DemoModeBanner from './components/DemoModeBanner';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import UploadInspection from './pages/UploadInspection';
import PotholeMap from './pages/PotholeMap';
import PotholeList from './pages/PotholeList';
import MaintenanceTickets from './pages/MaintenanceTickets';
import TicketDetails from './pages/TicketDetails';
import InspectionHistory from './pages/InspectionHistory';
import Settings from './pages/Settings';
import CitizenReport from './pages/CitizenReport';
import CitizenReports from './pages/CitizenReports';
import RepairVerification from './pages/RepairVerification';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const isAuthenticated = localStorage.getItem('token');
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  return children;
};

// Main Layout Component (for non-dashboard pages)
const MainLayout = ({ children }) => {
  const isAuthenticated = localStorage.getItem('token');
  
  if (!isAuthenticated) {
    return children;
  }
  
  return (
    <div className="flex min-h-screen bg-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <DemoModeBanner />
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

// Dashboard Layout (standalone with its own header)
const DashboardLayout = ({ children }) => {
  return (
    <div className="min-h-screen">
      {children}
    </div>
  );
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/citizen-report" element={<CitizenReport />} />
        <Route path="/tickets/:id/verification" element={<ProtectedRoute><MainLayout><RepairVerification /></MainLayout></ProtectedRoute>} />
        <Route path="/" element={
          <ProtectedRoute>
            <Navigate to="/dashboard" />
          </ProtectedRoute>
        } />
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <DashboardLayout>
              <Dashboard />
            </DashboardLayout>
          </ProtectedRoute>
        } />
        <Route path="/citizen-reports" element={
          <ProtectedRoute>
            <MainLayout>
              <CitizenReports />
            </MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/map" element={
          <ProtectedRoute>
            <MainLayout>
              <PotholeMap />
            </MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/upload" element={
          <ProtectedRoute>
            <MainLayout>
              <UploadInspection />
            </MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/potholes" element={
          <ProtectedRoute>
            <MainLayout>
              <PotholeList />
            </MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/tickets" element={
          <ProtectedRoute>
            <MainLayout>
              <MaintenanceTickets />
            </MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/tickets/:id" element={
          <ProtectedRoute>
            <MainLayout>
              <TicketDetails />
            </MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/inspections" element={
          <ProtectedRoute>
            <MainLayout>
              <InspectionHistory />
            </MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/settings" element={
          <ProtectedRoute>
            <MainLayout>
              <Settings />
            </MainLayout>
          </ProtectedRoute>
        } />
      </Routes>
    </Router>
  );
}

export default App;
