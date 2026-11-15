import React, { useState } from 'react';
import apiClient from '../api/client';

const CitizenReport = () => {
  const [form, setForm] = useState({ citizen_name: '', phone: '', description: '', road_name: '', area: '' });
  const [photo, setPhoto] = useState(null);
  const [coordinates, setCoordinates] = useState(null);
  const [trackingCode, setTrackingCode] = useState('');
  const [trackInput, setTrackInput] = useState('');
  const [trackedReport, setTrackedReport] = useState(null);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');

  const update = (event) => setForm({ ...form, [event.target.name]: event.target.value });

  const captureLocation = () => {
    setMessage('');
    if (!navigator.geolocation) {
      setMessage('This browser does not support GPS location.');
      return;
    }
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => setCoordinates({ latitude: coords.latitude, longitude: coords.longitude }),
      () => setMessage('Location permission was not granted. You can still submit without GPS.'),
      { enableHighAccuracy: true, timeout: 10000 }
    );
  };

  const submitReport = async (event) => {
    event.preventDefault();
    if (!photo) return setMessage('Please select a road photo.');
    const data = new FormData();
    Object.entries(form).forEach(([key, value]) => data.append(key, value));
    if (coordinates) {
      data.append('latitude', coordinates.latitude);
      data.append('longitude', coordinates.longitude);
    }
    data.append('photo', photo);
    setBusy(true);
    setMessage('');
    try {
      const response = await apiClient.post('/api/citizen-reports', data);
      setTrackingCode(response.data.complaint_code);
      setTrackedReport(response.data);
      setForm({ citizen_name: '', phone: '', description: '', road_name: '', area: '' });
      setPhoto(null);
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Report could not be submitted. Please try again.');
    } finally {
      setBusy(false);
    }
  };

  const trackComplaint = async (event) => {
    event.preventDefault();
    setBusy(true);
    setMessage('');
    setTrackedReport(null);
    try {
      const response = await apiClient.get(`/api/citizen-reports/track/${encodeURIComponent(trackInput.trim())}`);
      setTrackedReport(response.data);
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Unable to track this complaint.');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-10">
      <div className="mx-auto max-w-5xl">
        <header className="mb-8 text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-blue-700">RoadGuard AI · Citizen Portal</p>
          <h1 className="mt-3 text-3xl font-bold text-slate-900 md:text-4xl">Report a Road Problem</h1>
          <p className="mt-2 text-slate-600">Share a pothole photo and location so the municipal team can review it.</p>
        </header>

        {trackingCode && (
          <div className="mb-6 rounded-xl border border-emerald-200 bg-emerald-50 p-5 text-emerald-900">
            <p className="font-semibold">Your report was submitted.</p>
            <p className="mt-1 text-sm">Save this tracking code to check its status:</p>
            <p className="mt-2 text-2xl font-bold tracking-wider">{trackingCode}</p>
          </div>
        )}

        {message && <div className="mb-5 rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900">{message}</div>}

        <div className="grid gap-6 md:grid-cols-2">
          <form onSubmit={submitReport} className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
            <h2 className="mb-5 text-xl font-bold text-slate-900">Submit a new complaint</h2>
            <div className="space-y-4">
              <label className="block text-sm font-medium text-slate-700">Your name
                <input required name="citizen_name" minLength="2" maxLength="100" value={form.citizen_name} onChange={update} className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2" />
              </label>
              <label className="block text-sm font-medium text-slate-700">Phone number
                <input required name="phone" minLength="10" maxLength="15" value={form.phone} onChange={update} className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2" />
              </label>
              <label className="block text-sm font-medium text-slate-700">Road / street name
                <input name="road_name" value={form.road_name} onChange={update} className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2" placeholder="e.g. University Road" />
              </label>
              <label className="block text-sm font-medium text-slate-700">Area / locality
                <input name="area" value={form.area} onChange={update} className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2" placeholder="e.g. Phagwara" />
              </label>
              <label className="block text-sm font-medium text-slate-700">Describe the problem
                <textarea required name="description" minLength="10" maxLength="2000" rows="3" value={form.description} onChange={update} className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2" placeholder="Describe the pothole and any safety concern..." />
              </label>
              <label className="block text-sm font-medium text-slate-700">Road photo (JPG, PNG, WEBP · max 8 MB)
                <input required type="file" accept="image/jpeg,image/png,image/webp" onChange={(e) => setPhoto(e.target.files?.[0] || null)} className="mt-1 block w-full text-sm" />
              </label>
              <div className="rounded-lg bg-slate-50 p-3 text-sm text-slate-600">
                {coordinates ? `GPS captured: ${coordinates.latitude.toFixed(5)}, ${coordinates.longitude.toFixed(5)}` : 'GPS location is optional.'}
                <button type="button" onClick={captureLocation} className="ml-2 font-semibold text-blue-700 underline">Capture my location</button>
              </div>
              <button disabled={busy} className="w-full rounded-lg bg-blue-700 px-4 py-3 font-semibold text-white hover:bg-blue-800 disabled:opacity-50">{busy ? 'Please wait...' : 'Submit Road Complaint'}</button>
            </div>
          </form>

          <div className="space-y-6">
            <form onSubmit={trackComplaint} className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
              <h2 className="mb-2 text-xl font-bold text-slate-900">Track your complaint</h2>
              <p className="mb-4 text-sm text-slate-600">Enter the tracking code you received after submission.</p>
              <input required value={trackInput} onChange={(e) => setTrackInput(e.target.value)} placeholder="e.g. RGA-12AB34CD" className="w-full rounded-lg border border-slate-300 px-3 py-2" />
              <button disabled={busy} className="mt-3 w-full rounded-lg border border-blue-700 px-4 py-2 font-semibold text-blue-700 hover:bg-blue-50 disabled:opacity-50">Track Status</button>
            </form>

            {trackedReport && (
              <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
                <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Complaint {trackedReport.complaint_code}</p>
                <p className="mt-2 text-2xl font-bold text-slate-900">{trackedReport.status}</p>
                <p className="mt-2 text-sm text-slate-600">{trackedReport.description}</p>
                <p className="mt-3 text-sm text-slate-600">{trackedReport.road_name || 'Road not specified'} · {trackedReport.area || 'Area not specified'}</p>
                <p className="mt-1 text-xs text-slate-500">Submitted {new Date(trackedReport.created_at).toLocaleString()}</p>
              </div>
            )}

            <div className="rounded-2xl bg-blue-950 p-6 text-white">
              <h3 className="text-lg font-bold">What happens next?</h3>
              <ol className="mt-3 list-inside list-decimal space-y-2 text-sm text-blue-100">
                <li>Your complaint is saved with a unique tracking code.</li>
                <li>The municipal team can review the report.</li>
                <li>Use the tracking code to check its latest status.</li>
              </ol>
              <p className="mt-4 text-xs text-blue-200">GPS is collected only when you choose to share it. Do not upload photos containing private or sensitive information.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CitizenReport;
