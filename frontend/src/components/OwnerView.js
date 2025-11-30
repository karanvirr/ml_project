import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Line, Bar, Doughnut } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const OwnerView = ({ storeId }) => {
  const [forecast, setForecast] = useState(null);
  const [insights, setInsights] = useState([]);
  const [marketBasket, setMarketBasket] = useState([]);
  const [segments, setSegments] = useState([]);
  const [seasonal, setSeasonal] = useState([]);
  const [timeHabits, setTimeHabits] = useState(null);
  const [sentiment, setSentiment] = useState([]);
  const [personas, setPersonas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [forecastRes, insightsRes, marketBasketRes, segmentsRes, seasonalRes, timeHabitsRes, sentimentRes, personasRes] = await Promise.all([
          axios.get(`/api/stores/${storeId}/forecast`),
          axios.get(`/api/owner/${storeId}/insights`),
          axios.get('/api/analytics/market-basket'),
          axios.get('/api/analytics/customer-segments'),
          axios.get('/api/analytics/seasonal-analysis'),
          axios.get('/api/analytics/time-habits'),
          axios.get('/api/analytics/sentiment'),
          axios.get('/api/analytics/persona-insights')
        ]);
        setForecast(forecastRes.data);
        setInsights(insightsRes.data);
        setMarketBasket(marketBasketRes.data);
        setSegments(segmentsRes.data);
        setSeasonal(seasonalRes.data);
        setTimeHabits(timeHabitsRes.data);
        setSentiment(sentimentRes.data);
        setPersonas(personasRes.data);
      } catch (error) {
        console.error("Error fetching owner data:", error);
      }
      setLoading(false);
    };

    fetchData();
  }, [storeId]);

  if (loading) return <div style={{ textAlign: 'center', marginTop: '2rem' }}>Loading Dashboard...</div>;

  // --- Chart Data Preparation ---

  const chartData = forecast ? {
    labels: forecast.ds,
    datasets: [
      {
        label: 'Sales Forecast',
        data: forecast.yhat,
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
        tension: 0.4,
      },
      {
        label: 'Lower Bound',
        data: forecast.yhat_lower,
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderDash: [5, 5],
        pointRadius: 0,
        fill: false,
      },
      {
        label: 'Upper Bound',
        data: forecast.yhat_upper,
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderDash: [5, 5],
        pointRadius: 0,
        fill: false,
      }
    ],
  } : null;

  const segmentsData = segments.length > 0 ? {
    labels: segments.map(s => s.segment_name),
    datasets: [{
      label: 'Avg Spend',
      data: segments.map(s => s.total_spend),
      backgroundColor: [
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
      ],
      borderWidth: 1,
    }]
  } : null;

  const seasonalData = seasonal.length > 0 ? {
    labels: seasonal.map(s => s.month),
    datasets: [{
      label: 'Monthly Sales',
      data: seasonal.map(s => s.total_price),
      borderColor: '#10b981',
      backgroundColor: 'rgba(16, 185, 129, 0.2)',
      tension: 0.3,
      fill: true
    }]
  } : null;

  const timeHabitsData = timeHabits ? {
    labels: timeHabits.daily_sales.map(d => d.day_of_week),
    datasets: [{
      label: 'Sales by Day',
      data: timeHabits.daily_sales.map(d => d.total_price),
      backgroundColor: 'rgba(139, 92, 246, 0.7)',
      borderColor: 'rgba(139, 92, 246, 1)',
      borderWidth: 1
    }]
  } : null;

  const sentimentData = sentiment.length > 0 ? {
    labels: sentiment.map(s => s.sentiment),
    datasets: [{
      data: sentiment.map(s => s.count),
      backgroundColor: [
        '#ef4444', // Negative (Red)
        '#eab308', // Neutral (Yellow)
        '#22c55e', // Positive (Green)
      ],
      borderWidth: 0
    }]
  } : null;

  const personasData = personas.length > 0 ? {
    labels: personas.map(p => p.persona),
    datasets: [{
      label: 'Avg Spend per Visit',
      data: personas.map(p => p.avg_spend),
      backgroundColor: 'rgba(236, 72, 153, 0.7)', // Pink
      borderColor: 'rgba(236, 72, 153, 1)',
      borderWidth: 1
    }]
  } : null;

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top', labels: { color: '#94a3b8' } },
      title: { display: true, text: '7-Day Sales Forecast', color: '#f8fafc', font: { size: 16 } },
    },
    scales: {
      y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
      x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
    }
  };

  return (
    <div className="owner-dashboard" style={{ display: 'flex', flexDirection: 'column', gap: '2rem', paddingBottom: '2rem' }}>

      {/* 1. Key Insights Cards */}
      <div className="insights-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
        {insights.map((insight, idx) => (
          <div key={idx} className="glass-card">
            <h3 style={{ color: 'var(--text-muted)', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '1px' }}>
              {insight.kpi}
            </h3>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', margin: '0.5rem 0', color: 'var(--primary)' }}>
              {insight.value}
            </div>
            <p style={{ fontSize: '0.95rem', color: 'var(--text-main)', opacity: 0.9 }}>
              {insight.recommendation}
            </p>
          </div>
        ))}
      </div>

      {/* 2. Main Forecast Chart */}
      <div className="glass-card" style={{ padding: '2rem' }}>
        {chartData && <Line options={chartOptions} data={chartData} />}
      </div>

      {/* 3. Advanced Analytics Section */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem' }}>

        {/* Market Basket Analysis */}
        <div className="glass-card">
          <h3 style={{ marginBottom: '1rem', color: '#f8fafc' }}>🛍️ Frequently Bought Together</h3>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', color: '#e2e8f0' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', textAlign: 'left' }}>
                  <th style={{ padding: '0.75rem' }}>Product Pair</th>
                  <th style={{ padding: '0.75rem' }}>Confidence</th>
                  <th style={{ padding: '0.75rem' }}>Lift</th>
                </tr>
              </thead>
              <tbody>
                {marketBasket.map((rule, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                    <td style={{ padding: '0.75rem' }}>{rule.pair}</td>
                    <td style={{ padding: '0.75rem' }}>{(rule.confidence * 100).toFixed(1)}%</td>
                    <td style={{ padding: '0.75rem', color: rule.lift > 2 ? '#4ade80' : 'inherit' }}>{rule.lift}x</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Customer Segmentation */}
        <div className="glass-card">
          <h3 style={{ marginBottom: '1rem', color: '#f8fafc' }}>👥 Customer Segments (by Spend)</h3>
          {segmentsData && (
            <Bar
              data={segmentsData}
              options={{
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                  y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
                  x: { ticks: { color: '#94a3b8' } }
                }
              }}
            />
          )}
          <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
            {segments.map((seg, idx) => (
              <div key={idx} style={{ background: 'rgba(255,255,255,0.05)', padding: '0.5rem 1rem', borderRadius: '8px', fontSize: '0.85rem' }}>
                <strong>{seg.segment_name}</strong>: {seg.customer_count} customers
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* 4. Seasonal & Time Analysis */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem' }}>

        {/* Seasonal Trends */}
        <div className="glass-card">
          <h3 style={{ marginBottom: '1rem', color: '#f8fafc' }}>📅 Seasonal Trends</h3>
          {seasonalData && (
            <Line
              data={seasonalData}
              options={{
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                  y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
                  x: { ticks: { color: '#94a3b8' } }
                }
              }}
            />
          )}
        </div>

        {/* Time Habits */}
        <div className="glass-card">
          <h3 style={{ marginBottom: '1rem', color: '#f8fafc' }}>🕒 Peak Shopping Days</h3>
          {timeHabitsData && (
            <Bar
              data={timeHabitsData}
              options={{
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                  y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
                  x: { ticks: { color: '#94a3b8' } }
                }
              }}
            />
          )}
        </div>

      </div>

      {/* 5. Sentiment & Persona Analysis (NEW) */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem' }}>

        {/* Sentiment Analysis */}
        <div className="glass-card">
          <h3 style={{ marginBottom: '1rem', color: '#f8fafc' }}>😊 Customer Sentiment</h3>
          <div style={{ height: '300px', display: 'flex', justifyContent: 'center' }}>
            {sentimentData && (
              <Doughnut
                data={sentimentData}
                options={{
                  responsive: true,
                  plugins: { legend: { position: 'right', labels: { color: '#94a3b8' } } },
                }}
              />
            )}
          </div>
        </div>

        {/* Persona Insights */}
        <div className="glass-card">
          <h3 style={{ marginBottom: '1rem', color: '#f8fafc' }}>🕴️ Spending by Persona</h3>
          {personasData && (
            <Bar
              data={personasData}
              options={{
                indexAxis: 'y', // Horizontal Bar Chart
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                  x: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
                  y: { ticks: { color: '#94a3b8' } }
                }
              }}
            />
          )}
        </div>

      </div>

    </div>
  );
};

export default OwnerView;