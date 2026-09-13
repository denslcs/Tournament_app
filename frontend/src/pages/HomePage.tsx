import { Typography, Box, Card, CardContent } from '@mui/material';

function HomePage() {
  return (
    <Box sx={{ textAlign: 'center', py: 5 }}>
      <Typography variant="h2" gutterBottom>
        🏆 Tournament Manager
      </Typography>
      
      <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto', mb: 4 }}>
        Платформа для управления спортивными турнирами. 
        Создавайте турниры, отслеживайте результаты, 
        следите за турнирной сеткой в реальном времени.
      </Typography>

      <Box sx={{ display: 'flex', gap: 3, mt: 4, flexWrap: 'wrap', justifyContent: 'center' }}>
        <Box sx={{ flex: '1 1 300px', maxWidth: 400 }}>
          <Card sx={{bgcolor: '#195c1e', color: '#fdfdfd'}}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                 Групповой этап
              </Typography>
              <Typography color="text.secondary">
                Команды играют друг с другом в группах
              </Typography>
            </CardContent>
          </Card>
        </Box>
        
        <Box sx={{ flex: '1 1 300px', maxWidth: 400 }}>
          <Card sx={{bgcolor: '#195c1e', color: '#fdfdfd'}}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                 Плей-офф
              </Typography>
              <Typography color="text.secondary">
                Лучшие команды выходят в финальную стадию
              </Typography>
            </CardContent>
          </Card>
        </Box>
        
        <Box sx={{ flex: '1 1 300px', maxWidth: 400 }}>
          <Card sx={{bgcolor: '#195c1e', color: '#fdfdfd'}}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                 Статистика
              </Typography>
              <Typography color="text.secondary">
                Отслеживайте результаты и таблицы
              </Typography>
            </CardContent>
          </Card>
        </Box>
      </Box>
    </Box>
  );
}

export default HomePage;