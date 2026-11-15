import React, { useEffect, useState } from 'react';
import { citizenReportService } from '../api/citizenReports';

const statuses = ['Submitted', 'Under Review', 'Assigned', 'Resolved', 'Rejected'];

export default function CitizenReports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(null);

  const loadReports = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await citizenReportService.getReports(filter ? { status: filter } : {});
      setReports(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to load citizen complaints.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadReports(); }, [filter]);

  const changeStatus = async (id, status) => {
    setSaving(id);
    try {
      await citizenReportService.updateStatus(id, status);
      await loadReports();
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not update complaint status.');
    } finally {
      setSaving(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Citizen Complaints</h1>
          <p className="mt-1 text-sm text-slate-600">Review public road reports and update their progress.</p>
        </div>
        <select value={filter} onChange={(e) => setFilter(e.target.value)} className="rounded-lg border border-slate-300 bg-white px-3 py-2">
          <option value="">All statuses</option>
          {statuses.map((status) => <option key={status} value={status}>{status}</option>)}
        </select>
      </div>

      {error && <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
      {loading ? <div className="rounded-xl bg-white p-8 text-center text-slate-600">Loading complaints...</div> :
        reports.length === 0 ? <div className="rounded-xl bg-white p-8 text-center text-slate-600">No citizen complaints found.</div> :
        <div className="overflow-x-auto rounded-xl bg-white shadow-sm ring-1 ring-slate-200">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50"><tr>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase text-slate-500">Complaint</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase text-slate-500">Location</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase text-slate-500">Photo</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase text-slate-500">Submitted</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase text-slate-500">Status</th>
            </tr></thead>
            <tbody className="divide-y divide-slate-100">
              {reports.map((report) => <tr key={report.id} className="align-top">
                <td className="px-4 py-4">
                  <p className="font-semibold text-slate-900">{report.complaint_code}</p>
                  <p className="mt-1 max-w-xs text-sm text-slate-600">{report.description}</p>
                </td>
                <td className="px-4 py-4 text-sm text-slate-700">{report.road_name || 'Road not specified'}<br />{report.area || 'Area not specified'}</td>
                <td className="px-4 py-4">{report.image_path && <a href={`http://localhost:8000${report.image_path}`} target="_blank" rel="noreferrer"><img src={`http://localhost:8000${report.image_path}`} alt="Reported road issue" className="h-20 w-28 rounded object-cover" /></a>}</td>
                <td className="px-4 py-4 text-sm text-slate-600">{new Date(report.created_at).toLocaleString()}</td>
                <td className="px-4 py-4"><select value={report.status} disabled={saving === report.id} onChange={(e) => changeStatus(report.id, e.target.value)} className="rounded-lg border border-slate-300 px-2 py-2 text-sm">
                  {statuses.map((status) => <option key={status} value={status}>{status}</option>)}
                </select></td>
              </tr>)}
            </tbody>
          </table>
        </div>}
      <p className="text-xs text-slate-500">Citizen phone numbers are not displayed in this review table or in public tracking results.</p>
    </div>
  );
}
