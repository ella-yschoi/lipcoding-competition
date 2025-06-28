import React, { useState } from 'react';
import Login from './Login';
import Signup from './Signup';
import MentorList from './MentorList';
import MatchList from './MatchList';
import { getProfile } from './api';
import MentorMatchRequests from './MentorMatchRequests';

function App() {
  const [token, setToken] = useState(null);
  const [profile, setProfile] = useState(null);
  const [showSignup, setShowSignup] = useState(false);

  const handleLogin = async (tk) => {
    setToken(tk);
    try {
      const user = await getProfile(tk);
      setProfile(user);
    } catch {
      setProfile(null);
    }
  };

  if (!token) {
    return (
      <div style={{ padding: 40 }}>
        <h1>멘토-멘티 매칭 앱</h1>
        {showSignup ? (
          <>
            <Signup onSignup={() => setShowSignup(false)} />
            <button
              onClick={() => setShowSignup(false)}
              style={{ width: '100%' }}
            >
              로그인으로 돌아가기
            </button>
          </>
        ) : (
          <>
            <Login onLogin={handleLogin} />
            <button
              onClick={() => setShowSignup(true)}
              style={{ width: '100%' }}
            >
              회원가입
            </button>
          </>
        )}
      </div>
    );
  }

  return (
    <div style={{ padding: 40 }}>
      <h1>멘토-멘티 매칭 앱</h1>
      <div style={{ marginBottom: 16 }}>
        <b>{profile?.name}</b> ({profile?.role})
        <div style={{ color: '#555', fontSize: 14 }}>{profile?.bio}</div>
      </div>
      {profile?.role === 'mentee' && (
        <MentorList token={token} myId={profile.id} />
      )}
      {profile?.role === 'mentor' && <MentorMatchRequests token={token} />}
      <MatchList token={token} myId={profile.id} />
      <button
        onClick={() => {
          setToken(null);
          setProfile(null);
        }}
      >
        로그아웃
      </button>
    </div>
  );
}

export default App;
