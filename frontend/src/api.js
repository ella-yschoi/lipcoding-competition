const API_URL = 'http://localhost:8000';

export async function signup(data) {
  const res = await fetch(`${API_URL}/users/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('회원가입 실패');
  return await res.json();
}

export async function login({ username, password }) {
  const res = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username, password }),
  });
  if (!res.ok) throw new Error('로그인 실패');
  return await res.json();
}

export async function getProfile(token) {
  const res = await fetch(`${API_URL}/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('프로필 조회 실패');
  return await res.json();
}

export async function getUsers() {
  const res = await fetch(`${API_URL}/users/`);
  if (!res.ok) throw new Error('사용자 목록 조회 실패');
  return await res.json();
}

export async function createMatch(token, mentor_id) {
  const res = await fetch(`${API_URL}/matches/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ mentor_id }),
  });
  if (!res.ok) throw new Error('매칭 신청 실패');
  return await res.json();
}

export async function getMatches(token) {
  const res = await fetch(`${API_URL}/matches/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('매칭 목록 조회 실패');
  return await res.json();
}
