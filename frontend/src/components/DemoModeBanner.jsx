import React from 'react';

const DemoModeBanner = () => {
  return (
    <div className="bg-amber-500 text-black px-6 py-3 text-center font-bold border-b-4 border-amber-600 shadow-md">
      <div className="flex items-center justify-center space-x-2">
        <span className="text-xl">⚠️</span>
        <span className="uppercase tracking-wider">Demo Mode — Detection data is simulated</span>
        <span className="text-xl">⚠️</span>
      </div>
    </div>
  );
};

export default DemoModeBanner;
