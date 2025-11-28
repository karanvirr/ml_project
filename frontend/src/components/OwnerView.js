import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const API_URL = 'http://localhost:8000/api';

function OwnerView({ storeId }) {
  const [insights, setInsights] = useState([]);
  const [forecastData, setForecastData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // Fetch Insights
        const insightRes = await axios.get(`${API_URL}/owner/${storeId}/insights`);
        setInsights(insightRes.data);

        // Fetch Forecast
        const forecastRes = await axios.get(`${API_URL}/stores/${storeId}/forecast?horizon=7`);
        const { ds, yhat, yhat_lower, yhat_upper } = forecastRes.data;
        
        setForecastData({
          labels: ds,
          datasets: [
            {
              label: 'Forecast (yhat)',
              data: yhat,
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1,
              fill: false,
            },
            {
              label: 'Confidence Interval',
              data: yhat_upper,
              fill: '+1', // Fill to the 'yhat_lower' dataset
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'transparent',
              pointRadius: 0,
            },
            {
                label: 'Lower Bound', // Not shown in legend
                data: yhat_lower,
                borderColor: 'transparent',
                pointRadius: 0,
                legend: { display: false }
            }
          ],
        });

      } catch (error) {
        console.error("Error fetching owner data:", error);
      }
      setLoading(false);
    };

    fetchData();
  }, [storeId]);

  if (loading) {
    return <div>Loading insights for {storeId}...</div>;
  }

  return (
    <div className="owner-view">
      <h2>Business Dashboard (Store: {storeId})</h2>
      
      <h3>Key Insights & Alerts</h3>
      <div className="insights-grid">
        {insights.map((item, index) => (
          <div key={index} className="insight-card">
            <h3>{item.kpi}</h3>
            <div className="kpi-value">{item.value}</div>
            <div className="recommendation">{item.recommendation}</div>
          </div>
        ))}
      </div>

      <h3>7-Day Sales Forecast</h3>
      <div className="chart-container">
        {forecastData ? (
          <Line data={forecastData} options={{ responsive: true, plugins: { legend: { display: false } } }} />
        ) : (
          <p>No forecast data available.</p>
        )}
      </div>
    </div>
  );
}

export default OwnerView;