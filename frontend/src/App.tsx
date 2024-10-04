import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from 'react-router-dom'
import Home from './pages/Home'
import LoadItems from './pages/LoadItems'
import MatchItems from './pages/MatchItems'
import CurrentData from './pages/CurrentData'
import RootLayout from './layouts/RootLayout'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const App: React.FC = () => {
  const queryClient = new QueryClient()

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <RootLayout>
          <Routes>
            <Route path="/" element={<Navigate to="/home" replace={true} />} />
            <Route path="/home" element={<Home />} />
            <Route path="/load-items" element={<LoadItems />} />
            <Route path="/match-items" element={<MatchItems />} />
            <Route path="/current-data" element={<CurrentData />} />
          </Routes>
        </RootLayout>
      </Router>
    </QueryClientProvider>
  )
}

export default App
