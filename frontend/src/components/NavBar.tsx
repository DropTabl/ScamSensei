
import React from 'react';

const NavBar = () => {
  return (
    <header className="bg-scamSensei-teal p-4 text-white">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <div className="bg-white text-scamSensei-teal p-1.5 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
              <path d="M12 9v4"></path>
              <path d="M12 17h.01"></path>
            </svg>
          </div>
          <h1 className="text-xl font-bold">Scam Sensei</h1>
        </div>
        <div className="text-sm">
          WhatsApp Scam Detector
        </div>
      </div>
    </header>
  );
};

export default NavBar;
