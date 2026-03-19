import { useState } from 'react'

export default function SearchBar({ onSearch, initialQuery = '', compact = false }) {
  const [query, setQuery] = useState(initialQuery)

  function handleSubmit(e) {
    e.preventDefault()
    if (query.trim()) onSearch(query.trim())
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 8 }}>
      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Search the mini-web..."
        style={{
          width: compact ? 400 : 500,
          padding: '10px 16px',
          fontSize: compact ? 14 : 16,
          border: '1px solid #dfe1e5',
          borderRadius: 24,
          outline: 'none',
          boxShadow: '0 1px 6px rgba(0,0,0,0.1)'
        }}
      />
      <button
        type="submit"
        style={{
          padding: '10px 20px',
          background: '#f8f9fa',
          border: '1px solid #dfe1e5',
          borderRadius: 4,
          cursor: 'pointer',
          fontSize: 14
        }}
      >
        Search
      </button>
    </form>
  )
}