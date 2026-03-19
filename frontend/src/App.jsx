import { useState } from 'react'
import Home from './pages/Home'
import Results from './pages/Results'

export default function App() {
  const [query, setQuery] = useState(null)

  return query
    ? <Results query={query} onSearch={q => setQuery(q)} />
    : <Home onSearch={q => setQuery(q)} />
}