import React, { useState } from 'react';
import { signup } from './api';

export default function Signup({ onSignup }) {
  const [form, setForm] = useState({
    username: '',
    password: '',
    name: '',
    role: 'mentee',
    bio: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    setSuccess(false);
    try {
      await signup(form);
      setSuccess(true);
      onSignup && onSignup();
    } catch (err) {
      setError('회원가입 실패: ' + err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 350, margin: '40px auto' }}>
      <h2>회원가입</h2>
      <input name="username" placeholder="아이디" value={form.username} onChange={handleChange} required style={{ width: '100%', marginBottom: 8 }} />
      <input name="password" type="password" placeholder="비밀번호" value={form.password} onChange={handleChange} required style={{ width: '100%', marginBottom: 8 }} />
      <input name="name" placeholder="이름" value={form.name} onChange={handleChange} required style={{ width: '100%', marginBottom: 8 }} />
      <select name="role" value={form.role} onChange={handleChange} style={{ width: '100%', marginBottom: 8 }}>
        <option value="mentee">멘티</option>
        <option value="mentor">멘토</option>
      </select>
      <textarea name="bio" placeholder="소개" value={form.bio} onChange={handleChange} style={{ width: '100%', marginBottom: 8 }} />
      <button type="submit" style={{ width: '100%' }}>회원가입</button>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
      {success && <div style={{ color: 'green', marginTop: 8 }}>회원가입 성공! 로그인 해주세요.</div>}
    </form>
  );
}
