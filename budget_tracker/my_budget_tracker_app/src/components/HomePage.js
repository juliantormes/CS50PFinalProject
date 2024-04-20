import React, { useEffect, useState } from 'react';
import axiosInstance from '../api/axiosApi';
import { format, startOfMonth, endOfMonth, addMonths, subMonths, parse } from 'date-fns';
import { useNavigate, useLocation } from 'react-router-dom';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const HomePage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const year = parseInt(searchParams.get('year')) || new Date().getFullYear();
  const month = parseInt(searchParams.get('month')) || new Date().getMonth() + 1; // getMonth() is 0-indexed

  const [data, setData] = useState({
    incomes: [],
    expenses: [],
    creditCardExpenses: [],
  });
  
  useEffect(() => {
    const currentDate = new Date(year, month - 1, 1); // Month is 1-indexed in URL, 0-indexed in Date
    fetchData(currentDate);
  }, [year, month]);

  const fetchData = async (currentDate) => {
    const start = format(startOfMonth(currentDate), 'yyyy-MM-dd');
    const end = format(endOfMonth(currentDate), 'yyyy-MM-dd');
    const token = localStorage.getItem('token');

    try {
      const config = {
        headers: { Authorization: `Token ${token}` }
      };

      const incomeResponse = await axiosInstance.get(`incomes/?start_date=${start}&end_date=${end}`, config);
      const expenseResponse = await axiosInstance.get(`expenses/?start_date=${start}&end_date=${end}`, config);

      setData({
        incomes: incomeResponse.data,
        expenses: expenseResponse.data,
      });
    } catch (error) {
      console.error('Failed to fetch financial data:', error);
      if (error.response && error.response.status === 401) {
        localStorage.removeItem('token');
        navigate('/login');
      }
    }
  };

  const handleMonthChange = (direction) => {
    const newDate = direction === 'prev' ? subMonths(new Date(year, month - 1, 1), 1) : addMonths(new Date(year, month - 1, 1), 1);
    navigate(`/home?year=${newDate.getFullYear()}&month=${newDate.getMonth() + 1}`);
  };

  const ChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      tooltip: {
        callbacks: {
          label: function(context) {
            return `${context.label}: $${context.parsed.toLocaleString()}`;
          }
        }
      }
    }
  };

  const prepareChartData = (dataItems) => ({
    labels: dataItems.map(item => item.category_name || 'Undefined Category'),
    datasets: [{
      data: dataItems.map(item => item.amount),
      backgroundColor: ['#7293cb', '#e1974c', '#84ba5b', '#d35e60', '#808585'],
    }],
  });

  return (
    <div className="homepage">
      <header className="homepage-header">
        <h1>Budget Tracker</h1>
        <div className="date-navigation">
          <button onClick={() => handleMonthChange('prev')}>Previous Month</button>
          <span>{format(new Date(year, month - 1, 1), 'MMMM yyyy')}</span>
          <button onClick={() => handleMonthChange('next')}>Next Month</button>
        </div>
        <button className="logout-button" onClick={() => {
          localStorage.removeItem('token');
          navigate('/login');
        }}>LOGOUT</button>
      </header>
      <div className="financial-summary">
        <div className="pie-chart-container">
          <Pie data={prepareChartData(data.incomes)} options={ChartOptions} />
        </div>
        <div className="pie-chart-container">
          <Pie data={prepareChartData(data.expenses)} options={ChartOptions} />
        </div>
      </div>
    </div>
  );
};

export default HomePage;
