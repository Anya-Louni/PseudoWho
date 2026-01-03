# PseudoQui - Frontend

Beautiful, interactive React frontend for the PseudoQui animal guessing game.

## Features

- **Modern UI/UX**: Gradient design with smooth animations
- **Real-time Interactions**: Instant feedback on game state
- **Statistics Dashboard**: Comprehensive analytics and tree visualization
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Beautiful Animations**: Smooth transitions and interactions

## Installation

### Requirements
- Node.js 14+
- npm or yarn

### Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## Building for Production

```bash
npm run build
```

This creates an optimized build in the `build/` directory.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── MenuScreen.jsx      # Main menu
│   │   ├── GameScreen.jsx      # Game interface
│   │   └── StatisticsScreen.jsx # Stats dashboard
│   ├── hooks/
│   │   └── useGameStore.js     # Zustand state management
│   ├── styles/
│   │   └── styles.css          # Complete styling
│   ├── App.jsx                 # Main app component
│   └── index.jsx               # Entry point
├── public/
│   └── index.html
├── package.json
└── README.md
```

## API Integration

The frontend communicates with the Python backend via REST API endpoints:

### Game Endpoints
- `POST /api/game/start` - Start new game
- `POST /api/game/answer` - Submit answer
- `POST /api/game/guess-result` - Submit guess result
- `POST /api/game/learn` - Teach new animal
- `POST /api/game/end` - End game

### Data Endpoints
- `GET /api/tree/display` - Tree text representation
- `GET /api/stats` - Game statistics
- `GET /api/animals` - List of animals

## Features

### Game Screen
- Question display
- Yes/No answer buttons
- Question counter
- Guess feedback
- Learn new animal form

### Statistics Screen
- Tree structure metrics
- Game performance stats
- Known animals list
- Tree visualization
- Insights and analysis

### Menu Screen
- Play game option
- View statistics
- Game instructions
- Feature highlights

## Styling

The app features:
- **Color Scheme**: Purple gradient theme
- **Animations**: Smooth slide-in and hover effects
- **Responsive Grid**: Mobile-friendly layouts
- **Modern Components**: Cards, buttons, badges
- **Accessibility**: Clear contrast and readable text

## Configuration

API endpoint can be configured via environment variable:
```bash
REACT_APP_API_URL=http://your-api-url/api
```

Default is `http://localhost:5000/api`

## Development

For development with hot reload:
```bash
npm start
```

## Performance

- Lazy loading of components
- Efficient state management with Zustand
- Optimized CSS animations
- Minimal re-renders

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Author

Created for University Project - PseudoQui Assignment

## License

MIT
