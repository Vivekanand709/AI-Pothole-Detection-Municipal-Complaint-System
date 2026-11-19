import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '../api/client';

export default function RepairVerification() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [beforePhoto, setBeforePhoto] = useState(null);
  const [afterPhoto, setAfterPhoto] = useState(null);
  const [notes, setNotes] = useState('');
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');

  const submit = async (event) => {
    event.preventDefault();
    if (!beforePhoto || !afterPhoto) {
      setMessage('Please upload both before and after photos.');
      return;
    }
    const data = new FormData();
    data.append('before_photo', beforePhoto);
    data.append('after_photo', afterPhoto);
    data.append('notes', notes);
    setBusy(true);
    setMessage('');
    try {
      await apiClient.post(`/api/tickets/${id}/verification`, data);
      setMessage('Repair evidence submitted. Ticket marked as resolved.');
      setTimeout(() => navigate(`/tickets/${id}`), 900);
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Could not submit repair evidence.');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <button onClick={() => navigate(`/tickets/${id}`)} className="text-blue-700 hover:underline">← Back to ticket</button>
      <header>
        <p className="text-sm font-semibold uppercase tracking-wider text-blue-700">RoadGuard AI · Quality Control</p>
        <h1 className="mt-2 text-3xl font-bold text-slate-900">Repair Verification</h1>
        <p className="mt-2 text-slate-600">Upload clear photos from before and after the road repair. Submission resolves this ticket.</p>
      </header>
      {message && <div role="status" className="rounded-lg bg-blue-50 p-4 text-blue-900">{message}</div>}
      <form onSubmit={submit} className="space-y-5 rounded-2xl bg-white p-6 shadow-sm">
        <div className="grid gap-5 md:grid-cols-2">
          <label className="block text-sm font-semibold text-slate-700">Before repair photo
            <input className="mt-2 block w-full rounded-lg border p-3" type="file" accept="image/jpeg,image/png,image/webp" onChange={e => setBeforePhoto(e.target.files?.[0] || null)} required />
            {beforePhoto && <img className="mt-3 h-48 w-full rounded-lg object-cover" src={URL.createObjectURL(beforePhoto)} alt="Before repair preview" />}
          </label>
          <label className="block text-sm font-semibold text-slate-700">After repair photo
            <input className="mt-2 block w-full rounded-lg border p-3" type="file" accept="image/jpeg,image/png,image/webp" onChange={e => setAfterPhoto(e.target.files?.[0] || null)} required />
            {afterPhoto && <img className="mt-3 h-48 w-full rounded-lg object-cover" src={URL.createObjectURL(afterPhoto)} alt="After repair preview" />}
          </label>
        </div>
        <label className="block text-sm font-semibold text-slate-700">Repair notes (optional)
          <textarea value={notes} onChange={e => setNotes(e.target.value)} rows={3} maxLength={2000} className="mt-2 w-full rounded-lg border p-3 font-normal" placeholder="Describe the repair carried out..." />
        </label>
        <button disabled={busy} className="rounded-lg bg-blue-700 px-6 py-3 font-semibold text-white hover:bg-blue-800 disabled:opacity-50">{busy ? 'Submitting...' : 'Submit evidence & resolve ticket'}</button>
      </form>
    </div>
  );
}
