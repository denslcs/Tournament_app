import { useParams, Link } from 'react-router-dom';
import { tournaments } from '../data/tournaments';

function MatchPage() {
  const { id } = useParams();
  const match = tournaments.find(t => t.id === Number(id));

  if (!match) {
    return <h1>Турнир не найден</h1>;
  }

  return (
    <div>
      <Link 
        to="/tournaments" 
        style={{ 
          color: '#0cc98a', 
          textDecoration: 'none',
          display: 'inline-block',
          marginBottom: '30px'
        }}
      >
        ← Назад к списку турниров
      </Link>

      <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
        <img 
          src={match.icon} 
          alt={match.name}
          style={{ width: '64px', height: '64px', borderRadius: '12px' }}
        />
        <h1 style={{ margin: 0 }}>{match.name}</h1>
      </div>
      
      <div style={{ marginTop: '20px' }}>
        <p><strong>📅 Дата:</strong> {match.date}</p>
        <p><strong> Команд:</strong> {match.teamsCount}</p>
        <p><strong>📊 Статус:</strong> {match.status}</p>
      </div>

      <div style={{ marginTop: '40px' }}>
        <h2>Групповой этап</h2>
        <p style={{ color: '#aaa' }}>Здесь будет таблица групп и расписание матчей</p>
      </div>

      <div style={{ marginTop: '30px' }}>
        <h2>Плей-офф</h2>
        <p style={{ color: '#aaa' }}>Здесь будет сетка плей-офф</p>
      </div>
    </div>
  );
}

export default MatchPage;