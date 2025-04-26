import { useState } from 'react'
import './App.css'
import axios from 'axios'

type MovieInfo = {
  rating: string;
  year: string;
  description: string;
};
type MoviesResponse = Record<string, MovieInfo>;

function App() {
  const [query, setQuery] = useState('')
  const [movies, setMovies] = useState<MoviesResponse>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = (searchQuery: string) => {
    setLoading(true)
    const formData = new FormData();
    formData.append('query', searchQuery);
    axios.post('http://localhost:5000/recommend', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
      .then((response) => {
        console.log(response.data.response)
        setMovies(response.data.response)
        setLoading(false)
      })
      .catch((error) => {
        console.error('Error fetching recommendations:', error)
        setError(error.message)
        setLoading(false)
      })
    setQuery(searchQuery)
  }
  
  if (loading) return <div className="container">Loading...</div>;
  if (error) return <div className="container error">Error: {error}</div>;

  return (
    <div className="container">
      <h1>Movie Recommender</h1>
      <div className="search-container">
        <input
          type="text"
          placeholder="Search for a movie..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="search-input"
        />
        <button
          onClick={() => handleSearch(query)}
          className="search-button"
        >
          Search
        </button>
      </div>
      <div className="movies-grid">
        {Object.entries(movies).map(([title, info]) => (
          <div className="movie-card" key={title}>
            <h2>{title}</h2>
            <div className="movie-meta">
              <span className="year">{info.year}</span>
              <span className="rating">⭐ {info.rating}</span>
            </div>
            <p className="description">{info.description}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App
