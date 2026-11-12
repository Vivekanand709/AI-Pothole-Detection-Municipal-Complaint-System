import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { inspectionService } from '../api/inspections';

const UploadInspection = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [roadName, setRoadName] = useState('');
  const [area, setArea] = useState('');
  const [notes, setNotes] = useState('');
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      const validTypes = ['video/mp4', 'video/avi', 'video/quicktime', 'video/x-msvideo'];
      if (!validTypes.includes(file.type)) {
        setError('Please select a valid video file (MP4, AVI, MOV)');
        setVideoFile(null);
        return;
      }
      setVideoFile(file);
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!videoFile) {
      setError('Please select a video file');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess(false);

    try {
      await inspectionService.uploadInspection(videoFile, {
        road_name: roadName,
        area: area,
        notes: notes
      });
      setSuccess(true);
      // Reset form
      setVideoFile(null);
      setRoadName('');
      setArea('');
      setNotes('');
      
      // Navigate to inspection history after a delay
      setTimeout(() => {
        navigate('/inspections');
      }, 2000);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to upload video. Please try again.';
      setError(errorMessage);
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Upload Road Inspection</h1>

      <div className="bg-white rounded-lg shadow-md p-6">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {success && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            Video uploaded successfully! Processing will start automatically. Redirecting to inspection history...
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Video File *
            </label>
            <input
              type="file"
              accept="video/mp4,video/avi,video/quicktime,video/x-msvideo"
              onChange={handleFileChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
            <p className="text-sm text-gray-500 mt-1">
              Supported formats: MP4, AVI, MOV (Max 500MB)
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Road Name
            </label>
            <input
              type="text"
              value={roadName}
              onChange={(e) => setRoadName(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="e.g., Main Street"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Area/Region
            </label>
            <input
              type="text"
              value={area}
              onChange={(e) => setArea(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="e.g., Downtown"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Notes
            </label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={3}
              placeholder="Additional notes about this inspection..."
            />
          </div>

          <button
            type="submit"
            disabled={uploading}
            className="w-full bg-municipal-blue text-white py-3 rounded-lg hover:bg-municipal-dark transition-colors disabled:opacity-50"
          >
            {uploading ? 'Uploading...' : 'Upload & Start Processing'}
          </button>
        </form>

        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h3 className="font-semibold text-blue-800 mb-2">What happens next?</h3>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>• Video will be processed in the background</li>
            <li>• AI will detect potholes frame by frame</li>
            <li>• GPS coordinates will be assigned (demo mode uses simulated data)</li>
            <li>• Severity will be calculated for each detection</li>
            <li>• Maintenance tickets will be created automatically</li>
            <li>• Results will appear on the map and in the dashboard</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default UploadInspection;
