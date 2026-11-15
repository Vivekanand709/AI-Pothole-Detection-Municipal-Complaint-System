import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ticketService } from '../api/tickets';

const TicketDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [resolutionNotes, setResolutionNotes] = useState('');
  const [assignedTeam, setAssignedTeam] = useState('');
  const [beforePhoto, setBeforePhoto] = useState(null);
  const [afterPhoto, setAfterPhoto] = useState(null);
  const [verificationNotes, setVerificationNotes] = useState('');
  const [verifications, setVerifications] = useState([]);

  useEffect(() => {
    loadTicket();
  }, [id]);

  const loadTicket = async () => {
    try {
      setLoading(true);
      const data = await ticketService.getTicket(id);
      setTicket(data);
      const evidence = await ticketService.getVerification(id).catch(() => []);
      setVerifications(evidence);
      setResolutionNotes(data.resolution_notes || '');
      setAssignedTeam(data.assigned_team || '');
    } catch (error) {
      console.error('Error loading ticket:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStatus = async (newStatus) => {
    try {
      setUpdating(true);
      await ticketService.updateTicket(id, { status: newStatus });
      await loadTicket();
    } catch (error) {
      console.error('Error updating ticket:', error);
    } finally {
      setUpdating(false);
    }
  };

  const handleAssign = async () => {
    if (!assignedTeam) return;
    try {
      setUpdating(true);
      await ticketService.assignTicket(id, assignedTeam);
      await loadTicket();
    } catch (error) {
      console.error('Error assigning ticket:', error);
    } finally {
      setUpdating(false);
    }
  };

  const handleResolve = async () => {
    try {
      setUpdating(true);
      await ticketService.resolveTicket(id, resolutionNotes);
      await loadTicket();
    } catch (error) {
      console.error('Error resolving ticket:', error);
    } finally {
      setUpdating(false);
    }
  };

  const handleSubmitVerification = async () => {
    if (!beforePhoto || !afterPhoto) return;
    try {
      setUpdating(true);
      await ticketService.submitVerification(id, beforePhoto, afterPhoto, verificationNotes);
      setBeforePhoto(null);
      setAfterPhoto(null);
      setVerificationNotes('');
      await loadTicket();
    } catch (error) {
      alert(error.response?.data?.detail || 'Could not submit repair evidence.');
    } finally {
      setUpdating(false);
    }
  };

  const handleClose = async () => {
    try {
      setUpdating(true);
      await ticketService.closeTicket(id);
      await loadTicket();
    } catch (error) {
      console.error('Error closing ticket:', error);
    } finally {
      setUpdating(false);
    }
  };

  const getStatusBadge = (status) => {
    const colors = {
      'Open': 'bg-blue-100 text-blue-800',
      'Assigned': 'bg-yellow-100 text-yellow-800',
      'In Progress': 'bg-purple-100 text-purple-800',
      'Resolved': 'bg-green-100 text-green-800',
      'Closed': 'bg-gray-100 text-gray-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getPriorityBadge = (priority) => {
    const colors = {
      'Low': 'bg-green-100 text-green-800',
      'Medium': 'bg-yellow-100 text-yellow-800',
      'High': 'bg-orange-100 text-orange-800',
      'Critical': 'bg-red-100 text-red-800'
    };
    return colors[priority] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return <div className="flex items-center justify-center h-64">Loading ticket details...</div>;
  }

  if (!ticket) {
    return <div className="text-red-600">Ticket not found</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-800">Ticket Details</h1>
        <button
          onClick={() => navigate('/tickets')}
          className="text-blue-600 hover:text-blue-800"
        >
          ← Back to Tickets
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Ticket Information</h2>
            <div className="space-y-3">
              <div>
                <span className="text-sm text-gray-600">Ticket ID:</span>
                <span className="ml-2 font-medium">{ticket.ticket_id}</span>
              </div>
              <div>
                <span className="text-sm text-gray-600">Pothole ID:</span>
                <span className="ml-2 font-medium">#{ticket.pothole_id}</span>
              </div>
              <div>
                <span className="text-sm text-gray-600">Priority:</span>
                <span className={`ml-2 px-2 py-1 text-xs font-semibold rounded-full ${getPriorityBadge(ticket.priority)}`}>
                  {ticket.priority}
                </span>
              </div>
              <div>
                <span className="text-sm text-gray-600">Status:</span>
                <span className={`ml-2 px-2 py-1 text-xs font-semibold rounded-full ${getStatusBadge(ticket.status)}`}>
                  {ticket.status}
                </span>
              </div>
              <div>
                <span className="text-sm text-gray-600">Assigned Team:</span>
                <span className="ml-2 font-medium">{ticket.assigned_team || 'Unassigned'}</span>
              </div>
              <div>
                <span className="text-sm text-gray-600">Created:</span>
                <span className="ml-2 font-medium">{new Date(ticket.created_at).toLocaleString()}</span>
              </div>
              {ticket.resolved_at && (
                <div>
                  <span className="text-sm text-gray-600">Resolved:</span>
                  <span className="ml-2 font-medium">{new Date(ticket.resolved_at).toLocaleString()}</span>
                </div>
              )}
            </div>
          </div>

          <div>
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Description</h2>
            <p className="text-gray-700 bg-gray-50 p-4 rounded-lg">
              {ticket.description || 'No description provided'}
            </p>

            {ticket.resolution_notes && (
              <div className="mt-4">
                <h3 className="text-md font-semibold text-gray-800 mb-2">Resolution Notes</h3>
                <p className="text-gray-700 bg-green-50 p-4 rounded-lg">
                  {ticket.resolution_notes}
                </p>
              </div>
            )}
          </div>
        </div>


        <div className="mt-8 pt-6 border-t">
          <h2 className="text-lg font-semibold text-gray-800 mb-2">Before / After Repair Verification</h2>
          <p className="text-sm text-gray-600 mb-4">Upload genuine photos from before and after the repair. Submitting both records the evidence and marks this ticket as resolved.</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label className="block text-sm font-medium text-gray-700">Before repair photo
              <input type="file" accept="image/jpeg,image/png,image/webp" onChange={(e) => setBeforePhoto(e.target.files?.[0] || null)} className="mt-2 block w-full text-sm" />
            </label>
            <label className="block text-sm font-medium text-gray-700">After repair photo
              <input type="file" accept="image/jpeg,image/png,image/webp" onChange={(e) => setAfterPhoto(e.target.files?.[0] || null)} className="mt-2 block w-full text-sm" />
            </label>
          </div>
          <textarea value={verificationNotes} onChange={(e) => setVerificationNotes(e.target.value)} rows={2} maxLength={2000} placeholder="Repair notes (optional)" className="mt-4 w-full px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleSubmitVerification} disabled={updating || !beforePhoto || !afterPhoto} className="mt-3 px-5 py-2 bg-emerald-600 text-white rounded-lg disabled:opacity-50">Submit Repair Evidence</button>
          {verifications.length > 0 && <div className="mt-6 space-y-3">
            <h3 className="font-semibold text-gray-800">Submitted evidence</h3>
            {verifications.map((item) => <div key={item.id} className="grid grid-cols-1 md:grid-cols-2 gap-4 border rounded-lg p-3">
              <div><p className="text-sm font-medium mb-2">Before</p><img src={`http://localhost:8000${item.before_image_url}`} alt="Before repair" className="w-full h-48 object-cover rounded" /></div>
              <div><p className="text-sm font-medium mb-2">After</p><img src={`http://localhost:8000${item.after_image_url}`} alt="After repair" className="w-full h-48 object-cover rounded" /></div>
              {item.notes && <p className="md:col-span-2 text-sm text-gray-600">{item.notes}</p>}
            </div>)}
          </div>}
        </div>

        {/* Actions */}
        <div className="mt-8 pt-6 border-t">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Actions</h2>
          
          <div className="space-y-4">
            {/* Assign Team */}
            {ticket.status === 'Open' && (
              <div className="flex items-center space-x-4">
                <input
                  type="text"
                  value={assignedTeam}
                  onChange={(e) => setAssignedTeam(e.target.value)}
                  placeholder="Enter team name"
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
                <button
                  onClick={handleAssign}
                  disabled={updating || !assignedTeam}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  Assign Team
                </button>
              </div>
            )}

            {/* Status Updates */}
            <div className="flex flex-wrap gap-2">
              {ticket.status === 'Open' && (
                <button
                  onClick={() => handleUpdateStatus('Assigned')}
                  disabled={updating}
                  className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 disabled:opacity-50"
                >
                  Mark as Assigned
                </button>
              )}
              {ticket.status === 'Assigned' && (
                <button
                  onClick={() => handleUpdateStatus('In Progress')}
                  disabled={updating}
                  className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
                >
                  Start Progress
                </button>
              )}
              {ticket.status === 'In Progress' && (
                <>
                  <button
                    onClick={() => handleUpdateStatus('Assigned')}
                    disabled={updating}
                    className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 disabled:opacity-50"
                  >
                    Back to Assigned
                  </button>
                  <button
                    onClick={handleResolve}
                    disabled={updating}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
                  >
                    Mark as Resolved
                  </button>
                </>
              )}
              {ticket.status === 'Resolved' && (
                <button
                  onClick={handleClose}
                  disabled={updating}
                  className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50"
                >
                  Close Ticket
                </button>
              )}
            </div>

            {/* Resolution Notes Input */}
            {(ticket.status === 'In Progress' || ticket.status === 'Assigned') && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Resolution Notes
                </label>
                <textarea
                  value={resolutionNotes}
                  onChange={(e) => setResolutionNotes(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  rows={3}
                  placeholder="Add notes about the resolution..."
                />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TicketDetails;
