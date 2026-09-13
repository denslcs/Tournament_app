export interface Tournament {
  id: number;
  name: string;
  date: string;
  teamsCount: number;
  status: string;
  icon: string;
}

export const tournaments: Tournament[] = [
  {
    id: 1,
    name: "Турнир по CS2",
    date: "12.09.2026",
    teamsCount: 8,
    status: "Идёт",
    icon: "/icons/icons8-counter-strike-48.png"
  },
  {
    id: 2,
    name: "Турнир по Dota 2",
    date: "01.10.2026",
    teamsCount: 16,
    status: "Скоро",
    icon: "/icons/icons8-dota-2-48.png"  
  },
  {
    id: 3,
    name: "Турнир по LOL",
    date: "20.11.2026",
    teamsCount: 8,
    status: "Регистрация",
    icon: "/icons/icons8-league-of-legends-infernal-drake-48.png"
  },
  {
    id: 4,
    name: "Турнир по Fortnite",
    date: "05.09.2026",
    teamsCount: 20,
    status: "Завершён",
    icon: "/icons/icons8-fortnite-48.png"
  },
  {
    id: 5,
    name: "Турнир по Valorant",
    date: "10.09.2026",
    teamsCount: 12,
    status: "Отменён",
    icon: "/icons/icons8-valorant-48.png"
  }
];