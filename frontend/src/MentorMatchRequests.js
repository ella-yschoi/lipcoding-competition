import React, { useEffect, useState } from 'react';

const API_URL = 'http://localhost:8000';

async function getPendingRequests(token) {
  const res = await fetch(`${API_URL}/mentor/match-requests/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('매칭 요청 목록 조회 실패');
  return await res.json();
}

async function updateMatchStatus(token, matchId, status) {
  const res = await fetch(
    `${API_URL}/mentor/match-requests/${matchId}/status?status=${status}`,
    {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
    }
  );
  if (!res.ok) throw new Error('상태 변경 실패');
  return await res.json();
}

export default function MentorMatchRequests({ token }) {
  const [requests, setRequests] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const fetchRequests = () => {
    getPendingRequests(token)
      .then(setRequests)
      .catch(() => setError('매칭 요청 목록을 불러오지 못했습니다.'));
  };

  useEffect(() => {
    fetchRequests();
    // eslint-disable-next-line
  }, [token]);

  const handleStatus = async (id, status) => {
    setError('');
    setSuccess('');
    try {
      await updateMatchStatus(token, id, status);
      setSuccess('상태 변경 완료!');
      fetchRequests();
    } catch (e) {
      setError('상태 변경 실패: ' + e.message);
    }
  };

  return (
    <div style={{ margin: '24px 0' }}>
      <h3>받은 매칭 신청 (대기중)</h3>
      {requests.length === 0 && <div>대기중인 매칭 신청이 없습니다.</div>}
      <ul>
        {requests.map((r) => (
          <li key={r.id} style={{ marginBottom: 8 }}>
            <span>멘티: {r.mentee_id}</span>
            <span style={{ marginLeft: 8, color: '#888' }}>
              상태: {r.status}
            </span>
            <button
              onClick={() => handleStatus(r.id, 'accepted')}
              style={{ marginLeft: 8 }}
            >
              수락
            </button>
            <button
              onClick={() => handleStatus(r.id, 'rejected')}
              style={{ marginLeft: 4 }}
            >
              거절
            </button>
          </li>
        ))}
      </ul>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
      {success && <div style={{ color: 'green', marginTop: 8 }}>{success}</div>}
    </div>
  );
}
