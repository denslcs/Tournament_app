import { Link } from 'react-router-dom';
import { tournaments } from '../data/tournaments';
import { 
  Typography, 
  Card, 
  Chip, 
  Box, 
  Avatar,
  Stack
} from '@mui/material';

function TournamentsPage() {
  return (
    <Box>
      <Typography variant="h3" gutterBottom sx={{ mb: 3 }}>
        Список турниров
      </Typography>
      
      <Stack spacing={2} sx={{ mt: 3 }}>
        {tournaments.map((match) => (
          <Link
            to={`/match/${match.id}`}
            key={match.id}
            style={{ textDecoration: 'none', color: 'inherit' }}
          >
            <Card 
              sx={{ 
                p: 2,
                bgcolor: '#1e1e1e',
                color: '#fff',
                border: '1px solid #444',
                borderRadius: 2,
                '&:hover': { 
                  bgcolor: '#2a2a2a',
                  borderColor: '#555'
                }
              }}
            >
              <Box sx={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center' 
              }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Avatar 
                    src={match.icon} 
                    alt={match.name}
                    sx={{ width: 48, height: 48, borderRadius: 1 }}
                  />
                  <Box>
                    <Typography variant="h6" sx={{ m: 0, fontSize: '18px' }}>
                      {match.name}
                    </Typography>
                    <Typography variant="body2" sx={{ color: '#aaa', m: 0 }}>
                      📅 {match.date} • 👥 {match.teamsCount} команд
                    </Typography>
                  </Box>
                </Box>
                
                <Chip 
                  label={match.status}
                  sx={{ 
                    backgroundColor: 
                      match.status === 'Идёт' ? '#4caf50' :  
                      match.status === 'Скоро' ? '#ff9800' :
                      match.status === 'Регистрация' ? '#2196f3' : 
                      match.status === 'Завершён' ? '#757575' : 
                      match.status === 'Отменён' ? '#f44336' : '#777',
                    color: '#fff',
                    fontWeight: 'bold',
                    mr: 1
                  }}
                />
              </Box>
            </Card>
          </Link>
        ))}
      </Stack>
    </Box>
  );
}

export default TournamentsPage;