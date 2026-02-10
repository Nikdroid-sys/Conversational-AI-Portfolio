import React from 'react';
import './Icons.css';
import SettingsIcon from './SettingsIcon';
import AboutIcon from './AboutIcon';

const Icons = ({ onSettingsClick, onAboutClick }) => {
  return (
    <div className="icons-container">
      <div className="icon" onClick={onSettingsClick}>
        <SettingsIcon />
        <span>Settings</span>
      </div>
      <div className="icon" onClick={onAboutClick}>
        <AboutIcon />
        <span>About</span>
      </div>
    </div>
  );
};

export default Icons;