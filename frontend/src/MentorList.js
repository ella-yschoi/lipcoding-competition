import React, { useEffect, useState } from 'react';
import { getUsers, createMatch } from './api';

export default function MentorList({ token, myId, onMatch }) {
  const [mentors, setMentors] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    getUsers()
      .then(users => setMentors(users.filter(u => u.role === 'mentor' && u.id !== myId)))
      .catch(() => setError('멘토 목록을 불러오지 못했습니다.'));
  }, [myId]);

  const handleMatch = async (mentorId) => {
    setError('');
    setSuccess('');
    try {
      await createMatch(token, mentorId);
      setSuccess('매칭 신청 완료!');
      onMatch && onMatch();
    } catch (e) {
      setError('매칭 신청 실패: ' + e.message);
    }
  };

  return (
    <div style={{ margin: '24px 0' }}>
      <h3>멘토 목록</h3>
      {mentors.length === 0 && <div>멘토가 없습니다.</div>}
      <ul>
        {mentors.map(m => (
          <li key={m.id} style={{ marginBottom: 8 }}>
            <b>{m.name}</b> <span style={{ color: '#888' }}>@{m.username}</span>
            <div style={{ fontSize: 13, color: '#555' }}>{m.bio}</div>
            <button onClick={() => handleMatch(m.id)} style={{ marginTop: 4 }}>매칭 신청</button>
          </li>
        ))}
      </ul>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
      {success && <div style={{ color: 'green', marginTop: 8 }}>{success}</div>}
    </div>
  );
}
