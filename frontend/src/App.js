import React, { useState } from 'react';
import './App.css';
import ShopperView from './components/ShopperView';
import OwnerView from './components/OwnerView';

function App() {
  const [view, setView] = useState('shopper'); // 'shopper' or 'owner'

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Mall Assistant</h1>
        <nav>
          <button onClick={() => setView('shopper')} className={view === 'shopper' ? 'active' : ''}>
            Shopper View
          </button>
          <button onClick={() => setView('owner')} className={view === 'owner' ? 'active' : ''}>
            Store Owner View
          </button>
        </nav>
      </header>
      <main>
        {view === 'shopper' ? <ShopperView /> : <OwnerView storeId="s1" />} {/* Hardcoding s1 for demo */}
      </main>
    </div>
  );
}

export default App;