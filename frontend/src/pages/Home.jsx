import { useState } from 'react'
import SearchBar from '../components/SearchBar'
import { useCrawl } from '../hooks/useCrawl'

export default function Home({ onSearch }) {
  const [showCrawl, setShowCrawl] = useState(false)
  const [seedUrl, setSeedUrl] = useState('')
  const [depth, setDepth] = useState(2)
  const [pages, setPages] = useState(50)
  const { status, loading, error, startCrawl } = useCrawl()

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: 120 }}>
      <h1 style={{
        fontFamily: "'Fredoka One', cursive",
        fontSize: 80, letterSpacing: 2,
        background: 'linear-gradient(135deg, #e8334a 0%, #ff85a1 50%, #e8334a 100%)',
        backgroundSize: '200% auto',
        WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
        animation: 'shimmer 3s linear infinite',
        filter: 'drop-shadow(0 4px 12px rgba(232,51,74,0.25))'
        }}>
        Lav-oogle
    </h1>
      <p style={{ color: '#5f6368', marginBottom: 32, fontSize: 14 }}>
        a very serious search engine™
      </p>

      <SearchBar onSearch={onSearch} />

      <div style={{ marginTop: 24, display: 'flex', gap: 12 }}>
        <button
          onClick={() => onSearch('the')}
          style={ghostBtn}
        >
          I'm Feeling Lucky
        </button>
        <button
          onClick={() => setShowCrawl(s => !s)}
          style={ghostBtn}
        >
          🕷️ Crawl a Site
        </button>
      </div>

      {showCrawl && (
        <div style={{
          marginTop: 32, padding: 24, border: '1px solid #dfe1e5',
          borderRadius: 8, width: 480, display: 'flex', flexDirection: 'column', gap: 12
        }}>
          <h3 style={{ fontSize: 16 }}>Crawl a new site</h3>
          <input
            placeholder="https://example.com"
            value={seedUrl}
            onChange={e => setSeedUrl(e.target.value)}
            style={inputStyle}
          />
          <div style={{ display: 'flex', gap: 12 }}>
            <label style={{ fontSize: 13 }}>
              Depth
              <input type="number" min={1} max={4} value={depth}
                onChange={e => setDepth(Number(e.target.value))}
                style={{ ...inputStyle, width: 60, marginLeft: 8 }} />
            </label>
            <label style={{ fontSize: 13 }}>
              Max pages
              <input type="number" min={10} max={100} value={pages}
                onChange={e => setPages(Number(e.target.value))}
                style={{ ...inputStyle, width: 70, marginLeft: 8 }} />
            </label>
          </div>
          <button
            onClick={() => startCrawl(seedUrl, depth, pages)}
            disabled={loading || !seedUrl}
            style={{ ...ghostBtn, background: '#1a73e8', color: '#fff', border: 'none' }}
          >
            {loading ? 'Crawling...' : 'Start crawl'}
          </button>
          {status && (
            <p style={{ fontSize: 13, color: '#34A853' }}>
              ✓ {status.pages_crawled} pages crawled, {status.links_found} links, PageRank computed
            </p>
          )}
          {error && <p style={{ fontSize: 13, color: '#EA4335' }}>✗ {error}</p>}
        </div>
      )}
    </div>
  )
}

const ghostBtn = {
  padding: '10px 20px', background: '#f8f9fa',
  border: '1px solid #dfe1e5', borderRadius: 4,
  cursor: 'pointer', fontSize: 14
}

const inputStyle = {
  padding: '8px 12px', border: '1px solid #dfe1e5',
  borderRadius: 4, fontSize: 14, width: '100%'
}