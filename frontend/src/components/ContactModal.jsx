import React, { useState } from 'react';
import './ContactModal.css';

const ContactModal = ({ show, onClose, onSubmit }) => {
  const [name, setName] = useState('');
  const [contact, setContact] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ name, contact });
    onClose();
  };

  return (
    <div className={`contact-panel ${show ? 'show' : ''}`}>
      <button className="contact-close" onClick={onClose}>
        &times;
      </button>
      <div className="contact-form-container">
        <h2>Tell us about yourself!</h2>
        <p>Optionally, provide a way to contact you</p>
        <form onSubmit={handleSubmit} className="contact-form">
          <label htmlFor="name">Name</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <label htmlFor="contact">Contact (Email or Phone or linkedin)</label>
          <input
            type="text"
            id="contact"
            value={contact}
            onChange={(e) => setContact(e.target.value)}
          />
          <button type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
};

export default ContactModal;

