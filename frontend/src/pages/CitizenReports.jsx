import React, { useEffect, useMemo, useState } from 'react';
import { citizenReportService } from '../api/citizenReports';

const statuses = ['Submitted', 'Under Review', 'Assigned', 'Resolved', 'Rejected'];

const statusStyles = {
  Submitted: 'bg-sky-100 text-sky-800',
  'Under Review': 'bg-amber-100 text-amber-800',
  Assigned: 'bg-violet-100 text-violet-800',
  Resolved: 'bg-emerald-100 text-emerald-800',
  Rejected: 'bg-rose-100 text-rose-800',
};

export default function CitizenReports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [search, setSearch] = useState('');
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

  const counts = useMemo(() => ({
    total: reports.length,
    pending: reports.filter((r) => !['Resolved', 'Rejected'].includes(r.status)).length,
    assigned: reports.filter((r) => r.status === 'Assigned').length,
    resolved: reports.filter((r) => r.status === 'Resolved').length,
  }), [reports]);

  const visibleReports = useMemo(() => {
    const term = search.trim().toLowerCase();
    if (!term) return reports;
    return reports.filter((r) =>
      [r.complaint_code, r.description, r.road_name, r.area, r.citizen_name]
        .filter(Boolean).some((value) => String(value).toLowerCase().includes(term))
    );
  }, [reports, search]);

  const changeStatus = async (id, status) => {
    setSaving(id);
    setError('');
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
          <p className="text-sm font-semibold uppercase tracking-wider text-blue-700">RoadGuard AI · Municipal Console</p>
          <h1 className="mt-1 text-3xl font-bold text-slate-900">Citizen Complaints</h1>
          <p className="mt-1 text-sm text-slate-600">Review public road reports, search complaints and update their progress.</p>
        </div>
        <button onClick={loadReports} disabled={loading} className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-50">
          {loading ? 'Refreshing…' : '↻ Refresh'}
        </button>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {[
          ['Reports in view', counts.total, 'bg-blue-50 text-blue-800'],
          ['Open / pending', counts.pending, 'bg-amber-50 text-amber-800'],
          ['Assigned', counts.assigned, 'bg-violet-50 text-violet-800'],
          ['Resolved', counts.resolved, 'bg-emerald-50 text-emerald-800'],
        ].map(([label, value, style]) => (
          <div key={label} className={`rounded-2xl p-5 ring-1 ring-black/5 ${style}`}>
            <p className="text-sm font-semibold opacity-80">{label}</p>
            <p className="mt-2 text-3xl font-bold">{value}</p>
          </div>
        ))}
      </div>

      <div className="flex flex-col gap-3 rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200 md:flex-row">
        <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search by complaint code, road, area or description…" className="min-w-0 flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none" />
        <select value={filter} onChange={(e) => setFilter(e.target.value)} className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm">
          <option value="">All statuses</option>
          {statuses.map((status) => <option key={status} value={status}>{status}</option>)}
        </select>
      </div>

      {error && <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}

      {loading ? <div className="rounded-xl bg-white p-8 text-center text-slate-600">Loading complaints…</div> :
        visibleReports.length === 0 ? <div className="rounded-xl bg-white p-10 text-center shadow-sm ring-1 ring-slate-200">
          <p className="text-lg font-semibold text-slate-800">No complaints found</p>
          <p className="mt-1 text-sm text-slate-500">Try changing the search text or status filter.</p>
        </div> :
        <div className="grid gap-4 xl:grid-cols-2">
          {visibleReports.map((report) => (
            <article key={report.id} className="overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-slate-200">
              <div className="flex flex-wrap items-start justify-between gap-3 border-b border-slate-100 p-5">
                <div>
                  <p className="text-xs font-bold uppercase tracking-wider text-blue-700">{report.complaint_code}</p>
                  <h2 className="mt-1 font-semibold text-slate-900">{report.road_name || 'Road not specified'}</h2>
                  <p className="text-sm text-slate-500">{report.area || 'Area not specified'}</p>
                </div>
                <span className={`rounded-full px-3 py-1 text-xs font-bold ${statusStyles[report.status] || 'bg-slate-100 text-slate-700'}`}>{report.status}</span>
              </div>
              <div className="grid gap-4 p-5 sm:grid-cols-[128px_1fr]">
                {report.image_path ? <a href={`http://localhost:8000${report.image_path}`} target="_blank" rel="noreferrer" aria-label="Open complaint photo">
                  <img src={`http://localhost:8000${report.image_path}`} alt="Citizen submitted road damage" className="h-28 w-32 rounded-xl object-cover ring-1 ring-slate-200" />
                </a> : <div className="flex h-28 w-32 items-center justify-center rounded-xl bg-slate-100 text-xs text-slate-500">No photo</div>}
                <div className="min-w-0">
                  <p className="text-sm leading-6 text-slate-700">{report.description}</p>
                  <p className="mt-2 text-xs text-slate-500">Reported by {report.citizen_name || 'Citizen'} · {new Date(report.created_at).toLocaleString()}</p>
                  {report.latitude != null && report.longitude != null && <a className="mt-1 inline-block text-xs font-semibold text-blue-700 hover:underline" href={`https://www.google.com/maps?q=${report.latitude},${report.longitude}`} target="_blank" rel="noreferrer">Open GPS location ↗</a>}
                  <label className="mt-4 block text-xs font-semibold uppercase tracking-wide text-slate-500">Update complaint status
                    <select value={report.status} disabled={saving === report.id} onChange={(e) => changeStatus(report.id, e.target.value)} className="mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium normal-case text-slate-800 disabled:opacity-50">
                      {statuses.map((status) => <option key={status} value={status}>{status}</option>)}
                    </select>
                  </label>
                </div>
              </div>
            </article>
          ))}
        </div>}
      <p className="text-xs text-slate-500">Citizen phone numbers are not shown in this review screen. Status changes are saved to the backend.</p>
    </div>
  );
}
