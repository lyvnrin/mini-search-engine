import SearchBar from '../components/SearchBar'
import { useSearch } from '../hooks/useSearch'
import { useEffect } from 'react'

export default function Results({ query, onSearch }) {
  const { results, loading, error, search } = useSearch()

  useEffect(() => { search(query) }, [query])

  return (
    <div>
      {/* Header */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: 24,
        padding: '16px 24px', borderBottom: '1px solid #ebebeb'
      }}>
        <a href='/' style={{ textDecoration: 'none' }}><span style={{
            fontFamily: "'Fredoka One', cursive",
            fontSize: 32, cursor: 'pointer', letterSpacing: 1,
            background: 'linear-gradient(135deg, #e8334a, #ff85a1)',
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
            flexShrink: 0
            }}>
            Lav-oogle
            </span></a>
        <SearchBar onSearch={onSearch} initialQuery={query} compact />
      </div>

      {/* Results */}
      <div style={{ maxWidth: 600, marginLeft: 180, padding: '20px 0' }}>
        {loading && <p style={{ color: '#5f6368' }}>Searching...</p>}
        {error && <p style={{ color: '#EA4335' }}>Error: {error}</p>}

        {results && (
          <>
            <p style={{ fontSize: 13, color: '#5f6368', marginBottom: 20 }}>
              {results.total} result{results.total !== 1 ? 's' : ''}
            </p>
            {results.total === 0 && (
              <p style={{ color: '#5f6368' }}>No results. Try crawling a site first.</p>
            )}
            {results.results.map(r => (
              <div key={r.id} style={{ marginBottom: 28 }}>
                <div style={{ fontSize: 12, color: '#202124', marginBottom: 2 }}>{r.url}</div>
                <a href={r.url} target="_blank" rel="noreferrer"
                  style={{ fontSize: 20, color: '#1a0dab' }}>
                  {r.title}
                </a>
                <p style={{ fontSize: 13, color: '#4d5156', marginTop: 4, lineHeight: 1.5 }}>
                  {r.snippet}
                </p>
                <p style={{ fontSize: 11, color: '#5f6368', marginTop: 4 }}>
                  PageRank: {r.rank_score.toExponential(3)} · Score: {r.combined_score.toFixed(4)}
                </p>
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  )
}