import React, { useEffect, useState } from 'react';
import { getMatches } from './api';

export default function MatchList({ token, myId }) {
  const [matches, setMatches] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    getMatches(token)
      .then(setMatches)
      .catch(() => setError('매칭 목록을 불러오지 못했습니다.'));
  }, [token]);

  return (
    <div style={{ margin: '24px 0' }}>
      <h3>내 매칭 목록</h3>
      {matches.length === 0 && <div>매칭 내역이 없습니다.</div>}
      <ul>
        {matches.map((m) => (
          <li key={m.id} style={{ marginBottom: 8 }}>
            <span>
              멘토: {m.mentor_id} / 멘티: {m.mentee_id}
            </span>{' '}
            <span style={{ color: '#888' }}>상태: {m.status}</span>
          </li>
        ))}
      </ul>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
    </div>
  );
}
