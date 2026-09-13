import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { 
  AppBar, Toolbar, Typography, Container, Box
} from '@mui/material';
import HomePage from './pages/HomePage';
import TournamentsPage from './pages/TournamentsPage';
import MatchPage from './pages/MatchPage';

function App() {
  return (
    <BrowserRouter>
      <Box
        sx={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          backgroundImage: 'url(/images/3d-fantasy-scene.jpg)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
          zIndex: -2,
        }}
      />

      <AppBar position="static" sx={{ backgroundColor: 'rgb(17, 78, 11, 0.8)' }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1, color: '#fcfcfc' }}>
             Tournament Manager
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Link to="/" style={{ color: '#fff', textDecoration: 'none' }}>
              Главная
            </Link>
            <Link to="/tournaments" style={{ color: '#fff', textDecoration: 'none' }}>
              Турниры
            </Link>
          </Box>
        </Toolbar>
      </AppBar>

      <Container  
        sx={{ 
          mt: 0, 
          mb: 0, 
          bgcolor: 'rgba(18, 18, 18, 0.9)', 
          borderRadius: 1,
          p: 3,
          minHeight: '100vh'
        }}
      >
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/tournaments" element={<TournamentsPage />} />
          <Route path="/match/:id" element={<MatchPage />} />
        </Routes>
      </Container>

    </BrowserRouter>
  );
}

export default App;