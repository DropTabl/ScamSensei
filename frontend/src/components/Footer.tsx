
import React from 'react';

const Footer = () => {
  return (
    <footer className="mt-8 p-4 text-center text-gray-600 text-sm bg-scamSensei-light/30">
      <p>© {new Date().getFullYear()} Scam Sensei • WhatsApp Scam Detector</p>
      <p className="mt-1">Stay safe online</p>
    </footer>
  );
};

export default Footer;
