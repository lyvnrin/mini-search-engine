import { useState } from 'react'

const API = import.meta.env.VITE_API_URL || ''

export function useCrawl() {
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function startCrawl(seedUrl, maxDepth = 2, maxPages = 50) {
    setLoading(true)
    setError(null)
    setStatus(null)
    try {
      const res = await fetch(`${API}/crawl/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ seed_url: seedUrl, max_depth: maxDepth, max_pages: maxPages })
      })
      if (!res.ok) throw new Error('Crawl failed')
      const data = await res.json()
      setStatus(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return { status, loading, error, startCrawl }
}